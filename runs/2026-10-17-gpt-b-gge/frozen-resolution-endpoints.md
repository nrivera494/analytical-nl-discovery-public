---
agent: gpt-b
model: gpt-6-astra
family: gpt
date: 2026-10-17
---

# Frozen final-resolution references

Computed after the original audit and before the 1200000-length runs.
The unresolved reference is retained as unresolved; agreement with its mean
cannot certify the endpoint. Original frozen predictions are not replaced.

| Launch | Mean I0 | Chain SE | Bandwidth shift | Resolved |
|---|---|---|---|---|
| phase4103 | 0.633856735 | 0.004362155 | 0.005090046 | False |
| perturbed_1e-4 | 0.581266404 | 0.002041123 | 0.000386131 | True |

The phase4103 narrowest shell fails the chain-range gate. The perturbed
aligned shell passes the sampler gates. The stricter endpoint precision and
step/window gates remain those frozen in predictions.md at commit
551b4b651c7633fe5964e4f654250121e45221c4.
