# Configuration

agent: gpt-b; model: gpt-6-astra; family: gpt.

Launch convention: $u(x,0)=N\exp(-x^2/2)$, with the same dispersion and
power normalization as the fundamental-sech cases. `N` therefore multiplies
field amplitude. Full physical configurations are
`runs/2026-10-10-gpt-b-soliton-solver/gaussian_*.toml`.

- `soliton_gaussian_scattering.py --output <raw>/scattering.json` computes
  the imaginary Zakharov–Shabat eigenvalues by half-line shooting. Exact
  sech controls and finer-step/larger-window Gaussian checks are included.
- `soliton_inherited_amplitude.py <raw>/inherited_amplitude.json` differentiates
  the largest scattering eigenvalue. This is a neutral-coordinate diagnostic;
  its separated-soliton energy Fano factor is a different readout from a binary
  spectral mask.
- Native configurations and batch adjoints use the commands in the solver run.
  The Raman-free N=1.25 and N=1.5 cases use output band 10 and `--no-bath`.
  Their temporal step is allowed to exceed 3 fs because the Raman response
  is absent. The Raman case uses the finer grid declared in its TOML.

`surrogate_prediction.json` was committed before either Gaussian covariance
was propagated. It tests the candidate of substituting the classical IST
soliton width into the coherent-sech formula. No inherited covariance was
fitted to the test outputs. This substitution is not an assumption of the
final soliton bound.

`soliton_launch_perturbation.py` tests the first Duhamel correction for a
Gaussian-minus-sech launch mismatch, keeping the inherited covariance.
The raw JSON records N, dominant soliton amplitude, normalized distance,
interpolation parameter, Fourier basis and quadrature settings. Runs
labelled `launch_born` are ideal Kerr finite-basis approximation checks;
their matching full RK4IP/discrete-adjoint values use exactly the same
basis. They are not additional physical Raman simulations and their
approximate values have no asserted one-sided bound property.

The inherited-amplitude evaluator also gives the odd carrier-frequency
gradient, checks a unit response to carrier shifts, and compares N-sech
launches with the closed gamma-function identity for their largest
scattering eigenvalue's energy noise. This diagnostic is not the energy
noise after arbitrary physical Raman fission.

`stretch_forecast.json` was frozen in commit `342e7c4` before the N=2
Gaussian fission propagation. It forecasts the dominant soliton's carrier,
not the total-field spectral moment. `soliton_ssfs_response.py --raw <raw>`
is a subsequent, explicitly post-hoc full-response momentum diagnostic.
It does not change the failed frozen first-moment forecast.

`soliton_mean_fit.py --output <raw>/mean_fit.json` measures classical
sech-core fit errors and carrier shifts from the propagated fields. These
fits do not replace the propagated covariance. The late N=1.5 and N=2
fission readout spaces use spectral cells of width .08 and .3, respectively.
Their cell eigenvalues are Ritz approximations, not full-field certificates.

The N=2 fission cell refinement uses
`soliton_batch_adjoint.py <gaussian_N2_Raman_fission.toml> --band 14
--bin-width .15 --source-stride 6 --omit-adjoint --output-suffix batch_cells015`.
The coarser run uses width .3. Native selected-mask configurations are
`gaussian_N2_cells015_native*.toml` in the solver run. They retain the
same physical frequency bins while enlarging the temporal sample count;
their step counts and source quadratures are explicit in those files.
