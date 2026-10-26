# ZSFormalization

This Lean project implements the first end-to-end formalization recommended on pages 58–63 of **Assess Claim Novelty.pdf**: the sharp even-exponent Zakharov–Shabat bound, Fourier majorization for passive masks, and attained optimality for integer sech sources. It also proves noninteger sech ceilings with exact rational certificates and the even-exponent Gaussian ceilings.

The PDF's full 63-page conversation was used to identify the intended scope. In particular, this project does not assert the earlier, false conjecture that transform-limited pulses maximize the leading eigenvalue for every unimodal source.

For every positive integer order `N`, the checked result is

\[
\max_{\substack{|m|\le1,\;mS_N\in\mathcal S\\
                 \zeta\text{ an }L^2\text{ ZS eigenvalue of }\mathcal F^{-1}(mS_N)}}
  \operatorname{Im}\zeta=N-\tfrac12,
\qquad
\max\frac{4\operatorname{Im}\zeta}{\int|N\operatorname{sech}t|^2dt}
  =\frac{2N-1}{N^2}.
\]

Here `S_N = ZS.sechSource N` is a constructed nonnegative Schwartz spectrum whose inverse Fourier transform is exactly `N sech t`. The identity mask attains both maxima. In Lean, `N = k + 1`, with `k : ℕ`; `IsGreatest` records both the upper bound and an attained witness. At order four, the optimal normalized fraction is exactly `7/16`.

The main statements are:

```lean
ZS.canonical_integer_sech_optimality
ZS.canonical_integer_sech_fraction_optimality
ZS.canonical_order_four_fraction_optimum
ZS.canonical_sech_polynomial_ceiling
ZS.canonical_gaussian_ceiling
```

There are no source-shape assumptions left to discharge in these canonical statements. The more general `IsSechSource` and `IsGaussianSource` interfaces are retained for reuse; `sechSource_spec` and `gaussianSource_spec` prove them for the concrete constructions.

`IsEigenvalue q ζ` means `ζ.im > 0` and the existence of a nonzero square-integrable spinor satisfying the actual differential equations

\[
v_1'=-i\zeta v_1+qv_2,\qquad
v_2'=-\overline q\,v_1+i\zeta v_2.
\]

No spectral bound or spinor asymptotic is included in this definition. The proof derives nonvanishing, the differential inequality for
`x = (|v₁|² - |v₂|²)/(|v₁|² + |v₂|²)`, and both limits `x(-∞) = 1`, `x(+∞) = -1` from the ODE and the L² hypotheses. It then integrates the weighted inequality over finite intervals and passes to the whole line. Monotonicity of `x` is not assumed.

For `n = k + 1 ≥ 1`, the resulting estimate is

\[
(2n)^{2n}\eta^{2n-1}
\int_{-1}^{1}(1-s^2)^{n-1}\,ds
\le 2(2n-1)^{2n-1}\int_{\mathbb R}|q|^{2n}.
\]

The Fourier majorization step is proved by convolution-power induction and Plancherel. The mask can have any pointwise phase and attenuation with `|m(ξ)| ≤ 1`, provided the product `mS` remains Schwartz. The theorem does not silently extend to rougher masked spectra.

The sech spectrum is constructed as the Fourier transform of a formally constructed Schwartz pulse. Its nonnegativity is proved using the autocorrelation identity

\[
\int h(s)h(s-t)\,ds=\tfrac14\operatorname{sech}t,
\qquad h(s)=\exp(s-\exp(2s)).
\]

Thus its Fourier transform is a nonnegative squared magnitude. Fourier inversion proves the exact transform-limited waveform. This route avoids a complex contour integral; the familiar closed-form expression `π N sech(π² ξ)` for the spectrum is not separately evaluated in this project.

The sharpness witness is the explicit spinor

\[
v_1(t)=e^{-t/2}\operatorname{sech}^{N}t,
\qquad v_2(t)=-e^{t/2}\operatorname{sech}^{N}t,
\qquad \zeta=i(N-\tfrac12).
\]

Its ODE and square integrability are checked for every real `N > 1/2`. For integer `N`, the upper bound makes this an optimal eigenvalue over all admissible masks. For noninteger `N`, the project proves that the displayed height is attained and bounds every attainable height from above; it does not assert exact optimality at the lower endpoint.

The noninteger source ceiling is checked in the polynomial form

\[
(2n)^{2n}\eta^{2n-1}
\le 2(2n-1)^{2n-1}N^{2n}.
\]

