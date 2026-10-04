"""Write expected/*.json from a run's stats.json (used once, to record the canonical run).

  python analysis/set_expected.py outputs/full/stats.json expected/paper_values.json full
  python analysis/set_expected.py outputs/quick/stats.json expected/quick_values.json quick
Each number is stored rounded to the precision at which the paper prints it. Discrepancy maxima, which
differ between platforms in their last digits, enter only as threshold indicators (0/1).
"""
import json
import sys

# quantity -> decimals
FULL = {"datasets": 0, "studies_total": 0, "zero_cell_studies": 0, "datasets_with_zero_cells": 0,
        "configurations": 0, "mada_fitted": 0, "mada_refused": 0, "refusals_matched": 0, "app_refused_mada_fitted": 0,
        "app_fitted_mada_refused": 0, "within_tolerance": 0, "all_within_tolerance": 0, "meta_regression_configurations": 0,
        "checks_total": 0, "checks_passed": 0, "fits_reml_ml": 0, "fits_fixed_mm": 0, "fits_vc": 0,
        "reml_ml_below_1e-6": 0, "fixed_mm_vc_below_1e-12": 0, "loglik_below_1e-9": 0, "derived_below_1e-6": 0,
        "moses_cases": 0, "moses_fitted": 0, "moses_agree": 0, "mada_not_converged": 0,
        "ex_k": 0, "ex_zero": 0, "ex_sens": 3, "ex_sens_lo": 3, "ex_sens_hi": 3, "ex_spec": 3, "ex_spec_lo": 3, "ex_spec_hi": 3,
        "ex_auc": 3, "ex_pauc": 3, "ex_rho": 2, "ex_mada_sens": 3, "ex_mada_spec": 3, "ex_mada_auc": 3, "ex_lrpos": 2, "ex_lrneg": 2,
        "ex_ml_tau2_sens": 2, "ex_reml_tau2_sens": 2,
        "mr_k": 0, "mr_sens_saq": 2, "mr_sens_saq_se": 2, "mr_sens_saq_p": 3, "mr_fpr_saq": 2, "mr_fpr_saq_p": 2, "mr_mada_sens_saq": 2,
        "mr_sens_iaq": 2, "mr_sens_saq_prob": 2}
QUICK = {"datasets": 0, "configurations": 0, "mada_fitted": 0, "refusals_matched": 0, "all_within_tolerance": 0,
         "reml_ml_below_1e-6": 0, "derived_below_1e-6": 0, "ex_sens": 3, "ex_spec": 3, "ex_auc": 3}

stats, out, mode = sys.argv[1:4]
st = json.load(open(stats))
spec = FULL if mode == "full" else QUICK
vals = {}
for k, d in spec.items():
    v = round(float(st[k]), d)
    vals[k] = {"value": int(v) if d <= 0 else v, "decimals": d}
json.dump({"source": f"Canonical run ({mode} mode): values as printed in the paper.", "values": vals}, open(out, "w"), indent=1)
print(f"wrote {len(vals)} expected values to {out}")
