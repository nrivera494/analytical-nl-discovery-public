---
agent: gpt-f
model: gpt-6-astra
family: gpt
date: 2026-10-20
task: T-20261020-claude-interactive-01
---

# Symbolic identities and scale screening

Run `2026-10-20-gpt-f-thermodynamic-ledger` contains only algebra and dimensional arithmetic authorized by the literature task. It does not propagate a field, evolve a kinetic equation, measure a thermalization rate or verify the proposed Raman reduction.

Reproduce with:

```sh
~/agent-work/venv/bin/python -W ignore runs/2026-10-20-gpt-f-thermodynamic-ledger/check.py
```

The source inputs and illustrative assumptions are separated in `config.json`. `summary.json` records the mixed-NLS substitution, scalar Raman integration by parts, symmetric-band cancellation, unitary covariance identity, coupling/dispersion commutator and formal ultraviolet integrals. The last integrals diagnose an invalid infinite-band classical extension; they are not an extrapolation of the envelope model to physical infinite optical frequency.

The two-dimensional rotation is a simple symbolic example of the general identity $U I U^\dagger=I$. It does not audit an experimental coupling matrix. The Raman moment is for the specified single-oscillator response, and the assumed kinetic-length ratios are not empirical estimates. The source solver commit is recorded for repository reproducibility but the solver was not used.
