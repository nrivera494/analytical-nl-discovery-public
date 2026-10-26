---
date: 2026-10-19
agent: claude-interactive
model: claude-opus-5-5
family: claude
task: T-20261019-claude-interactive-15
duration_min: 30
---

## Did

Applied the record discrepancies that the three 2026-10-19 manuscript agents (claude-interactive.18, .19, .20) reported, checking each against the runs first.

## Found

- **R-0001, section 8.** "At non-integer $N$ the headroom is at most 0.44%" was wrong for $N<2.5$; I wrote that sentence. Minimizing the closed-form ceiling over $n$ puts the between-integer maxima at 5.59% ($N\approx1.30$), 0.671% (2.40), 0.205% (3.43) and 0.088% (4.45). Confirmed independently of claude-interactive.18.
- **R-0014.** The τ ≤ 8 ratio "0.86–1.11" did not match the committed `ratio_i_at` values; the correct ones are 1.098/1.106/1.024 for $\Gamma=\sqrt{18}$ and 0.766/0.855/0.935 for $\Gamma=1$. The 500 pJ brightness numbers used a different launch's $\Phi_{NL}$.
- **R-0011 and R-0012** still described C-20261019-pi-chatgpt-02 and -01 as under verification; they are now R-0014 and R-0015.
- **R-0013** merged two different $Z_b$ estimates; both are now given, with their source run.
- **C-20261010-claude-a-01 and the GPT 6 Pro review** wrote the brightness condition as $\Phi\ll N_{\rm ph}$; the card's condition is $\Phi/\sqrt{N_{\rm ph}}\ll1$.
- **C-20261016-claude-a-01:** a rounding slip, 2.777% → 2.776%.
- **T-20261008-claude-a-03** was superseded and is now cancelled with its outcome; P6 stays in T-20261019-gpt-e-04.

## Changed

- R-0001, R-0011, R-0012, R-0013 and R-0014.
- C-20261010-claude-a-01 and C-20261016-claude-a-01, with audit-trail rows.
- docs/review-2026-10-18-pi-chatgpt-similariton-normal-dispersion-verification.md.
- T-20261008-claude-a-03 cancelled.

## Not verified

- claude-interactive.20's 0.09 brightness value for the 500 pJ seed is its own leading-order evaluation.
- The between-integer maxima are closed-form evaluations, not new runs.

## Loose ends

The manuscript agents' own tasks for these fixes (.18-02, .19-02, .19-03, .20-02) sit in PRs #83–#85. Close them once those PRs merge.
