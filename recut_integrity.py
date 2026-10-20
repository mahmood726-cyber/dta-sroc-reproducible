"""Hash release files, verify upstream pins, and preserve the original oracle.
Run: python recut_integrity.py --write | --verify | --original-counts
No Node, R, git or third-party Python modules are used here.
"""
import argparse
import hashlib
import json
from pathlib import Path
from publication_privacy import publishable_files

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "SOURCE_SHA256.json"
EXCLUDE = {".git", "__pycache__", ".pytest_cache", "results", "outputs"}
def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def files():
    return {p.relative_to(ROOT).as_posix(): digest(p)
            for p in publishable_files(ROOT) if p != MANIFEST}
def require(condition, message):
    if not condition: raise SystemExit("FAIL: " + message)
def pins(base):
    count = 0
    for name in ("MANIFEST.json", "MANIFEST-plus.json", "MANIFEST-plus-raw.json"):
        path = base / "validate" / name
        if not path.exists(): continue
        data = json.loads(path.read_text(encoding="utf-8"))
        for record in data.get("files", [data] if "path" in data else []):
            p = base / record["path"]
            require(p.is_file(), "missing " + str(p))
            require(digest(p) == record["sha256"], "upstream hash " + str(p))
            if "bytes" in record: require(p.stat().st_size == record["bytes"], "size " + str(p))
            if "plus" in name: require(b"\r" not in p.read_bytes(), "LF corpus " + str(p))
            count += 1
    m = json.loads((base / "validate/MANIFEST-plus.json").read_text())
    pin = (base / "validate/plus-pins.js").read_text()
    literal = pin.split("Object.freeze(", 1)[1].rsplit(");", 1)[0]
    require(json.loads(literal) == m, "browser pins differ: " + str(base))
    return count
def verify():
    expected = json.loads(MANIFEST.read_text(encoding="utf-8"))["files"]
    actual = files()
    require(actual == expected, "source inventory differs: " + ", ".join(
        p for p in sorted(set(actual) | set(expected)) if actual.get(p) != expected.get(p)))
    protected = json.loads((ROOT / "ORIGINAL_VALIDATION_SHA256.json").read_text())["files"]
    for p, sha in protected.items():
        require(digest(ROOT / p) == sha, "original validation changed: " + p)
    sources = json.loads((ROOT / "APP_SOURCES.json").read_text())
    for p, item in sources["files"].items():
        require(digest(ROOT / p) == item["sha256"], "published release copy changed: " + p)
    count = pins(ROOT / "app/dta-sroc") + pins(ROOT / "validation-plus/dta-sroc")
    # The full upstream package manifest is unchanged; only mada's transitive
    # dependency set is shipped and verified, matching webr-runner.js.
    base = ROOT / "app/r-shiny/shinylive/webr"
    packages = json.loads((base / "repo/manifest.json").read_text())
    for p in packages["packages"]:
        if p["package"] not in sources["browser_packages"]: continue
        path = base / p.get("path", "repo/" + packages["layout"] + p["file"])
        require(digest(path) == p["sha256"] and path.stat().st_size == p["bytes"],
                "browser R package " + p["package"])
    print(f"PASS: {len(actual)}/{len(expected)} source files; {len(protected)} unchanged original files; "
          f"{len(sources['files'])} release-derived copies; {count} corpus pins; "
          f"{len(sources['browser_packages'])} browser R packages")
def original_counts():
    s = json.loads((ROOT / "outputs/full/stats.json").read_text())
    require((s["checks_passed"], s["checks_total"]) == (855, 855), "original check counts")
    require((s["configurations"], s["mada_fitted"], s["refusals_matched"], s["moses_agree"]) ==
            (105, 80, 25, 18), "original grid coverage")
    print(f"ORIGINAL: {s['checks_passed']}/{s['checks_total']} checks PASS; "
          "105 configurations, 80 fits, 25 matched refusals; Moses-Littenberg 18/18")
def main():
    p = argparse.ArgumentParser(description=__doc__)
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--verify", action="store_true")
    mode.add_argument("--original-counts", action="store_true")
    a = p.parse_args()
    if a.write:
        snapshot = files()
        MANIFEST.write_text(json.dumps({"algorithm": "sha256",
            "allmeta_tag": "v1.8.0", "allmeta_commit": "1cb3f8409c7af75ed41f7e1811f9c502f900fc79",
            "allmeta_doi": "10.5281/zenodo.23515177",
            "scope": "All publishable archive files respecting .gitignore, except this manifest and .git.",
            "files": snapshot}, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote SOURCE_SHA256.json: {len(snapshot)} files")
    elif a.verify: verify()
    else: original_counts()
if __name__ == "__main__":
    main()
