---
date: 2026-10-19
agent: claude-interactive.16
model: claude-opus-5-5
family: claude
task: T-20261019-claude-interactive-09
duration_min: 70
---

## Did

- **Setup.** Claimed T-20261019-claude-interactive-09 and merged PR #70's branch (`task/T-20261019-claude-interactive-07`) into it. PR #70 holds the promising-tier rules.
- **Read the rules.** AGENTS.md, `docs/PROMOTION.md`, `docs/WORKFLOW.md`, `docs/AUDIT_PROTOCOL.md`, `results/README.md`, `results/_TEMPLATE/`, `scripts/validate.py`, and R-0001 and R-0002 as models.
- **Read the record.**
  - The four claim cards, gpt-b's four reports and PI summaries, and gpt-b's logs of 2026-10-17 and 2026-10-18. I read the logs to establish what gpt-b had read.
  - The literature files of gpt-b's runs.
  - The literature, oracle and lab sections of the problem card.
  - The manuscript's README and `main.tex`, both the main text and appendices A–G.
  - I did not read the proposer's exploration note; I only link it.
- **Wrote four promising results**, each with `RESULT.md`, a `verification-*.md` pointer and `repro/README.md`:
  - R-0007 (C-20261016-claude-interactive.7-01);
  - R-0008 (C-20261018-claude-interactive.7-01);
  - R-0009 (C-20261018-claude-interactive.7-02);
  - R-0010 (C-20261018-claude-interactive.7-03).
- **Checked the numbers.** I checked the run-attributed numbers against the committed run JSON with small read-only scripts, and recomputed the closed forms I added: $f_0\ge0.565$, $-23.28$ dB, $-33.3$ dB and $-5.5$ dB. The helper's independent pass then found a few remaining transcription and wording errors. They are listed under Found and fixed.
- **G7.**
  - I regenerated all four run figures (`plot.py` or `analyse.py`) and the three manuscript figures (`make_figures.py`). Each script was executed with its `fig_summary.png`, `summary.json` or `figures/` output redirected to the scratchpad.
  - The run figures are pixel-identical to the committed ones; the manuscript PNGs and `figure_data.json` are byte-identical.
  - The regenerated `summary.json` files differ only in their lists of component files.
  - Two of the scripts read gpt-b's raw store, which exists on this machine.
  - `git status` was clean afterwards.
- **Updated the records.**
  - The four claim cards: status `sim-verified` → `promoted`, `result` set, an Outcome paragraph and an audit-trail row added. No Statement was changed.
  - The problem card: `results` set and an audit-trail row added. Its status is unchanged.
- **Created tasks** T-20261019-claude-interactive.16-01 to -07.
- **CAS check for R-0010.** Wrote `results/promising/R-0010-displaced-thermal-kerr-squeezing-no-go/repro/derivation.py`, a sympy expansion of gpt-b's exact displaced-thermal moments; no simulation. Section 4 of R-0010 describes it.
- **Number check.** A read-only same-family helper, claude-interactive.16.1, cross-checked the numbers, links and statements of the four results. Its findings are under Found. It is a transcription check, not a review.

## Found

**G5 is open for all four results.** gpt-b's reports are cross-family verifications, not clean-context adversarial audits:
- they were done under verify tasks;
- by gpt-b's own logs, it read the proposer's cited-run metadata (2026-10-17) and the proposer's run config, meta and summary files (2026-10-18) as well as the cards, problem file and evaluator. That is outside the reading list of `docs/AUDIT_PROTOCOL.md`. It read no proposer notes, logs or scripts;
- no optimization-based counterexample search was run;
- gpt-b left blockers open and marked none of the claims `audited`; for 7-01 it wrote "not a completed promotion audit".

The audit pointers are therefore `verification-*.md`. One task, T-20261019-claude-interactive.16-01, covers clean-context audits of all four.

**Gate decisions:**

| Result | G1 | G2 | G3 | G4 | G5 | G6 | G7 | G8 |
|---|---|---|---|---|---|---|---|---|
| R-0007 | met | met | met | met | open | open | met | open |
| R-0008 | met | open | met | met | open | met | met | open |
| R-0009 | met | open | met | met | open | open | met | open |
| R-0010 | met | met | met | met | open | open | met | open |

