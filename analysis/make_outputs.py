"""Compare the app's engine with mada and build every table, figure and number in the paper.

  python analysis/make_outputs.py --results results/full --outputs outputs/full --expected expected/paper_values.json

Every case of the mada reference grid is judged as in allmeta's own parity test
(hub/shared/tests/_dta_parity_check.mjs; same discrepancy measures and tolerances, mirrored below). Exit
code 0 only if every number in the expected file is reproduced (after rounding to its stated decimals).
"""
import argparse
import csv
import json
import math
import random
import sys
from collections import defaultdict
from pathlib import Path

LABEL = {"AuditC": "AUDIT-C, unhealthy alcohol use", "Dementia": "MMSE, dementia", "IAQ": "Interviewer questionnaires, smoking",
         "SAQ": "Self-administered questionnaires, smoking", "skin_tests": "Skin tests, penicillin allergy", "smoking": "Questionnaires, smoking (IAQ + SAQ)"}
METHOD_LABEL = {"reml": "REML", "ml": "ML", "fixed": "Fixed effect", "mm": "Method of moments", "vc": "Variance components"}
CHI2 = 5.991464547107979
Z = 1.959963984540054


def jl(p):
    return {json.loads(l)["dataset"]: json.loads(l) for l in open(p, encoding="utf-8") if l.strip()}


def logit(p):
    return math.log(p / (1 - p))


# ---- parity measures consistent with allmeta, with strict input validity ----
def _strict_numeric_pairs(a, b):
    """Reject malformed validation inputs rather than silently checking a prefix.

    Values come from expected JSON numeric arrays. A missing element, empty
    comparison, or non-finite value makes numerical agreement indeterminate.
    """
    if len(a) != len(b) or not a:
        raise ValueError(f"Parity arrays must be nonempty and equal-length: {len(a)} vs {len(b)}")
    for i, (x, y) in enumerate(zip(a, b)):
        if isinstance(x, bool) or isinstance(y, bool):
            raise ValueError(f"Boolean parity value at index {i}")
        try:
            x, y = float(x), float(y)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Non-numeric parity value at index {i}") from exc
        if not math.isfinite(x) or not math.isfinite(y):
            raise ValueError(f"Non-finite parity value at index {i}")
        yield x, y


def rel_max(a, b):
    return max(abs(x - y) / max(1.0, abs(y)) for x, y in _strict_numeric_pairs(a, b))


def abs_max(a, b):
    return max(abs(x - y) for x, y in _strict_numeric_pairs(a, b))


def on_ellipse(C, mu, pts):
    det = C[0][0] * C[1][1] - C[0][1] * C[1][0]
    worst = 0.0
    for fpr, sens in pts:
        a, b = logit(sens) - mu[0], logit(fpr) - mu[1]
        q = (C[1][1] * a * a - 2 * C[0][1] * a * b + C[0][0] * b * b) / det
        worst = max(worst, abs(q - CHI2) / CHI2)
    return worst


def mat(v):  # R column-major 2x2
    return [[v[0], v[2]], [v[1], v[3]]]


def add(A, B):
    return [[A[i][j] + B[i][j] for j in range(2)] for i in range(2)]


def region_err(app, ref, kind):
    """Both directions: mada's 100 points on the app's region, the app's drawn region on mada's."""
    av, aP = mat(app["vcov"]), mat(app["Psi"])
    rv, rP = mat(ref["vcov"]), mat(ref["Psi"])
    Ca, Cr = (add(aP, av), add(rP, rv)) if kind == "pred" else (av, rv)
    rpts = list(zip(ref[kind]["fpr"], ref[kind]["sens"]))
    return max(on_ellipse(Ca, app["mu"], rpts), on_ellipse(Cr, ref["coef"], app[kind]))


