# Premise checks for the chi3 novelty audit

Agent: gpt-a. Model: gpt-6-astra. Family: gpt.

Run `check.py` with the project's Python environment. These are dimensionless
quadratures, phase-matching substitutions, probability identities, and a scalar
covariance ODE. They do not simulate fiber propagation or establish a physical
conversion efficiency or a quantum-noise coefficient.

- A Gaussian's energy and temporal intensity variance do not depend on quadratic
  phase. Its launch Hamiltonian grows with the square of chirp. Fixed energy and
  RMS duration therefore do not specify the Hamiltonian ceiling.
- For cubic dispersion, the zero-nonlinear-phase resonance relative to a soliton
  shifted by `-r` is `3*b/c + 3*r`. The proposal's coefficient `4*r` fails the
  phase-matching equation. Finite soliton nonlinear phase must be retained in a
  physical yield calculation.
- A blue **edge** gives an inequality; the exact moment identity uses the blue
  conditional mean. Frequency-selective loss can increase the surviving photons'
  centroid, so a lossless moment argument cannot silently include such loss.
- A positive local diffusion/drift ratio does not imply the same lower bound on
  the final variance/shift ratio. Restoring deterministic dynamics can attenuate
  noise injected earlier. The scalar ODE is a logical counterexample only; it
  does not prove this dynamics is realizable in the proposed fiber class.
- Direct evaluation of a Raman nonlinear generator conserves the power-envelope
  norm without self-steepening, but does not conserve physical photon number.
  With the standard shock coefficient `1/omega0`, photon number is conserved and
  the envelope energy decreases by the passive Raman spectral integral. Two
  alias-free grids check the instantaneous identity, not propagation accuracy.

The analytic formulas are checked against independent numerical integration or
direct substitution. Configurations and summary values are versioned. ODE arrays
are stored at the absolute `raw_location` in `meta.yaml`.
