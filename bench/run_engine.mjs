// Run the app's JavaScript engine (app/shared/dta-bivariate.js, loaded unchanged) on every case of the
// mada reference grid: same data, method, continuity-correction rule and covariates. The page
// app/dta-sroc/index.html passes its parsed rows to the same functions (fit, mosesLittenberg,
// regionEllipse, srocAt). The configurations are fixed below (identical to bench/reference_mada.R), so
// this output depends only on the corpus and the engine, not on R. Output: one JSON object per dataset.
//
//   node bench/run_engine.mjs results/full/corpus.csv results/full/engine.jsonl
import { readFileSync, writeFileSync, mkdirSync } from "fs";
import { createHash } from "crypto";
import { createRequire } from "module";
import { dirname, join } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, "..");
const require = createRequire(import.meta.url);
const ENGINE = join(ROOT, "app", "shared", "dta-bivariate.js");
const B = require(ENGINE);
const sha = (f) => createHash("sha256").update(readFileSync(f)).digest("hex");

function parseCSV(text) {
  const rows = []; let row = [], cur = "", q = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) { if (c === '"') { if (text[i + 1] === '"') { cur += '"'; i++; } else q = false; } else cur += c; }
    else if (c === '"') q = true;
    else if (c === ",") { row.push(cur); cur = ""; }
    else if (c === "\n") { row.push(cur); rows.push(row); row = []; cur = ""; }
    else if (c !== "\r") cur += c;
  }
  if (cur.length || row.length) { row.push(cur); rows.push(row); }
  const h = rows.shift();
  return rows.filter((r) => r.length > 1).map((r) => Object.fromEntries(h.map((k, i) => [k, r[i]])));
}

const METHODS = ["reml", "ml", "fixed", "mm", "vc"], CC = ["all", "single", "none"];
const REG = { smoking: ["type", "population", "type + population"] };
const FPRGRID = [0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 0.99];

// R model.matrix: character covariates become treatment-coded factors with alphabetically sorted levels.
function design(studies, rhs) {
  const names = ["(Intercept)"], cols = [];
  for (const t of rhs.split("+").map((s) => s.trim())) {
    const v = studies.map((s) => s[t]), lev = [...new Set(v)].sort();
    for (const l of lev.slice(1)) { names.push(t + l); cols.push(v.map((x) => (x === l ? 1 : 0))); }
  }
  return { X: studies.map((_, i) => [1, ...cols.map((c) => c[i])]), covariateNames: names };
}

function one(rows, opts) {
  let f;
  try { f = B.fit(rows, opts); } catch (e) { return { ok: false, error: String(e.message || e) }; }
  const o = { ok: true, coef: f.coef, vcov: f.vcov.flat(), Psi: f.Psi.flat(), logLik: f.logLik, AIC: f.AIC, BIC: f.BIC,
    converged: f.converged, niter: f.niter, negeigen: f.negeigen };
  if (f.p === 1) {
    Object.assign(o, { mu: [f.muLogitSe, f.muLogitFPR], summary: { sens: [f.sens, ...f.sensCI], fpr: [f.fpr, ...f.fprCI], corRandom: f.corRandom },
      lr: { pos: [f.lrPos, ...f.lrPosCI], neg: [f.lrNeg, ...f.lrNegCI], dor: f.dor }, hsroc: f.hsroc, auc: f.auc });
    if (f.srocSlope != null) o.sroc = { fpr: FPRGRID, rg: FPRGRID.map((x) => B.srocAt(f, x, "ruttergatsonis")), naive: FPRGRID.map((x) => B.srocAt(f, x, "naive")) };
    o.conf = B.regionEllipse(f, "confidence", 100).map((p) => [p.fpr, p.tpr]);
    o.pred = B.regionEllipse(f, "prediction", 100).map((p) => [p.fpr, p.tpr]);
  } else {
    o.coefTable = f.coefTable.map((c) => ({ outcome: c.outcome, term: c.term, estimate: c.estimate, se: c.se, z: c.z, p: c.p }));
  }
  return o;
}

const [corpusFile, out] = process.argv.slice(2);
const corpus = parseCSV(readFileSync(corpusFile, "utf8"));
const lines = [];
for (const ds of [...new Set(corpus.map((r) => r.dataset))]) {
  const studies = corpus.filter((r) => r.dataset === ds);
  const rows = studies.map((r) => ({ tp: +r.TP, fp: +r.FP, fn: +r.FN, tn: +r.TN }));
  const fits = [];
  for (const cc of CC) for (const m of METHODS) fits.push({ method: m, correction: cc, ...one(rows, { method: m, correctionControl: cc }) });
  for (const rhs of REG[ds] || []) for (const m of METHODS) {
    const d = design(studies, rhs);
    fits.push({ method: m, correction: "all", formula: `cbind(tsens, tfpr) ~ ${rhs}`, ...one(rows, { method: m, correctionControl: "all", ...d }) });
  }
  const moses = CC.map((cc) => {
    try { const r = B.mosesLittenberg(rows, { correctionControl: cc }); return r ? { correction: cc, ok: true, A1: r.A1, B1: r.B1 } : { correction: cc, ok: false }; }
    catch (e) { return { correction: cc, ok: false, error: String(e.message || e) }; }
  });
  const deeks = B.deeksTest(rows);
  lines.push(JSON.stringify({ dataset: ds, k: rows.length, zero_cell_studies: rows.filter((r) => !(r.tp && r.fp && r.fn && r.tn)).length,
    fits, moses, spearman_all: B.thresholdSpearman(rows, { correctionControl: "all" }), deeks: deeks && { slope: deeks.slope, t: deeks.t, p: deeks.p } }));
}
mkdirSync(dirname(out), { recursive: true });
writeFileSync(out, lines.join("\n") + "\n");
console.log(`engine (${process.version}): ${lines.length} datasets -> ${out}; dta-bivariate.js sha256 ${sha(ENGINE).slice(0, 16)}`);