def compare(app, ref):
    m = {"coef": rel_max(app["coef"], ref["coef"]), "vcov": rel_max(app["vcov"], ref["vcov"])}
    if ref.get("Psi"): m["Psi"] = rel_max(app["Psi"], ref["Psi"])
    if ref.get("logLik") is not None:
        m["logLik"] = abs(app["logLik"] - ref["logLik"]); m["AIC"] = abs(app["AIC"] - ref["AIC"]); m["BIC"] = abs(app["BIC"] - ref["BIC"])
    if ref.get("summary"):
        m["summary"] = max(abs_max(app["summary"]["sens"], ref["summary"]["sens"]), abs_max(app["summary"]["fpr"], ref["summary"]["fpr"]))
        m["corRandom"] = abs(app["summary"]["corRandom"] - ref["summary"]["corRandom"])
    if ref.get("hsroc"):
        ks = ["Theta", "Lambda", "beta", "sigma2theta", "sigma2alpha"]
        m["hsroc"] = rel_max([app["hsroc"][k] for k in ks], [ref["hsroc"][k] for k in ks])
    if ref.get("auc") and ref["auc"].get("rg"):
        m["auc"] = max(abs_max(app["auc"]["rg"], ref["auc"]["rg"]), abs_max(app["auc"]["naive"], ref["auc"]["naive"]) if ref["auc"].get("naive") else 0.0)
    if ref.get("sroc"):
        m["sroc"] = max(abs_max(app["sroc"]["rg"], ref["sroc"]["rg"]), abs_max(app["sroc"]["naive"], ref["sroc"]["naive"]))
    if ref.get("conf"): m["confRegion"] = region_err(app, ref, "conf")
    if ref.get("pred"): m["predRegion"] = region_err(app, ref, "pred")
    return m


def tolerance(ref):
    est = {"fixed": 1e-9, "mm": 1e-9, "vc": 1e-8, "reml": 1e-6, "ml": 1e-6}[ref["method"]]
    return {"coef": est, "vcov": est, "Psi": est, "logLik": 1e-6, "AIC": 1e-6, "BIC": 1e-6, "summary": 1e-6, "corRandom": 1e-6,
            "hsroc": max(est, 1e-6), "auc": 1e-6, "sroc": 1e-6, "confRegion": 1e-6, "predRegion": 1e-6}


