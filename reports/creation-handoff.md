# qiaomu-poster v1.1.0 handoff

Updated 2026-11-18. Upgraded existing canonical skill instead of creating a duplicate. User supplies an avatar; agent refreshes the configured GEO facts, creates a personalized poster and finishes local delivery. Public release requested.

References studied: K2F flyer (single action and layered logistics, no K2F runtime adoption), OpenAI imagegen (identity invariants and transparency, no generated text/QR dependency), existing qiaomu-poster (original assets, mixed-script typography and final QR checks). See avatar-prior-art-research.md for individual source and metric boundaries.

Keep: exact facts/CTA and original identity. Adapt: event preset to an avatar-only conversational entry. Reject: questionnaire for already configured facts, inferred names/roles, expired invitations, fixed template as final output. Invent: date-aware avatar project bootstrap with immutable source, archive label/CTA, and a mandatory agent finish.

Design advantage: only avatar is required while the event is valid; three structure starters reduce setup without replacing visual judgment. Validated advantage: 16 runtime regression tests, 25 heuristic trigger cases, three real layout renders and one refined output, full/540px QR decoding. Hypothesis: lower user effort improves adoption; no comparative user or conversion study.

Artifact pointers: references/avatar-workflow.md, presets/geo-2026.json, scripts/avatar.py, examples/avatar-workflow, reports/avatar-evidence.json. CLI draft status is explicit. Missing evidence: independent human aesthetic evaluation and unattended provider-driven benchmark. Historical 18-case evidence is preserved separately.

Publication contract: feature branch → PR checks → merge → versioned v1.1.0 Release → real isolated npx discovery/install. This source document does not itself establish remote publication; release evidence is attached after publication.
