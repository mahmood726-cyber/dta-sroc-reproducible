# v1.1.0 recut notes

Finalized 2026-10-20 for allmeta v1.8.0, commit
1cb3f8409c7af75ed41f7e1811f9c502f900fc79, DOI 10.5281/zenodo.23515177
(concept DOI 10.5281/zenodo.20516880). The archive version is 1.1.0.
The completed release RUN_PLAN run used allmeta 1cb3f84 on 2026-10-20.

## Finalize

- Replaced every release SHA/DOI placeholder, including manifest generator
  metadata. CITATION.cff and .zenodo.json identify version 1.1.0 and
  2026-10-20; all creators/authors are unchanged. Related identifiers retain
  archive v1.0.0 DOI 10.5281/zenodo.23164857 and the allmeta concept DOI,
  and include the supplied v1.8.0 DOI.
- Updated README, CHANGELOG, RUN_PLAN_EXPECTED, validation-plus/README and
  FIX_NOTES to describe the completed release rerun. Removed obsolete current
  preparation-source and pending-rerun claims. Replaced stale log line ranges
  with the release-log ranges in the table below.
- README numerical differences versus the release log: **none**. All recorded
  counts, subgroup counts, worked-example rounding and tolerances are retained.
  Corrected the unsupported assertion that CRLF checkout copies already match
  Git blobs. No Git, Node or R process was run in this finalization sandbox.
- Copied the release log into provenance/run_plan-2026-10-20-release.log.
  Replaced complete local directory prefixes with the LOCAL marker and retained
  the filename. Also redacted host paths in five historical upstream logs,
  including non-home drive paths, and contact addresses in those logs and four
  bundled dependency files. The audit below identifies each affected file/line.
- Contact-address redaction uses fixed-width text, including in R.wasm, preserving
  byte offsets, binary section sizes and VFS offsets. Copyright holders, licence
  terms, public repository links and publication creators are unchanged.
- Added COPY_MAP.json for all 245 copied files (173 app/dependency files and
  72 validation/support/evidence files). Reused fix_app_sources.py; removed its
  preparation-commit fallback. Added FINAL_BLOBS.cmd in both workspace and
  archive; RUN_FIX.cmd forwards to the final runner.
- The helper requires the exact v1.8.0 tag/commit, reads Git stdout as bytes,
  checks the complete map and existing content before writing, verifies every
  restored blob, reports BLOB PASS 245/245, then retains only privacy-redacted
  published bytes. It records upstream_blob_sha256 separately from published
  sha256, writes provenance/BLOB_VERIFICATION.json and runs the archive's
  manifest generator, verifier and privacy check. Corpus bytes must match
  exactly; other differences may only be CRLF conversion or audited redaction.
- Privacy and exact published-byte identity conflict for nine upstream files.
  These are explicitly marked privacy_derivatives in APP_SOURCES.json.
  BLOB PASS describes the restoration/verification stage; it must not be
  represented as final byte identity for those nine files. The other 236 files
  will be exact Git blobs after the human-side runner succeeds.
- Added publication_privacy.py to enumerate every publishable file according
  to this archive's .gitignore and audit raw file bytes, including binaries.
  recut_integrity.py now uses that same inventory and real release metadata.
  APP_SOURCES hashes and SOURCE_SHA256 were regenerated for the finalized tree.
- RUN_PLAN.cmd already uses caller-supplied R_HOME, R_LIBS_USER and R_LIBS,
  documented in RUN_PLAN_EXPECTED.md. It contains no machine-specific paths
  and needed no changes. Canonical environment pins remain unchanged.
- The 39 original protected files, all seven corpus pins and 14 browser
  R package pins remain unchanged. No expected value, tolerance, corpus,
  numerical count, R reference script or scientific checker was rewritten.

## Completed release run: 2026-10-20, allmeta 1cb3f84

Evidence: [redacted release log](provenance/run_plan-2026-10-20-release.log).
The runner recorded exit 0, and the log ends RECUT_RUN_PASS.