The following enclosures use exact rational arithmetic. Each lower endpoint is attained by the unmasked source, and each upper endpoint bounds every admissible passive mask. The percentages are exact decimal presentations of the proved rational upper gaps, rounded upward relative to the polynomial root.

| Source order N | Exponent 2n | Attained height | Upper height | Maximum relative gap to this baseline |
|---|---:|---:|---:|---:|
| 5/2 | 6 | 2 | 2.0087344 | 0.43672% |
| 7/2 | 8 | 3 | 3.0046338 | 0.15446% |
| 11/2 | 12 | 5 | 5.001944 | 0.03888% |
| 19/2 | 20 | 9 | 9.0006687 | 0.00743% |

These are `canonical_sech_five_halves_enclosure`, `canonical_sech_seven_halves_enclosure`, `canonical_sech_eleven_halves_enclosure`, and `canonical_sech_nineteen_halves_enclosure`.

For the Gaussian pulse `N exp(-t²/2)`, the source is constructed with the exact Fourier formula

\[
S_N(\xi)=N\sqrt{2\pi}\exp(-2\pi^2\xi^2).
\]

Mathlib's Fourier convention is `exp(-2π i t ξ)`. The corresponding bound, for every positive integer `n`, is

\[
(2n)^{2n}\eta^{2n-1}\int_{-1}^{1}(1-s^2)^{n-1}\,ds
\le2(2n-1)^{2n-1}N^{2n}\sqrt{\pi/n}.
\]

The general real-`p` ZS inequality, sharp Hausdorff–Young theorem, strongest continuous-exponent Gaussian ceiling, and certified Gaussian eigenvalue enclosure needed for the quoted `0.015%` tightness gap are **not formalized here**. They are the later milestones distinguished in the PDF. The near-integer and large-order asymptotic expansions are also outside this implementation.

The project concerns the static ZS problem. It does not formalize NLS time evolution, inverse-scattering energy identities, Raman/TOD transport, or the numerical propagation examples. The quantity `4η / sourceEnergy` is explicitly defined as the normalized spectral statistic used in the conversation; its physical interpretation is not an additional theorem of this project.

The source files are organized as follows:

| File in `ZSFormalization/` | Checked contribution |
|---|---|
| `Scalar.lean` | Sharp integer-power scalar inequality |
| `BoundState.lean` | Actual ZS/L² definitions, nonvanishing, differential inequality |
| `Endpoints.lean` | Spinor endpoint limits derived from ODE and L² data |
| `Moment.lean` | Finite-interval integration and whole-line moment estimate |
| `FourierMajorant.lean` | Convolution majorization and even-moment Fourier bound |
| `SpectralBound.lean` | End-to-end bound for actual eigenvalues and passive sources |
| `Sech.lean` | Exact sech moments and polynomial ceilings |
| `SechSharpness.lean` | Explicit integer-order L² eigenfunction |
| `Corollaries.lean` | Attained optima, energy normalization, rational certificates |
| `Sources.lean` | Concrete sech Schwartz spectrum, positivity, canonical optima |
| `RealSech.lean` | Real-order L² witness and concrete noninteger enclosures |
| `Gaussian.lean` | Exact Gaussian moments and even-exponent ceilings |
| `GaussianSource.lean` | Gaussian Schwartz construction, Fourier pair, canonical ceiling |

To reproduce the check, install Lean's `elan` toolchain manager, enter this project directory, and run:

```sh
lake exe cache get
lake build
lake env lean Audit.lean
```

`lean-toolchain` pins **Lean v4.35.0-rc4**. `lakefile.toml` and `lake-manifest.json` pin mathlib to commit **1f414401f69059aa7eead47b53ee40bd38455eeb** and pin its transitive dependencies. The first command retrieves mathlib's compiled cache. The source archive excludes `.lake`; it includes all project source and configuration needed to resolve these public dependencies.

`verification/build.log` records the successful build. `Audit.lean` prints the important definitions and theorem signatures as well as transitive axiom dependencies; `verification/axioms.txt` records its output. Every audited theorem depends only on `propext`, `Classical.choice`, and `Quot.sound`. There is no `sorryAx`, no added axiom, and no `native_decide` proof dependency. The canonical theorem statements are included in the audit so the audit can be checked for hidden analytical hypotheses as well as axioms.

The development contains genuine analytical proofs. Intermediate lemmas naturally assume the differential inequality or source specification they consume; the final canonical theorems discharge these assumptions from the definitions and constructions described above.
