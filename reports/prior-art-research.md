# Prior-art research · 2026-10-27

Research question: how to turn URLs and brand assets into compelling commercial registration posters with exact facts and verified final QR codes, without imposing one house template?

## Search and evidence

Built-in qiaomu-meta-skill discovery searched **skills.sh + SkillsMP**, using `commercial event poster typography`, `brand logo image generation`, `poster design layout`. It returned 58 deduplicated candidate families. One skills.sh query returned no parseable candidates; the other two and all three SkillsMP queries succeeded. This is partial catalog coverage, not a complete census. Raw results: [prior-art-candidates.json](prior-art-candidates.json).

Four relevant source SKILL.md files were read directly from GitHub. Source blob IDs are recorded in [source-review.json](source-review.json). Repository metadata and license text were separately checked. Metrics below are dated snapshots; installs are catalog adoption telemetry, stars are repository-level interest, neither is a quality rating. No rating evidence was available.

| Source | skills.sh installs | Repository stars | Last push | License checked |
| --- | ---: | ---: | --- | --- |
| [suzheng/k2f event-poster](https://github.com/suzheng/k2f/tree/main/skills/marketing/k2f-event-poster) | 624 | 3 | 2026-10-15 | Apache-2.0, repository LICENSE |
| [Anthropic frontend-design](https://github.com/anthropics/skills/tree/main/skills/frontend-design) | 1M | 184065 | 2026-10-09 | Apache-2.0, per-skill LICENSE.txt |
| [OpenAI imagegen](https://github.com/openai/skills/tree/main/skills/.system/imagegen) | 5.7K | 28332 | 2026-09-08 | Apache-2.0, per-skill LICENSE.txt |
| [K-Dense latex-posters](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/latex-posters) | 2K | 54834 | 2026-10-26 | MIT, repository LICENSE |

## Keep / adapt / reject / invent

- **Keep:** event identity, reading hierarchy and a single action from k2f; brand-driven form and expressive type from frontend-design; identity invariants and generate/edit distinction from imagegen; real rendered inspection and editable facts from latex-posters.
- **Adapt:** web typography to Chinese/Latin display typography; image prompts to transparent assets and a separate formal logo; final rendering checks to full-size and phone-width QR decoding.
- **Reject:** mandatory proprietary K2F engine; fixed top/middle/bottom layout; academic text-heavy columns; web interaction prescriptions as poster requirements; silent provider fallback; pretending unsupported quality parameters exist.
- **Invent for this workflow:** project-relative manifest, bounded title grouping, stale HTML/PNG detection, explicit per-brand metaphor/topology records, isolated pinned runtime, real failure fixture from rejected GEO spacing, and 18 graded commercial cases with evidence limits.

No upstream code or prompt text was copied. This is an independently authored workflow, not an upstream fork. General design sources and links are in [references/sources.md](../references/sources.md).

## Evidence and non-claims

Validated engineering advantage: executable generation/render/audit commands and adverse-case tests, plus final QR checks for this real 18-poster batch. Design value is supported by inspectable before-problem descriptions and final outputs, not a controlled comparison. Higher aesthetic preference, universal superiority and increased registrations remain untested hypotheses. Catalog popularity does not establish them.