| Check | Observed result | Log lines |
|---|---|---|
| Full original reproduction | 855/855 checks; 105 configurations; 80 fits; 25 matched refusals; Moses 18/18 (13 fits, 5 refusals) | 15-77 |
| Paper quantities | 53/53 reproduced | 15-69 |
| Original pinned replay | 855/855; no failed checks or coverage failures | 81-110 |
| Extras | 195,291/195,291; 27 configurations; 114 dataset-schema candidates | 112-119 |
| Raw-scale gate | PASS; 3,528 configurations; 222 raw and eight standardized out-of-tolerance configurations, all noted; largest relative difference 1.89e-4 | 121-138 |
| Negative controls | 23/23; zero failures and zero skipped | 140-170 |
| Existing Python oracle tests | 8/8 | 172-184 |
| Integrity during release run | 299/299 source files, 39 protected files, 245 copies, seven corpus pins, 14 browser R packages | 9, 186, 190 |

The raw gate does not claim universal numerical agreement. Its unchanged subgroup
counts are in RUN_PLAN_EXPECTED.md. The integrity count above is historical;
finalization adds documentation and tooling, so the current source count differs.

The recorded environment was R 4.6.0 (mada 0.5.12, mvmeta 1.0.3,
ellipse 0.5.0), Node 24.13.0 and Python 3.13.13 (log lines 70-71).
Node was pinned to 24.15.0; fonttools 4.67.0 vs pinned 4.66.1,
packaging 26.0 vs pinned 26.3, pillow 12.2.0 vs pinned 12.3.0.
The runner used --allow-version-mismatch. Docker/CI pins are unchanged.

## Verification and remaining runner step

Finalization ran Python integrity checks, the existing eight oracle tests,
publication privacy checks, Python syntax checks and six isolated tests of the
blob helper with simulated Git responses (6/6 PASS). The simulated tests are not Git-blob
verification. Final integrity: 303/303 source entries; 39 protected files,
245 release-derived copies, seven corpus pins and 14 browser R packages PASS.
All 245 copies match the supplied checkout after the documented privacy
transformation and newline normalization; 127 differ only in newline encoding.
The archived release log matches its source except for directory redactions. Run FINAL_BLOBS.cmd from the workspace (or archive) for actual
Git-blob restoration and verification; its result has not been claimed here.
Browser/webR execution, pixel comparisons and cross-platform checks were not
performed by the recorded command-line run or this finalization pass.
In particular, the privacy-redacted webR binary has not been browser-tested.

No release was tagged, uploaded or published. The archive v1.1.0 DOI is not
assigned; no identifier was invented. The v1.0.0 manuscript docs/paper.md
still contains two historical '[DOI to be added on release]' annotations;
they cannot be filled with an unassigned v1.1.0 archive DOI.
No unresolved release angle-bracket placeholder remains. LOCAL/redacted markers,
HTML/XML elements, command argument examples and output-name templates are
intentional syntax, not missing release values. Specifically: docs/make_numbers.py
uses a source-description argument example; docs/screenshots/compose.py uses
output/work-directory argument examples; analysis/compare_runs.py uses a missing
value diagnostic; README uses a platform artifact-name template.

## Earlier preparation and release re-sync

Preparation initially used d04b0a9. The 2026-10-20 release re-sync copied
245 files from the supplied v1.8.0 checkout; ten changed and 235 were already
identical to that working tree. That comparison was not against Git blobs.
The build-info stamp reports v1.8.0, embedded SHA
42a94da2110a02200d0b5bff4c56f636b9cbffa9, built 2026-10-20T20:32:27Z.
It is upstream build metadata, not the release commit identity.

The re-sync changed export-bar layout, validation display, build metadata and
six mobile pixel-reference images plus their reference manifest. No validated
calculation changed. RUN_PLAN preserves previous outputs in numbered sibling
directories under ignored results/ and outputs/. The upstream browser manifest
retains historical generated-source hashes; its corpus hashes are verified.
The preserved original oracle includes the 59203eb shape/finiteness checks.

### Copies refreshed (SHA-256 before -> after)

