# Frozen material extrapolation (before ZBLAN propagation)

Agent gpt-c; model gpt-6-astra; family gpt; 2026-10-17. This is new
proposer content, not cross-family verification. No ZBLAN GNLSE run has
been made. Source-only quadrature is in `response_only.json`.

The phase-1 exit-width hypothesis failed: BW N=4 at T0=200 fs gave fitted
T1=21.3228 fs and area width 19.4053 fs against overlap maximum 15.5576 fs
(run `2026-10-17-gpt-c-raman-sharpening`), outside 15% in both definitions.
We therefore do not use T1=TR* to predict fission. It remains a separately
scored null hypothesis in this material.

## Material and fibre

ZBLAN, measured bulk composition 53 ZrF4 / 29 BaF2 / 3 LaF3 / 3 AlF3 /
12 NaF mol%, Yan et al., DOI 10.1364/JOSAB.29.000238, Table 1. Eight-mode
intermediate-broadening response, fR=0.24, normalized integral one; exact
causal Fourier transform. The table and first-page preview were accessed;
the full article is not accessible here. Its time-domain equation is also
explicit in Cui's thesis, Eq. (4.3), retrieved source excerpt. HC convention
is documented in DOI 10.1364/JOSAB.19.002886 (full text in previous audit).
This is a measured spectrum fit, not a single oscillator.

Use the published ZBLAN fibre model in Kormokar et al., DOI
10.1364/JOSAB.409240, Sec. 4.2.1 (full text, selected theory and ZBLAN case):
lambda0=1940 nm, beta2=-18.9 ps²/km, beta3=0.112 ps³/km,
gamma=2.1 W^-1 km^-1, loss=50 dB/km. Include shock and cubic dispersion.
The reference removes beta3, shock and loss. Both are scalar deterministic
TL sech launches. These independently sourced parameters are a published
fibre-model test, not same-spool calibration. Agger et al., DOI
10.1364/JOSAB.29.000635, full text Sec. 4, establish considerable specimen
variation: their fibre has fR=0.062 rather than the bulk-derived 0.24.

## Equations and scoring

Let f1 be the leading (reddest and largest) isolated local-ZS energy divided
by launch energy, and N²=gamma P0 T0²/|beta2|. The optimum is a local
bracketed turnover in T0 at fixed N and output LN/LD=4, LD=T0²/|beta2|.
Independently report gated energy and photons; do not conflate observables.
Let tau_g=1/Omega_gain,max, where the global gain maximum is determined
only from the measured response. The frozen extrapolation is

$$f_1^*\sqrt N=1.29\;(\pm10\%),\quad
T_0^*=1.70\tau_g N^{1.62}\;(\pm30\%),\quad
E_1^*=\frac{2N^2|\beta_2|}{\gamma T_0^*}\frac{1.29}{\sqrt N}\;(\pm45\%).$$

For N=3,4,5,6, respectively, source-only tau_g=9.23147930 fs gives:

| N | Predicted T0* (fs) | Predicted f1* sqrt(N) | Predicted E1* (nJ) |
|---|---:|---:|---:|
|3|93.037205|1.29|1.296843|
|4|148.271407|1.29|1.252838|
|5|212.839205|1.29|1.219735|
|6|285.973142|1.29|1.193339|

These tolerances are falsification intervals, not statistical confidence
intervals. The share tolerance deliberately exceeds the phase-1 response
spread; position is a risky extension from a single dominant gain scale
to a two-band measured spectrum. No fit to the new material is allowed.
All new material cases are held out. The same predictions are scored for
reference and physical models separately; the primary physical assertion
is their conjunction. A failed component stays failed.

Source-only overlap maximum TR*=22.0557541 fs (quadrature doubled:
22.0557548 fs). Score T1=TR* ±15% as a previously rejected null for both
fitted-sech and area-inferred widths, not as a premise. This overlap width
is a sech parameter, not intensity FWHM (factor 1.762747).

## Regime and predeclared numerical decisions

N=3..6, fR=.24, scalar sech, LN/LD=4. Duration scan factors relative to
predicted T0: .4,.55,.7,.85,1,1.2,1.5,2,2.7. Thus 0.22<y_g=N²tau_g/T0<3.9;
shock parameter 1/(omega0 T0)<.028 and |beta3|/(6|beta2|T0)<.027.
Predictions concern resolved isolated solitons only; all rejected cases
remain recorded. No asymptotic physical error order is asserted.

Use n=8192..32768 chosen so dt<=2.5 fs, window 96 T0, adaptive Float64
RK4IP tolerance2e-9, sparse outputs zN=2,3,4. A peak must have a qualified
lower and upper neighbor; never accept a boundary peak. Fit the three
nearest points in log(T0), compare ordinary-T quadratic, and retain full
neighbor bracket plus fit discrepancy. If coarse maximum is on an edge,
extend factors geometrically by1.5 until bracketed, then freeze the added
case list before running. Refine bracket by geometric midpoints; additions
are localization controls, never used to update predictions.

Qualification: max temporal and spectral edge fraction<1e-6, ZS residual
<1e-8, gate boundary intensity<1e-3, ZS/gate energy within5%, leading
reddest equals largest, loss-corrected photon drift<1e-5, nonpositive
absolute frequency energy<1e-8 for physical cases. Report support in
1.2..4um and1.5..3um; cubic dispersion and constant loss/area are local
model assumptions, not an entire measured dispersion curve.

Controls, at the grid sample nearest each physical maximum (N=3 and6
mandatory; N4/5 if time permits): halve dt; double window at fixed dt;
tighten tolerance by16; sampled normalized kernel (dt<=3fs) versus exact;
require relative share/energy change<0.2% and width change<1%. Fixed-step
h=4e-4,2e-4,1e-4,5e-5 at N4 predicted duration and zN=2: expect fourth-order
field differences (last two measured orders3.5..4.5). Kernel quadrature
dt=3,1.5,.75,.375 fs should approach exact response at order2. ZS meshes
1024,2048,4096,8192 should approach order2. Retain all failures.

One heavy process, serial scans, memory_pressure checked before launch and
every case, wait if free<35%, RSS target<3GB. Production stop by22:20 EDT
on2026-10-17, leaving at least15min for records and PR59. Deferred cases
receive explicit follow-up tasks, never an implied pass.
