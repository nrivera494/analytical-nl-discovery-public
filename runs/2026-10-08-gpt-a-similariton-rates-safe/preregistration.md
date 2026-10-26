# Stable-step repetition of the frozen rate test

- agent: gpt-a
- model: gpt-6-astra
- family: gpt
- task: T-20261008-gpt-a-01

The earlier fixed-step rate run developed high-frequency instability. Keep it as a failed numerical run. Repeat the previously frozen perturbations and fit windows with both linear and nonlinear phase caps. Check grid, step, window and perturbation amplitude separately before accepting fitted rates. The caps are numerical controls, not changes to the PDE.