| Archive path | SHA-256 before -> after | Why |
|---|---|---|
| `app/hub/shared/results-export.js` | `8fd30b46fc6e0d09b98326f69edf14757659dbcf2cf1434ca8c5de60c057cc71` -> `16ffa76bc74275565214c2e142d7f0d0847a5a8eded2614efb04aa172acd71f4` | Release export-bar CSS adds wrapping and maximum width; no calculation changes. |
| `app/shared/alm-validate.js` | `3de6a685c77fa26d68ae39b1da9619c5ada49fd22ef5170237268e1401a09fb7` -> `b451c1377164842466aa0d7ad4cb6dd7a1340456a61e891a01646b4375c4ed87` | Release validation display avoids duplicating the R version prefix; comparison logic unchanged. |
| `app/shared/build-info.js` | `f75a435e283d007883ce8fb2f66da7a1cf6132cd5a391a57419b137a69c9c238` -> `44c8a7d1e2cdad4d4b1c4806cffdd4f9817dc39161cd0de5374761a71bd19177` | Release build identity stamp now reports v1.8.0. |
| `validation-plus/dta-sroc/validate/pixel-references/dta-sroc-8-cards.png` | `1781712ae8b2802d8f32bea2b4f9c0ca09df944a6039e2c78251c3ea41160819` -> `3e66065a7231ff3a41f4334651bd1a36800d829a9ddef8ec6817dc79c066c673` | Release mobile pixel reference for configuration 8; upstream documents positioning/rasterization changes. |
| `validation-plus/dta-sroc/validate/pixel-references/dta-sroc-8-plot.png` | `3c42a34c2ed3c31077e28a319dd0e0395590dafc4e6b47a987e7dbebe614662a` -> `05934bdb8e46a5fdf4ab78ae334846acedaa1439f57b1fe639226016f9cb955c` | Release mobile pixel reference for configuration 8; upstream documents positioning/rasterization changes. |
| `validation-plus/dta-sroc/validate/pixel-references/dta-sroc-8-table.png` | `742d8b21331899f77ed6c1dcb554d00287359d403ee4203fb818c6b3163720d2` -> `a77e4f56e4df251ebdd925a5707b52f7f07d7357d5c616b468ffa33769bb759c` | Release mobile pixel reference for configuration 8; upstream documents positioning/rasterization changes. |
| `validation-plus/dta-sroc/validate/pixel-references/dta-sroc-9-cards.png` | `62871e2492a1aa3fb70b4e2690e240a081529724a125ca5bf70f5aac4b324f2c` -> `cadd5b8ca3e48feb0f324fcaa890628f5b957ac6549256e8d2f6224cd75e052c` | Release mobile pixel reference for configuration 9; upstream documents positioning/rasterization changes. |
| `validation-plus/dta-sroc/validate/pixel-references/dta-sroc-9-plot.png` | `4de49e00d07fcbd9362ef76852e50b6fcb89e75a790bbfd4aa8707a3d42747b7` -> `40db75bd20f5ade299f76ef713bc41156bc63e4f9508de8021222b2d5f4372b6` | Release mobile pixel reference for configuration 9; upstream documents positioning/rasterization changes. |
| `validation-plus/dta-sroc/validate/pixel-references/dta-sroc-9-table.png` | `f5e86509c35b7095c9c56be7a856db62943643800294d5cff917cee8629e58bc` -> `ac7e68ab8f8bca1450a14bc65e581c36462bda4cf8aacffffd256d2b604f2cd8` | Release mobile pixel reference for configuration 9; upstream documents positioning/rasterization changes. |
| `validation-plus/dta-sroc/validate/pixel-references/REFERENCE.json` | `7799ce225e7f81cce0b05acd2ab633b6fcd87dca94343b4e84ceed249ba160be` -> `fb2bc77287dc3c304e4eac71e2f09bf62101dd267bfc7931f648be557fd47096` | Release pixel-reference hashes and review explanation for six mobile images. |



## Privacy audit

