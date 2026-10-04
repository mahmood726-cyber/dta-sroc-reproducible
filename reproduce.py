#!/usr/bin/env python3
"""Re-run the DTA validation and check every number in the paper.

  python reproduce.py            # full run: all six mada datasets, 105 configurations (about a minute)
  python reproduce.py --quick    # 2 datasets, a few seconds

Steps: check tool versions -> build the corpus from the R package mada -> mada reference fits over the
method / correction / covariate grid (R) -> the app's engine on the same data (Node) -> tables, figures,
statistics -> expected vs reproduced, PASS/FAIL per number. Exit code 0 only if all pass.
"""
import argparse
import os
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
R_PINS = {"mada": "0.5.12", "mvmeta": "1.0.3", "ellipse": "0.5.0"}
QUICK = ["AuditC", "skin_tests"]


def sh(cmd, **kw):
    p = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, **kw)
    if p.returncode:
        sys.exit(f"command failed ({p.returncode}): {' '.join(map(str, cmd))}\n{p.stdout}\n{p.stderr}")
    return p.stdout


def check_versions(strict):
    problems = []
    rscript = shutil.which("Rscript") or sys.exit("Rscript not found on PATH (R 4.6.0 needed; see README or use Docker)")
    node = shutil.which("node") or sys.exit("node not found on PATH (Node 24.15.0 needed)")
    pk = ",".join(f"'{p}'" for p in R_PINS)
    rv = sh([rscript, "-e", f"cat(as.character(getRversion()), sapply(c({pk}), function(p) tryCatch(as.character(packageVersion(p)), error=function(e) 'missing')))"]).split()
    nv = sh([node, "--version"]).strip().lstrip("v")
    if rv[0] != "4.6.0": problems.append(f"R {rv[0]} (pinned 4.6.0)")
    for (p, want), got in zip(R_PINS.items(), rv[1:]):
        if got == "missing": sys.exit(f"R package {p} missing: run  Rscript bench/install_r_packages.R")
        if got != want: problems.append(f"{p} {got} (pinned {want})")
    want_node = (ROOT / ".nvmrc").read_text().strip()
    if nv != want_node: problems.append(f"node {nv} (pinned {want_node})")
    from importlib.metadata import version
    for line in (ROOT / "requirements.txt").read_text().splitlines():
        line = line.split("#")[0].split(";")[0].strip()
        if "==" in line:
            k, v = line.split("==", 1)
            try:
                if version(k) != v: problems.append(f"{k} {version(k)} (pinned {v})")
            except Exception:
                sys.exit(f"python package {k} missing: run  python -m pip install -r requirements.txt")
    print(f"environment: R {rv[0]} (mada {rv[1]}, mvmeta {rv[2]}, ellipse {rv[3]}), Node {nv}, Python {platform.python_version()}, {platform.system()} {platform.machine()}")
    if problems:
        msg = "version mismatch: " + "; ".join(problems)
        if strict: sys.exit(msg + "\n(use --allow-version-mismatch to run anyway)")
        print("WARNING: " + msg)
    return rscript, node


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--allow-version-mismatch", action="store_true")
    a = ap.parse_args()
    mode = "quick" if a.quick else "full"
    res, out = ROOT / "results" / mode, ROOT / "outputs" / mode
    t0 = time.time()
    rscript, node = check_versions(strict=not a.allow_version_mismatch)
    if res.exists(): shutil.rmtree(res)
    res.mkdir(parents=True)
    env = {**os.environ, "OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1"}
    print(sh([rscript, "bench/build_corpus.R", str(res / "corpus.csv")], env=env).strip().splitlines()[0])
    if a.quick:
        lines = (res / "corpus.csv").read_text(encoding="utf-8").splitlines(keepends=True)
        keep = [lines[0]] + [l for l in lines[1:] if l.split(",", 1)[0].strip('"') in QUICK]
        (res / "corpus.csv").write_text("".join(keep), encoding="utf-8", newline="")
        print("quick mode: datasets", ", ".join(QUICK))
    print(sh([rscript, "bench/reference_mada.R", str(res / "corpus.csv"), str(res / "mada.jsonl")], env=env).strip().splitlines()[-1])
    print(sh([node, "bench/run_engine.mjs", str(res / "corpus.csv"), str(res / "engine.jsonl")], env=env).strip())
    expected = "expected/quick_values.json" if a.quick else "expected/paper_values.json"
    rc = subprocess.run([sys.executable, "analysis/make_outputs.py", "--results", str(res), "--outputs", str(out), "--expected", expected], cwd=ROOT).returncode
    print(f"total time {time.time() - t0:.0f} s; outputs in {out.relative_to(ROOT)}")
    sys.exit(rc)


if __name__ == "__main__":
    main()
