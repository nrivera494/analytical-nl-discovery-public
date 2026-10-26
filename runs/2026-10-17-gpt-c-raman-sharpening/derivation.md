---
agent: gpt-c
model: gpt-6-astra
family: gpt
run_id: 2026-10-17-gpt-c-raman-sharpening
---

# What is exact, and what needs simulation

For sech launch,
$$E_{\rm in}=\frac{2N^2|\beta_2|}{\gamma T_0},\qquad
E_1=\frac{2N^2|\beta_2|}{\gamma}\frac{f_1(T_0)}{T_0}.$$
Thus maximizing share at fixed $N$ differs from maximizing energy. At an
interior smooth share maximum,
$$\left.\frac{dE_1}{dT_0}\right|_{T_0^*}=-\frac{E_1(T_0^*)}{T_0^*}<0.$$
This exact algebra applies to any fixed, consistently specified output-length
prescription, including a fixed physical length or fixed $zN=LN/L_D$.
It refutes the original energy-maximum interpretation independently of every
simulation; it does not locate the maximum under a different input constraint.

For Gaussian launch A=sqrt(P0) exp[-t^2/(2T0^2)], the launch integral is
sqrt(pi) P0 T0. The corresponding normalized energy fraction is therefore
2/sqrt(pi) times the sech-denominator fraction of the same leading energy.
A statement about equal leading energy does not imply equal energy fractions.

For the delayed response H(Omega)=integral_0^infty h(t) exp(-i Omega t) dt,
let G(Omega)=-Im H(Omega)>=0 in the positive-gain region. The exact momentum
identity of the no-shock scalar model gives, for a sech intensity of width T,

$$\frac{d\bar\Omega}{dz}=-\gamma f_R P\,\frac{R(T)}{T},\qquad
R(T)=\frac{\pi}{2}\int_0^\infty
\frac{x^3 G(x/T)}{\sinh^2(\pi x/2)}\,dx.$$

The sech evaluation is exact for that instantaneous profile; continuing to
use the same profile along z is an adiabatic assumption. Substituting the
usual total-gamma soliton area relation P=|beta2|/(gamma T^2) yields
-|beta2| fR R(T)/T^3. The electronic-gamma convention multiplies the rate
by 1/(1-fR) and changes the inferred area-law width, but cannot change the
maximizer of R. This constant-normalization-invariant maximum is what is
compared with the measured fission-soliton width. The full shift rate and
R have different optima; maximizing R alone is not a derivation of a
fission-transfer optimum.

If H has a finite third moment, expand G(x/T)=mu1 x/T+O(T^-3). Exponential
sech spectral decay justifies termwise integration for these specified
responses, giving R(T)=8 mu1/(15 T)+O(T^-3). This is an isolated-profile
Raman-overlap expansion, not the saturated fission excess law. The latter
includes interaction, separation length and breather phase and is not
proved by this calculation.

The peak-share and position laws are numerical. Soliton scaling removes
beta2 and gamma from the reference equation; it does not determine their
N exponents or imply response/shape universality. Finite-N regression
uncertainties and heldout errors must not be called asymptotic remainders.

For an increasingly narrow single-oscillator gain line, the overlap maximum
also has a useful diagnostic limit: up to a positive constant,
R(T) is x^4/sinh^2(pi x/2), x=T/tau1. Its stationary point satisfies
u coth(u)=2, u=pi x/2. This checks the overlap quadrature and shows explicitly
that tau1 alone supplies a scale, not a fission selection principle. No
novelty claim is made for this algebraic narrow-line limit.

For the reference ZS definition, $f_1=2\eta/N^2$ and the area-inferred width is
$T_{\rm area}=T_0/(2\eta)=T_0/(N^2 f_1)$. Inserting the original approximate
peak laws gives
$$T_{\rm area}^*\simeq\frac{1.70}{1.29}\tau_1N^{0.12}.$$
Identifying this quantity with the measured intensity width additionally
assumes the ordinary total-gamma sech soliton area relation. The delayed
response need not preserve that relation exactly, which is why the fitted,
FWHM and area-inferred widths are measured separately in this test.

For equal launch energy and intensity FWHM, let $T_s,T_g$ denote sech and
Gaussian width parameters. Direct integration gives
$$k\equiv\frac{T_g}{T_s}=\frac{\operatorname{arcosh}\sqrt2}{\sqrt{\log2}},
\qquad \frac{N_g}{N_s}=\left(\frac{2k}{\sqrt\pi}\right)^{1/2}.$$
The same physical output length then requires
$(zN)_g=(zN)_s(N_g/N_s)/k^2$. These are exact normalization identities, not
new claims of shape-independent fission physics.

For the physical comparison, the directly measured energy fraction and photon
fraction are different integrals:
$$f_E=\frac{\int |A_1(t)|^2dt}{E_{\rm in}},\qquad
\nu_1=\frac{\int_{\omega>0}|\widetilde A_1(\omega)|^2\omega^{-1}d\omega}
{\int_{\omega>0}|\widetilde A_{\rm in}(\omega)|^2\omega^{-1}d\omega}.$$
Here $A_1$ is the resolved temporal gate containing the leading pulse. A
centroid-frequency correction is an approximation to the second integral.
Both integrals are evaluated directly, including the finite-bandwidth launch
denominator. The local-ZS proxy instead rescales the demodulated field by
$\sqrt{g/b}$, with $b=|\beta_2(\omega_c)|/|\beta_2(\omega_0)|$ and
$g=\omega_c/\omega_0$, before extracting its eigenvalue. It is a local
quadratic-dispersion soliton-content diagnostic, not an exact invariant of the
higher-order-dispersion GNLSE. Its agreement with the direct gate is checked.

For a sech launch at fixed energy, $P_0=E_{\rm in}/(2T_0)$ and
$N^2=\gamma E_{\rm in}T_0/(2|\beta_2|)$. Thus the chosen 3 nJ launch and
10 kW peak-power cap imply $T_0\ge150$ fs. The tested resource constraint
additionally fixes $L=2$ m and $T_0\le500$ fs. A discrete scan identifies
the largest tested output energy; it does not certify a continuous optimum.
