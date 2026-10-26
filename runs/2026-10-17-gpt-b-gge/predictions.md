---
agent: gpt-b
model: gpt-6-astra
family: gpt
date: 2026-10-17
claim: C-20261016-claude-interactive.7-03
---

# Independent GGE predictions, frozen before production

## Statement under test

The resonant scalar HG Hamiltonian H=(1/2)sum S_pqrs a_p* a_q* a_r a_s
conserves N, E=sum q_p |a_p|^2 and H separately. A complete triangular HG
cutoff also preserves angular momentum L=a^dagger Lz a. A flat distribution
conditioned on N,E,H,L is stationary. Convergence to it additionally requires
ergodicity; conservation laws alone do not prove equilibration. The proposed
three-constraint law is tested alongside the four-constraint law.

## Cases and frozen comparison

K=5,N=1,E=0.6. Initial excited energy is divided equally between groups 1
and 2, uniformly within each group: I_q=E/[2q(q+1)] there, I0=1-3E/4.
Use random phase seeds 4101--4106 and all-real aligned phases. The held-out
launch is K=5,E=0.9 with excitation energy divided equally between groups 1
and 4, seeds 4201--4204 and all-real phases. These describe physically
preparable modal amplitudes; 'aligned' is a basis convention, not necessarily
a centre-focused field when odd HG modes have nonzero amplitude.

Before propagating these cases, compute independent shell predictions by
sampling the Dirichlet intensity law and uniform phases and conditioning on
H and on (H,L). Use at least 1000000 samples per shell in batches. Report
effective sample size and compare kernel widths 0.2,0.1,0.05 times the
unconditioned standard deviation. Do not report a resolved shell prediction
if effective size <200 or bandwidth shifts exceed 0.01 in condensate fraction.
Record the resulting numbers in a committed supplemental prediction file
before running deterministic production trajectories. No fitted dynamical
coefficients are allowed.

Propagate to s=24000, observing block moments over [4000,24000], step 0.04;
repeat selected cases at 0.02. A shell prediction passes if mean I0 is within
max(0.01,3 combined SE) AND changes by <max(0.01,3 SE) between the two final
halves. H,N,E,L drifts must be <1e-5. Record Kohn and breathing bilinears:
their conservation in the untruncated PDE must not be silently assumed in a
finite Galerkin model. If additional exact invariants are found, the
incomplete-shell prediction is a failed test, not a verified GGE.

For memory erasure, repeat core launch pairs with sigma=0.03,0.1,0.3,1,3,
at least four disorder seeds 7101--7104, s<=8000 initially. Use the shared
Dirichlet run for overlapping cases. Report the last-half phase dependence,
H wandering and RJ deviations, with a resolved erasure criterion
|difference in mean I0|<max(0.01,3 SE) and both means within the same
tolerance of RJ. This does not establish a universal threshold in Ld/z.

The exact rescaling s=g N S0000 z leaves these dimensionless endpoints
unchanged. Full nonresonant checks at 1/kappa=0.1,0.05,0.025,0.0125 and
s<=4 test the O(1/kappa) normal-form error, not long-distance persistence.

## Literature and scope

Read Fusaro et al., DOI 10.1103/PhysRevLett.122.123902, and Podivilov et al.,
DOI 10.1103/PhysRevLett.122.103902. Search resonant trapped NLS invariants,
integrability/ergodicity obstruction, optical generalized Gibbs ensembles,
Picozzi and Christodoulides. A literature absence is restricted to documented
searches. No proposer's code/notes/logs/PR text before audit report commits.

Resource controls and temporal-grid exclusions match the Dirichlet run.

## Follow-up freeze after the initial trajectories (2026-10-17)

The initial 24000-length data are retained. They show slow variation and a
step-sensitive endpoint for seed 4103, while the all-real launch has an exact
x↔y reflection constraint. They do not resolve unrestricted-shell ergodicity.
Extend seeds 4101,4103,4104,0 at E=0.6 and seeds 4201,4204,0 at E=0.9 to
s=240000 at ds=0.02. Retain only 1000-length block moments and checkpoints;
sample every 10 (24000 observations, below the requested limit). Repeat
E=0.6 seeds 4103 and 0 at ds=0.01. Use the original, already frozen shell
predictions, the final two thirds, and the original endpoint/stationarity
criteria. This is a diagnostic extension selected after seeing the short
runs, not an additional blind validation. All original failures remain.
No claim of asymptotic ergodicity follows from merely increasing the length.

Also extend the sigma=3 matched launch pairs (phase 4101 versus aligned 0,
four disorder seeds 7101–7104) to s=24000 with ds=0.04. Assess the [8000,24000]
and [18000,24000] windows. Require the entire difference ±2 SE to lie within
±0.02 and both mean condensate fractions ±2 SE to lie within 0.02 of RJ for
resolved erasure. Compatibility with a broad interval alone is insufficient.
This follows the initial strong-disorder failure and is labelled diagnostic.

