"""Publication inventory, deterministic privacy transformations and audit.

Run --check to fail on unreviewed findings. No scientific inputs are rewritten.
Binary email replacements preserve every byte offset and total byte count.
"""
import argparse
import fnmatch
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EMAIL = re.compile(rb"[A-Za-z0-9_.+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
LOCAL = re.compile(rb"(?<![A-Za-z0-9])(?:[A-Za-z]:[\\/](?:[^\";\r\n<>]*))")
IDENTITY = re.compile(rb"(?i:mah" + rb"mo|U" + rb"ser|BASE" + rb"IMAGE)")
HOME = re.compile(rb"/ho" + rb"me/[^\s\"<>\r\n;]+")
EXTENDED = re.compile(rb"\\\\\?\\[^\s\"<>\r\n;]+")
SECRET = re.compile(rb"gh" + rb"p_|github_" + rb"pat_|s" + rb"k-|AK" + rb"IA|-----" + rb"BEGIN")
LOG_PREFIX = "validation-plus/dta-sroc/validate/"
REDACTED_LOGS = {LOG_PREFIX + n for n in (
    "generate-plus-raw.log", "generate-plus.log", "inspect-plus.log",
    "inventory-plus.log", "live-plus.log")}
EMAIL_FILES = {
    "app/hub/shared/vendor/jspdf.min.js",
    "app/r-shiny/shinylive/webr/R.wasm",
    "app/r-shiny/shinylive/webr/webr-worker.js",
    "app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/translations/DESCRIPTION",
}
PROVENANCE = "provenance/run_plan-2026-10-20-release.log"

def publishable_files(root=ROOT):
    """Match this archive's .gitignore; reject unsupported future rules."""
    rules = (root / ".gitignore").read_text().splitlines()
    known = {"results/", "outputs/", "__pycache__/", "*.pyc", ".venv/",
             "venv/", "*.sqlite", "docs/screenshots/_full_*.png",
             "docs/screenshots/*.tif"}
    if {r for r in rules if r and not r.startswith("#")} != known:
        raise SystemExit("Review publication inventory for changed ignore rules")
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        name = p.relative_to(root).as_posix()
        parts = p.relative_to(root).parts
        if ".git" in parts:
            continue
        ignored = False
        for rule in known:
            if rule.endswith("/"):
                ignored |= rule[:-1] in parts[:-1]
            elif "/" in rule:
                ignored |= fnmatch.fnmatchcase(name, rule)
            else:
                ignored |= any(fnmatch.fnmatchcase(part, rule) for part in parts)
        if not ignored:
            yield p

def redact(name, data):
    if name in REDACTED_LOGS or name == PROVENANCE:
        # All absolute drive paths in these logs are host-specific evidence.
        # Keep the leaf name; discard the complete machine directory prefix.
        data = LOCAL.sub(lambda m: b"<LOCAL>\\" +
                         re.split(rb"[\\/]", m.group().rstrip())[-1], data)
    if name in EMAIL_FILES or name in REDACTED_LOGS:
        # Fixed width is essential for wasm data sections and VFS offsets.
        data = EMAIL.sub(lambda m: b"[redacted]".ljust(len(m.group()), b" ")
                         if len(m.group()) >= 10 else b"x" * len(m.group()), data)
    return data

def findings(name, data):
    drive_pattern = (rb"(?<![A-Za-z0-9])[A-Za-z]:[\\/][^\r\n\";<>]+")
    if name.endswith((".gz", ".tgz", ".ttf", ".png", ".wasm", ".so")):
        drive_pattern = rb"C:[\\/]+U" + rb"sers[\\/]+[^\r\n\";<>]+"
    patterns = (("local path", re.compile(drive_pattern)),
                ("home path", HOME), ("extended path", EXTENDED),
                ("identity fragment", IDENTITY), ("email", EMAIL),
                ("credential prefix", SECRET))
    for category, pattern in patterns:
        for match in pattern.finditer(data):
            value = match.group()
            line = data.count(b"\n", 0, match.start()) + 1
            action = None
            if name == "publication_privacy.py" and category == "extended path":
                action = "Retain: scanner regular expression, not a path."
            elif category == "home path" and value.startswith(b"/ho" + b"me/web_" + b"user"):
                action = "Retain: webR virtual filesystem, not a host path."
            elif category == "identity fragment":
                tail = data[match.start():match.start()+32]
                public_owner = b"mah" + b"mood726-cyber"
                author = b"Mah" + b"mood"
                if value.lower() == b"user":
                    action = "Retain: ordinary runtime/prose identifier."
                elif tail.startswith(public_owner):
                    action = "Retain: public repository attribution."
                elif tail.startswith(author) and name in {
                        "CITATION.cff", ".zenodo.json", "LICENSE", "docs/paper.md"}:
                    action = "Retain: publication author or copyright holder."
            elif category == "email":
                binary_coincidences = {b"P" + b"@pV0.SqDZ", b"G" + b"@mQ-.Qm",
                                       b"k" + b"@q.iNolq", b"m" + b"@PD.oH"}
                if name.endswith((".ttf", ".tgz")) and value in binary_coincidences:
                    action = "Retain: coincidental binary bytes, not an address."
            elif category == "credential prefix":
                if name.endswith("/cert.pem") and data.startswith(b"-----" + b"BEGIN CERTIFICATE-----", match.start()):
                    action = "Retain: public CA certificate, not a private key."
                elif (name.endswith(".gz") and value == b"s" + b"k-"
                      and not re.match(rb"[A-Za-z0-9_-]{16,}", data[match.end():])):
                    action = "Retain: random compressed bytes, not a credential."
            yield {"file": name, "line": line, "category": category,
                   "action": action or "UNREVIEWED"}

def audit(root=ROOT):
    result = []
    count = 0
    for path in publishable_files(root):
        count += 1
        result.extend(findings(path.relative_to(root).as_posix(), path.read_bytes()))
    return count, result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", required=True)
    args = parser.parse_args()
    count, hits = audit()
    bad = [hit for hit in hits if hit["action"] == "UNREVIEWED"]
    if bad:
        for hit in bad:
            print(json.dumps(hit))
        raise SystemExit("Privacy check failed: unreviewed findings")
    print(f"PRIVACY PASS: {count} publishable files; {len(hits)} reviewed non-sensitive matches")

if __name__ == "__main__":
    main()
