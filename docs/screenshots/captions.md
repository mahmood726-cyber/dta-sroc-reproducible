# Figure 1: using the app, step by step

Data: the app's built-in copies of mada's AuditC (AUDIT-C for unhealthy alcohol use, 14 studies; steps 1–4 and 6) and smoking (self-reported smoking, 51 two-by-two tables; step 5). App: allmeta commit 76d3e9d.

## How the images were captured
- **Browser:** Google Chrome, driven by Playwright (`capture.mjs`), light theme.
- **Window:** 1106 × 900 CSS px.
- **Resolution:** 6 device pixels per CSS pixel, so no image is ever enlarged.
- **Cropping:** each image is cropped tightly to the panels it shows.
- **Composites:** steps 2, 3, 5 and 6 are labelled composites (A, B, C) of regions of one page state, stacked by `compose.py`. Steps 1 and 4 are single crops.
- **Formats:** final width 2556–3300 px, lossless PNG plus uncompressed TIFF at 382–493 dpi for a 170 mm print width.
- **Legibility:** text measured in the page prints at 9.0 pt or larger at 170 mm. See `legibility.json`.

## Steps
- **step1: Data entry.** One row per study (`label, TP, FP, FN, TN`), here AuditC loaded from the list of mada's six datasets.
- **step2: Choosing the model (composite).**
  - (A) Estimation method REML (mada's default; also ML, method of moments, variance components, fixed effect); continuity correction 0.5 to all studies when any cell is zero (mada's default; also affected studies only, or none); no covariate.
  - (B) Notes: a threshold effect is likely (Spearman ρ > 0.6), and two studies have a zero cell, so the correction was applied to every study.
- **step3: Summary results (composite).**
  - (A) Summary sensitivity 0.891 (95% CI 0.808 to 0.941) and specificity 0.780 (0.715 to 0.833); LR+ 4.04, LR− 0.14; diagnostic odds ratio 28.9; AUC 0.887 (partial AUC 0.861); AIC; the Moses–Littenberg regression; Spearman's threshold correlation; Deeks' test.
  - (B) Between-study variances (1.38 and 0.41 on the logit scale) and correlation (0.85); Rutter–Gatsonis parameters; log-likelihood.
- **step4: ROC space.** Each study (circle area proportional to its size), the Moses–Littenberg SROC curve (blue), the bivariate (Rutter–Gatsonis) SROC curve, summary point (diamond) and 95% confidence (solid) and prediction (dashed) regions (red).
- **step5: Meta-regression and export (composite).**
  - (A) The last data column (questionnaire type) as a study-level covariate.
  - (B) Coefficients on the logit scale: self-administered questionnaires (SAQ) lower logit sensitivity by 1.073 (SE 0.398; p = 0.0071) with no difference in the false-positive rate (p = 0.82).
  - (C) Export buttons: Methods + Results (Markdown), text, JSON, CSV, and data (Markdown).
- **step6: Fagan nomogram and Deeks' funnel (composite).**
  - (A) At a pre-test probability of 20%, a positive test gives 50% and a negative test 3%.
  - (B) Deeks' funnel plot: log diagnostic odds ratio against 1/√(effective sample size), with the regression line (p = 0.031).

## To regenerate
Serve the repository root, for example `python -m http.server 8000`, then:

```bash
node docs/screenshots/capture.mjs work http://localhost:8000/app/dta-sroc/index.html
python docs/screenshots/compose.py work docs/screenshots
```
