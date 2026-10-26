# Literature audit provenance

Agent `gpt-a`; model `gpt-6-astra`; family `gpt`; task `T-20261013-gpt-a-01`.

This is a literature-review record, not a propagation simulation. `summary.json` records the four reviewer judgments, source/access counts and the compression-length normalization comparison. Novelty and impact scores are assessments using `docs/RANKING_RUBRIC.md`, not measured physical quantities. The premise calculations have their own run, `2026-10-13-gpt-a-novelty-premises`.

`source-ledger.json` gives each located publication's DOI or arXiv identifier, access level, relevant finding and access location. Full text means that the body and indicated relevant sections were inspected; it does not certify every equation. Abstract-only and bibliographic-only records do not verify equations or numerical measurements. Alternate arXiv/journal identifiers are included where checked. The review document explains the corrected attributions and unresolved questions.

`config.json` preserves the live search strings and procedure. Publisher-deposited Crossref metadata, full query/result records, reachable PDFs, extracted text and the incoming card snapshots are stored outside git at the absolute path in `meta.yaml`. The raw directory includes a file manifest. Search indexing dates were not treated as publication dates. A failed direct download sometimes had an independently available indexed author or publisher text; the ledger states that distinction.

The optional `accessed-web-texts.json` raw archive is incomplete after an automatic command guard blocked an append containing mathematical text. It is not relied on as a complete archive. The raw `archive-status.json` records the failure; search results and downloaded files remain available. No guard bypass was attempted.

To revisit the audit, search the queries, resolve each identifier, inspect the specified sections and update access labels independently. Search results can change. No masked benchmark was searched, no propagation solver was executed, and no solver changes were made. The solver commit in `meta.yaml` records workspace provenance only.
