# Expected results for RUN_PLAN.cmd

Run from the archive directory in Windows cmd. The numerical results below
were observed against allmeta v1.8.0 (1cb3f84) in the 2026-10-20 release run `provenance/run_plan-2026-10-20-release.log` (lines 15-184), ending in
`RECUT_RUN_PASS`; the runner recorded exit 0. They remain rerun acceptance
criteria. The plan exits immediately on failure.

Canonical pins are Node 24.15.0 (`.nvmrc`) and `requirements.txt`. The recorded
run used Node 24.13.0, fonttools 4.67.0 (pinned 4.66.1), packaging 26.0
(pinned 26.3), and pillow 12.2.0 (pinned 12.3.0), with
`reproduce.py --allow-version-mismatch` (log lines 70-71). The published plan
retains and comments this flag; it warns about mismatches instead of enforcing
those pins. `SOURCE_SHA256.json` was regenerated after `RUN_PLAN.cmd` was
edited, before the recorded run. Docker/CI retains the canonical pins.

Set R_HOME to the R 4.6.0 installation, R_LIBS_USER to the library containing
mada 0.5.12 and mvmeta 1.0.3, and R_LIBS to the extra package library in your
calling environment. Keep machine-specific settings outside the archive.
The plan requires all three variables and preserves their values.

| Label / command | Expected result |
|---|---|
| Local environment / setlocal | Changes remain local to the runner batch. |
| R executable PATH / set PATH | `%R_HOME%\bin` is first on PATH. |
| R user library / inherited R_LIBS_USER | Caller-supplied `%R_LIBS_USER%`. |
| R extra library / inherited R_LIBS | Caller-supplied `%R_LIBS%`. |
| Isolate R environment / set R_ENVIRON_USER | NUL. |
| Runner executables / rem | Rscript path is recorded; Node and Python are on PATH. |
| Python UTF-8 output / set PYTHONUTF8 | 1, for consistent Windows output. |
| Verify prepared source / python recut_integrity.py --verify | PASS; all source entries match, 245 release-derived copies and original protected files unchanged, seven corpus pins and 14 browser R packages verified. Exact source/protected counts are read from the manifests. |
| Original validation / python reproduce.py --allow-version-mismatch | R 4.6.0, mada 0.5.12, mvmeta 1.0.3, ellipse 0.5.0, recorded Node 24.13.0 (pinned 24.15.0). 855/855 checks PASS. Six datasets, 159 tables, 18 with zero cells; 105 configurations, 80 fits, 25 matched refusals; 53/53 paper numbers reproduced: ALL PASS. Exit 0. |
| Original N/N / python recut_integrity.py --original-counts | ORIGINAL: 855/855 checks PASS; 105 configurations, 80 fits, 25 matched refusals; Moses-Littenberg 18/18. |
| Original pinned replay / python validation-plus/run.py original | 855/855 checks PASS, no failed checks or coverage failures; unchanged corpus against the archived release engine. |
| Extras numerical replay / python validation-plus/run.py extras | 195,291/195,291 checks PASS; 27 configurations, 114 candidates, empty failures. The run confirms 195,291/195,291 (log lines 112-119). |
| Raw-scale gate / python validation-plus/run.py raw | PASS: raw-scale gate; 3,528 configurations; no silent out-of-tolerance case; identical pinned divergence sets (222 raw, eight standardized). All divergences noted; maximum relative difference 1.89e-4 (log lines 121-138). See subgroup targets below. |
| Extras negative controls / python validation-plus/run.py tests | Node test runner: 23/23 tests pass, zero failures and zero skipped. Includes deliberate fit/prediction/refusal corruption and invalid-input tests. |
| Original oracle tests / python -B -m unittest discover -s tests -v | 8/8 existing Python tests pass. |
| Verify after validation / python recut_integrity.py --verify | Same immutable source/corpus checks pass. Runtime outputs are excluded. |
| Regenerate file inventory / python recut_integrity.py --write | SOURCE_SHA256.json written with the same source hashes, after verification. Only the archive file inventory is regenerated, not upstream corpus manifests. |
| Verify regenerated inventory / python recut_integrity.py --verify | PASS, same counts. |
| Completion / echo | RECUT_RUN_PASS, followed by exit code 0. |

Every 'if errorlevel 1 exit /b 1' guard continues only on success. No script
updates expected/paper_values.json or expected/quick_values.json.

Raw-scale gate subgroup targets (agreeing configurations / configurations):

| Set | mada on supplied input | Standardized and back-transformed mada |
|---|---:|---:|
| Near-standardized, no note | 54/54 | 54/54 |
| Near-standardized, note | 96/96 | 96/96 |
| Scale scan, no note | 30/30 | 30/30 |
| Scale scan, note | 2,009/2,130 | 2,130/2,130 |
| Shift scan, note | 636/660 | 660/660 |
| Reference raw years, note | 14/18 | 18/18 |
| Synthetic raw years, note | 467/540 | 532/540 |

The raw gate also prints individual check counts for each group. Accept its
pinned divergence test and explicit PASS, not an invented global agreement
count. Existing upstream logs and browser summaries are not fresh evidence.

## Final Git-blob preparation

From the containing workspace, run FINAL_BLOBS.cmd with git and Python on PATH.
It uses archive/COPY_MAP.json and archive/fix_app_sources.py; no candidate fallback
is allowed. The v1.8.0 tag and full commit must agree. It reads each blob with
git cat-file, checks all inputs before writes, verifies BLOB PASS 245/245,
then applies the privacy transformations listed in RECUT_NOTES.md. APP_SOURCES.json
records both upstream blob hashes and published hashes. Finally it runs the
archive integrity generator, verification and publication privacy check.
Privacy-redacted files are documented derivatives, not claimed as exact blobs.
No corpus, expected value, R reference or tolerance is regenerated.
