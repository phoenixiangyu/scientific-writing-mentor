# Fluent prose and off-text editorial questions

The author's default is readable manuscript prose with editorial problems in comments or a sidecar. This separates the paper from work needed to support it; it does not authorize false statements.

## Missing support

1. Identify what the supplied material establishes.
2. Draft at that supported level: an observation, association or bounded finding may be defensible when a stronger mechanism is not.
3. Keep transitions readable. Do not insert `[TODO]`, "citation needed", "the author should", or an editing question into clean prose.
4. Anchor a comment to the revised text. State the missing item, its consequence, what to supply or verify, and whether it blocks finalization.
5. If a proposed factual claim has no truthful supported formulation, leave that claim out of the clean draft and retain it in the issue record with its required evidence. Anchor to related retained text. Explain this outside the paper; do not invent a substitute fact or silently delete a supported finding.

An **editorial gap** is different from a **research limitation**. A request to verify a citation or provide a replicate count belongs in comments. An actual failure condition or limitation changing the conclusion belongs in the scientifically appropriate manuscript location.

## Format

- DOCX: use native comments through an available document workflow. If unsupported, supply an anchored sidecar and disclose that it is a sidecar. Keep a submission copy free of editorial comments.
- Markdown/plain text: give clean prose plus `revision-notes.md` or `review-issues.json`; use exact quotes and section/paragraph locations.
- LaTeX: keep the rendered paper free of editorial placeholders. Use a sidecar unless the user requests a particular source-comment system.
- Chat: give clean prose first, a compact anchored issue list second when needed.

Suggested issue record:

```json
{"issues":[{"id":"E01","anchor":"Exact phrase in the revision","location":"Discussion, paragraph 2","kind":"evidence","severity":"blocking","question":"Which result supports the mechanism?","needed":"Provide the discriminating test or approve an association-level claim.","status":"open"}]}
```

Kinds: `evidence`, `citation`, `data`, `method`, `statistics`, `logic`, `venue`. Severity: `blocking` or `advisory`. Status: `open` or `resolved`.

`scripts/check_review.py DRAFT ISSUES.json` verifies fields, anchors and common placeholder leakage. `--final` also rejects open blocking issues. It does not evaluate scientific truth or whether a source supports a claim.

Resolve blocking issues before calling the paper submission-ready, or report remaining blockers outside the manuscript. Clean-looking prose can remain a draft.
