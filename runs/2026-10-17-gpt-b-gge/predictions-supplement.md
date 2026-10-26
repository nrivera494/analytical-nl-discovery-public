---
agent: gpt-b
model: gpt-6-astra
family: gpt
date: 2026-10-17
---

# Conditioned sampler supplement, before deterministic production

The independent two-million-draw direct sampler has completed. Its full
predictions, including unresolved rare shells, are in shell_predictions.json.
No GGE deterministic production trajectories have been run. Ordinary rejection
is inadequate for several high-H or high-|L| launches. The original failed
effective-sample-size checks are retained.

To resolve those shells, use Metropolis sampling on x_m=e_m I_m/E, sum x=1,
with uniform phases and Gaussian weights in H and (optionally) L. Symmetric
phase steps and pairwise transfers of x preserve the flat reference measure.
Widths remain 0.2,0.1,0.05 times the independently measured shell SD. Four
chains, two starting at the input and two at an independent Dirichlet draw,
are annealed from width 0.4 to the target width; burn-in is discarded.
Use >=1000000 steps per chain and width. Report chain means, block standard
errors, split-Rhat, and bandwidth shifts. No resolved prediction unless
Rhat<1.05 and between-chain range <0.01. Cross-check against direct sampling
where the latter has effective sample size >=200.

The all-real aligned launch has exact x/y reflection symmetry. This is an
invariant submanifold of the chosen HG model. Record its norm outside that
submanifold; do not interpret a mismatch with the unrestricted shell as a
failure of Hamiltonian conservation. The card's aligned-launch endpoint
prediction is nevertheless tested as written. Numerical predictions from
the conditioned sampler will be committed before those trajectories.

Before any memory-scan trajectories, extend the lower disorder strengths to
sigma=0.003 and 0.01 as well, with the same four seeds and 8000-L_NL length.
This brackets Ld both above and below the observation length. In addition to
the preregistered compatibility test, distinguish statistical non-rejection
from demonstrated equivalence: report whether the entire +/-2 SE interval
for the launch difference lies inside +/-0.02. A broad interval is not
evidence that memory has been erased.

The first conditioned sampler left four (H,L) shells unresolved by the
between-chain range criterion, and another failed the bandwidth criterion.
Increase those five samples to four million steps per chain at widths 0.1
and 0.05. Keep the initial results and both sets of convergence diagnostics.
This refinement is performed before any GGE trajectory data are generated.
