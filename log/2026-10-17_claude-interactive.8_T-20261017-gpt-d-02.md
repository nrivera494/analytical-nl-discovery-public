---
date: 2026-10-17
agent: claude-interactive.8
model: claude-opus-5-5
family: claude
task: T-20261017-gpt-d-02
duration_min: 60
---

Tasks T-20261017-gpt-d-02 and T-20261017-gpt-d-03: cross-family verification of gpt-d's claims
C-20261017-gpt-d-01 (exact sech Raman loss ratio) and C-20261017-gpt-d-02 (arctangent concentration
ceiling). The branch `task/T-20261017-gpt-d-02` stacks on gpt-d's PR #58 (merge of
`origin/task/T-20261017-gpt-d-01`). T-20261017-gpt-d-03 was claimed with `task.py`, and all its work is on
this branch. The model id `claude-opus-5-5` was given by the orchestrator.

## Did

- **Freeze.** Held-out points, tolerances and propagation launches were frozen in commit f784fed (`runs/2026-10-17-claude-interactive.8-sech-tightness/predictions.md`) before any check ran.
- **Rederivation.** I rederived both claims independently: the energy identity, the sech autocorrelation, the Laplace transform to trigamma, both expansions, the general moment expansion with remainder, and the bathtub argument, including a proof of the single-interval level sets.
- **Own code.** An mpmath library, my own photon-conserving GNLSE (RK4IP) and a positive-intensity optimizer. No proposer code was used.
- **Runs.**
  - `2026-10-17-claude-interactive.8-sech-tightness` (S): claim 01 static and launch-plane checks.
  - `2026-10-17-claude-interactive.8-concentration` (C): claim 02, 7 propagation launches, convergence, Julia cross-check with the agents' solver b9fa957.
  - `2026-10-17-claude-interactive.8-hc-relaxed` (H): multi-peak Hollenbeck–Cantrell response.
- **Literature.** A literature subagent (claude-interactive.8.1, web only, clean context) plus my own fetches of arXiv:2607.05244 (HTML) and arXiv:2603.21734 (abstract).
- **Audits.** Both audit reports were committed (6320014) before I read any proposer material. I then read gpt-d's proof note and appended post-audit notes.
- **Cards.** Both claim cards are now status `audited`, with Checks rows, Outcome and audit-trail rows. Statements and regimes are unchanged.

## Found

