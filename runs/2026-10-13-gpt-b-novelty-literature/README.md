# Source audit evidence

Agent: gpt-b; model: gpt-6-astra; family: gpt.

Run `2026-10-13-gpt-b-novelty-literature` records the literature evidence for task `T-20261013-gpt-b-01`. It is a source audit, not a simulation or a replication of reported experiments.

- `sources.json` indexes the active cards' source/access judgments and cached retrieval metadata. A downloaded PDF alone does not count as a full-text reading. Relevant sections were inspected for each source labeled full text; thesis and tutorial labels do not imply a cover-to-cover reading.
- `summary.json` transcribes the source-reported numerical values needed to distinguish incompatible efficiency and selectivity metrics. The page pointers refer to the cached PDFs, including their supplements. Original scratch numbers retained in superseded drafts are not promoted to evidence by this run.
- `searchlog.json` records live query batches from this review. Direct identifier/URL retrievals are also represented in `sources.json`; the log does not claim to record every click or to prove exhaustive absence of a theorem.
- `config.json` gives the assigned cards, baseline and methods; `meta.yaml` gives provenance. The separate trace and comb-balance runs contain the mathematical checks.

Full texts, extracted text, rendered page images and raw retrieval metadata are stored outside git at `~/analytical-nl-discovery-data/2026-10-13-gpt-b-novelty-literature/`. Cached-file hashes and source URLs permit later comparison. A failed metadata request (for example HTTP rate limiting) is not evidence that the source does not exist; source access is recorded separately in the active bibliography.

Two located historical leads lack DOI/arXiv identifiers: the Zakharov–Shabat publisher scan and the NIST seminar event. They are explicitly labeled in `sources.json`, and neither supplies an unidentified theorem to the active cards. The vague Handbook chapter remains unidentified. Remaining full-text and proof leads are registered as follow-up tasks in the review.
