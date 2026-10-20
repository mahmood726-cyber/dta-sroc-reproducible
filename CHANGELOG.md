# Changelog

## 1.1.0 - 2026-10-20

- Finalize allmeta v1.8.0, commit `1cb3f8409c7af75ed41f7e1811f9c502f900fc79`,
  DOI `10.5281/zenodo.23515177`. The 2026-10-20 release rerun passed.
  Add COPY_MAP.json and ../FINAL_BLOBS.cmd, reusing fix_app_sources.py for
  binary-safe blob restoration followed by documented privacy redaction.
- Preserve the original validation inputs, R reference generation, expected
  values and tolerances. The recorded 2026-10-20 `provenance/run_plan-2026-10-20-release.log` (lines 15-184)
  reports 855/855 checks (105 configurations; 80 fits, 25 matched refusals;
  Moses 18/18), 53/53 paper numbers and pinned replay 855/855.
- Add PR #133 extras validation with unchanged scientific inputs: bivariate meta-regression, conditional
  ROC regions and post-test probabilities. The recorded run passed
  195,291/195,291 checks over 27 configurations and the raw-scale gate over
  3,528 configurations: 222 raw / 8 standardised out-of-tolerance configurations,
  all noted, maximum relative difference 1.89e-4. This is not universal
  numerical agreement. Negative controls passed 23/23; oracle tests passed 8/8.
- Include post-v1.0.0 commit `59203eb`: `analysis/make_outputs.py` fails closed
  on empty, unequal-length, non-numeric or non-finite parity arrays, with
  eight tests and a CI step. No tolerance or expected value changed.
- Update `app/shared/dta-bivariate.js`: Moses-Littenberg refuses degenerate
  inputs (constant S, identical FPRs, slope near 1 or non-finite coefficients);
  Spearman correlation is `null` when undefined. The original 855/855 checks,
  including Moses 18/18, were re-run against this engine.
- Disclose the recorded environment deviation: Node 24.13.0 (pinned 24.15.0),
  fonttools 4.67.0 (pinned 4.66.1), packaging 26.0 (pinned 26.3), and
  pillow 12.2.0 (pinned 12.3.0), using `reproduce.py --allow-version-mismatch`
  (`provenance/run_plan-2026-10-20-release.log`, lines 70-71). `SOURCE_SHA256.json` was regenerated after
  `RUN_PLAN.cmd` was edited, before that run. Canonical Docker/CI pins remain.
- Bundle local app dependencies; add provenance/integrity manifests, an isolated
  runner wrapper and `RUN_PLAN.cmd` using caller-supplied R environment variables.
- Update release metadata, preserving all creators and historical identifiers.

## v1.0.0 baseline (historical)

The v1.0.0 archive validated the allmeta DTA SROC app at **allmeta commit `76d3e9d56891583849c1d08d77a8bc8666f2c2bd`**, the merge of
[allmeta PR #77](https://github.com/mahmood726-cyber/allmeta/pull/77). Its archived `app/` was byte-identical to that commit; v1.1.0 uses the allmeta v1.8.0 release noted above.

## Earlier versions of the app (history)

Versions of the app before PR #77 had known issues. All were found by this repository's first validation run, against allmeta `0f8b86d`, and fixed in PR #77.

| Issue | Before PR #77 | Since PR #77 |
|---|---|---|
| Estimation method | ML only (Nelder–Mead). mada's default is REML; on the six datasets the between-study covariance differed from mada's REML fit by up to 15% (relative). | REML (default), ML, method of moments, variance components and fixed effect, porting mvmeta: IGLS start, then BFGS with the analytic gradient. All agree with mada. |
| Prediction region | Drawn from the between-study covariance Ψ alone. mada's `plot.reitsma(predict = TRUE)` uses Ψ + vcov, so the app's region was too narrow. A test asserted the Ψ-only region with values not obtained from mada. | Ψ + vcov, as mada; the test now uses mada's values. |
| Continuity-correction note | Said 0.5 was added to "that study only", while the model added it to every study. | The rule is a setting (all / single / none, as mada) and the note states what was done. |
| Stat labels | Uppercase styling turned "ρ", "α" and "β" into capital Greek letters shown as P, A and B. | Labels shown as written. |
| Footer | Said the Moses–Littenberg line "is what metafor::reitsma falls back to"; metafor has no such function. | Describes the methods as implemented. |

PR #77 also added: the three continuity-correction rules, bivariate meta-regression, Rutter–Gatsonis parameters, AUC and partial AUC, log-likelihood and AIC, mada's six datasets as examples, and a parity test over the full grid used here (`hub/shared/tests/dta-bivariate-mada-parity.spec.mjs`). The hsroc app, which shares the engine, keeps its documented ML fit and gains mada's prediction region.

## This repository

- **v1.0.0 (historical):** validation of allmeta `76d3e9d` against mada 0.5.12 on 105 method × correction × covariate configurations. All 105 agree: 80 fits within tolerance and the same 25 refusals; 855/855 checks pass.
