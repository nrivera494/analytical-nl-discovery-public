# Reproducible independent similariton verification

Start with **TECHNICAL_NOTES.md**, which contains definitions, derivations,
quantum-noise accounting, analytical counterexamples, numerical convergence
results, and primary-literature access scope.

These programs do not import or execute the research repository's code.
They use two independent methods: a conservative real-space hydrodynamic
operator followed by a covariance Lyapunov equation, and a full gain-NLSE
in exact lens coordinates followed by discrete tangent/adjoint propagation.

## Requirements

Python 3, NumPy and SciPy. No network access is required to run the
calculations. The reproduction command writes its Python, NumPy and SciPy
versions to an environment file. Setting OPENBLAS_NUM_THREADS=1 avoids
threading overhead in the small dense covariance calculations.

## Commands

Run these commands from this directory, or pass the absolute path to the
Python program:

    OPENBLAS_NUM_THREADS=1 python reproduce.py --suite all

Outputs go into a new subdirectory named reproduced, leaving the supplied
calculation data in place. An alternate directory can be specified:

    OPENBLAS_NUM_THREADS=1 python reproduce.py --suite all --output-dir /tmp/similariton_reproduced

The full suite includes all original grid, time-step and box comparisons
and can take several minutes. The fastest concrete check of complete-noise
squeezing is:

    OPENBLAS_NUM_THREADS=1 python reproduce.py --suite quick

That computes two resolutions of the short-distance full NLSE
counterexample. Expected matched-LO minimum eigenvalue: approximately
0.89648647, with shot noise normalized to one.

To reproduce only the independent reduced covariance calculation:

    OPENBLAS_NUM_THREADS=1 python reproduce.py --suite fv

Additional named suites are base, extended, window and certification.
Every configuration is explicit in reproduce.py.

The original main programs also have standalone command-line interfaces:

    OPENBLAS_NUM_THREADS=1 python fv_covariance.py --output results_fv_new.json
    OPENBLAS_NUM_THREADS=1 python lens_nlse.py --output results_nlse_new.json

## Files and exact scope

| File | Contents |
|---|---|
| fv_covariance.py | Real-space midpoint finite volumes for the core Sturm–Liouville operator, numerical eigenbasis, differential Lyapunov covariance integration, width transient and gain scans |
| lens_nlse.py | Full gain-NLSE with all second derivatives, exact cubic tangent and real adjoint, coherent vacuum plus both ASE quadratures, physical LO and actual Fourier-spectrum readouts |
| reproduce.py | Explicit settings for all suites and environment metadata |
| analyze_results.py | Fits existing full-field shape responses and summarizes analytic brightness examples and reduced covariance slopes |
| results_fv.json | Core grids 32 through 1024; phase-regulated grids; two unchirped transients; dense large-gain covariance data with native orthonormal readouts |
| results_fv_midpoint_readout.json | Superseded diagnostic data: continuous-polynomial midpoint readouts leaked the energy mode into shape modes at high gain |
| results_nlse.json | Two short-time counterexamples and four moderate-gain grid/step comparisons |
| results_nlse_extended.json | Smaller epsilon grid/step comparisons and two full-field shape-response runs through gain logarithm 6 |
| results_nlse_window.json | Output-window and spectral-aperture convergence comparisons |
| results_nlse_certification.json | Refined complete-noise covariance cases with explicit commutator and tangent-adjoint checks |
| analysis_summary.json | Derived fits, scaling slopes and order-of-limits examples |
| build_figures.py | Builds the PDF and PNG verification figure from existing corrected data, without propagation |
| similariton_verification.pdf / .png | Four-panel plot of compensated variance envelopes, covariance ratios and full-field shape response |

To regenerate analysis_summary.json from the supplied data, run:

    python analyze_results.py

This analysis command reads the supplied JSON files from its own directory.
It does not run propagation. A rerun of the base suite with the current
solver adds the later certification diagnostic keys to those records;
the originally supplied base JSON predates that instrumentation. This
does not change the numerical method or stated covariance values.

## Numerical definitions

