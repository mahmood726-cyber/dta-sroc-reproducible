"""Compose Figure 1 (step1..step6) from the high-resolution regions captured by capture.mjs.

  python docs/screenshots/compose.py <work-dir> <out-dir>

Each step is one region or a stack of regions from the same page state, cropped tightly (uniform margins
trimmed) and labelled A, B, C in a left gutter, as in the figure legend. Regions keep their relative scale. The final image is
2400-3300 px wide, written as lossless PNG and as uncompressed TIFF whose dpi makes it 170 mm wide (>= 300 dpi).
Legibility is checked from the font sizes capture.mjs recorded in the page: printed size (pt) of a text of
f CSS px = f x (final px per CSS px) / (final width px / 170 mm) x 72 / 25.4 x ... (see pt() below).
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
import matplotlib

D, OUT = Path(sys.argv[1]), Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
META = json.loads((D / "regions_meta.json").read_text(encoding="utf-8"))
DPR = META["dpr"]
PRINT_IN = 170 / 25.4                       # 170 mm column width, inches
WMIN, WMAX = 2400, 3300
FDIR = Path(matplotlib.get_data_path()) / "fonts" / "ttf"
BOLD = str(FDIR / "DejaVuSans-Bold.ttf")
LABEL_PX = 84                               # sub-panel label height at final scale (bold sans)

# step -> rows of (label, region); regions in one row are placed side by side. One region = no label.
SPEC = {
    "step1": [[("", "d1_data")]],
    "step2": [[("A", "d2_model")], [("B", "d3_notes")]],
    "step3": [[("A", "d3_stats")], [("B", "d3_hsroc")]],
    "step4": [[("", "d4_roc")]],
    "step5": [[("A", "d5_setting")], [("B", "d5_table")], [("C", "d6_export")]],
    "step6": [[("A", "d6_fagan")], [("B", "d6_deeks")]],
}


def trim(im, tol=10, pad=2 * DPR):
    """Remove uniform margins (colour of the corners), keep a small pad."""
    px = im.load(); w, h = im.size
    bg = px[1, 1]
    same = lambda c: all(abs(a - b) <= tol for a, b in zip(c, bg))
    def rowblank(y): return all(same(px[x, y]) for x in range(0, w, 3))
    def colblank(x): return all(same(px[x, y]) for y in range(0, h, 3))
    t = 0
    while t < h - 1 and rowblank(t): t += 1
    bt = h - 1
    while bt > t and rowblank(bt): bt -= 1
    l = 0
    while l < w - 1 and colblank(l): l += 1
    r = w - 1
    while r > l and colblank(r): r -= 1
    return im.crop((max(0, l - pad), max(0, t - pad), min(w, r + 1 + pad), min(h, bt + 1 + pad)))


def body_and_min(fonts):
    """char-weighted median font size and smallest size among texts of >= 4 characters (CSS px)."""
    if not fonts: return None, None
    fs = sorted(fonts); tot = sum(n for _, n in fs); acc = 0; med = fs[-1][0]
    for f, n in fs:
        acc += n
        if acc >= tot / 2: med = f; break
    mins = [f for f, n in fs if n >= 4]
    return med, (min(mins) if mins else min(f for f, _ in fs))


def pt(css_px, scale, width):
    """printed size in points of text of css_px when the image (width px, scale final px per device px) is 170 mm wide"""
    return css_px * DPR * scale / (width / PRINT_IN) * 72


report = []
for step, rows in SPEC.items():
    grid = [[(lab, trim(Image.open(D / "regions" / f"{name}.png").convert("RGB")), name) for lab, name in row] for row in rows]
    ims = [x for row in grid for x in row]
    multi = len(ims) > 1
    gap = 8 * DPR
    # the scale to the final width depends on the gutter, which depends on the label size: two passes
    gut = 0
    for _ in range(2):
        row_w = [sum(gut + im.width + gap for _, im, _ in row) + gap for row in grid]
        width_native = max(row_w)
        scale = WMAX / width_native if width_native > WMAX else (WMIN / width_native if width_native < WMIN else 1.0)
        label_native = round(LABEL_PX / scale)
        gut = round(label_native * 1.75) if multi else 0
    H = gap + sum(max(im.height for _, im, _ in row) + gap for row in grid)
    canvas = Image.new("RGB", (width_native, H), "white"); d = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(BOLD, label_native) if multi else None
    y = gap
    for row in grid:
        x0 = gap
        for lab, im, _ in row:
            x = x0 + gut
            if multi:
                d.text((x0, y + 2), lab, fill=(20, 24, 30), font=font)
            canvas.paste(im, (x, y))
            d.rectangle((x - 2, y - 2, x + im.width + 1, y + im.height + 1), outline=(190, 190, 190), width=max(2, round(2 / scale)))
            x0 = x + im.width + gap
        y += max(im.height for _, im, _ in row) + gap
    zoom = {name: 1.0 for _, _, name in ims}
    final = canvas.resize((round(width_native * scale), round(H * scale)), Image.LANCZOS) if scale != 1 else canvas
    W, Hf = final.size
    dpi = W / PRINT_IN
    final.save(OUT / f"{step}.png", optimize=True)
    final.save(OUT / f"{step}.tif", compression=None, dpi=(dpi, dpi))
    per = []
    for lab, _, name in ims:
        b_, m_ = body_and_min(META["regions"][name]["fonts"])
        z = zoom[name]; per.append((lab, round(pt(b_ * z, scale, W), 1), round(pt(m_ * z, scale, W), 1)))
    report.append({"step": step, "width_px": W, "height_px": Hf, "aspect_h_over_w": round(Hf / W, 2), "tiff_dpi_at_170mm": round(dpi),
                   "body_text_pt_min_over_panels": min(x[1] for x in per), "smallest_text_pt": min(x[2] for x in per),
                   "per_panel_body_smallest_pt": per, "label_pt": round(LABEL_PX / dpi * 72, 1) if multi else None})
    print(report[-1])
(OUT / "legibility.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
