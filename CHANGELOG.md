# Changelog

## Validated version

This repository validates the allmeta DTA SROC app at **allmeta commit `76d3e9d56891583849c1d08d77a8bc8666f2c2bd`**, the merge of
[allmeta PR #77](https://github.com/mahmood726-cyber/allmeta/pull/77). `app/` is byte-identical to that commit.

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

- **Unreleased:** validation of allmeta `76d3e9d` against mada 0.5.12 on 105 method × correction × covariate configurations. All 105 agree: 80 fits within tolerance and the same 25 refusals; 855/855 checks pass.
