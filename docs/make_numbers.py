"""Write docs/numbers.json: every number printed in docs/paper.md, its value as printed, and the stats key it comes from.

  python docs/make_numbers.py outputs/full/stats.json "<source description>"
Fails if a printed value is not what the run gives after rounding as printed.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# (quantity, as printed, stats key, how the printed text is derived from the value)
N = [
    ("Datasets distributed with mada", "6", "datasets", "int"),
    ("Two-by-two tables in those datasets", "159", "studies_total", "int"),
    ("Tables with a zero cell", "18", "zero_cell_studies", "int"),
    ("Method x correction x covariate configurations", "105", "configurations", "int"),
    ("Configurations agreeing", "105", "within_tolerance", "int"),
    ("Configurations mada fits", "80", "mada_fitted", "int"),
    ("Configurations mada refuses", "25", "mada_refused", "int"),
    ("Refusals the app matches", "25", "refusals_matched", "int"),
    ("Meta-regression configurations", "15", "meta_regression_configurations", "int"),
    ("Individual checks", "855", "checks_total", "int"),
    ("Individual checks passed", "855", "checks_passed", "int"),
    ("MM / VC / fixed-effect estimates within 10^-12", "yes", "fixed_mm_vc_below_1e-12", "flag"),
    ("REML / ML estimates within 10^-6", "yes", "reml_ml_below_1e-6", "flag"),
    ("Log-likelihoods within 10^-9 (well inside the 10^-6 required)", "yes", "loglik_below_1e-9", "flag"),
    ("Derived quantities within 10^-6", "yes", "derived_below_1e-6", "flag"),
    ("Moses-Littenberg comparisons", "18", "moses_cases", "int"),
    ("Moses-Littenberg comparisons agreeing", "18", "moses_agree", "int"),
    ("Worked example: studies", "14", "ex_k", "int"),
    ("Worked example: sensitivity", "0.891", "ex_sens", "3dp"),
    ("Worked example: sensitivity lower 95% limit", "0.808", "ex_sens_lo", "3dp"),
    ("Worked example: sensitivity upper 95% limit", "0.941", "ex_sens_hi", "3dp"),
    ("Worked example: specificity", "0.780", "ex_spec", "3dp"),
    ("Worked example: specificity lower 95% limit", "0.715", "ex_spec_lo", "3dp"),
    ("Worked example: specificity upper 95% limit", "0.833", "ex_spec_hi", "3dp"),
    ("Worked example: mada sensitivity", "0.891", "ex_mada_sens", "3dp"),
    ("Worked example: mada specificity", "0.780", "ex_mada_spec", "3dp"),
    ("Worked example: AUC", "0.887", "ex_auc", "3dp"),
    ("Worked example: LR+", "4.04", "ex_lrpos", "2dp"),
    ("Worked example: LR-", "0.14", "ex_lrneg", "2dp"),
    ("Worked example: REML logit-sensitivity variance", "1.38", "ex_reml_tau2_sens", "2dp"),
    ("Worked example: ML logit-sensitivity variance", "1.22", "ex_ml_tau2_sens", "2dp"),
    ("Meta-regression: tables", "51", "mr_k", "int"),
    ("Meta-regression: SAQ effect on logit sensitivity", "−1.07", "mr_sens_saq", "2dp"),
    ("Meta-regression: its SE", "0.40", "mr_sens_saq_se", "2dp"),
    ("Meta-regression: its p value", "0.007", "mr_sens_saq_p", "3dp"),
    ("Meta-regression: sensitivity, SAQ", "0.88", "mr_sens_saq_prob", "2dp"),
    ("Meta-regression: sensitivity, IAQ", "0.96", "mr_sens_iaq", "2dp"),
    ("Meta-regression: SAQ effect on logit FPR", "0.07", "mr_fpr_saq", "2dp"),
    ("Meta-regression: its p value", "0.82", "mr_fpr_saq_p", "2dp"),
]


def shown(v, how):
    if how == "int": return str(int(round(v)))
    if how == "flag": return "yes" if v == 1 else "no"
    if how.endswith("dp"): return f"{v:.{int(how[0])}f}".replace("-", "−")
    return how if v == how else f"MISMATCH {v}"


st = json.loads(Path(sys.argv[1]).read_text())
src = sys.argv[2] if len(sys.argv) > 2 else "reproduce.py full run"
out, bad = [], []
for q, printed, k, how in N:
    s = shown(st[k], how)
    if s != printed: bad.append(f"{q}: printed {printed}, run gives {s}")
    out.append({"quantity": q, "printed": printed, "stats_key": k, "value": st[k]})
if bad: sys.exit("numbers.json NOT written:\n  " + "\n  ".join(bad))
(ROOT / "docs" / "numbers.json").write_text(json.dumps({"source": src, "numbers": out}, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"docs/numbers.json: {len(out)} numbers, all as printed")
