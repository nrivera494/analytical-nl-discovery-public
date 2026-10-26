---
id: C-0004
problem: P-004
title: "Spacetime symmetry mapping extends to pulsed Kerr amplifiers with dispersion sign flipped"
type: symmetry-mapping
status: refuted
proposed_by: claude-bootstrap
proposer_model: unknown
proposer_family: claude
verified_by: null
verifier_family: null
audited_by: null
auditor_family: null
created: 2026-10-01
updated: 2026-10-04
solver_commit: null
result: null
---

## Statement

For a multimode amplifier with saturated gain, thermo-optic nonlinearity, Kerr nonlinearity and group-velocity dispersion, the map (phase conjugation, gain↔absorption substitution, $\beta_2\to-\beta_2$) takes a target output field to the input field that produces it, for inputs slowly varying on the thermal time scale.

## Regime

To be determined; expected to require pulse-averaged heating (repetition period much shorter than the thermal time) and to fail with Raman.

## Assumptions

Instantaneous Kerr; no Raman; quasi-static temperature over a pulse.

## Predictions

1. Forward propagation of the mapped input in the original amplifier reproduces the target output to solver tolerance.
2. With $\beta_2$ not flipped, the reconstruction error grows with the ratio of fiber length to dispersion length.
3. Held-out: adding Raman at silica strength breaks the mapping by an amount that scales with the Raman fraction.

## Derivation

None. Hypothesis: phase conjugation reverses Kerr phase accumulation only if dispersion is also reversed, as in a temporal mirror.

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Symmetry check: which map inverts the pulsed amplifier? Scalar NLSE with gain, $\beta_2=-1$, $\beta_3=0.1$, Kerr, $L=2L_D$ | **Fails.** With $\beta_2\to-\beta_2$ as claimed, the reconstruction error is 1.42 (1.39 with $\beta_3=0$). Phase conjugation plus envelope time reversal plus gain→loss, with $\beta_2$, $\beta_3$ and $\gamma$ **unchanged**, reconstructs the input to $7\times10^{-12}$. Without the time reversal the map still works when $\beta_3=0$ ($6\times10^{-12}$) but fails when $\beta_3\neq0$ (0.58). The algebra agrees: with $B(z',t')=A^*(L-z',-t')$ the NLSE maps onto itself with $g\to-g$ and all dispersion and Kerr signs unchanged | claude (claude-b, proposing family) | 2026-10-04-claude-b-c0004-mapping-check | 2026-10-04 |

## Outcome

**Refuted on 2026-10-04** by the proposing family's cheap check (run `2026-10-04-claude-b-c0004-mapping-check`).
- **What fails:** the claimed need to flip the sign of dispersion. Prediction 2 has it backwards: the map works with $\beta_2$ unchanged and fails with it flipped.
- **The correct map** is phase conjugation plus envelope time reversal plus mirrored gain and loss. It is the known exact-compensation condition for optical phase conjugation:
  - Pepper & Yariv, OL 5, 59 (1980), DOI 10.1364/OL.5.000059, bibliographic record;
  - Watanabe & Shirasaki, J. Lightwave Technol. 14, 243 (1996), DOI 10.1109/50.485581, bibliographic record.
- **Amplifiers:** the slow-envelope version, with thermo-optic heating, is Chen, Wisal, Fink, Stone & Cao, Nat. Phys. 21, 839 (2025), DOI 10.1038/s41567-025-02853-5 (full text read by gpt-a; see P-004).
- **What remains for P-004:** its open symmetry question, the error of the slow-envelope map when transit time, Raman, gain dynamics and thermal history are kept. The envelope time reversal found here is required once odd dispersion is present, and causal Raman breaks it.

The claim is kept (AGENTS.md rule 7).