All publishable files were scanned, including binary files; ignored runtime
outputs and Git internals are excluded. Line numbers below refer to the
pre-redaction input at finalization; binary lines mean newline-byte counts.
Repeated matches on one line are counted in parentheses. Sensitive text is
not repeated here. Each match is listed by file, line, kind and action.
Public authors/repository identifiers, ordinary code/prose identifiers,
webR virtual-home paths, public CA certificates and coincidental binary
byte sequences are reviewed non-sensitive matches. They are retained to
preserve attribution, runtime functionality and package integrity.

| File | Lines (occurrences) | Match kind | Action |
|---|---|---|---|
| `.github/workflows/reproduce.yml` | 121, 123, 153, 155, 156 (2) | identity fragment | Retain: public attribution/repository or ordinary runtime/prose identifier. |
| `.zenodo.json` | 9, 25, 30 | identity fragment | Retain: public attribution/repository or ordinary runtime/prose identifier. |
| `CHANGELOG.md` | 38 | identity fragment | Retain: public attribution/repository or ordinary runtime/prose identifier. |
| `CITATION.cff` | 7, 8, 28, 34 | identity fragment | Retain: public attribution/repository or ordinary runtime/prose identifier. |
| `FIX_NOTES.md` | 15 | identity fragment | Retain: public attribution/repository or ordinary runtime/prose identifier. |
| `LICENSE` | 3 | identity fragment | Retain: public attribution/repository or ordinary runtime/prose identifier. |
| `README.md` | 3 (2), 4, 7, 9, 10, 47, 66, 82 | identity fragment | Retain: public attribution/repository or ordinary runtime/prose identifier. |
| `RECUT_NOTES.md` | 93 | identity fragment | Retain: public attribution/repository or ordinary runtime/prose identifier. |
| `RUN_PLAN.cmd` | 5, 7, 10, 11, 15 | identity fragment | Retain: public attribution/repository or ordinary runtime/prose identifier. |
| `RUN_PLAN_EXPECTED.md` | 16, 25 (3), 27 | identity fragment | Retain: public attribution/repository or ordinary runtime/prose identifier. |
| `analysis/make_outputs.py` | 322 | identity fragment | Retain: public attribution/repository or ordinary runtime/prose identifier. |
| `app/dta-sroc/plus-ui.js` | 40 | identity fragment | Retain: public attribution/repository or ordinary runtime/prose identifier. |
| `app/dta-sroc/validate/MANIFEST.json` | 1 | identity fragment | Retain: public attribution/repository or ordinary runtime/prose identifier. |
| `app/dta-sroc/validate/README-plus.md` | 11, 36, 42 | identity fragment | Retain: public attribution/repository or ordinary runtime/prose identifier. |
| `app/dta-sroc/validate/adapter.js` | 146, 209 | identity fragment | Retain: public attribution/repository or ordinary runtime/prose identifier. |
| `app/hub/shared/vendor/jspdf.min.js` | 7, 9, 10, 54, 89, 112, 129, 138, 163, 203, 275, 335, 361 | email | Redacted: machine directory prefix or contact address; numerical evidence unchanged. |
| `app/hub/shared/vendor/jspdf.min.js` | 51, 86 (16), 134 | identity fragment | Retain: public attribution/repository or ordinary runtime/prose identifier. |
| `app/r-shiny/shinylive/webr/R.js` | 1823 (2) | home path | Retain: webR virtual filesystem, not a host path. |
| `app/r-shiny/shinylive/webr/R.js` | 1823 (233) | identity fragment | Retain: public attribution/repository or ordinary runtime/prose identifier. |
| `app/r-shiny/shinylive/webr/R.wasm` | 29885, 30769, 30770, 36544, 36545, 36546, 37320, 37321, 38082, 38083, 41054, 41055, 42977, 42978, 42979, 46793, 46794, 52327, 52328, 52329, 52330, 52696, 52697, 60136, 60137, 60140, 63801, 63802, 64419, 64420, 73975, 73976, 79838, 79839, 79857 | email | Redacted: machine directory prefix or contact address; numerical evidence unchanged. |
| `app/r-shiny/shinylive/webr/R.wasm` | 216, 219 (2), 229, 574 (3), 575, 29456, 29466 (10), 29467 (3), 29471, 29474 (2), 30654, 30655, 30689 (2), 30829 (2), 30841, 31463, 31470, 31521, 31522, 31601, 31618, 31619, 40425, 43232, 60171, 64433 (2), 64471, 64474 (2), 64572, 64614, 73370 (2), 73371 (12), 73904, 74005, 74153, 79703, 81345 (2) | identity fragment | Retain: public attribution/repository or ordinary runtime/prose identifier. |
| `app/r-shiny/shinylive/webr/R.wasm` | 33372, 33436, 34081, 35149, 35850, 37287, 38341, 38757, 41524, 45132, 45583, 46063, 47931, 49857, 51179, 52113, 55026, 55803, 56008, 56633, 57359, 57510, 59196, 65346, 65731, 65944, 66766, 67425, 68626, 69368, 69545, 81018, 81101, 81257, 81411, 81413, 81414, 81415 (3), 81416 (2) | local path | Redacted: machine directory prefix or contact address; numerical evidence unchanged. |
| `app/r-shiny/shinylive/webr/library.data.gz` | 44924 | credential prefix | Retain: random compressed bytes, not a credential. |
| `app/r-shiny/shinylive/webr/library.data.gz` | 24, 563, 1672, 2311, 2528, 2611, 3533, 4442, 4860, 5159, 5851, 8485, 8950, 9794, 10111, 10377, 11342, 13876, 15127, 16588, 16964, 18219, 18466, 18533, 19027, 19855, 20102, 20112, 20571, 23538, 23693, 27031, 27381, 27483, 27803, 27986, 28888, 29388, 30669, 31295, 31747, 32111, 32430, 32966, 34466, 34898, 35585, 36329, 38037, 38650, 39138, 39497, 39601, 39666, 40120, 42285, 42889, 44158, 48751, 48799, 48803, 50373, 52267, 52919, 53552, 53623, 54172 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/library.js.metadata` | 1 (9) | identity fragment | Retain: public attribution/repository or ordinary runtime/prose identifier. |
| `app/r-shiny/shinylive/webr/packages/Matrix/Matrix_1.7-5.tgz` | 2542, 3326, 3863, 5413, 5601, 6666, 6813, 7166, 7875, 8524, 8942, 9384, 9622, 10099, 10266, 10927 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/packages/lattice/lattice_0.22-9.tgz` | 1107, 1256, 2227, 2342, 2540, 3146 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/packages/mathjaxr/mathjaxr_2.0-0.tgz` | 1042, 2089, 2998, 3225, 4202, 4659, 5148, 5505, 6956, 8363, 8876, 8941, 9057, 9676, 10253, 10871 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/packages/metadat/metadat_1.4-0.tgz` | 421, 1567, 2431 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/packages/metafor/metafor_4.8-0.tgz` | 1286, 1571, 2131, 2625, 3085, 5134, 6123, 6445, 6597, 6805, 7922, 8846, 9983, 10692, 12246 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/packages/mvtnorm/mvtnorm_1.2-4.tgz` | 1517 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/packages/nlme/nlme_3.1-169.tgz` | 524, 3041, 4041, 4621, 6160, 6495 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/packages/numDeriv/numDeriv_2016.8-1.1.tgz` | 179 | email | Retain: coincidental byte sequence in compressed package/font, not an address. |
| `app/r-shiny/shinylive/webr/repo/bin/emscripten/contrib/4.5/digest_0.6.39.tgz` | 123 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/repo/bin/emscripten/contrib/4.5/ellipse_0.5.0.tgz` | 783 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/repo/bin/emscripten/contrib/4.5/mixmeta_1.2.2.tgz` | 323 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/repo/bin/emscripten/contrib/4.5/mvmeta_1.0.3.tgz` | 65, 578, 651, 765 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/vfs/etc/fonts/fonts.conf` | 5 | home path | Retain: webR virtual filesystem, not a host path. |
| `app/r-shiny/shinylive/webr/vfs/etc/fonts/fonts.conf` | 5 | identity fragment | Retain: public attribution/repository or ordinary runtime/prose identifier. |
| `app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem` | 25, 51, 82, 117, 139, 161, 183, 214, 236, 258, 282, 299, 321, 352, 372, 396, 420, 441, 473, 495, 518, 541, 561, 581, 610, 625, 647, 668, 689, 720, 750, 780, 802, 826, 851, 881, 922, 951, 980, 1002, 1023, 1053, 1083, 1113, 1135, 1151, 1173, 1189, 1220, 1252, 1284, 1301, 1316, 1346, 1376, 1401, 1420, 1450, 1472, 1493, 1525, 1558, 1576, 1606, 1636, 1656, 1685, 1698, 1712, 1737, 1767, 1799, 1816, 1848, 1865, 1895, 1911, 1940, 1970, 2004, 2026, 2042, 2063, 2078, 2110, 2126, 2157, 2173, 2202, 2234, 2250, 2267, 2298, 2314, 2344, 2359, 2389, 2421, 2437, 2468, 2499, 2530, 2546, 2579, 2594, 2624, 2639, 2669, 2683, 2713, 2743, 2758, 2773, 2803, 2821, 2839, 2854, 2884, 2913, 2927, 2943, 2973, 2988, 3004, 3034, 3064, 3080, 3095, 3125, 3156, 3172, 3187, 3202, 3232, 3262, 3278, 3309, 3326, 3356, 3377, 3407, 3422, 3453, 3468, 3498, 3529 | credential prefix | Retain: public CA certificate, not a private key. |
| `app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem` | 11, 1250, 1282 | identity fragment | Retain: public attribution/repository or ordinary runtime/prose identifier. |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/doc.data.gz` | 140, 815, 900, 1495, 2554, 2911, 4750, 5256, 5314, 5947, 6067, 6421, 6599, 8435, 9002, 9728, 10536, 13087, 13688, 13821, 14119, 14195 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/base/help.data.gz` | 1268, 1286, 1895, 2506, 4008, 4379, 4901, 5987, 6253, 6964, 7365, 8866 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/afm.data.gz` | 70, 727, 2267, 2399, 2481 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/fonts.data.gz` | 287, 516, 711 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/help.data.gz` | 1180 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/libs.data.gz` | 661, 863, 1402, 1522, 4459, 4640, 4821, 4875, 5161, 5229, 5302, 5800 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/graphics/help.data.gz` | 67, 324, 1240 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grid/doc.data.gz` | 409, 656, 751, 1740, 2192 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/methods/help.data.gz` | 1290, 1642 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/parallel.data.gz` | 622 | credential prefix | Retain: random compressed bytes, not a credential. |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/parallel.data.gz` | 581, 1218 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/splines/help.data.gz` | 22 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats/help.data.gz` | 113, 1151, 1458, 2149, 2974, 3392, 3886 (2), 5183, 5716 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats4/help.data.gz` | 91 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/tools/help.data.gz` | 65, 278 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/translations.data.gz` | 2384, 3356, 4243, 4499, 6937, 9268, 9657, 9671 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/translations/DESCRIPTION` | 5 | email | Redacted: machine directory prefix or contact address; numerical evidence unchanged. |
| `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/utils/help.data.gz` | 285, 1052 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSans-Bold.ttf` | 459 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSans-BoldItalic.ttf` | 1674 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSans-Italic.ttf` | 424, 427, 1134 | email | Retain: coincidental byte sequence in compressed package/font, not an address. |
| `app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSans-Italic.ttf` | 877, 1714 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSans-Regular.ttf` | 360, 363, 904 | email | Retain: coincidental byte sequence in compressed package/font, not an address. |
| `app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSans-Regular.ttf` | 477, 988 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSansMono-Bold.ttf` | 515, 552, 673, 693, 872, 874, 1019, 1250, 1268, 1494, 1607 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSansMono-Regular.ttf` | 1584 | email | Retain: coincidental byte sequence in compressed package/font, not an address. |
| `app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSansMono-Regular.ttf` | 562, 1528 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSerif-Bold.ttf` | 442, 497 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSerif-Italic.ttf` | 2587, 2709, 2878, 2879 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSerif-Regular.ttf` | 2896 | email | Retain: coincidental byte sequence in compressed package/font, not an address. |
| `app/r-shiny/shinylive/webr/vfs/usr/share/gdal.data.gz` | 1, 96, 537, 1036 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/vfs/usr/share/proj.data.gz` | 3945, 4055, 5355, 6802 | local path | Retain: random binary byte sequence, not a host path. |
| `app/r-shiny/shinylive/webr/webr-worker.js` | 35, 36 | email | Redacted: machine directory prefix or contact address; numerical evidence unchanged. |
| `app/r-shiny/shinylive/webr/webr-worker.js` | 2 (2), 3 (2) | identity fragment | Retain: public attribution/repository or ordinary runtime/prose identifier. |
| `app/r-shiny/shinylive/webr/webr.mjs` | 2 | home path | Retain: webR virtual filesystem, not a host path. |
| `app/r-shiny/shinylive/webr/webr.mjs` | 2 | identity fragment | Retain: public attribution/repository or ordinary runtime/prose identifier. |
| `app/shared/alm-validate.js` | 3, 4 | identity fragment | Retain: public attribution/repository or ordinary runtime/prose identifier. |
| `app/shared/autosave.js` | 4, 58 | identity fragment | Retain: public attribution/repository or ordinary runtime/prose identifier. |
| `app/shared/build-info.js` | 28 | identity fragment | Retain: public attribution/repository or ordinary runtime/prose identifier. |
| `app/shared/ma-studies-v1.js` | 350, 351, 398, 608 | identity fragment | Retain: public attribution/repository or ordinary runtime/prose identifier. |
| `app/shared/truthcert-export.js` | 4, 6 | identity fragment | Retain: public attribution/repository or ordinary runtime/prose identifier. |
| `bench/install_r_packages.R` | 12 | identity fragment | Retain: public attribution/repository or ordinary runtime/prose identifier. |
| `docs/paper.md` | 3, 29, 38, 85, 88 | identity fragment | Retain: public attribution/repository or ordinary runtime/prose identifier. |
| `docs/screenshots/step1.png` | 748, 1084 | local path | Retain: random binary byte sequence, not a host path. |
| `docs/screenshots/step2.png` | 933 | local path | Retain: random binary byte sequence, not a host path. |
| `docs/screenshots/step4.png` | 246, 302, 323 | local path | Retain: random binary byte sequence, not a host path. |
| `docs/screenshots/step6.png` | 850 | local path | Retain: random binary byte sequence, not a host path. |
| `provenance/run_plan-2026-10-20-release.log` | 3, 73 (2), 74 (2) | identity fragment | Retain: public attribution/repository or ordinary runtime/prose identifier. |
| `provenance/run_plan-2026-10-20-release.log` | 73, 74 | local path | Redacted: machine directory prefix or contact address; numerical evidence unchanged. |
| `publication_privacy.py` | 17 | extended path | Retain: scanner pattern, not a host path. |
| `publication_privacy.py` | 79, 84 | identity fragment | Retain: public attribution/repository or ordinary runtime/prose identifier. |
| `validation-plus/dta-sroc/validate/MANIFEST.json` | 1 | identity fragment | Retain: public attribution/repository or ordinary runtime/prose identifier. |
| `validation-plus/dta-sroc/validate/README-plus.md` | 11, 36, 42 | identity fragment | Retain: public attribution/repository or ordinary runtime/prose identifier. |
| `validation-plus/dta-sroc/validate/adapter.js` | 146, 209 | identity fragment | Retain: public attribution/repository or ordinary runtime/prose identifier. |
| `validation-plus/dta-sroc/validate/generate-plus-raw.R` | 2, 4 | identity fragment | Retain: public attribution/repository or ordinary runtime/prose identifier. |
| `validation-plus/dta-sroc/validate/generate-plus-raw.log` | 1 (2), 2 (2), 3 (2) | identity fragment | Redacted with the machine directory prefix. |
| `validation-plus/dta-sroc/validate/generate-plus-raw.log` | 1, 2, 3 | local path | Redacted: machine directory prefix or contact address; numerical evidence unchanged. |
| `validation-plus/dta-sroc/validate/generate-plus.log` | 6 (2) | identity fragment | Redacted with the machine directory prefix. |
| `validation-plus/dta-sroc/validate/generate-plus.log` | 6, 7, 8 | local path | Redacted: machine directory prefix or contact address; numerical evidence unchanged. |
| `validation-plus/dta-sroc/validate/inspect-plus.log` | 62, 239 | email | Redacted: machine directory prefix or contact address; numerical evidence unchanged. |
| `validation-plus/dta-sroc/validate/inspect-plus.log` | 6 (2) | identity fragment | Redacted with the machine directory prefix. |
| `validation-plus/dta-sroc/validate/inspect-plus.log` | 6, 7, 8 | local path | Redacted: machine directory prefix or contact address; numerical evidence unchanged. |
| `validation-plus/dta-sroc/validate/inventory-plus.log` | 6 (2) | identity fragment | Redacted with the machine directory prefix. |
| `validation-plus/dta-sroc/validate/inventory-plus.log` | 6, 7, 8 | local path | Redacted: machine directory prefix or contact address; numerical evidence unchanged. |
| `validation-plus/dta-sroc/validate/live-plus.log` | 6 (2), 14 (2), 21 (2), 28 (2), 35 (2), 42 (2), 49 (2), 56 (2), 63 (2), 70 (2), 77 (2), 84 (2), 91 (2), 98 (2), 105 (2), 112 (2), 119 (2), 126 (2), 133 (2), 140 (2), 147 (2), 154 (2) | identity fragment | Redacted with the machine directory prefix. |
| `validation-plus/dta-sroc/validate/live-plus.log` | 6, 7, 8, 14, 15, 16, 21, 22, 23, 28, 29, 30, 35, 36, 37, 42, 43, 44, 49, 50, 51, 56, 57, 58, 63, 64, 65, 70, 71, 72, 77, 78, 79, 84, 85, 86, 91, 92, 93, 98, 99, 100, 105, 106, 107, 112, 113, 114, 119, 120, 121, 126, 127, 128, 133, 134, 135, 140, 141, 142, 147, 148, 149, 154, 155, 156 | local path | Redacted: machine directory prefix or contact address; numerical evidence unchanged. |
| `validation-plus/dta-sroc/validate/pixel-references/dta-sroc-2-cards.png` | 64 | local path | Retain: random binary byte sequence, not a host path. |
| `validation-plus/dta-sroc/validate/pixel-references/dta-sroc-6-cards.png` | 29 | local path | Retain: random binary byte sequence, not a host path. |

## Finalization file changes

- `.zenodo.json`
- `APP_SOURCES.json`
- `CHANGELOG.md`
- `CITATION.cff`
- `COPY_MAP.json`
- `FINAL_BLOBS.cmd`
- `FIX_NOTES.md`
- `README.md`
- `RECUT_NOTES.md`
- `RUN_FIX.cmd`
- `RUN_PLAN_EXPECTED.md`
- `SOURCE_SHA256.json`
- `app/hub/shared/vendor/jspdf.min.js`
- `app/r-shiny/shinylive/webr/R.wasm`
- `app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/translations/DESCRIPTION`
- `app/r-shiny/shinylive/webr/webr-worker.js`
- `fix_app_sources.py`
- `provenance/run_plan-2026-10-20-release.log`
- `publication_privacy.py`
- `recut_integrity.py`
- `validation-plus/README.md`
- `validation-plus/dta-sroc/validate/generate-plus-raw.log`
- `validation-plus/dta-sroc/validate/generate-plus.log`
- `validation-plus/dta-sroc/validate/inspect-plus.log`
- `validation-plus/dta-sroc/validate/inventory-plus.log`
- `validation-plus/dta-sroc/validate/live-plus.log`

The workspace FINAL_BLOBS.cmd is also added as the requested entry point.
Workspace test_finalize_helpers.py contains the six simulated helper tests.
The first test-fixture attempt hit the local Python 3.13 temporary-directory
ACL issue; replacement fixtures passed. Three empty finalize-test-* directories
remain outside the archive because this sandbox cannot remove their restrictive
ACLs. They contain no publication files.
