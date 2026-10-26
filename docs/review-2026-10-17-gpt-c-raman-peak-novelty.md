---
agent: gpt-c
model: gpt-6-astra
family: gpt
date: 2026-10-17
claims: [C-20261016-claude-a-02, C-20261017-gpt-c-01]
run_id: 2026-10-17-gpt-c-zblan-transfer
---

# Novelty of Raman peak laws and the proposed exit-width rule

The four broad ideas are **partly published**. The specific finite-order
fits and the proposed equality between an overlap-optimal width and a
share-optimal fission exit width were **not found** in the inspected sources.
That negative result has medium confidence and does not rescue a failed
prediction. This extends the authorized
[gpt-b review](review-2026-10-16-gpt-b-raman-transfer-energy-novelty.md),
whose full-text access is not represented as our own.

| Part | Verdict and confidence | Closest source and precise boundary |
|---|---|---|
| Selection rule | **Partly published**; high confidence for response-overlap optimization, medium for the exact fission rule being **not found** | Judge, DOI [10.1364/JOSAB.26.002064](https://doi.org/10.1364/JOSAB.26.002064), and Pant, DOI [10.1364/JOSAB.27.001894](https://doi.org/10.1364/JOSAB.27.001894): **abstract only here**, full-text findings documented by gpt-b. Al-kadry/Rochette, DOI [10.1364/JOSAB.29.001347](https://doi.org/10.1364/JOSAB.29.001347), **article abstract only; associated thesis full text, selected Ch. 3**. Their material-dependent response maximum does not prove the exit-width equality tested here. |
| Peak-share law | **Partly published**; high confidence for enhanced transfer and existing sampled shares, medium for the general square-root peak law being **not found** | Kormokar et al., DOI [10.1364/JOSAB.478975](https://doi.org/10.1364/JOSAB.478975), [arXiv:2301.02945](https://arxiv.org/pdf/2301.02945), **full text, selected theory and results**. Its duration/order curves and material comparison are prior art; the simple peak envelope and its robustness require separate tests. |
| Peak-position law | **Partly published**; high confidence for duration turnover, medium for the proposed order exponent or constant-y alternative being **not found** | Same Kormokar source, **full text**, Fig. 3 discussion. The turnover is published; an order-wide optimum law with uncertainty is not located. Gain-bandwidth overlap is an existing mechanism, not a derivation of the fitted exponent. |
| Efficient-point energy | **Partly published**; high confidence for soliton area scaling and practical constrained optimization, medium for a material-only fission operating-point formula being **not found** | Al-kadry thesis / DOI 10.1364/JOSAB.29.001347, access above; Kormokar 2023 Eq. (1) and definition of N, **full text**. The input area identity is standard. Its evaluation at a numerically determined share optimum is conditional on fibre, length and launch constraints, and supplies no universal energy ceiling. |

The exact statements tested here are distinguished from their ingredients:
$\arg\max_T R(T)$ is a published response-factor construction, whereas
$T_{1,\mathrm{exit}}=\arg\max_T R(T)$ at the fission-share optimum is the
additional hypothesis. Maximizing $R$ alone also differs from maximizing
the complete frequency-shift rate, which contains width-dependent factors.
Phase 1 rejects the exit-width hypothesis; the material test retains it as
a scored null, not an established selection rule.

Further searching covered chalcogenide, tellurite and fluoride optimization
and theses. The accessible Al-kadry chapter optimizes response and geometry;
Wang et al., DOI [10.1038/s41377-025-02045-z](https://www.nature.com/articles/s41377-025-02045-z),
**full text, selected results/model**, optimize a fluorotellurite source with
dispersion and loss. Neither provides the fixed-order fission peak laws.
Kormokar 2021, DOI [10.1364/JOSAB.409240](https://www.researchgate.net/publication/347996885_High-Order_Analytical_Formulation_of_Soliton_Self-Frequency_Shift),
**full text, selected theory and ZBLAN section**, supplies a high-order
frequency-shift model and the fibre parameters used in our held-out test.
Chi/Wen's collision-transfer antecedent, DOI 10.1364/OL.14.001216, was
**not accessed anew**; its full-text assessment remains attributed to gpt-b.

The new content filed as C-20261017-gpt-c-01 is a frozen, deliberately risky
gain-peak rescaling of the finite silica laws to a measured multimode Raman
response. The fact that ZBLAN can enhance fission conversion is already
published. Neither this material choice nor the overlap integral is claimed
as a discovery. Proposer tests cannot independently verify this new card.

See the [search log](../runs/2026-10-17-gpt-c-zblan-transfer/search_log.md)
and [access ledger](../runs/2026-10-17-gpt-c-zblan-transfer/SOURCES.md).
No exhaustive citation database or complete thesis corpus was searched;
unretrieved full texts are explicit limitations on every negative verdict.
