"""Run unchanged upstream validation in a disposable, archive-local lane layout."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / "validation-plus/dta-sroc/validate"
WORK = ROOT / "outputs/validation-plus"
VALIDATE = WORK / "allmeta/dta-sroc/validate"

def stage():
    # No junctions or links to the read-only candidate. The scripts' original
    # allmeta/dta-sroc/validate paths resolve entirely below outputs/.
    dest = WORK / "allmeta/dta-sroc"
    shutil.copytree(ROOT / "app/dta-sroc", dest, dirs_exist_ok=True)
    shutil.copytree(UPSTREAM, VALIDATE, dirs_exist_ok=True)
    shared = WORK / "allmeta/shared"
    shared.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / "app/shared/dta-bivariate.js", shared / "dta-bivariate.js")

def run(args, log):
    env = {**os.environ, "OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1"}
    result = subprocess.run(args, cwd=WORK, text=True, encoding="utf-8",
                            errors="replace", capture_output=True, env=env)
    (WORK / log).write_text(result.stdout + result.stderr, encoding="utf-8")
    print(result.stdout, end="", flush=True)
    if result.stderr: print(result.stderr, end="", file=sys.stderr)
    if result.returncode: raise SystemExit(result.returncode)
    return result.stdout

def check(kind):
    names = {"original": "replay-original-plus.mjs", "extras": "check-plus.mjs",
             "raw": "check-plus-raw.mjs", "tests": "test-plus.mjs"}
    cmd = ["node"] + (["--test"] if kind == "tests" else [])
    output = run(cmd + [str(VALIDATE / names[kind])], kind + ".log")
    if kind in ("original", "extras"):
        result = json.loads(output)
        expected = 855 if kind == "original" else 195291
        failures = result.get("failed", result.get("failures", []))
        if (result.get("checks"), result.get("passed")) != (expected, expected) or failures or result.get("coverageFails"):
            raise SystemExit("FAIL: unexpected count, failures, or missing original coverage")
        print(f"{kind}: {result['passed']:,}/{result['checks']:,} checks PASS")
    elif kind == "raw":
        if "Raw-scale corpus: 3528 configurations;" not in output or "PASS: raw-scale gate" not in output:
            raise SystemExit("FAIL: raw-scale gate did not report the expected coverage")
        print("raw-scale gate: PASS (3,528 configurations; agreement counts are reported by subgroup)")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("stage", "original", "extras", "raw", "tests", "regenerate"))
    args = parser.parse_args()
    stage()
    if args.mode == "stage":
        print("Staged unchanged validation at " + str(VALIDATE))
    elif args.mode == "regenerate":
        # Optional reference rebuild: only scratch copies are ever regenerated.
        for script in ("generate-plus.R", "generate-plus-raw.R"):
            run(["Rscript", "allmeta/dta-sroc/validate/" + script], script + ".log")
        run(["node", str(VALIDATE / "pin-plus.mjs")], "pin-plus.log")
        run(["node", str(VALIDATE / "check-plus-raw.mjs"), "--pin"], "pin-plus-raw.log")
        check("extras")
        check("raw")
    else:
        check(args.mode)

if __name__ == "__main__":
    main()
