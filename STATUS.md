# Status

## PI priorities

Edit this section by hand. Agents read it at the start of every session.

1. Independent review of the problem registry (task `T-0001`). No derivation work on a problem until it has been audited by a second model family.
2. After the review: first vertical slice on the highest-ranked audited problem.

## Dashboard

<!-- DASHBOARD:START -->
Updated 2026-10-26.

- **Problems** (43): audited: 18 · candidate: 14 · parked: 11
- **Claims** (44): proposed: 9 · cheap-checks-passed: 9 · promoted: 14 · refuted: 9 · withdrawn: 3
- **Tasks** (380): open: 271 · blocked: 4 · done: 104 · cancelled: 1
- **Results** (15): formalized: 1 · promising: 14 (top: R-0001)
- **Log entries**: 97 (latest: `2026-10-20_claude-interactive.22_T-20261020-claude-interactive-04.md`)

Waiting on the PI:

- `T-20261002-claude-interactive-02` (p1) — Choose the raw-data storage platform
- `T-20261020-claude-interactive.23-05` (p2) — PI decision on P-20261020-gpt-g-02: families disagree on novelty (gpt high, claude medium)

Blocked (the task file says on what):

- `T-20261002-claude-interactive-03` (p2) — Approval-gated scheduler for unattended sessions
- `T-20261004-claude-interactive-09` (p2) — Derive modal-partition timing jitter of a weakly multimode soliton
- `T-20261004-claude-interactive-10` (p2) — Derive the walk-off correction to the noise of a weakly multimode soliton
- `T-0004` (p3) — Run the public rediscovery benchmark, easy tier

Claims in the pipeline:

- `C-20261004-claude-a-01` (cheap-checks-passed) — Passive parabolic pulse: Legendre–Pöschl–Teller linear propagator, and matched-LO squeezing whose profile limit vanishes at zeta* = 4.737
- `C-20261004-gpt-a-01` (cheap-checks-passed) — A three-mode response expansion predicts finite-distance weak-LP02 retention to next order
- `C-20261008-claude-a-01` (cheap-checks-passed) — Amplifier similariton: the energy, centre-frequency, timing and compressed-timing noise follow exact moment equations driven by the pulse's own time-frequency covariance
- `C-20261008-gpt-a-01` (cheap-checks-passed) — Gain similariton: global attraction on parabolas, conditional nonlinear attraction, and a compressive exclusion
- `C-20261008-gpt-a-02` (cheap-checks-passed) — Full gain-NLSE: strong global attraction is false; density and width attraction have a narrower evidential scope
- `C-20261016-claude-b-03` (cheap-checks-passed) — No conservation-law ceiling on dispersive-wave band yield with third-order dispersion: the photon-number/momentum/Hamiltonian program (sharp Gagliardo-Nirenberg Kerr control) has value 1 on the whole line and 0.74-0.95 on simulation windows; with pure beta2 normal dispersion it reduces exactly to the Cantelli bound
- `C-20261016-claude-interactive.7-03` (cheap-checks-passed) — Without intra-group disorder, weakly nonlinear multimode fibres with equidistant mode groups thermalize to the microcanonical ensemble of (N, E_lin, H_res), not to Rayleigh-Jeans, so the condensate fraction depends on the input phases at fixed mode powers
- `C-20261019-claude-interactive.12-01` (cheap-checks-passed) — Weak normal dispersion, any smooth unchirped peak: the second-order coefficient of the best-quadrature excess depends on the peak shape only through kappa4 = p''''(0)/(6 p''(0)^2), c2(Phi, kappa4) = c2_Gauss(Phi) - (sqrt(6)/8)(kappa4 - 1/2)
- `C-20261020-claude-interactive.21-01` (cheap-checks-passed) — Time-reversal selection rule: for time-symmetric launches the Raman gain changes multimode modal photon fractions only at second order in parity-odd parameters; the first-order Raman modal transfer of a stationary Gaussian field is a closed-form functional of the energy spectra

Open tasks by priority:

- `T-20261004-claude-b-08` (p1, verify, gpt) — Check the archive Raman-noise contraction against an explicit Wigner benchmark
- `T-20261004-claude-b.4-01` (p1, explore, any) — Map the plateau-adjacent second noise dip at long fiber lengths
- `T-20261004-claude-interactive-07` (p1, derive, gpt) — Derive the walk-off boundary of a weakly multimode GRIN soliton beyond first order
- `T-20261004-gpt-b-02` (p1, loose-end, not-gpt) — Audit and repair Raman Wigner noise normalization
- `T-20261006-claude-interactive-02` (p1, infra, any) — Normalize the sampled Raman response in the solver
- `T-20261008-claude-a-02` (p1, verify, not-claude) — Verify C-20261008-claude-a-01: amplifier-similariton collective-coordinate noise
- `T-20261008-claude-b-02` (p1, verify, not-claude) — Independently verify C-20261008-claude-b-01: first-order null, sign change of K* at zeta_c ~ 2.67, and the zeta = 2 counterexample
- `T-20261008-gpt-a-02` (p1, audit, not-gpt) — Audit conditional similariton attraction and the compressive exclusion
- `T-20261008-gpt-a-03` (p1, verify, not-gpt) — Independently verify the gain-NLSE obstruction and width-mode rates
- `T-20261008-gpt-a-04` (p1, literature, any) — Resolve inaccessible similariton stability and rate prior art
- `T-20261008-gpt-b-02` (p1, verify, claude) — Independently verify local Raman exchange and cubic modal phase covariance
- `T-20261009-gpt-b-02` (p1, literature, any) — Close full-text attribution gaps for similariton attraction
- `T-20261010-claude-a-02` (p1, verify, not-claude) — Verify C-20261010-claude-a-02: momentum bound lambda_gen <= <w^2>_in/<w^2>_out and its tightness
- `T-20261010-claude-a-03` (p1, audit, not-claude) — Audit C-20261010-claude-a-03: parity bound for non-negative spectral filters; cross-check with binary certificates
- `T-20261010-claude-interactive-02` (p1, literature, any) — Literature audit for fast lower bounds on filtered Fano factors in fibre
<!-- DASHBOARD:END -->
