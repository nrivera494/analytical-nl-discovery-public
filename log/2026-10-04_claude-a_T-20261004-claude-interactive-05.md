---
date: 2026-10-04
agent: claude-a
model: claude-opus-5-5
family: claude
task: T-20261004-claude-interactive-05
duration_min: 70
---

## Did

I replaced the stopped subagent claude-interactive.1 on the round-1 P-001 queue, as `docs/plan-2026-10-round1.md` assigns, and claimed T-20261004-claude-interactive-05. Subagent claude-a.1 (claude-opus-5-5) ran the literature search in parallel; I re-read its key source.

1. Derived the linear response of a passively expanding parabolic pulse in the hydrodynamic limit, $\varepsilon=1/N\to0$:
   - the comoving Legendre separation;
   - the Pöschl–Teller time dependence and its closed-form Legendre-function propagator;
   - the matched-local-oscillator covariance for a coherent input;
   - the edge logarithm in that covariance.
   The full derivation is in `claims/notes/C-20261004-claude-a-01-derivation.md`.
2. Ran the cheap checks the task lists (units, zero-length identity, low-power limit, conservation laws, commutator and uncertainty), plus symbolic residuals and independent ODE cross-checks. All are in run `2026-10-04-claude-a-c01-cheap-checks`: symbolic and numeric only, no NLSE simulation, about 6 s.
3. Wrote claim C-20261004-claude-a-01 with frozen predictions and a held-out case. Withdrew C-0001, pointing to it. Retargeted T-0002 to test exactly the new predictions.

I did not run the NLSE solver and did not compare any prediction with a simulation (task instruction; verification is T-0002, non-Claude).

## Found

**Exact separation (hydrodynamic leading order).**
- In $\xi=T/(T_0a)$, the (density, phase) perturbation separates in Legendre $P_l(\xi)$.
- With $\theta=\varepsilon\Phi_{NL}$, each block obeys $p''+l(l+1)\,\mathrm{sech}^2\theta\,p=0$.
- The propagator is $\Phi_l(\mu)\Phi_l(\mu_0)^{-1}$, built from $P_l$ and $Q_l$ of $\mu=\tanh\theta$, where $\mu$ is the fraction of the final spectral width already generated.
- Background: $a=\cosh^2\theta$, $\zeta=\theta/2+\sinh(2\theta)/4$.
- Blocks $l\le2$ come from symmetries: phase and norm, translation and boost, $\zeta$-shift and power scaling. $l\ge3$ is new.
- The full perturbation equation is $\mathcal L_\mu\phi=\mathcal L_\xi\phi$, symmetric between "time" and "space".

**Prior art.** The separation is a special case of Fedichev & Fischer, PRA 69, 033602 (2004), arXiv:cond-mat/0303063, Eqs. (22)–(25), for a superfluid in a time-dependent trap, solved there by WKB. I checked their Eqs. (8)–(14) and (22)–(27) myself. Not found: the closed form, the optical identification, and anything about homodyne noise.

**Matched-LO noise.**
- $C_{AA}=1$, $C_{AP}=\langle G\rangle$, $C_{PP}=\langle G^2\rangle+K$.
- As $\varepsilon\to0$, the profile-limited squeezing is $R_\infty(\zeta)$. It goes from 1/15 (pure SPM) to 2/65 as $\zeta\to\infty$, and vanishes at $\zeta^*=4.737126$, where $Q_2(\mu^*)=0$ and $\mu^*=0.937612$.
- Classical meaning of $\zeta^*$: at fixed fibre length, the output chirp rate is stationary (a maximum, $1.0738/\beta_2L$) in the launched peak power. A power fluctuation then shifts the core phase uniformly.

**Edge term.**
- $K=1+\tfrac13(1-M_{2,11})^2J_\delta$. With the cut-off $\delta\propto\varepsilon^{2/3}$ this is $1+2\mu^4\ln(1/\varepsilon)+$const for the unchirped launch, slope 1.546 at $\zeta^*$. The cut-off exponent is an assumption, argued from the local healing length.
- For the static 1D Thomas–Fermi edge, the $O(\varepsilon^{4/3})$ edge-layer mass vanishes by a Hastings–McLeod identity (Tracy–Widom left tail; checked numerically, B8). This supports, but does not prove, an $\varepsilon^2\ln$ error for the dynamic blocks.

**C-0001.** Its singular-vector prediction is not supported. The vacuum metric ($\langle pp\rangle\propto1/(1-\xi^2)$) mixes Legendre blocks, so field-metric singular vectors and covariance eigenmodes are not Legendre modes. Its frozen frequency ratios belong to the instantaneous generator only.

**Bug caught and fixed before freezing.** The first version of the held-out (pre-chirped) table used $1/\sqrt{a_m}$ instead of $\sqrt{a_m}$ when converting $\varepsilon\Phi$ to input units, and reported the blocks in unit-orbit variables. Direct integration in $\zeta$ exposed this (now check B5). The frozen table is the corrected one.

