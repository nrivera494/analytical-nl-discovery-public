---
agent: gpt-b
model: gpt-6-astra
family: gpt
run_id: 2026-10-16-gpt-b-raman-literature
task: T-20261016-claude-a-07
---

# Literature digitisation and unit conversions

This run records small analyses of published evidence. It contains no fibre simulation, and no solver was executed. `meta.yaml` records the checked-out solver revision only for repository provenance. Its wall time is elapsed literature-session time, not compute time.

The report is `docs/review-2026-10-16-gpt-b-raman-transfer-energy-novelty.md`. Raw source downloads and rendered pages live at `raw_location` in `meta.yaml`, outside git. Failed downloads were retained and explicitly excluded from the full-text access claims.

## Reproduction

From the repository root:

```sh
~/agent-work/venv/bin/python runs/2026-10-16-gpt-b-raman-literature/digitise_fig3.py
~/agent-work/venv/bin/python runs/2026-10-16-gpt-b-raman-literature/compare_experiments.py
```

The first script regenerates `fig3_digitised.csv`, `summary.json` and `fig3_comparison.png` from the manually inspected symbol centres embedded in the script. The source is arXiv:2301.02945v1, PDF page 8, image xref 66. Raw files include `kormokar-2023-fig3-original.png` and its enlarged version `kormokar-2023-fig3.png`. Both the preprint and publisher's version (DOI 10.1364/JOSAB.478975) were accessed in full and their Fig. 3 plots visually compared.

The second script regenerates the experimental CSV and JSON from source-reported values and explicit conditional fibre coefficients. It computes sech-equivalent N and the proposed optimum; it does not fit experimental data or claim that chirped/Gaussian/pedestal-bearing launches satisfy the model. Values below N=3 are marked extrapolations.

`prior_art_summary.json` is a source transcription and elementary conversion record: the Domingue/Bartels published table, Judge/Pant's reported 18 fs response-overlap maximum, and Al-kadry/Rochette's corresponding chalcogenide scale. The conditional silica energy uses `2 * 21.7 / (1.3 * 18)` nJ; the width ratio uses `18 / 12.2`. The report explains why neither is a published fission-efficiency selection law.

`search_queries.json` preserves 196 queries in 68 batches/access-note entries. It is a record of this research session, not an export of unrelated browsing or chat history.

## Reading bounds and fit limitations

The 45 Fig. 3 symbols have conservative reading bounds of ±0.4 percentage points and ±15 fs, not statistical confidence intervals. Only N=6 has a two-sided sampled maximum. The additional ±100 fs peak-grid scale is not a bound on an interpolated continuous maximum. A two-point position fit that treats the N=5 boundary value as a true maximum is explicitly conditional and has no residual degrees of freedom. Tail-slope sensitivity intervals are corner checks of the reading bounds over a finite duration range, not asymptotic error estimates.

Source values without published uncertainties retain their reported rounding. No missing experimental uncertainty was invented. The source-access level and reference-plane limitations accompany every case.

## Environment and checks

Python from the user-designated virtual environment; NumPy 2.0.2, SciPy 1.13.1, PyMuPDF 1.26.5. The scripts were executed, the comparison plot was visually inspected, and the report's table values were checked against the generated JSON. Repository validation is recorded in the session log. All operations were small, single-process literature tasks; Julia and propagation solvers were not started.
