# Longer-distance resolution check

- agent: gpt-a
- model: gpt-6-astra
- family: gpt
- task: T-20261008-gpt-a-01

The exploratory long Gaussian input with w=2, q=-0.5 reaches a large high-frequency guard after gain length 9 on the fixed 16384-point lens grid. Its apparent later entrance is not accepted. Freeze spatial doubling, a second doubling, step/cap halving and window doubling before inspecting those refinements. Restart at gain length 6 from the archived, mass-conserving lens checkpoint, when its frequency guard is negligible and its observable trajectory agrees with the original-coordinate solver. Spectral zero padding preserves the represented periodic field; window expansion is by zero extension in negligible tails. The raw checkpoint SHA256 is recorded in config.toml. This is a refinement of an exploratory continuation, not a new held-out prediction.
