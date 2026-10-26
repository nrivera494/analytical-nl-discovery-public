---
id: T-20261004-claude-b-06
title: "Explore how far a finite-fraction GRIN multimode soliton launch departs from the Manakov/LP01 noise value"
type: explore
status: done
priority: 2
problem: P-20261004-root-03
claim: null
family_required: any
lease_hours: 8
created_by: claude-b
created: 2026-10-04
---

## Goal

Give P-20261004-root-03 a first quantitative look at its open quantity in the simplest model. The Claude review (T-20261004-root-02, PR #7) reduced the card's question to one deviation: the filtered Fano factor of a multimode soliton launch minus the LP01 (Manakov-limit) value at the same $\zeta$. That deviation comes from the non-Manakov overlaps ($C_{22}=1/2$ for LP02) and from walk-off. If it is tiny in the pure-Kerr model, the card's interest rests on Raman and four-wave mixing; if it is sizeable, the card is worth a derivation.

## Context

This is an exploration, not the blocked derivation task T-20261004-claude-interactive-10. Use the pure-Kerr two-mode NLS with the ideal GRIN overlap matrix and no Raman. Launch $a=\sqrt{p_1/\Sigma}\,\operatorname{sech}\tau$ and $b=\sqrt{p_2/\Sigma}\,\operatorname{sech}\tau$, with $\Sigma=\sum C_{mn}p_mp_n$; this is the card's $\gamma_{\rm eff}$ energy. Read out with a hard bandpass on all modes, and mode-resolved. Compare with the scalar LP01 soliton at the same $\zeta$ and with the Manakov rotation formulas.

## Deliverables

- A run folder with config, meta.yaml and summary.json.
- A note in `explorations/`.
- An audit-trail row on P-20261004-root-03.
- A session log and a pull request.

## Outcome (claude-b, 2026-10-04)

Done in the pure-Kerr model. Runs `2026-10-04-claude-b-manakov-deviation-scan` and `2026-10-04-claude-b-manakov-deviation-edge-scan`; note `explorations/2026-10-04-claude-b-manakov-deviation.md`; audit row on P-20261004-root-03.
- **$\delta=0$:** the all-mode filtered Fano factor is within 0.016 dB of LP01 at $\zeta=2$ (slightly lower), and 0.03–0.31 dB above it at $\zeta=5$ ($p_2=0.3$; about 7 times less at $p_2=0.15$).
- **Walk-off** ($\delta=0.94$) traps the components at carriers $+p_2\delta$ and $-p_1\delta$.
  - At each launch's best scanned band it costs 0.40 dB at $\zeta=2$, and 1.7–2.5 dB at $\zeta=5$.
  - At equal band the cost ranges from 3.6 dB (narrow) down to $-0.125$ dB ($p_2=0.15$, widest band, where LP01 is 4.3 dB from its own best).
- **At the best band** the GRIN launch never beats LP01 by more than 0.014 dB.
- **Mode-resolved bands** centred on the trapped carriers are worse.
- **Mode-resolved counts:** the LP01–LP02 correlation is $-0.10$ to $-0.57$ and follows the Manakov rotation within 2–6% at $\delta=0$.

**Not done**, in T-20261004-claude-b-07:
- folding the result into the card body;
- optimizing the band per launch (position, width, smooth shape).

The full-model version (Raman, measured profile, more modes) belongs to T-20261004-claude-b-03 and T-20261004-claude-interactive-10.
