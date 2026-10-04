# Bivariate meta-analysis of diagnostic test accuracy in a browser: a tool validated against the R package mada

**Mahmood Ahmad**¹ [AUTHOR TO COMPLETE: ORCID, corresponding-author e-mail]

¹ [AUTHOR TO COMPLETE: affiliation]

## Abstract

**Background:** Meta-analysis of diagnostic test accuracy uses the bivariate random-effects model, usually in R, Stata or SAS. We built a browser tool for it and validated it against R.

**Methods:** The allmeta DTA SROC app fits the bivariate model by five estimators, with three continuity-correction rules and optional meta-regression, and reports summary sensitivity and specificity, likelihood ratios, the summary ROC curve and its area, and confidence and prediction regions. We compared it with the R package mada on all six datasets that mada distributes (159 two-by-two tables), across 105 configurations, in a containerised analysis run on four platforms.

**Results:** All 105 configurations agreed: 80 fits within numerical tolerance and the same 25 refusals. All 855 individual checks passed.

**Conclusions:** The app reproduces mada offline, without installation or programming.

**Keywords:** diagnostic test accuracy; bivariate meta-analysis; summary ROC curve; HSROC; meta-regression; software validation; reproducibility; browser-based software

## Introduction

Diagnostic accuracy studies report sensitivity and specificity, which are correlated across studies through threshold differences. The bivariate random-effects model pools both on the logit scale with a between-study covariance [1]. It is equivalent to the hierarchical summary ROC (HSROC) model [2,3] and replaces the Moses–Littenberg regression [4]. It is fitted with the R package mada [5], built on mvmeta [6], or with Stata's metandi [7].

We describe the DTA SROC app, a member of allmeta, a collection of offline browser tools for evidence synthesis [8], and validate it against mada.

## Methods

### Implementation