## Changed

- New: `claims/C-20261004-claude-a-01-passive-parabola-legendre-propagator.md` (status cheap-checks-passed).
- New: `claims/notes/C-20261004-claude-a-01-derivation.md`.
- New: `runs/2026-10-04-claude-a-c01-cheap-checks/`, containing check.py, config.yaml, meta.yaml, summary.json and R_inf_vs_zeta.png. There is no raw output.
- `claims/C-0001-similariton-gegenbauer-modes.md`: proposed → withdrawn, superseded by C-20261004-claude-a-01, with an outcome section.
- `problems/P-001-…`:
  - claims list updated;
  - Fedichev–Fischer, pulsed-Kerr and beyond-Thomas–Fermi items added to the literature section;
  - gap, conjectures and an audit-trail row updated;
  - no change to status, priority, literature_state or novelty.
- `tasks/T-0002-…`: retargeted to C-20261004-claude-a-01, blocked → open (unblocked by the merge of this PR).
- New tasks T-20261004-claude-a-01 to -04 (see Loose ends).
- `tasks/T-20261004-claude-interactive-05-…`: status done.

## Not verified

- Every prediction of C-20261004-claude-a-01 against the NLSE. This is for T-0002.
- The noise cut-off $\delta\propto\varepsilon^{2/3}$ and hence the edge slope 1.546. This is a healing-length argument; T-0002 P4 tests it.
- The classical block error order. Only the $\varepsilon^{4/3}$ bound is asserted. Cancellation down to $\varepsilon^2\ln$ is argued for the static edge but not derived for the dynamic, sharp-cornered launch (T-20261004-claude-a-01).
- Literature read from the subagent's report: Zambelli–Stringari (full text, claude-a.1) and Menotti–Stringari (claude-a.1, keyword search only). Everything else beyond Fedichev–Fischer is abstract only or not accessed:
  - Shirasaki–Haus, Bergman–Haus, Doerr et al., Fetter–Feder, Anderson et al.: abstract only;
  - Finot et al. 2007, Boscolo et al. 2008: not accessed;
  - Tracy–Widom 1994: abstract only; the left-tail expansion was quoted from memory and confirmed numerically (B8).
- Whether the matched-LO profile limit $1-(\int I^2)^2/(\int I\int I^3)$ is already published for Gaussian or sech pulses. It is likely; full texts were not read (T-20261004-claude-a-03).

## Loose ends

- T-20261004-claude-a-01: derive the edge-layer correction to the classical blocks (does the $\varepsilon^{4/3}$ term cancel dynamically?).
- T-20261004-claude-a-02: amplifier similariton with gain Langevin noise (P-001's second target).
- T-20261004-claude-a-03 (not-claude): full-text novelty check of the pulsed-Kerr literature and Finot et al.
- T-20261004-claude-a-04: optimal local oscillator (covariance eigenmodes) in the hydrodynamic theory.
- T-0002 (not-claude): verification of C-20261004-claude-a-01. It opens when this PR merges.

## Searches

Run by claude-a.1 on 2026-10-04, in the web search engine:
- "linearized perturbations expanding Thomas-Fermi condensate scaling solution free expansion collective modes Legendre"
- "Fedichev Fischer cosmological quasiparticle production harmonically trapped superfluid gases scaling solution"
- "quantum noise squeezing parabolic pulse similariton normal dispersion fiber"
- "parabolic pulse linear stability perturbation Legendre polynomials normal dispersion fiber self-similar"
- "expanding one-dimensional Bose-Einstein condensate phonon modes Pöschl-Teller sech^2 scaling time exact solution"
- "Shirasaki Haus squeezing of pulses in a nonlinear interferometer local oscillator pulse shape limit"
- "Kerr squeezing optical pulses fiber nonuniform nonlinear phase shift across pulse limits squeezing homodyne local oscillator pulse shape"
- "Fetter Feder Beyond the Thomas-Fermi approximation … collective modes logarithm correction"
- "Gallo Pelinovsky eigenvalues of a nonlinear ground state in the Thomas-Fermi approximation one dimension correction"
- "one-dimensional Bose gas breathing mode frequency beyond Thomas-Fermi correction logarithm"
- "self-similar parabolic pulse passive fiber perturbation modes Legendre OR Gegenbauer OR Pöschl-Teller hydrodynamic dispersionless limit"
- Title and author searches for Anderson et al. 1993, Finot et al. 2007, Boscolo et al. 2008, Boscolo–Turitsyn–Novokshenov–Nijhof 2002, Castin–Dum 1996, Kagan–Surkov–Shlyapnikov 1996, Joneckis–Shapiro, Doerr et al. 1994.

No item in these searches gave the closed-form propagator, any noise theory for passive parabolic pulses, or a dispersion-induced zero of the matched-LO squeezing limit.
