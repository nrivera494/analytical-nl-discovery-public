---
id: T-20261004-claude-b-07
title: "Fold the Manakov-deviation exploration into P-20261004-root-03 and optimize the band per launch"
type: explore
status: open
priority: 3
problem: P-20261004-root-03
claim: null
family_required: any
lease_hours: 4
created_by: claude-b
created: 2026-10-04
---

## Goal

Exploration T-20261004-claude-b-06 measured how far a finite-fraction GRIN LP01+LP02 soliton launch departs from the LP01 filtered Fano factor in the pure-Kerr two-mode model (run `2026-10-04-claude-b-manakov-deviation-scan`). This task finishes two things that exploration left open.

1. **Fold the result into the card body.** Its result is recorded only as an audit-trail row on P-20261004-root-03, because three review PRs (PR #6, PR #7, PR #9) were rewriting that card at the time. Once they are merged, add one sentence under the Manakov reduction in "Known sublimits and reductions" (or wherever the merged card states it), citing the run.
2. **Optimize the band per launch.** The card's quantity is the minimum Fano factor, i.e. the best band. In the edge scan (run `2026-10-04-claude-b-manakov-deviation-edge-scan`), five symmetric hard bands were tried; at the best of them walk-off ($\delta=0.94$) costs 0.40 dB at $\zeta=2$ and 1.7–2.5 dB at $\zeta=5$. Band centres on the trapped carriers ($+p_2\delta$, $-p_1\delta$) were worse.
   - Optimize band position and width, with a smooth (for example super-Gaussian) filter as well as the hard one.
   - Find whether any band brings a walk-off launch back to the LP01 best.
   - Separately, explain why the equal-band deviation turns negative ($-0.125$ dB) for $p_2=0.15$ at the widest band.

## Context

- **Code:** `runs/2026-10-04-claude-b-manakov-deviation-scan/twomode_lib.py`.
- **Filter edge on a grid:** set the hard filter by bin count, so the effective edge $(k_{\max}+\tfrac12)\,2\pi/T_W$ is controlled. A threshold on $|\omega|$ moves the edge when the window changes.
- **Independence:** same-family code. A check of the deviation with the solver belongs to T-20261004-claude-b-03 and T-20261004-claude-interactive-10.

## Deliverables

- A run folder for the extended scan (config, `meta.yaml`, `summary.json`).
- The card sentence.
- A log entry.
