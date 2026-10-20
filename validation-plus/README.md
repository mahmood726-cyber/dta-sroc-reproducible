# Extras validation for archive v1.1.0

This adds PR #133's bivariate meta-regression, conditional summary sensitivity
and specificity, 95% confidence/prediction regions in ROC space, and positive/
negative post-test probabilities at chosen prevalences. No fitted SROC curve is
claimed for the extras meta-regression. The numerical reference is R 4.6.0,
mada 0.5.12 and mvmeta 1.0.3, with metadat 1.6-0 and ellipse for the generator's
region-contour cross-check. Desktop package requirements also include jsonlite.

The recorded 2026-10-20 allmeta v1.8.0 (1cb3f84) release run in `provenance/run_plan-2026-10-20-release.log` (lines 112-119) confirms
**195,291/195,291** checks over 27 configurations (21 fits, six zero-cell
refusals), three covariate configurations and 114 candidate dataset schemas.
This matches APP.txt and the unchanged upstream check-plus.json.

The raw-scale gate passed over **3,528 configurations** (log lines 121-138):
222 out-of-tolerance configurations versus mada on supplied inputs and eight
versus the standardised/back-transformed reference, all with the scale note
shown; maximum relative difference 1.89e-4. This is not universal numerical
agreement. Negative controls passed 23/23 (lines 140-170). The original
pinned replay passed 855/855 (lines 81-110); full reproduction passed 855/855
(105 configurations; 80 fits, 25 matched refusals; Moses 18/18) and 53/53
paper numbers (lines 15-77); oracle tests passed 8/8 (lines 172-184).
See [detailed scope and limitations](dta-sroc/validate/README-plus.md),
including the retrospective iterative p-value tolerance decision and raw-scale limits.

From the archive root, with Node on PATH:

    python validation-plus/run.py extras
    python validation-plus/run.py raw
    python validation-plus/run.py original
    python validation-plus/run.py tests

The wrapper stages archived app files and the unchanged validation scripts in
outputs/validation-plus/allmeta/dta-sroc/. This preserves script-relative paths
and the R scripts' allmeta/dta-sroc/validate/ paths. It does not read the sibling
release checkout. Each invocation refreshes the scratch copies. Logs remain
in outputs/validation-plus/. The original command is an additional 855/855
pinned browser-adapter replay; python reproduce.py remains the original full
R-generated paper validation.

For an optional independent regeneration of the extras R references, use the
environment in RUN_PLAN.cmd, then:

    python validation-plus/run.py regenerate

This runs generate-plus.R, generate-plus-raw.R, pin-plus.mjs,
check-plus-raw.mjs --pin, then both checks, entirely in scratch. It leaves
the archived reference values and manifests unchanged. Inspect regenerated
outputs before any deliberate reference update; the normal runner plan never
regenerates or repins the extras reference corpus.

dta-sroc/validate/ preserves the complete upstream directory, with documented privacy redactions to logs,
including support files without "plus" in their names, R generators, manifest
pins, original replay inputs, strict-p-differences.json, logs and pixel
references. Existing upstream logs/summaries are historical PR evidence, not
results of this recut. No absent claims-plus.json or other invented evidence
was added. The upstream Playwright config imports shared test infrastructure
outside this copied directory; browser/pixel reproduction still requires that
upstream test environment and is not part of RUN_PLAN.cmd.

Run python recut_integrity.py --verify for source hashes, unchanged original
validation, corpus pins, browser pins and the shipped mada webR dependencies.
