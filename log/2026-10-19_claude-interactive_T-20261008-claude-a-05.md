---
date: 2026-10-19
agent: claude-interactive
model: claude-opus-5-5
family: claude
task: T-20261008-claude-a-05
duration_min: 15
---

## Did

Read Wabnitz, IEEE PTL 19, 507 (2007) in full, from the PI's download (`~/analytical-nl-discovery-data/wabnitz2007/`, not committed).

## Found

- The paper gives dispersionless parabolic ODEs with gain, two amplification regimes (width growing as $G^{1/3}$, peak as $G^{2/3}$), the self-similar fixed point, and phase portraits spiralling into it.
- It has no noise and no shape modes beyond the parabola's own, and states no relaxation rate.
- R-0011 (a)–(c) are not anticipated. The $l=2$ relaxation is anticipated qualitatively; the attraction of C-20261008-gpt-a-01 is partly anticipated, numerically.

## Changed

- `docs/review-2026-10-19-claude-interactive-wabnitz2007-fulltext.md` (new).
- R-0011: G6 met, Novelty section rewritten.
- C-20261008-claude-a-02 and C-20261008-gpt-a-01: novelty rows and audit-trail rows.
- Task a-05: progress note; stays open for three other papers.

## Not verified

I did not linearize Wabnitz's Eq. (7) about Eq. (8). The statement that this linearization gives the $l=2$ rate is GPT 6 Pro's.

## Loose ends

T-20261008-claude-a-05 remains open: McKinstrie 2002, Santhanam 2003, Kruglov 2002.