Gain is G=exp(tau), where tau=g*z and g is power gain per distance.
Gamma=g*sqrt(L_D*L_NL); epsilon=sqrt(L_NL/L_D).
The principal numerical setting is Gamma=sqrt(18), quantum-limited
inversion n_sp=1.

The finite-volume core uses eight numerical modes and reads the spectral
observable in its own orthonormal numerical eigenbasis, degrees zero
through four, which converges to the Legendre basis. Legendre formulas
only set eigenvector signs. Shape variance records use the native
orthonormal degree-two coefficient. The constant null eigenvalue is set
to zero to eliminate eigensolver roundoff in the exact conservation law.
All covariance
records are multiplied by the input coherent photon number N0; output
photon-weighted variance multiplies by an additional G. Phase records
also contain epsilon squared as stated in their keys.

The finite-volume eps=0 flag means that only the leading density input
and reservoir source is kept. It is not a physical zero-epsilon optical
state and is not a complete quantum covariance. The optional eps=.05
records add both phase sources at the finite-cell edge cutoff. Their
logarithmic cutoff dependence is intentional. Undefined zero-distance
phase or unchirped-spectrum readouts are stored as NaN and are excluded
from fits.

The full NLSE uses a smooth initial density proportional to
delta*log(1+exp((1-xi^2)/delta)), with delta=.25*epsilon^(2/3), normalized
to integral 4/3. It has the exact asymptotic initial chirp, not the
unchirped sharp-parabola seed of the principal reduced repository table.
This distinction is essential when interpreting discrepancies.

Full NLSE phase perturbations are finite-energy field perturbations.
The solver never launches the divergent sharp-edge density perturbation
P_l/sqrt(1-xi^2). Physical matched-LO covariance includes coherent vacuum
and both field quadratures of distributed ASE. Its shot-noise level is
one, and its quadratures obey [Q_A,Q_P]=2i.

The actual spectrum is Fourier transformed at the output and projected
inside the reference chirp edge. Sharp frequency cutoffs have some
window sensitivity; the provided box comparisons quantify this.

## Key expected results

The core proof gives density and phase photon-weighted variance exponents
1/3 and 5/3. Dense finite-volume regression over 12<=tau<=26 gives
0.32461 and 1.69203; the difference reflects persistent oscillatory
prefactors. Comparing equal phases of those oscillations from tau=18
through two covariance periods gives 0.33348834 and 1.66675915.
Spectral eigenvalue-ratio and phase–energy deficit fits give -0.66551
and -0.65351. The matched-LO phase covariance exponent
is 7/3, with a fitted 2.33351.

At tau=12, the 1024-cell leading core result is spectral ratio
0.003031086958 and phase–energy deficit 0.00008963256748.

The original midpoint-polynomial readout contained an O(h²) leakage of
the energy mode that became nonuniform relative to decaying shape modes.
The archived diagnostic JSON must not be used to infer high-gain shape
exponents. The corrected native readout has stable slopes across grids:
128- and 512-cell shape regression slopes differ by about 1e-12.
At tau=26 the compensated variance changes by about 2.2e-5 relative
between 512 and 1024 cells. The technical notes document the correction.

To regenerate the existing-data figure (requires Matplotlib):

    MPLCONFIGDIR=/tmp/similariton_mpl python build_figures.py

The full NLSE low shape mode, epsilon=.05, fits decay 0.333824878 and
frequency 0.47040123, versus the core predictions 1/3 and 0.47140452;
grid/step refinement is reported in the technical notes.

At tau=.02 the complete-noise full NLSE gives a matched-LO eigenvalue
0.896486465508. At tau=4, epsilon=.05, grid 8192, step .0005 and box
half-width 4, the full-field spectral ratio is 0.3124872157, phase–energy
deficit 0.02920070724 and matched-LO minimum 3.159235825.

These verify the reduced theory and representative full-model behavior.
They do not establish a uniform continuum boundary-error bound, an
infinite-bandwidth physical amplifier, or the fixed-photon-number
validity of arbitrarily large gain. Those limitations and the strongest
surviving modified claims are explicit in TECHNICAL_NOTES.md.