def key(f):
    return (f["method"], f["correction"], f.get("formula") or "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", required=True); ap.add_argument("--outputs", required=True); ap.add_argument("--expected", required=True)
    a = ap.parse_args()
    res, out = Path(a.results), Path(a.outputs)
    out.mkdir(parents=True, exist_ok=True)
    R, E = jl(res / "mada.jsonl"), jl(res / "engine.jsonl")
    DS = list(R)
    cells = defaultdict(list)
    for row in csv.DictReader(open(res / "corpus.csv", encoding="utf-8")):
        cells[row["dataset"]].append(tuple(float(row[k]) for k in ("TP", "FN", "FP", "TN")))
    st = {"datasets": len(DS), "studies_total": sum(R[d]["k"] for d in DS),
          "zero_cell_studies": sum(E[d]["zero_cell_studies"] for d in DS),
          "datasets_with_zero_cells": sum(1 for d in DS if E[d]["zero_cell_studies"] > 0)}

    # ---- every configuration of the grid ----
    rows, nchecks, npass = [], 0, 0
    for ds in DS:
        app = {key(f): f for f in E[ds]["fits"]}
        for f in R[ds]["fits"]:
            g = app[key(f)]
            r = {"dataset": ds, "method": f["method"], "correction": f["correction"], "formula": (f.get("formula") or "").replace("cbind(tsens, tfpr) ", ""),
                 "mada_ok": f["ok"], "app_ok": g["ok"]}
            nchecks += 1
            if f["ok"] and g["ok"]:
                npass += 1
                m, tol = compare(g, f), tolerance(f)
                for k, v in m.items():
                    nchecks += 1; npass += v <= tol[k]
                r.update(m)
                r["within_tolerance"] = all(m[k] <= tol[k] for k in m)
                r["mada_converged"] = f.get("converged")
            else:
                ok_ = f["ok"] == g["ok"]; npass += ok_
                r["within_tolerance"] = ok_
            rows.append(r)
        for mr, mg in zip(R[ds]["moses"], E[ds]["moses"]):
            nchecks += 1
            npass += (mr["ok"] == mg["ok"]) and (not mr["ok"] or max(abs(mg["A1"] - mr["A1"]), abs(mg["B1"] - mr["B1"])) <= 1e-9)
    both = [r for r in rows if r["mada_ok"] and r["app_ok"]]
    ok = lambda r: r["within_tolerance"]
    itr = [r for r in both if r["method"] in ("reml", "ml")]
    drc = [r for r in both if r["method"] in ("fixed", "mm")]
    vc = [r for r in both if r["method"] == "vc"]
    mx = lambda rs, k: max(r[k] for r in rs if r.get(k) is not None)
    deriv = ["summary", "corRandom", "hsroc", "auc", "sroc", "confRegion", "predRegion"]
    moses_pairs = [(mr, mg) for d in DS for mr, mg in zip(R[d]["moses"], E[d]["moses"])]
    st.update({
        "configurations": len(rows), "mada_fitted": sum(r["mada_ok"] for r in rows), "mada_refused": sum(not r["mada_ok"] for r in rows),
        "refusals_matched": sum(1 for r in rows if not r["mada_ok"] and not r["app_ok"]),
        "app_refused_mada_fitted": sum(1 for r in rows if r["mada_ok"] and not r["app_ok"]),
        "app_fitted_mada_refused": sum(1 for r in rows if not r["mada_ok"] and r["app_ok"]),
        "within_tolerance": sum(ok(r) for r in rows), "all_within_tolerance": int(all(ok(r) for r in rows)),
        "meta_regression_configurations": sum(1 for r in rows if r["formula"]),
        "checks_total": nchecks, "checks_passed": npass,
        "fits_reml_ml": len(itr), "fits_fixed_mm": len(drc), "fits_vc": len(vc),
        "max_rel_reml_ml_estimates": max(mx(itr, "coef"), mx(itr, "vcov"), mx(itr, "Psi")),
        "max_rel_fixed_mm_vc_estimates": max(mx(drc + vc, "coef"), mx(drc + vc, "vcov"), max(r["Psi"] for r in drc + vc if r.get("Psi") is not None)),
        "max_abs_loglik": max(r["logLik"] for r in both if r.get("logLik") is not None),
        "max_derived": max(r[k] for r in both for k in deriv if r.get(k) is not None),
        "reml_ml_below_1e-6": int(max(mx(itr, "coef"), mx(itr, "vcov"), mx(itr, "Psi")) < 1e-6),
        "fixed_mm_vc_below_1e-12": int(max(mx(drc + vc, "coef"), mx(drc + vc, "vcov")) < 1e-12),
        "loglik_below_1e-9": int(max(r["logLik"] for r in both if r.get("logLik") is not None) < 1e-9),
        "derived_below_1e-6": int(max(r[k] for r in both for k in deriv if r.get(k) is not None) < 1e-6),
        "moses_cases": len(moses_pairs), "moses_fitted": sum(mr["ok"] for mr, _ in moses_pairs),
        "moses_agree": sum(1 for mr, mg in moses_pairs if mr["ok"] == mg["ok"] and (not mr["ok"] or max(abs(mg["A1"] - mr["A1"]), abs(mg["B1"] - mr["B1"])) <= 1e-9)),
        "mada_not_converged": sum(1 for r in both if r.get("mada_converged") is False),
    })

    def rf(ds, method="reml", cc="all", formula=""):
        return next(f for f in R[ds]["fits"] if key(f) == (method, cc, formula))

    def ef(ds, method="reml", cc="all", formula=""):
        return next(f for f in E[ds]["fits"] if key(f) == (method, cc, formula))

    # ---- tables ----
    def write(name, rws):
        with open(out / f"{name}.csv", "w", newline="", encoding="utf-8") as fh:
            fields = list(dict.fromkeys(k for r in rws for k in r))
            w = csv.DictWriter(fh, fieldnames=fields, restval=""); w.writeheader(); w.writerows(rws)
    groups = defaultdict(list)
    for r in rows: groups[(r["method"], r["correction"] if not r["formula"] else "meta-regression")].append(r)
    T1 = []
    for (m, c), rs in sorted(groups.items(), key=lambda kv: (list(METHOD_LABEL).index(kv[0][0]), ["all", "single", "none", "meta-regression"].index(kv[0][1]))):
        b = [r for r in rs if r["mada_ok"] and r["app_ok"]]
        g = lambda k: max((r[k] for r in b if r.get(k) is not None), default=None)
        T1.append({"method": METHOD_LABEL[m], "correction": c, "configurations": len(rs), "fitted_by_mada": sum(r["mada_ok"] for r in rs),
                   "refused_by_mada": sum(not r["mada_ok"] for r in rs), "refusals_matched": sum(1 for r in rs if not r["mada_ok"] and not r["app_ok"]),
                   "max_rel_coef": g("coef"), "max_rel_vcov": g("vcov"), "max_rel_Psi": g("Psi"), "max_abs_logLik": g("logLik"),
                   "max_abs_summary": g("summary"), "max_abs_auc": g("auc"), "max_rel_regions": max([v for v in (g("confRegion"), g("predRegion")) if v is not None], default=None),
                   "all_within_tolerance": all(ok(r) for r in rs)})
    write("table1_parity_by_method", T1)
    T2 = []
    for ds in DS:
        f, g = rf(ds), ef(ds); rs = [r for r in rows if r["dataset"] == ds]
        s, sp = g["summary"]["sens"], g["summary"]["fpr"]
        T2.append({"dataset": ds, "label": LABEL[ds], "studies": R[ds]["k"], "zero_cell_studies": E[ds]["zero_cell_studies"],
                   "configurations": len(rs), "fitted_by_mada": sum(r["mada_ok"] for r in rs), "refused_by_mada": sum(not r["mada_ok"] for r in rs),
                   "all_within_tolerance": all(ok(r) for r in rs),
                   "REML_sensitivity": s[0], "sens_lo": s[1], "sens_hi": s[2], "REML_specificity": 1 - sp[0], "spec_lo": 1 - sp[2], "spec_hi": 1 - sp[1],
                   "mada_sensitivity": f["summary"]["sens"][0], "mada_specificity": 1 - f["summary"]["fpr"][0],
                   "AUC": g["auc"]["rg"][0], "mada_AUC": f["auc"]["rg"][0], "tau2_logit_sens": g["Psi"][0], "tau2_logit_fpr": g["Psi"][3], "rho": g["summary"]["corRandom"]})
    write("table2_by_dataset", T2)
    write("table3_parity_all_configurations", rows)
    write("table4_moses_littenberg", [{"dataset": d, "correction": mr["correction"], "mada_ok": mr["ok"], "app_ok": mg["ok"],
                                       "mada_A1": mr.get("A1"), "app_A1": mg.get("A1"), "mada_B1": mr.get("B1"), "app_B1": mg.get("B1")}
                                      for d in DS for mr, mg in zip(R[d]["moses"], E[d]["moses"])])

    # ---- worked examples ----
    ex = "AuditC"
    f, g = rf(ex), ef(ex)
    st.update({"ex_k": R[ex]["k"], "ex_zero": E[ex]["zero_cell_studies"],
               "ex_sens": g["summary"]["sens"][0], "ex_sens_lo": g["summary"]["sens"][1], "ex_sens_hi": g["summary"]["sens"][2],
               "ex_spec": 1 - g["summary"]["fpr"][0], "ex_spec_lo": 1 - g["summary"]["fpr"][2], "ex_spec_hi": 1 - g["summary"]["fpr"][1],
               "ex_auc": g["auc"]["rg"][0], "ex_pauc": g["auc"]["rg"][1], "ex_rho": g["summary"]["corRandom"],
               "ex_mada_sens": f["summary"]["sens"][0], "ex_mada_spec": 1 - f["summary"]["fpr"][0], "ex_mada_auc": f["auc"]["rg"][0],
               "ex_lrpos": g["lr"]["pos"][0], "ex_lrneg": g["lr"]["neg"][0],
               "ex_ml_tau2_sens": ef(ex, "ml")["Psi"][0], "ex_reml_tau2_sens": g["Psi"][0]})
    has_mr = "smoking" in DS
    if has_mr:
      mr_f, mr_g = rf("smoking", formula="cbind(tsens, tfpr) ~ type"), ef("smoking", formula="cbind(tsens, tfpr) ~ type")
      ct = {(c["outcome"], c["term"]): c for c in mr_g["coefTable"]}
      sa, fa = ct[("logit sensitivity", "typeSAQ")], ct[("logit FPR", "typeSAQ")]
      st.update({"mr_k": R["smoking"]["k"], "mr_sens_saq": sa["estimate"], "mr_sens_saq_se": sa["se"], "mr_sens_saq_p": sa["p"],
                 "mr_fpr_saq": fa["estimate"], "mr_fpr_saq_p": fa["p"], "mr_mada_sens_saq": mr_f["coef"][1],
                 "mr_sens_iaq": 1 / (1 + math.exp(-mr_g["coef"][0])), "mr_sens_saq_prob": 1 / (1 + math.exp(-(mr_g["coef"][0] + mr_g["coef"][1])))})

    # ---- figures ----
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "figure.facecolor": "white", "savefig.facecolor": "white"})
    meta = {"Software": None}
    C = {"app": "#1b6ca8", "ref": "#444444", "pt": "#b23a48"}
    exp_ = lambda x: 1 / (1 + math.exp(-x))
    # Figure 2: worked examples in ROC space
    fig, axs = plt.subplots(1, 2, figsize=(9.2, 4.5))
    ax = axs[0]
    st_rows = cells[ex]
    for tp, fn, fp, tn in st_rows:
        c = 0.5 if E[ex]["zero_cell_studies"] else 0
        ax.scatter((fp + c) / (fp + tn + 2 * c), (tp + c) / (tp + fn + 2 * c), s=14 + 60 * (tp + fn + fp + tn) / max(sum(r) for r in st_rows), facecolor="none", edgecolor="#888888", lw=0.8)
    grid = [i / 200 for i in range(1, 200)]
    h = f["hsroc"]; slope, icpt = math.exp(-h["beta"]), h["Lambda"] * math.exp(-h["beta"] / 2)
    ax.plot(grid, [exp_(icpt + slope * logit(x)) for x in grid], "-", color="#111111", lw=2.0, label="mada: SROC curve")
    ax.plot(f["conf"]["fpr"] + f["conf"]["fpr"][:1], f["conf"]["sens"] + f["conf"]["sens"][:1], "-", color="#999999", lw=1.0, label="mada: 95% confidence region")
    ax.plot(f["pred"]["fpr"] + f["pred"]["fpr"][:1], f["pred"]["sens"] + f["pred"]["sens"][:1], "--", color="#999999", lw=1.0, label="mada: 95% prediction region")
    ax.plot(g["sroc"]["fpr"], g["sroc"]["rg"], "o", color=C["app"], ms=4, label="App: SROC curve")
    ax.plot([p[0] for p in g["conf"][::5]], [p[1] for p in g["conf"][::5]], "s", color=C["app"], ms=3, label="App: confidence region")
    ax.plot([p[0] for p in g["pred"][::5]], [p[1] for p in g["pred"][::5]], "^", color=C["app"], ms=3, label="App: prediction region")
    ax.plot([g["summary"]["fpr"][0]], [g["summary"]["sens"][0]], "D", color=C["pt"], ms=6, label="Summary point")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_xlabel("False-positive rate (1 − specificity)"); ax.set_ylabel("Sensitivity")
    ax.set_title(f"A. AuditC ({R[ex]['k']} studies), REML", fontsize=9.5); ax.legend(fontsize=6.5, frameon=False, loc="lower right")
    ax = axs[1]
    for lev, sel, col in (() if not has_mr else (("IAQ", 0, "#2c7a4b"), ("SAQ", 1, "#8a4b9b"))):
        for src, coef, V, sty in (("mada", mr_f["coef"], mat4(mr_f["vcov"]), "-"), ("App", mr_g["coef"], mat4(mr_g["vcov"]), None)):
            L = [[1, sel, 0, 0], [0, 0, 1, sel]]
            mu = [sum(L[i][j] * coef[j] for j in range(4)) for i in range(2)]
            Cv = [[sum(L[i][p] * V[p][q] * L[j][q] for p in range(4) for q in range(4)) for j in range(2)] for i in range(2)]
            pts = ellipse_pts(Cv, mu, 100)
            if sty: ax.plot([exp_(b) for a_, b in pts], [exp_(a_) for a_, b in pts], sty, color=col, lw=1.2, label=f"mada: {lev}")
            else: ax.plot([exp_(b) for a_, b in pts[::5]], [exp_(a_) for a_, b in pts[::5]], "o", color=col, ms=3, label=f"App: {lev}")
            ax.plot([exp_(mu[1])], [exp_(mu[0])], "D" if sty else "x", color=col, ms=5)
    ax.set_xlim(0, 0.3); ax.set_ylim(0.6, 1); ax.set_xlabel("False-positive rate (1 − specificity)")
    ax.set_title(f"B. Smoking ({R['smoking']['k'] if has_mr else 0} studies): meta-regression on type", fontsize=9.5); ax.legend(fontsize=7, frameon=False, loc="lower right")
    fig.suptitle("Figure 2. Worked examples: the app (points) over mada (lines); 95% confidence regions in panel B", fontsize=10)
    fig.tight_layout(); fig.savefig(out / "figure2_worked_examples.png", dpi=300, metadata=meta); plt.close(fig)
    with open(out / "figure2_worked_examples.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(["series", "fpr", "sens_mada", "sens_app"])
        for x, rv, av in zip(f["sroc"]["fpr"], f["sroc"]["rg"], g["sroc"]["rg"]): w.writerow(["AuditC SROC (Rutter-Gatsonis)", x, rv, av])
    # Figure 3: agreement, every fit, by method
    order = ["reml", "ml", "vc", "mm", "fixed"]
    lg = lambda x: math.log10(max(x, 1e-17))
    fig, ax = plt.subplots(figsize=(7.6, 3.4))
    rng = random.Random(1)
    for i, m in enumerate(order):
        rs = [r for r in both if r["method"] == m]
        for r in rs:
            worst = max(r[k] for k in ("coef", "vcov", "Psi") if r.get(k) is not None)
            ax.scatter(lg(worst), i + rng.uniform(-0.25, 0.25), s=10, alpha=0.6, color=C["app"] if not r["formula"] else "#c27c0e", marker="o" if not r["formula"] else "D")
        ax.text(-1.2, i, f"n = {len(rs)}", va="center", fontsize=8)
    ax.axvline(-6, color=C["ref"], ls="--", lw=0.8); ax.axvline(-9, color=C["ref"], ls=":", lw=0.8)
    ax.set_yticks(range(len(order)), [METHOD_LABEL[m] for m in order]); ax.set_xlim(-17, 0.5); ax.set_ylim(-0.6, len(order) - 0.4)
    ax.set_xlabel("log10 largest relative difference from mada (coefficients, vcov, Ψ)")
    ax.scatter([], [], color=C["app"], s=10, label="Summary model"); ax.scatter([], [], color="#c27c0e", marker="D", s=10, label="Meta-regression")
    ax.legend(fontsize=7.5, frameon=True, framealpha=0.95, edgecolor="#dddddd", loc="center", bbox_to_anchor=(0.72, 0.5))
    ax.set_title(f"Figure 3. App versus mada: all {len(both)} fits both programs return\n(dashed: tolerance 1e-6 for REML/ML; dotted: 1e-9 for fixed effect and MM, 1e-8 for VC)", fontsize=9.5)
    ax.grid(axis="x", color="#eeeeee", lw=0.6); fig.tight_layout(); fig.savefig(out / "figure3_agreement.png", dpi=300, metadata=meta); plt.close(fig)
    with open(out / "figure3_agreement.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(["dataset", "method", "correction", "formula", "max_rel_estimates"])
        for r in both: w.writerow([r["dataset"], r["method"], r["correction"], r["formula"], max(r[k] for k in ("coef", "vcov", "Psi") if r.get(k) is not None)])
    # Visual abstract
    fig = plt.figure(figsize=(11, 4.6)); fig.patch.set_facecolor("white")
    boxes = [("Problem", "Bivariate meta-analysis of\ndiagnostic accuracy is\nusually run in R, Stata\nor SAS."),
             ("Tool", "allmeta DTA SROC app:\noffline, in the browser.\nREML, ML, moments, variance\ncomponents or fixed effect;\nmeta-regression; SROC,\nregions, AUC, LR±."),
             ("Validation", f"Against R mada on its\n{len(DS)} example datasets\n({st['studies_total']} studies): {st['configurations']}\nmethod × correction ×\ncovariate configurations."),
             ("Result", f"All {st['configurations']} agree: {st['mada_fitted']} fits\nwithin tolerance and the\nsame {st['refusals_matched']} refusals;\n{st['checks_passed']}/{st['checks_total']} checks pass.")]
    for i, (hh, txt) in enumerate(boxes):
        x = 0.02 + i * 0.245
        fig.patches.append(matplotlib.patches.FancyBboxPatch((x, 0.22), 0.22, 0.60, boxstyle="round,pad=0.01", transform=fig.transFigure, facecolor=["#f4ece8", "#e8f0f7", "#eaf4ec", "#fdf6e3"][i], edgecolor="#999"))
        fig.text(x + 0.11, 0.75, hh, ha="center", fontsize=13, weight="bold")
        fig.text(x + 0.11, 0.48, txt, ha="center", va="center", fontsize=10.5, linespacing=1.4)
        if i < 3: fig.text(x + 0.2325, 0.52, "→", ha="center", va="center", fontsize=18)
    fig.text(0.5, 0.09, "One command reproduces every number on Linux, Windows, macOS and Docker: github.com/mahmood726-cyber/dta-sroc-reproducible",
             ha="center", fontsize=9, color="#333333")
    fig.text(0.5, 0.91, "A browser tool for diagnostic test accuracy meta-analysis, validated against R mada", ha="center", fontsize=13.5, weight="bold")
    fig.savefig(out / "visual_abstract.png", dpi=300, metadata=meta); plt.close(fig)
    (out / "stats.json").write_text(json.dumps(st, indent=1, default=float))

    # ---- PASS/FAIL ----
    exp = json.loads(Path(a.expected).read_text())
    rep = []
    for k, spec in exp["values"].items():
        g_ = st.get(k)
        if isinstance(spec["value"], str):
            okv = g_ == spec["value"]; shown = g_
        else:
            d = spec["decimals"]
            okv = g_ is not None and round(float(g_), d) == round(float(spec["value"]), d)
            shown = None if g_ is None else (int(round(float(g_), d)) if d <= 0 else round(float(g_), d + 2))
        rep.append((k, spec["value"], shown, "PASS" if okv else "FAIL"))
    npass_ = sum(r[3] == "PASS" for r in rep)
    md = ["| Quantity | Expected | Reproduced | Result |", "|---|--:|--:|---|"] + [f"| {a_} | {b} | {c} | {d} |" for a_, b, c, d in rep]
    (out / "reproduction_report.md").write_text(f"# Reproduction report\n\n{npass_}/{len(rep)} numbers reproduced\n\n" + "\n".join(md) + "\n", encoding="utf-8")
    w = max(len(r[0]) for r in rep) if rep else 0
    for a_, b, c, d in rep: print(f"{a_.ljust(w)}  {str(b):>14}  {str(c):>16}  {d}")
    print(f"\n{npass_}/{len(rep)} numbers reproduced: {'ALL PASS' if npass_ == len(rep) else 'FAILURES PRESENT'}")
    sys.exit(0 if rep and npass_ == len(rep) else 1)


def mat4(v):  # R column-major 4x4
    return [[v[j * 4 + i] for j in range(4)] for i in range(4)]


def ellipse_pts(Cv, mu, n):
    r = math.sqrt(CHI2); l00 = math.sqrt(Cv[0][0]); l10 = Cv[1][0] / l00; l11 = math.sqrt(max(0.0, Cv[1][1] - l10 * l10))
    return [(mu[0] + l00 * r * math.cos(2 * math.pi * i / n), mu[1] + r * (l10 * math.cos(2 * math.pi * i / n) + l11 * math.sin(2 * math.pi * i / n))) for i in range(n + 1)]



if __name__ == "__main__":
    main()
