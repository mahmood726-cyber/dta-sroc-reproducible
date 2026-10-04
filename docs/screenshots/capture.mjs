// Figure 1: step-by-step workflow of the DTA SROC app, high resolution (Playwright + installed Google Chrome,
// headless). Viewport 1106 x 900 CSS px, light theme, device scale factor 6: every region is captured as a page
// clip at 6 device pixels per CSS pixel. compose.py lays the regions out (tight crops, labelled sub-panels) and
// checks legibility from the font sizes recorded here. Data: the app's built-in copies of mada's AuditC
// (steps 1-4, 6) and smoking (step 5) datasets.
//   node docs/screenshots/capture.mjs <work-dir> http://localhost:8000/app/dta-sroc/index.html
//   python docs/screenshots/compose.py <work-dir> docs/screenshots
import { chromium } from "playwright";
import { writeFileSync, mkdirSync } from "fs";
const [D, APP] = process.argv.slice(2);
const OUT = `${D}/regions`; mkdirSync(OUT, { recursive: true });
const DPR = 6;
const b = await chromium.launch({ channel: "chrome" });
const ctx = await b.newContext({ viewport: { width: 1106, height: 900 }, colorScheme: "light", deviceScaleFactor: DPR });
const p = await ctx.newPage();
const errs = []; p.on("pageerror", (e) => errs.push(e.message));
const meta = { dpr: DPR, viewport: [1106, 900], regions: {}, states: {} };
await p.goto(APP); await p.evaluate(() => { try { localStorage.clear(); } catch (e) {} }); await p.goto(APP); await p.waitForTimeout(500);
await p.addStyleTag({ content: "#hub-back{display:none!important}" });
const set = async (o) => { for (const [id, v] of Object.entries(o)) await p.selectOption("#" + id, v); await p.waitForTimeout(500); };
const load = async (key) => { await set({ "f-example": key }); await p.click("#btn-example"); await p.waitForTimeout(700);
  await p.evaluate(() => { document.getElementById("f-data").scrollTop = 0; }); };
const state = async (name) => (meta.states[name] = await p.evaluate(() => ({ stats: document.getElementById("stats-wrap").innerText,
  notes: document.getElementById("warn-banner").innerText, fit: window.__almResults().bivariate, mr: window.__almResults().meta_regression })));
// page rectangle of an element, or of the h2 / legend whose text starts with `h2:<text>` / `legend:<text>`
const rect = (sel, opt = {}) => p.evaluate(([sel, opt]) => {
  const pick = (tag, t) => [...document.querySelectorAll(tag)].find((h) => h.textContent.trim().startsWith(t));
  let e = sel.startsWith("h2:") ? pick("h2", sel.slice(3)) : sel.startsWith("legend:") ? pick("legend", sel.slice(7)) : document.querySelector(sel);
  if (!e) throw new Error("missing " + sel);
  if (opt.closest) e = e.closest(opt.closest);
  if (opt.up) for (let i = 0; i < opt.up; i++) e = e.parentElement;
  const r = e.getBoundingClientRect(); return { x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height };
}, [sel, opt]);
const union = (...rs) => { const x = Math.min(...rs.map((r) => r.x)), y = Math.min(...rs.map((r) => r.y));
  return { x, y, w: Math.max(...rs.map((r) => r.x + r.w)) - x, h: Math.max(...rs.map((r) => r.y + r.h)) - y }; };
async function region(name, r, pad = 6) {
  const c = { x: Math.max(0, Math.floor(r.x - pad)), y: Math.max(0, Math.floor(r.y - pad)), width: Math.ceil(r.w + 2 * pad), height: Math.ceil(r.h + 2 * pad) };
  await p.screenshot({ path: `${OUT}/${name}.png`, clip: c, fullPage: true });
  const fonts = await p.evaluate((c) => {
    const out = [];
    const inside = (rr) => rr.width > 0 && rr.height > 0 && rr.left + scrollX >= c.x - 1 && rr.right + scrollX <= c.x + c.width + 1 && rr.top + scrollY >= c.y - 1 && rr.bottom + scrollY <= c.y + c.height + 1;
    const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    for (let n = tw.nextNode(); n; n = tw.nextNode()) {
      const t = n.textContent.trim(); if (t.length < 2) continue;
      const el = n.parentElement; const cs = getComputedStyle(el); if (cs.visibility === "hidden" || cs.display === "none") continue;
      if (el.tagName === "TEXTAREA" || el.tagName === "SCRIPT" || el.tagName === "STYLE" || el.tagName === "OPTION") continue;
      const range = document.createRange(); range.selectNodeContents(n); const rr = range.getBoundingClientRect(); if (!inside(rr)) continue;
      let px = parseFloat(cs.fontSize);
      if (el.closest("svg") && el.getScreenCTM) { const m = el.getScreenCTM(); if (m) px = px * Math.hypot(m.a, m.b); }
      out.push([Math.round(px * 100) / 100, t.length]);
    }
    // text inside form fields (textarea content, selected options) is not a laid-out text node: record those fields too
    document.querySelectorAll("textarea, input[type=text], select").forEach((f) => { const rr = f.getBoundingClientRect(); if (inside(rr)) out.push([parseFloat(getComputedStyle(f).fontSize), 10]); });
    return out;
  }, c);
  meta.regions[name] = { clip: c, fonts };
}

// 1 data entry: AuditC (14 studies, two with a zero cell) from the example list
await load("AuditC"); await set({ "f-method": "reml", "f-cc": "all", "f-cov": "" }); await state("step1");
await region("d1_data", await rect("legend:Data", { closest: "fieldset" }));
// 2 choosing the model: REML, mada's default continuity correction, no covariate
await region("d2_model", await rect("legend:Bivariate model", { closest: "fieldset" }));
// 3 summary results: statistics, between-study covariance and HSROC parameters, notes
await state("step3");
await region("d3_stats", await rect("#stats-wrap .stats"));
await region("d3_hsroc", await rect("#stats-wrap table.coef"));
await region("d3_notes", await rect("#warn-banner"));
// 4 ROC space: studies, Moses and bivariate SROC curves, summary point, 95% confidence and prediction regions
await region("d4_roc", await rect("#svg-host svg"), 2);
// 6 Fagan nomogram, Deeks' funnel and export (still AuditC)
await region("d6_fagan", union(await rect("h2:Fagan"), await rect("#fagan-host svg")));
await region("d6_deeks", union(await rect("h2:Deeks"), await rect("#deeks-host svg")));
await region("d6_export", await rect("#alm-export-mount"));
// 5 meta-regression: smoking, covariate = questionnaire type (last column)
await load("smoking"); await state("step5");
await region("d5_setting", await rect("#f-cov", { up: 1 }));
await region("d5_table", await rect("#stats-wrap table.coef:last-of-type"));
meta.errors = errs;
writeFileSync(`${D}/regions_meta.json`, JSON.stringify(meta, null, 1));
console.log(JSON.stringify({ states: meta.states, regions: Object.keys(meta.regions), errors: errs }, null, 1));
await b.close();
