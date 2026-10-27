# qiaomu-poster v1.0.0 handoff

Updated 2026-10-27. Goal: URL/info/logo to precise, brand-specific commercial registration posters; full media counts, natural logo integration, considered Chinese/Latin type, exact final QR.

Canonical source: personal skill source directory, package `qiaomu-poster`. Other agent installations should link to it when managed locally. No independent personal-authoring copies.

Implemented: lean SKILL workflow; design/image/failure references; isolated setup; QR/render/audit/gallery commands; 18 editable cases with source assets; 20 heuristic trigger cases; 10 real-browser regression tests; provenance/rights/evidence reports.

Verified: 18/18 final exports audited; full and phone QR targets exact; all 10 regression tests pass. The title-gap case is seeded by the actual rejected first-pass layout, isolated in a small fixture. Review the report for limits.

Known constraint: bundled Chromium fails `decode()` for one 10000px JPG; the 18-case rerender used installed Google Chrome successfully. Use the documented browser override and do not suppress decode failures. System display fonts may differ across platforms.

Publishing path: feature branch → reviewed PR → merge → GitHub Release v1.0.0 → isolated `npx skills` discovery/install verification. Release-stage evidence is attached to the GitHub Release; this preparation document does not itself prove remote publication.

No final user aesthetic acceptance or conversion metrics are recorded. Follow-up quality feedback should become a specific failure case/reference update rather than a universal palette/layout rule.