- **G2.** Open where the quantitative core has no derivation: the 15-mode coefficient $c=0.092$ of R-0008 (T-20261018-claude-interactive.11-03), and the squeezing level of R-0009 (T-20261019-claude-interactive.16-04).
- **G6, R-0007.** Open although both families searched. gpt-b's search was bounded and mostly aimed at the GGE claim, and the microcanonical ideal-Bose-gas condensate-statistics papers were not accessed by either family (Grossmann & Holthaus; Navez et al.); see T-20261016-claude-interactive.7-02.
- **G6, R-0009.** Only Claude searched for its content: T-20261019-claude-interactive.16-02.
- **G6, R-0010.** Only gpt-b searched; the proposer's search was "Not done": T-20261019-claude-interactive.16-03.
- **G6, R-0008.** Met: both families searched, and the closest prior work (Bajer et al.; Najafabadi et al.; Sloan et al.) was read in full and the difference stated. This is a judgement call the PI may want to revisit.
- **Prior art, R-0010.** The coherent coefficient is published: Najafabadi et al., eq. (31), DOI 10.1016/j.optcom.2023.129717, full text (gpt-b). This is stated in its Novelty section.

**Record inconsistencies,** reported here and not fixed:
1. All four claim cards list gpt-b in `audited_by`, `auditor_family` and `auditor_model`, although no audit was completed. The manuscript README, item 8, noted this for C-20261016-claude-interactive.7-01 only. Task T-20261019-claude-interactive.16-06.
2. On C-20261018-claude-interactive.7-03, the Checks row and gpt-b's audit note call 0.218 dB the largest held-out error; the run maximum is 0.21732 dB. Task -06.
3. **Not slips**, although the manuscript README (item 7) lists them:
   - "within 0.218 dB" and "within 0.176 dB" are valid bounds on the run maxima 0.21732 and 0.17549 dB;
   - "below 1.3e-7 dB" is a valid bound on 1.216e-7 dB;
   - "f0 = 0.415" is the correct rounding of 0.4148.

   The README's item 4 gives $f_0=0.42$–0.50 for the $E'=0.9$ held-outs; the run gives 0.415–0.501. These belong to the manuscript refresh, T-20261018-claude-interactive.11-05.
4. **My own first draft got item 3 wrong.** It called 0.176 and 1.3e-7 slips, and wrote "within 0.175 dB" and "within 0.217 dB", which understate the maxima. The helper caught this, and the results, cards, tasks and PR now say it correctly.
5. The problem card's "Current answer" and "Conjectures" sections are still stale: T-20261018-claude-interactive.11-02. The convention differences between the proposer's and gpt-b's disorder amplitude $\sigma$ and launches are stated in each result's assumption ledger.

**Smaller observations:**
- The manuscript's $\lambda_{\rm lin}$ ranges ($-24.72$ to $-25.74$ dB at $z=10$; $-30.12$ to $-31.56$ dB at 20) reproduce with the selection $K=5$, $\sigma=0.3$, $E'\in\{0.3,0.6\}$ (31 cases). Including the $\sigma=3$ cases moves the $z=20$ end to $-31.69$ dB.
- The external-oscillator Sagnac formula error $-0.0317\%$ is the value with 65536 pump samples; 16384 samples give $-0.0356\%$.
- Schema. PR #70's template gives `verification-*.md` the same front matter as audits, so the key is `auditor:` even for a verifier. I added `report_type:` to say what the file is. A `verifier:` key might be clearer; not changed.

**claude-interactive.16.1's check.** It confirmed all links, the 26 cited task ids, the closed forms and most numbers. It found these, all fixed:
- **R-0007.** $f_0\ge0.57$ should be $\ge0.565$.
- **R-0008.**
  - The $\lambda_{\rm lin}$ end at $z=5$ is $-19.7$, not $-19.8$.
  - The $z=20$ end of $-31.6$ dB came from paths outside the $f_0\le0.87$ bound; inside it the end is $-31.46$ dB, and the selection is now stated.
  - The dashed line in the manuscript figure is the analytic $R/8$.
  - The $-7.21$ dB ceiling is a closed form.
- **R-0009.** One SD should be 1.67, not 1.68, and an unsupported sentence about Sloan et al. was removed.
- **R-0010.**
  - The "within 0.175 / 0.217 dB" wording is corrected (item 4 above).
  - The isotropic stage phase $s_*\approx21$ rad does not apply to the phase-elongated extracted condensate; gpt-b's trained phase was 41.2–41.4 rad.
  - The Sagnac experiment pumped by the extracted condensate was outside gpt-b's sign-off. The test is now stated for coherent shots with prepared power jitter.