- **C-20261017-gpt-d-01: pass.**
  - Closed form vs two quadratures at 48 held-out points: $3.3\times10^{-25}$ (S).
  - All six error exponents within $\pm0.01$ of prediction: long $-2$ and $-4$, $-4$ at $r=1$; short $1$ and $3$, $4$ at $r=1$ (S).
  - GNLSE launch plane, 16 sech launches: $1.7\times10^{-11}$; real-propagation Richardson: $4.1\times10^{-9}$ (S).
  - The agents' Julia solver reproduces $E(z)$ to $3.2\times10^{-15}$ (C).
  - Under HC the moment expansion survives, but $\rho_{\rm HC}/\rho_{\rm BW}$ reaches 3.07 at 300 fs (H).
  - The exact sech kernel for arbitrary responses is published (arXiv:2603.21734 Eq. 2, equal to the claim's kernel within $2\times10^{-35}$, S).
- **C-20261017-gpt-d-02: pass.**
  - Numerical bathtub equals the arctangent to $1.6\times10^{-10}$; 315 profiles give max $\rho/F=0.996$ (C).
  - 26,507 propagation planes, 0 violations, max $\rho/F=0.409$ (C).
  - Two post-freeze 30 fs fission launches ($N=3$, $N=6$; 14,002 planes): 0 violations, max 0.434 (C).
  - The best positive intensities reach only $0.52F$ at $\tau_2Q\le0.3$ (C).
  - Under HC the arctangent with $\tau_2=32$ fs is exceeded by up to 4% for intensities concentrated to about 13 fs or less; the general $F_W$ holds (H).
- **gpt-d's retained near-cancellation failure.** Explained independently: at $r=0.6$ the gap-ratio slope is 1.080 in their window and 1.0005 at $x\le10^{-4}$ (S).
- **Problems I caused and fixed.**
  - A sign error in my own short-pulse residual (first run reported slope 2). Fixed and rerun; the frozen prediction was unchanged.
  - My HC frequency grid initially started too high (2.5e11 rad/s) for picosecond pulses. Fixed and rerun.
  - A first refined-optimizer run was too slow and was stopped. A lighter version gave the reported numbers.
  - The fluoride launch's first window let $5\times10^{-3}$ of the energy reach the edges. A 4× window gives identical results; the wide-window run is cited.

## Changed

- `claims/C-20261017-gpt-d-01-exact-sech-raman-tightness.md`, `claims/C-20261017-gpt-d-02-concentration-raman-bound.md`: cheap-checks-passed → audited; verified_by and audited_by are claude-interactive.8 (claude); Checks, Outcome and audit-trail rows added.
- `claims/notes/audit-2026-10-17-claude-interactive.8-C-20261017-gpt-d-01.md`, `...-02.md`: new.
- `runs/2026-10-17-claude-interactive.8-{sech-tightness,concentration,hc-relaxed}/`: new. Raw data is in `~/analytical-nl-discovery-data/<run-id>/` on host COECIS-G3FLW49YGQ.
- `tasks/T-20261017-gpt-d-02`, `-03`: done. New tasks: `T-20261017-claude-interactive.8-01`, `-02`.
- **Not written.** The requested PI summaries `docs/summary-2026-10-17-claude-interactive.8-<claim>.md`. The verifier's harness refused to write them ("subagents should return findings as text"). Their text is in the description of PR #60 and in the report to the orchestrator.

## Not verified

- **HC amplitude convention.** $A_i$ against $A_i/\omega_i$, from the original paper (task T-20261017-claude-interactive.8-02). Both conventions give the same qualitative conclusions (H).
- **Original texts not read.** Gordon (DOI 10.1364/OL.11.000662), Herrmann–Nazarkin (DOI 10.1364/OL.19.002065) and Chen, Taylor and Efimov (DOI 10.1364/JOSAB.27.001022): abstract only. Blow–Wood (DOI 10.1109/3.40655): not accessed. The trigamma form is unpublished as far as searched; this is not a proof of novelty.
- **arXiv:2603.21734 Eq. (2).** I compared the kernel as transcribed by my subagent from §3 of v2. I read only the abstract myself.
- **Untested assumption.** The "orthogonal frequency projection" in C-...-02 was not tested. The Julia solver's smooth spectral window changed $E(z)$ by less than $3.2\times10^{-15}$ in the one case run.
- **Fluoride parameters.** The surrogate values are assumed, not sourced. They affect only which $(r,x)$ and dynamics are tested.

## Proposed card changes

For P-20261016-claude-interactive-02, which I did not edit:

1. **Claims list.** Add C-20261017-gpt-d-01 and C-20261017-gpt-d-02, both `audited`, once PR #58 and this PR merge.
2. **"Claims and current results" table**, two new rows:
   - **C-20261017-gpt-d-01** (audited; claude-interactive.8): exact trigamma form of the sech loss ratio, the $x^{-3}$ and $1-2T/\tau_2$ limits, and the general moment expansion. Verified to $10^{-25}$ and in the GNLSE (runs S, C).
   - **C-20261017-gpt-d-02** (audited; claude-interactive.8): $\rho\le\frac2\pi\arctan(\pi\tau_2Q/2)$, the relaxed optimum. Physical intensities reach $\le0.52F$ at small $\tau_2Q$. Single oscillator only: under HC, use $F_W$ (runs C, H).
3. **Sketch 2.** The conditional ceiling improves the energy-only bound by a factor $F(Q)$. In the 7 test launches, $Q_{\max}$ was 2.6–4.5 times the launch value for fission (1.0 for fundamental solitons). A launch-only cap on $Q$ is still missing.
4. **Literature.**
   - arXiv:2607.05244 Eq. (17): leading $E^2T^{-3}$ law, full text.
   - arXiv:2603.21734 Eq. (2): exact sech kernel for arbitrary response; §3 of v2 full text, read by subagent claude-interactive.8.1.
   - DOI 10.1364/JOSAB.27.001022 (Chen, Taylor, Efimov 2010): abstract only.
   - arXiv:2511.04013 (Nie et al.): approximate non-adiabatic oscillator formula; full text, subagent.
5. **Oracle caveat.**
   - The single Blow–Wood oscillator is not a calibrated silica response for Raman energy-loss predictions. Against the HC response with the same $f_R$, $\rho_{\rm HC}/\rho_{\rm BW}=3.0$ at 100–300 fs.
   - $h'(0^+)$, and hence $\kappa_U$, is $4.75\times10^{27}$ (HC) against $7.70\times10^{27}$ s⁻² (BW) (run H).
   - Use the general-response quadrature or a measured gain spectrum.

## Loose ends

- T-20261017-claude-interactive.8-01: a sharp ceiling for non-negative intensities (the gap between $0.52F$ and $F$).
- T-20261017-claude-interactive.8-02: the HC amplitude convention from the original paper.
- Input to existing tasks:
  - T-20261017-gpt-d-04 (prior art): the arXiv:2603.21734 kernel identity.
  - T-20261017-gpt-d-05 (realistic response): the HC results of run H, namely $F_W$, the arctangent exceedance and the HC/BW ratios.
