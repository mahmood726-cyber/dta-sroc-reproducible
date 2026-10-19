# dta-sroc-reproducible

[![reproduce](https://github.com/mahmood726-cyber/dta-sroc-reproducible/actions/workflows/reproduce.yml/badge.svg)](https://github.com/mahmood726-cyber/dta-sroc-reproducible/actions/workflows/reproduce.yml)
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/mahmood726-cyber/dta-sroc-reproducible?quickstart=1)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23164857.svg)](https://doi.org/10.5281/zenodo.23164857)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Latest verified run](https://img.shields.io/badge/latest%20verified%20run-results%20page-2c5e8a)](https://mahmood726-cyber.github.io/dta-sroc-reproducible/)

The [allmeta](https://github.com/mahmood726-cyber/allmeta) **DTA SROC app** runs meta-analysis of diagnostic test accuracy offline in the browser
([live](https://mahmood726-cyber.github.io/allmeta/dta-sroc/)). It offers:

- **The bivariate random-effects model** (Reitsma et al. 2005) by REML, ML, method of moments, variance components or fixed effect, as the R package mada (`reitsma`, which calls mvmeta).
- **Continuity correction** for zero cells as mada: all studies (default), affected studies only, or none.
- **Meta-regression** on one study-level covariate (numeric, or categories with the first as reference).
- **Outputs:** summary sensitivity and specificity with 95% CIs, likelihood ratios and diagnostic odds ratio, between-study covariance and correlation, Rutter–Gatsonis (HSROC) parameters, the SROC curve, AUC and partial AUC, 95% confidence and prediction regions, log-likelihood and AIC, the Moses–Littenberg line, Spearman's threshold correlation, a Fagan nomogram and Deeks' test, with Markdown, JSON and CSV export.

This repository validates the app against **mada** on every dataset that mada ships, and checks every number in the accompanying F1000Research article.

## Reproduce in one click

**1. See the latest verified run (nothing to run).** The [results page](https://mahmood726-cyber.github.io/dta-sroc-reproducible/) is republished by CI after every push to `main`: the PASS/FAIL table for every number in the paper, the result on Docker, Linux, Windows and macOS, the cross-platform comparison, and the figures.

**2. Open in GitHub Codespaces (one click).** Click the *Open in GitHub Codespaces* badge above, then *Create codespace*.
- The pinned environment is built from this repository's `Dockerfile`: R 4.6.0, the dated package snapshot, Node 24.15.0 and Python.
- The quick reproduction (2 datasets) then runs automatically. Its log ends with `QUICK RUN: ALL PASS`; the report is in `outputs/quick/reproduction_report.md`.
- For the full run, type `python reproduce.py` in the terminal (about a minute; writes `outputs/full/`).

Limits: you need to be signed in to GitHub; the codespace uses your own Codespaces allowance (personal accounts get a free monthly quota; this uses a 2-core machine); the first build takes several minutes, mostly installing R packages. `codespaces-check` in Actions builds the same devcontainer and runs its automatic quick run on every relevant change.

**3. Re-run the CI yourself (one click in a fork).** Only maintainers can trigger workflows here, so use your own copy:
1. Click **Fork**.
2. In your fork, open the **Actions** tab and click *I understand my workflows, go ahead and enable them*.
3. Choose **reproduce**, then **Run workflow** (branch `main`).

The run is the full validation on Docker, Linux, Windows and macOS. Each job's **summary** shows its PASS/FAIL report; **Artifacts** hold `reproduction-report-<platform>` and the complete outputs (`full-<platform>`); the *compare* job shows the cross-platform check. Publishing to Pages happens only on this repository.

**On your own machine:**

```bash
git clone https://github.com/mahmood726-cyber/dta-sroc-reproducible && cd dta-sroc-reproducible
docker build -t dta . && docker run --rm -v "$PWD/outputs:/work/outputs" dta        # canonical
```

Without Docker you need R 4.6.0, Node 24.15.0 and Python 3.12 or 3.13:
1. `Rscript bench/install_r_packages.R`
2. `python -m pip install -r requirements.txt`
3. `python reproduce.py` (or `--quick`)

`make setup` and `make reproduce` do the same. **To use the app**, open `app/dta-sroc/index.html` in a browser.

## What it shows

The app is validated at **allmeta commit `76d3e9d`** (the merge of [allmeta PR #77](https://github.com/mahmood726-cyber/allmeta/pull/77)). `app/` is byte-identical to that commit.

| | Result |
|---|---|
| Full grid: 6 datasets (159 two-by-two tables, 18 with a zero cell) × 5 methods × 3 correction rules, plus 15 meta-regressions = 105 configurations | All 105 agree with mada: 80 fits within tolerance and the same 25 refusals (no correction with a zero cell). 855/855 checks pass. |
| Moses–Littenberg (`mslSROC`), 6 datasets × 3 correction rules | 18/18 agree (13 fits, 5 refusals). |
| Worked example: AUDIT-C (14 studies), REML | Sensitivity 0.891 (0.808 to 0.941), specificity 0.780 (0.715 to 0.833), AUC 0.887, LR+ 4.04, LR− 0.14, as mada. |
| Meta-regression: smoking (51 tables) on questionnaire type | Self-administered vs interviewer-administered: logit sensitivity −1.07 (SE 0.40; p = 0.007), sensitivity 0.88 vs 0.96; false-positive rate unchanged (p = 0.82). |

Earlier versions of the app had known issues, found by this validation and fixed in allmeta PR #77; see [CHANGELOG.md](CHANGELOG.md).

Tolerances follow allmeta's own parity test (`hub/shared/tests/_dta_parity_check.mjs`, mirrored in `analysis/make_outputs.py`):

- coefficients, their covariance and Ψ within 10⁻⁹ relative for fixed effect and method of moments, 10⁻⁸ for variance components (same arithmetic and stopping rule as mvmeta), and 10⁻⁶ for REML and ML (same IGLS start and BFGS optimiser; observed maximum 2 × 10⁻⁷);
- log-likelihood, AIC and BIC within 10⁻⁶ absolute;
- summary points and CIs, between-study correlation, HSROC parameters, AUC and partial AUC (Rutter–Gatsonis and naive), SROC values: within 10⁻⁶;
- 95% confidence and prediction regions, checked both ways: each of mada's 100 points must lie on the app's region and each point of the app's drawn region on mada's, to 10⁻⁶ relative in the region equation;
- refusals must match.

The app's likelihood-ratio CIs (delta method), Deeks' test and Fagan nomogram are not computed by mada and are not part of this comparison.

## Layout

| Path | Contents |
|---|---|
| `app/` | The app, byte-identical to allmeta commit `76d3e9d` |
| `bench/build_corpus.R` | Builds the 6-dataset corpus from mada |
| `bench/reference_mada.R` | mada reference fits over the option grid |
| `bench/run_engine.mjs` | Runs the app's JavaScript engine on the same data |
| `analysis/make_outputs.py` | Tables, figures, statistics, PASS/FAIL |
| `analysis/compare_runs.py` | Cross-platform comparison |
| `expected/` | Every number as printed in the paper |
| `docs/` | Paper, `numbers.json`, Figure 1 screenshots and their capture script |
| `ci/build_site.py` | Builds the live results page from a CI run (reads outputs only) |
| `.devcontainer/` | Codespaces / dev-container definition; runs the quick reproduction on creation |

## Outputs and how they map to the paper

`python reproduce.py` writes to `outputs/full/`:

| File | Paper |
|---|---|
| `docs/screenshots/step1.png` … `step6.png` | Figure 1: using the app, step by step (`captions.md`) |
| `figure2_worked_examples.png` (+ `.csv`) | Figure 2: AUDIT-C SROC and regions; smoking meta-regression |
| `figure3_agreement.png` (+ `.csv`) | Figure 3: all fits, by method |
| `table1_parity_by_method.csv` | Table 1: agreement by method and correction rule |
| `table2_by_dataset.csv` | Table 2: results by dataset |
| `table3_parity_all_configurations.csv` | Every configuration (extended data) |
| `table4_moses_littenberg.csv` | Moses–Littenberg comparison (extended data) |
| `visual_abstract.png` | Visual abstract |
| `stats.json` | Every number quoted in the text |
| `reproduction_report.md` | Expected versus reproduced, PASS/FAIL per number |

## Environment and determinism

- **R 4.6.0.** The image is `rocker/r-ver:4.6.0`. mada 0.5.12, mvmeta 1.0.3, ellipse 0.5.0 and their dependencies come from the Posit Package Manager snapshot of 2026-10-01.
- **Node 24.15.0** (`.nvmrc`) runs the app's JavaScript engine. There are no npm dependencies.
- **Python** builds the tables and figures (numpy and matplotlib, pinned in `requirements.txt`).
- **Docker is the canonical environment.** CI runs the full validation on every push on Linux, Windows, macOS and Docker. `analysis/compare_runs.py` then requires the corpus and the engine's output to be bit-identical across the x86-64 runs; macOS on ARM is reported but not required to match (V8 there can differ in the last bit).
- **R's own values** differ between operating systems in the last bits. The printed numbers are chosen to be robust to this (discrepancy maxima enter only as threshold indicators), and are checked on every platform.

Run time: about a minute.

## Data

`bench/build_corpus.R` builds the corpus at run time from the six datasets shipped with mada (GPL-2): AuditC (Kriston et al. 2008), Dementia (Mitchell 2009), IAQ and SAQ (subsets of Patrick et al. 1994), skin_tests (Sousa-Pinto et al. 2021) and smoking (Patrick et al. 1994, complete). The app's example list (`app/dta-sroc/example-datasets.js`, generated by `_make_examples.R`) carries the same published counts with these sources.

## Cite

Ahmad M. Bivariate meta-analysis of diagnostic test accuracy in the browser: a tool validated against the R package mada [software], v1.0.0. Zenodo; 2026. doi:[10.5281/zenodo.23164857](https://doi.org/10.5281/zenodo.23164857). Machine-readable metadata: `CITATION.cff`.

## Licence

MIT, the same as allmeta.