- **G7.** The run figures of R-0008 and R-0009 need gpt-b's raw store; this is now stated in each result. G7 stays met: the manuscript figure regenerates from committed JSON, and the run figure from the documented raw-store location.
- **G2 of R-0010.** The helper noted that no CAS script existed, which led to `repro/derivation.py`.

**CAS check of R-0010 (i)** (same family as the proposer; independent of gpt-b's hand expansion):
- **Expansion.** At $s=c\,n_d^{1/6}$, $\lambda=n_d^{-1/3}\nu(1+8\nu c^6)/(4c^2)+n_d^{-2/3}\nu(28\nu c^6-1)/(8c^4)+O(n_d^{-1})$, with no odd powers of $n_d^{-1/6}$ through $n_d^{-5/6}$.
- **Leading term.** It reproduces gpt-b's $\nu/(4c^2)+2\nu^2c^4$ and the exact coefficient $3/(2\cdot4^{1/3})$.
- **Next order.** At the optimum the relative correction is $(\nu/4n_d)^{1/3}$. gpt-b's exact optima agree: the measured correction over the predicted one is 0.977–0.9996 for $1\le\nu\le30$, $10^8\le n_d\le10^{12}$ (`exact_summary.json`).
- **Status.** This next-order term is not part of the verified result; its cross-family check is task T-20261019-claude-interactive.16-07.

## Changed

- Added `results/promising/R-0007-condensed-rj-dirichlet-statistics/`, `R-0008-early-multimode-squeezing-curvature/`, `R-0009-condensate-squeezing-covariance-identity/` and `R-0010-displaced-thermal-kerr-squeezing-no-go/`, each with `RESULT.md`, `audit/verification-*.md` and `repro/README.md`.
- C-20261016-claude-interactive.7-01 and C-20261018-claude-interactive.7-01, -02, -03: `sim-verified` → `promoted`, `result: R-0007` to `R-0010`, `updated: 2026-10-19`, with an Outcome paragraph and an audit-trail row on each.
- P-20261016-claude-interactive.7-01: `results: [R-0007, R-0008, R-0009, R-0010]` and an audit-trail row. Status, priority and literature_state are unchanged.
- New tasks T-20261019-claude-interactive.16-01 (audits, G5), -02 and -03 (literature, G6), -04 (derivation, G2 of R-0009), -05 (Lean, G8), -06 (record slips) and -07 (cross-family check of the next-order term of R-0010).
- Added `results/promising/R-0010-displaced-thermal-kerr-squeezing-no-go/repro/derivation.py`.
- T-20261019-claude-interactive-09: status done.
- No generated file, solver file, run file or other result was edited, and no simulation was run.

## Not verified

- **R-0010's derivation.** I did not re-derive the exact displaced-thermal moment formula itself; it is gpt-b's, checked against Fock evolution by gpt-b and numerically by claude-interactive.11. I expanded it with sympy (`repro/derivation.py`) and checked the leading balance, the no-go and the linear Sagnac average by hand. The next-order term $(\nu/4n_d)^{1/3}$ comes from a check by the proposer's family only (T-20261019-claude-interactive.16-07).
- **The other cruxes.** I checked by hand the simplex map of R-0007, the sagitta argument of R-0008 and the $2\times2$ identity of R-0009, not with a CAS.
- **What gpt-b read** is taken from gpt-b's own reports and logs; I did not reconstruct its file accesses.
- **Literature.** No new search was done. Every source and access level is copied from the record.
- **Experimental sections.** These are qualitative. The signal sizes are model values, and there are no sample-size or noise budgets; T-20261018-claude-interactive.11-04 covers sample size for R-0007.

## Loose ends

- T-20261019-claude-interactive.16-01: clean-context adversarial audits of all four (G5).
- T-20261019-claude-interactive.16-02 and -03: second-family literature checks for R-0009 and R-0010 (G6). T-20261016-claude-interactive.7-02 covers R-0007.
- T-20261019-claude-interactive.16-04: derive the condensate covariance (G2 of R-0009). T-20261018-claude-interactive.11-03 covers G2 of R-0008.
- T-20261019-claude-interactive.16-05: Lean formalization of the exact parts (G8).
- T-20261019-claude-interactive.16-06: record slips on the cards.
- T-20261019-claude-interactive.16-07: cross-family check of the next-order term of R-0010 (i).
- Existing tasks: T-20261017-gpt-b-01, T-20261018-gpt-b-01, -02, -03, T-20261018-claude-interactive.11-02, -05.
