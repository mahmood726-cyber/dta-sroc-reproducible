"""Restore pinned v1.8.0 Git blobs, verify bytes, then prepare private-data-free copies."""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path, PurePosixPath

from publication_privacy import redact

ROOT = Path(__file__).resolve().parent
COMMIT = "1cb3f8409c7af75ed41f7e1811f9c502f900fc79"

def digest(data):
    return hashlib.sha256(data).hexdigest()

def safe_path(name):
    path = PurePosixPath(name)
    if (path.is_absolute() or ".." in path.parts or ".git" in path.parts
            or "\\" in name or ":" in name or not path.parts):
        raise SystemExit("Unsafe copy-map path")
    return path

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upstream", default=str(ROOT.parent / "allmeta"))
    args = parser.parse_args()
    repo = Path(args.upstream).resolve()

    def git(*arguments):
        proc = subprocess.run(["git", "-C", str(repo), *arguments],
                              capture_output=True)
        if proc.returncode:
            raise SystemExit("Git failed while reading the pinned release; no fallback allowed")
        return proc.stdout

    tag = git("rev-parse", "--verify", "refs/tags/v1.8.0^{commit}").decode().strip()
    if tag != COMMIT:
        raise SystemExit("v1.8.0 tag does not match the required release commit")
    sources_path = ROOT / "APP_SOURCES.json"
    sources = json.loads(sources_path.read_text(encoding="utf-8"))
    mapping = json.loads((ROOT / "COPY_MAP.json").read_text(encoding="utf-8"))
    expected = {name: item["source"] for name, item in sources["files"].items()}
    actual = {item["archive_path"]: item["allmeta_path"] for item in mapping}
    if len(mapping) != len(actual) or actual != expected or len(mapping) != 245:
        raise SystemExit("Copy map must cover all 245 recorded copies exactly once")

    prepared = {}
    for name, source in actual.items():
        safe_path(name)
        safe_path(source)
        destination = (ROOT / name).resolve()
        if not destination.is_relative_to(ROOT):
            raise SystemExit("Destination escapes archive")
        blob = git("cat-file", "blob", COMMIT + ":" + source)
        old = destination.read_bytes()
        published = redact(name, blob)
        # Only checkout newline conversion and the audited privacy transform
        # may differ. In particular, no scientific changes can be accepted.
        if redact(name, old).replace(b"\r\n", b"\n") != published.replace(b"\r\n", b"\n"):
            raise SystemExit("Unexpected content difference: " + name)
        if "/corpus/" in name and old != blob:
            raise SystemExit("Corpus bytes differ: " + name)
        prepared[name] = (blob, published)

    # All Git reads and semantic checks complete before any destination changes.
    redactions = []
    for name, (blob, published) in prepared.items():
        destination = ROOT / name
        try:
            destination.write_bytes(blob)
            if destination.read_bytes() != blob:
                raise SystemExit("Blob write verification failed: " + name)
        finally:
            # Never leave an unredacted blob in the publication tree.
            destination.write_bytes(published)
        if destination.read_bytes() != published:
            raise SystemExit("Published write verification failed: " + name)
        item = sources["files"][name]
        item["upstream_blob_sha256"] = digest(blob)
        item["sha256"] = digest(published)
        item["privacy_redacted"] = blob != published
        if blob != published:
            redactions.append(name)
    print(f"BLOB PASS {len(prepared)}/{len(mapping)}", flush=True)
    sources["copied_commit"] = COMMIT
    sources["blob_verification"] = (
        "All mapped Git blobs restored and checked before deterministic privacy redaction; "
        "sha256 describes published bytes, upstream_blob_sha256 describes release bytes.")
    sources["privacy_derivatives"] = redactions
    sources_path.write_text(json.dumps(sources, indent=2) + "\n",
                            encoding="utf-8", newline="\n")
    evidence = {"commit": COMMIT, "tag": "v1.8.0", "verified_blobs": len(prepared),
                "published_exact_blobs": len(prepared) - len(redactions),
                "privacy_derivatives": redactions}
    (ROOT / "provenance/BLOB_VERIFICATION.json").write_text(
        json.dumps(evidence, indent=2) + "\n", encoding="utf-8", newline="\n")
    for option in ("--write", "--verify"):
        subprocess.run([sys.executable, str(ROOT / "recut_integrity.py"), option],
                       cwd=ROOT, check=True)
    subprocess.run([sys.executable, str(ROOT / "publication_privacy.py"), "--check"],
                   cwd=ROOT, check=True)
    print(f"PUBLISHED PASS {len(prepared)}/{len(mapping)}; {len(redactions)} privacy derivatives")

if __name__ == "__main__":
    main()
