# Ranking rubric for verified results

Each accepted or under-review result is scored by at least two reviewers from different families, each in a clean context, using the anchors below. Scores are integers 1–5. Reviews go in `results/R-*/reviews/<agent>-<date>.yaml`.

| Criterion | 1 | 3 | 5 |
|---|---|---|---|
| `impact` | Refines a known result. | Gives a design rule a specialist group would adopt. | Names a new object or law that would reorganize how a class of systems is designed or taught. |
| `novelty` | Known result in new notation. | New result with clear precedent in a neighbouring field. | No close precedent found by two independent searches. |
| `lab_realizability` | Needs hardware that does not exist. | Testable with available fibers and sources after some development. | Testable now with the lab's equipment; discriminating measurement identified. |
| `simulation_realism` | Idealized model only. | Full model with measured fiber parameters, one solver. | Full model, two solvers, relaxed assumptions, realistic noise and imperfections. |
| `generality` | One operating point. | A one-parameter family. | A wide region of dimensionless parameter space, or several physical platforms. |
| `robustness` | Fragile to small perturbations. | Survives realistic perturbations with graceful degradation. | Attractor or protected quantity; insensitive to input and parameter variation. |

The aggregate is a weighted sum of per-criterion medians, with weights in `results/weights.yaml`. `scripts/rank_results.py` writes `results/RANKING.md` and flags any criterion where reviewers differ by two or more points. The PI may set `pi_score` in a result's front matter; it is shown next to the aggregate and does not replace it.

Reviewers give a one-sentence justification per score. A score without a justification is ignored.
