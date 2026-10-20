# Historical review fixes and final release status

The F1-F9 preparation review preceded the allmeta v1.8.0 release re-sync.
Its numerical counts and scientific acceptance criteria remain unchanged.
Release metadata is now finalized in README, CITATION.cff and .zenodo.json;
the 2026-10-20 release run against 1cb3f84 passed all recorded checks.

RUN_FIX.cmd now forwards to FINAL_BLOBS.cmd. The reused fix_app_sources.py
requires the exact release commit and never falls back to preparation sources.
It verifies upstream blobs before documented privacy transformations and
regenerates published manifests. Actual Git execution remains a human-side
runner step because Git cannot start in this sandbox.

See RECUT_NOTES.md, especially Finalize and Privacy audit, for the complete
current changes, evidence, redactions and verification limits. Historical
preparation inventory counts do not describe the final publication inventory.
