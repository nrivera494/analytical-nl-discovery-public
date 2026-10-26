---
agent: gpt-b
model: gpt-6-astra
family: gpt
date: 2026-10-17
---

# Independent partial quantum verification

Run the stages in `config.yaml` from the repository root with the full run
path and the shared Python environment. `run.py exact` propagates one-mode
Fock amplitudes independently of the classical/TWA core. `lyapunov` measures
classical tangent growth, `coherent` and `dephased` propagate Wigner/phase
ensembles, and `convergence` halves the stochastic step with a coupled
Brownian bridge. All shots within each disorder realization share one path.
No initial or final trajectory power projection is used.

`summarize.py` subtracts symmetric-order and finite-shot estimator biases,
keeps training and held-out photon numbers separate, and records other
coherence and variance clocks as diagnostics. Run `variance_clock_diagnostic.py`
before `summarize.py`: it corrects the original analysis label, which called
the normally ordered excess g2-1 a photon relative variance. The initial
all-excited-mode test is inconclusive on empty input modes; its original
numerical values are retained as explicitly labelled legacy diagnostics.
The occupied-mode photon-variance clock supports n-independence but is post hoc.
The single half-step run does not certify a disorder-ensemble convergence
limit. `plot.py` makes these distinctions visible.

Raw data are under
`~/analytical-nl-discovery-data/2026-10-17-gpt-b-scrambling/`.
The exact ballistic subcase and a logarithmic TWA trend do not validate
Gaussianity until collapse or the exact quantum chaotic branch. See the
cross-family audit for the refutation and outstanding checks.
