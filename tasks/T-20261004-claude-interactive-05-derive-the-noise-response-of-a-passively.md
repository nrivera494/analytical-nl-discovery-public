---
id: T-20261004-claude-interactive-05
title: "Derive the noise response of a passively expanding parabolic pulse and rewrite C-0001"
type: derive
status: done
priority: 1
problem: P-001
claim: C-20261004-claude-a-01
family_required: claude
lease_hours: 12
created_by: claude-interactive
created: 2026-10-04
---

## Goal

Replace C-0001, which rests on an analogy, with a derived, regime-bounded prediction for the **passive** propagation (no gain) of a parabolic pulse in normal dispersion. The prediction covers:
- the linear response of the pulse core in the semiclassical limit $\varepsilon=1/N\to0$, before the pulse edges break: which input perturbations map to which output energy, timing, frequency and chirp, and with what transfer coefficients;
- the leading edge correction and its scaling in $\varepsilon$;
- the quantum covariance of a specified measurement mode for a coherent input.

The predictions are frozen before any comparison.

## Context

Read AGENTS.md, `docs/plan-2026-10-round1.md`, the problem card, `docs/SOLVER.md` and, for the squeezing cards, `docs/multimode-squeezing-scope.md`. P-001 states what is known. Gallo–Pelinovsky's Gegenbauer result is for a frozen Thomas–Fermi model problem, not the evolving pulse. [BT] is an unobtainable private communication; name it if you arrive at a Gegenbauer projection. Frozen eigenmodes, finite-distance singular vectors and covariance eigenmodes are different objects; keep them apart. Verification is T-0002, by a non-Claude family; do not verify your own claim. Raw data: follow the interim local-storage rule in `runs/README.md`. Raw output goes to `~/analytical-nl-discovery-data/<run-id>/`, and its path is recorded as `raw_location` in `meta.yaml`. For this round's four problems, such runs may be cited by claims.

## Deliverables

- C-0001 rewritten, or a new claim `C-<date>-<agent>-NN` with C-0001 withdrawn and pointing to it. It must contain:
  - bounds on $\varepsilon$, $\zeta$ and the higher-order dispersion and Raman groups;
  - the assumption ledger;
  - frozen predictions, including one held-out case.
- Cheap checks recorded in the claim's checks table, with run ids: units, the zero-length identity, the linear (low-power) limit, conservation laws, and the commutator or uncertainty check for the covariance.
- T-0002 updated so it tests exactly these predictions.
- A session log and a pull request.

## Outcome

Done 2026-10-04 by claude-a. C-0001 was withdrawn and superseded by `C-20261004-claude-a-01` (status cheap-checks-passed). Cheap checks are in run `2026-10-04-claude-a-c01-cheap-checks`; T-0002 is retargeted; the log is `log/2026-10-04_claude-a_T-20261004-claude-interactive-05.md`.

Of the three Goal items:
- The core linear response is derived in closed form.
- The quantum covariance is given for the matched local oscillator.
- The leading edge correction is derived for the covariance (a logarithm, with the cut-off exponent assumed). For the classical blocks it is only bounded ($\ge\varepsilon^{4/3}$); the rest moved to T-20261004-claude-a-01.
