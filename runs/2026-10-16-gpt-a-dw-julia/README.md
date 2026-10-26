<!-- agent: gpt-a; model: gpt-6-astra; family: gpt -->

# Pinned-solver cross-check

`crosscheck.jl` supplies the independent dimensionless model to the pinned
agents' solver. Each resolved case has a flat-prefactor counterpart and a
counterpart using the solver's fixed frequency window. The deliberately
coarse cases test sensitivity near that window; they are not accuracy runs.

The first harness launch stopped at a Julia parse error before propagation.
The dotted-arithmetic spacing was corrected. The original error is retained
outside git as `parse-failure-01.log` in this run's raw directory. No failed
numerical output was removed and no solver source was changed.
