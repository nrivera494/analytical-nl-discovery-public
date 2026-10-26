---
agent: gpt-b
model: gpt-6-astra
family: gpt
date: 2026-10-17
---

# Reflection-sector numerical predictions, before controlled dynamics

The four-chain, width-0.05 predictions are:

| Excitation E | Groups | Mean condensate fraction | Chain/block SE | Width-0.1 shift |
|---|---|---|---|---|
| 0.6 | 1,2 | 0.6105717625 | 0.0013353892 | 0.0055491699 |
| 0.9 | 1,4 | 0.5544644544 | 0.0013390041 | 0.0047802799 |

Both pass the prespecified chain-range, Rhat and bandwidth gates. These
are finite-bandwidth estimates, not exact shell integrals. Compare dynamics
using the unchanged max(0.01,3 combined SE) rule and report bandwidth bias.
They are predictions for the exactly even nine-mode sector, not the full
fifteen-mode phase space. The original full-space predictions remain unchanged.
All values trace to run `2026-10-17-gpt-b-gge`, reflection_predictions.json.
