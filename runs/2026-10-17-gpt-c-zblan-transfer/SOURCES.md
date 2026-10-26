# Material and literature access ledger

Agent gpt-c; model gpt-6-astra; family gpt; accessed 2026-10-17.
This ledger distinguishes retrieved text from search snippets and from the
authorized starting review by gpt-b. No subscription or login was bypassed.

| Source | DOI / arXiv | Access and use |
|---|---|---|
| Yan et al., Raman transient response and enhanced SSFS in ZBLAN | [10.1364/JOSAB.29.000238](https://opg.optica.org/josab/abstract.cfm?uri=josab-29-2-238) | **Abstract only**, plus complete public Table 1 and publisher first-page preview through ResearchGate. Eight-mode table and measured bulk composition transcribed. Full article inaccessible. |
| Hollenbeck and Cantrell, multiple-vibrational-mode model | [10.1364/JOSAB.19.002886](https://doi.org/10.1364/JOSAB.19.002886) | **Full text**, selected Eq. (9) and Table 1/footnote in author-hosted ResearchGate PDF. Confirms Gamma=pi*c*Gaussian-table-width, gamma=pi*c*Lorentz-table-width, Omega=2*pi*c*position; no extra sqrt(log 2) correction. |
| Kormokar et al., high-order analytical SSFS | [10.1364/JOSAB.409240](https://www.researchgate.net/publication/347996885_High-Order_Analytical_Formulation_of_Soliton_Self-Frequency_Shift) | **Full text**, selected theory and Sec. 4.2.1. Source for the 1940 nm ZBLAN fibre model, dispersion, nonlinearity and loss. |
| Agger et al., ZBLAN measurement/simulation comparison | [10.1364/JOSAB.29.000635](https://www.researchgate.net/publication/250001776_Supercontinuum_generation_in_ZBLAN_fibers-detailed_comparison_between_measurement_and_simulation) | **Full text**, selected Sec. 4. Their fibre's measured fR=.062 differs from the bulk-model .24; fabrication/specimen variation limits transfer to an arbitrary spool. Not the response used here. |
| Kormokar et al., energy conversion efficiency | [10.1364/JOSAB.478975](https://doi.org/10.1364/JOSAB.478975), [arXiv:2301.02945](https://arxiv.org/pdf/2301.02945) | **Full text**, selected theory, Figs. 3 and 9 discussion, Sec. 6 and references. Published enhanced transfer, duration turnover and material dependence; Eq. (27) independently confirms the eight-mode ZBLAN form. No simple square-root peak law or 1.62 optimum exponent located. |
| Judge et al., tapered-PCF SSFS optimization | [10.1364/JOSAB.26.002064](https://opg.optica.org/josab/abstract.cfm?uri=josab-26-11-2064) | **Abstract only** in this phase. The authorized gpt-b review reports full-text access to the response-factor maximum; Al-kadry's accessible thesis also develops this construction. Do not upgrade our access to full text. |
| Pant et al., PCF characterization/optimization | [10.1364/JOSAB.27.001894](https://doi.org/10.1364/JOSAB.27.001894) | **Abstract only** here; gpt-b's review reports full-text overlap-width evidence. |
| Al-kadry and Rochette, mid-IR sources based on SSFS | [10.1364/JOSAB.29.001347](https://opg.optica.org/josab/abstract.cfm?uri=josab-29-6-1347) | Article **abstract only** here. Associated thesis **full text**, selected Ch. 3, pp. 47–48, Eqs. (3.1–3.2), Fig. 3.4: response factor, As2Se3 maximum and fundamental-soliton energy-width relation. |
| Wang et al., fluorotellurite Raman solitons | [10.1038/s41377-025-02045-z](https://www.nature.com/articles/s41377-025-02045-z) | **Full text**, selected Results/design and SSFS model. Fibre geometry, launch and loss are optimized; does not establish the fixed-order fission exit-width rule. |
| Comparative fluoride SSFS study (2025) | [10.1364/OE.555829](https://doi.org/10.1364/OE.555829) | **Not accessed** as primary full text. DOI/title located, abstract indexed; publisher retrieval failed. Discovery lead only, not evidence for absence of a law. |

Thesis repository: Alaa Al-kadry, *Mid-infrared soliton self-frequency shift
and supercontinuum sources based on As2Se3 chalcogenide microwires*, McGill,
2014, [full PDF](https://www.collectionscanada.gc.ca/obj/thesescanada/vol2/QMM/TC-QMM-123226.pdf).
No thesis DOI/arXiv located; the associated chapter's article identifier is
10.1364/JOSAB.29.001347. The PDF title page identifies Al-kadry, despite an
incorrect author label in one search result. Cui's Er:ZBLAN thesis
([repository PDF](https://deepblue.lib.umich.edu/bitstream/2027.42/174368/1/yifancui_1.pdf))
was available only as an indexed Eq. (4.3) excerpt; no DOI/arXiv located,
and direct retrieval failed. It was a discovery cross-check, not sole
authority for the response convention.

The response implementation uses Yan's measured-spectrum fit with the
HC broadening convention. It combines material and fibre parameters from
different published specimens/models. No measured uncertainty covariance
for the response table or same-spool dispersion/loss data was available.
Numerical error bars therefore exclude material calibration uncertainty.

Failed access attempts: publisher full texts for Yan/Judge/Pant, direct
downloads with local TLS-chain errors, and a browser PDF timeout. TLS was
not disabled. A zero-byte failed download is not treated as read evidence.