The app is a static web tool (https://mahmood726-cyber.github.io/allmeta/dta-sroc/). Its engine, `dta-bivariate.js`, ports mada's and mvmeta's estimation to pure JavaScript.

- **Data.** One row per study (true and false positives and negatives), with an optional covariate.
- **Continuity correction.** 0.5 is added to all studies when any cell is zero (mada's default), to affected studies only, or not at all.
- **Estimation.** REML or ML (with mvmeta's algorithm), method of moments [9], variance components, or fixed effect. An optional study-level covariate gives a bivariate meta-regression.
- **Outputs.** Summary sensitivity and specificity with 95% CIs; likelihood ratios; between-study covariance; HSROC parameters [3]; the SROC curve, AUC and partial AUC; 95% confidence and prediction regions; the Moses–Littenberg line; a Fagan nomogram; Deeks' test [10]; and Markdown, JSON and CSV export.

### Operation

The app needs only a browser and works offline. A user (Figure 1):

1. pastes the data or loads one of mada's datasets;
2. chooses the estimation method, continuity correction and covariate;
3. reads the summary estimates and HSROC parameters;
4. inspects the studies, SROC curve and regions in ROC space;
5. runs a meta-regression and exports the results;
6. reads the Fagan nomogram and Deeks' funnel plot.

### Validation

We validated allmeta commit 76d3e9d. The corpus was the six datasets in mada 0.5.12 [5]: AuditC [11], Dementia, IAQ, SAQ, skin_tests and smoking [12] (159 two-by-two tables; 18 with a zero cell).

mada fitted every dataset with five methods and three correction rules, plus three meta-regressions of smoking: 105 configurations. The app's engine ran on the same data. Earlier app versions fitted ML only and drew too narrow a prediction region; this validation found both, and they were corrected (allmeta PR #77).

Agreement required identical refusals, and estimates, their covariance and the between-study covariance within 10⁻⁹ (method of moments, fixed effect), 10⁻⁸ (variance components) or 10⁻⁶ (REML, ML), relative. Log-likelihoods and all derived quantities (summary points, CIs, AUC, HSROC parameters, SROC curves, regions) had to agree within 10⁻⁶.

One command (`python reproduce.py`) runs everything in a canonical Docker image (R 4.6.0, Node 24.15.0). Continuous integration repeats it on Linux, Windows, macOS and Docker and checks every reported number.

## Results

**Agreement.** mada fitted 80 configurations and refused 25 (no correction with a zero cell). The app refused the same 25 and agreed on all 80, including 15 meta-regressions (Table 1; Figure 3): within 10⁻¹² for method of moments, variance components and fixed effect, and 10⁻⁶ for REML and ML. All 855 checks passed, as did 18 Moses–Littenberg comparisons.

**Worked example.** For AUDIT-C (14 studies) [11], REML gave sensitivity 0.891 (95% CI 0.808 to 0.941) and specificity 0.780 (0.715 to 0.833), as mada did; AUC 0.887, LR+ 4.04 and LR− 0.14 (Figure 2A). REML's logit-sensitivity variance (1.38) exceeded ML's (1.22).

**Meta-regression.** In the smoking data (51 tables) [12], self-administered questionnaires had lower logit sensitivity than interviewer-administered ones (−1.07, SE 0.40; p = 0.007; 0.88 versus 0.96) and similar false-positive rates (0.07; p = 0.82) (Figure 2B; Table 2).

**Reproducibility.** Every number was reproduced on all four platforms.

## Discussion

The app gives reviewers the bivariate model in a browser, with results reproducible in one step.

Limitations: the test datasets are curated examples; only the logit transformation is offered; the meta-regression takes one covariate; comparative accuracy of several tests is not supported; and outputs mada lacks (likelihood-ratio CIs, Deeks' test, Fagan nomogram) were not compared.

## Conclusions

A browser tool can reproduce standard bivariate meta-analysis of diagnostic test accuracy on published datasets.

## Data availability

**Underlying data:** datasets distributed with the R package mada 0.5.12 [5] (GPL-2), built at run time.

**Extended data:** app, analysis code, expected values, figures and screenshots, archived at Zenodo: [DOI to be added on release] [13]. Licence: MIT.

## Software availability

- **Source code available from:** https://github.com/mahmood726-cyber/allmeta (`dta-sroc/`, `shared/dta-bivariate.js`); validated version: commit 76d3e9d56891583849c1d08d77a8bc8666f2c2bd
- **Archived source code at time of publication:** Zenodo. DTA SROC app: reproducible validation against mada (v1.0.0). [DOI to be added on release] [13]
- **Licence:** MIT
- **Reproduction:** one click via GitHub Codespaces (free account), a fork's "Run workflow" button, or `python reproduce.py`; verified runs: https://mahmood726-cyber.github.io/dta-sroc-reproducible/

## Competing interests

The author develops allmeta. [AUTHOR TO CONFIRM: no other competing interests.]

## Grant information

[AUTHOR TO COMPLETE]

## Acknowledgements

[AUTHOR TO COMPLETE.] Claude (Anthropic), an AI assistant, helped write the software, the analysis code and the draft of this manuscript. The author checked all code, results and text.

## References

1. Reitsma JB, Glas AS, Rutjes AWS, Scholten RJPM, Bossuyt PM, Zwinderman AH. Bivariate analysis of sensitivity and specificity produces informative summary measures in diagnostic reviews. J Clin Epidemiol. 2005;58(10):982–90. doi:10.1016/j.jclinepi.2005.02.022
2. Rutter CM, Gatsonis CA. A hierarchical regression approach to meta-analysis of diagnostic test accuracy evaluations. Stat Med. 2001;20(19):2865–84. doi:10.1002/sim.942
3. Harbord RM, Deeks JJ, Egger M, Whiting P, Sterne JAC. A unification of models for meta-analysis of diagnostic accuracy studies. Biostatistics. 2007;8(2):239–51. doi:10.1093/biostatistics/kxl004
4. Moses LE, Shapiro D, Littenberg B. Combining independent studies of a diagnostic test into a summary ROC curve: data-analytic approaches and some additional considerations. Stat Med. 1993;12(14):1293–316. doi:10.1002/sim.4780121403
5. Doebler P. mada: Meta-analysis of diagnostic accuracy [R package and datasets], version 0.5.12. The R Foundation; 2012. doi:10.32614/CRAN.package.mada
6. Gasparrini A, Armstrong B, Kenward MG. Multivariate meta-analysis for non-linear and other multi-parameter associations. Stat Med. 2012;31(29):3821–39. doi:10.1002/sim.5471
7. Harbord RM, Whiting P. metandi: meta-analysis of diagnostic accuracy using hierarchical logistic regression. Stata J. 2009;9(2):211–29. doi:10.1177/1536867X0900900203
8. Ahmad M. allmeta — open browser-only tools for evidence synthesis [software]. Zenodo; 2026. doi:10.5281/zenodo.20516880
9. Jackson D, White IR, Riley RD. A matrix-based method of moments for fitting the multivariate random effects model for meta-analysis and meta-regression. Biom J. 2013;55(2):231–45. doi:10.1002/bimj.201200152
10. Deeks JJ, Macaskill P, Irwig L. The performance of tests of publication bias and other sample size effects in systematic reviews of diagnostic test accuracy was assessed. J Clin Epidemiol. 2005;58(9):882–93. doi:10.1016/j.jclinepi.2005.01.016
11. Kriston L, Hölzel L, Weiser AK, Berner MM, Härter M. Meta-analysis: are 3 questions enough to detect unhealthy alcohol use? Ann Intern Med. 2008;149(12):879–88. doi:10.7326/0003-4819-149-12-200812160-00007
12. Patrick DL, Cheadle A, Thompson DC, Diehr P, Koepsell T, Kinne S. The validity of self-reported smoking: a review and meta-analysis. Am J Public Health. 1994;84(7):1086–93. doi:10.2105/ajph.84.7.1086
13. Ahmad M. Bivariate meta-analysis of diagnostic test accuracy in the browser: a tool validated against the R package mada (v1.0.0) [software]. Zenodo; 2026. [DOI to be added on release]

## Figure and table legends

**Figure 1.** Using the app, step by step (AUDIT-C data, steps 1–4 and 6; smoking data, step 5; Google Chrome, light theme; high-resolution captures cropped to the relevant panels).
(1) Data entry, one row per study, and the list of mada's datasets.
(2) The model settings (A) and the notes on threshold effect and continuity correction (B).
(3) Summary estimates (A) and between-study covariance with HSROC parameters (B).
(4) ROC space: studies, Moses–Littenberg and bivariate SROC curves, summary point, and 95% confidence (solid) and prediction (dashed) regions.
(5) Meta-regression setting (A), coefficients for questionnaire type (B) and export buttons (C).
(6) Fagan nomogram at 20% pre-test probability (A) and Deeks' funnel plot (B).
Panels 2, 3, 5 and 6 are labelled composites of regions of one page; panels 1 and 4 are single crops.

**Figure 2.** Worked examples, the app (points) over mada (lines): (A) AUDIT-C, REML: SROC curve and 95% confidence and prediction regions; (B) smoking, meta-regression on questionnaire type: 95% confidence regions of the summary point for each type.

**Figure 3.** App versus mada for all 80 fits both programs return: largest relative difference in coefficients, their covariance and the between-study covariance, by method.

**Table 1.** Agreement with mada by method and continuity-correction rule (and meta-regression): configurations, fits, refusals and largest differences.

**Table 2.** Results by dataset: tables, zero cells, configurations, and REML summary sensitivity, specificity and AUC from each program.