## Controlled reflection-sector diagnostic (after initial data, before new runs)

The exact all-real launch is even under x↔y, but the floating-point full-space
trajectory develops a large odd component. It is therefore neither a faithful
long integration of the exactly symmetric initial condition nor a controlled
physical perturbation. Retain it as a roundoff-departed trajectory.

Construct an orthonormal real isometry U from the nine-dimensional even
subspace into the fifteen HG modes and contract all four tensor indices with
U. Integrating the resulting Hamiltonian imposes the symmetry exactly without
projection or renormalization during propagation. Check its instantaneous
vector field against the full model restricted by U.

For E=0.6 (groups 1,2) and held-out geometry E=0.9 (groups 1,4), compute
independent microcanonical (N,E,H) predictions in this reduced sector with four
chains, widths 0.2,0.1,0.05 unconditioned H standard deviations, two million
steps per width/chain, and the earlier Rhat, chain-range and bandwidth gates.
Commit these numerical predictions before propagating the reduced model.
Then integrate to s=240000, ds=0.02, sample every 10, block 1000. Compare the
last two thirds with the frozen sector mean using max(0.01,3 combined SE),
requiring last-half stability and invariant drift <1e-5. This is a post-initial-
data diagnostic, not an additional blind validation of the original claim.

Also use full-space launches with phase of HG01 shifted explicitly by 1e-6
or 1e-4 radians, keeping every initial modal power, N and E unchanged. Record
the actual H and L changes and compare these controlled perturbations with
the existing full-shell predictions. Do not call the original roundoff
trajectory an exact symmetric launch. No new universal sector-selection or
relaxation law is proposed.

## Final resolution diagnostic (frozen after the first audit)

The first audit is already committed and remains an honest record of the
initial verification failure. Use the remaining session budget for a bounded
resolution attempt, without changing its original tests or deleting failures.

1. Refine the full (H,L) reference for E=0.6 phase 4103 and the controlled
   aligned-plus-1e-4 launch. Use four new MCMC chains, widths 0.05, 0.025,
   0.0125 unconditioned standard deviations and eight million moves per width
   and chain, with independent seeds starting at 9751. Preserve the original
   reference and report chain diagnostics and bandwidth shifts. Commit the
   numerical refined references before the new deterministic propagation.
2. Integrate those two full-space launches to s=1200000 at ds=0.01 and 0.005,
   with sample spacing 40 (30000 observation points), blocks 4000 and no
   projection. Also extend the exact E=0.6 reflection sector to that length
   at ds=0.01, using its already frozen reference. Compare [400000,1200000]
   to the appropriate shell with the original max(0.01,3 combined SE) gate.
   Use block lengths through 200000, requiring at least four blocks; require
   half-window stability and charge drift <1e-5. Require the two full-space
   step sizes to agree within max(0.01,3 combined SE). A wide uncertainty or
   unresolved shell is not a certified endpoint: also require measured 2 SE
   <0.01 and reference (2 SE + bandwidth shift) <0.01. These are follow-ups chosen
   after initial data, not new blind heldouts.
3. Extend sigma=3 paired phase-4101/aligned launches to s=96000 for disorder
   seeds 7101–7112, ds=0.04, sample spacing 4 and blocks 400. Repeat the first
   four disorder pairs at ds=0.02 as an ensemble convergence check. Assess
   [32000,96000] and [72000,96000]. The same erasure gate applies: the whole
   difference ±2 cluster SE must lie within ±0.02, and each mean ±2 SE within
   0.02 of RJ. This is a follow-up at a longer fibre length, not a universal
   kinetic law. Do not pool the two step sizes or treat time points as new
   disorder realizations.

The scripts remain serial and apply the memory gate before every heavy launch.
No additional adaptive sweep is planned for this session.

## Single sector step check after the long-window mismatch

The completed exact-sector extension has a large discrepancy with its frozen
shell reference, while its block precision and window-stability gates pass.
Before ending this session, make one additional convergence check rather than
treating that single-resolution result as settled: rerun the same exact
reflection-even E=0.6 launch to s=1200000 at ds=0.005, retaining sample spacing
40 and blocks 4000. This is selected after the mismatch, not a held-out case.
The original shell reference and all earlier results remain unchanged.

Use the same [400000,1200000] window, block lengths through 200000, endpoint
tolerance max(0.01,3 combined SE), charge drift <1e-5, precision bounds and
half-window stability gate. Compare the two sector step means with
max(0.01,3 combined SE). A failure remains a finite-window failure, not a
proof of infinite-time nonergodicity. Commit this amendment before launch;
run it serially after the already-running disorder ensemble. This replaces
the earlier plan to stop without another check, specifically because of the
new long-sector discrepancy. No further sweep is planned.
