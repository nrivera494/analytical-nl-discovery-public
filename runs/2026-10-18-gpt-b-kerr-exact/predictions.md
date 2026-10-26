# Frozen independent tests, 2026-10-18
Agent gpt-b; model gpt-6-astra; family gpt. Tasks T-20261018-claude-interactive.7-02 and -04.
No production calculation preceded this file. Reference is exact unitary evolution, not TWA.

## Definitions and derivation to test
Vacuum quadrature variance is one; H=chi N(N-1)/2; s=chi n_d z, n_d=|alpha|^2 is the displacement photon number. A displaced thermal input has t=(nu-1)/2 thermal photons, total mean n_d+t. For u_r=exp(-ir chi z)-1 and D_r=1-t u_r,
<a^r>=alpha^r exp[-i chi z r(r-1)/2] D_r^(-r-1) exp[n_d u_r/D_r], r=1,2.
This follows by integrating the exact coherent-state moments against the positive Gaussian P representation. Check against independent Fock density-matrix evolution at n_d=4,16,64 and nu=1,3,10 (cutoff increased until moments agree to 1e-8 relative/absolute).
Lambda=1+2(<N>-|<a>|^2)-2|<a^2>-<a>^2|.
For nu fixed and n_d large, test lambda_best/[nu^(4/3)n_d^(-1/3)] -> 3/(2*4^(1/3))=0.9449408. Fit exponent using n_d=1e6,1e8,1e10; held out n_d=1e7,1e9,1e12, nu=3,30; require exponent -1/3 +-0.03, prefactor within 3% for nu<=30 and n_d>=1e8. Explicitly score proposer's nu={3,10,30}, n_d={1e4,1e5,1e6}, tolerance 1 dB. Retain failures at small n_d/nu.
Measure relative asymptotic error power versus n_d (do not assume power). Test n_d=1e2..1e12, nu=1,3,10,30,100. No universal finite-n theorem inferred from the fit.

## TWA validity
Use analytic Gaussian integral for exact classical Weyl flow a(s)=a(0) exp[-is(|a(0)|^2-1)/n_d], Wigner complex variance nu/2. Compare its optimum and fixed s against exact moments. QMC trajectories are a third check (4 scrambles, 2^14 then 2^16 samples). Core n_d=16,64,256; held out 1024,4096; nu=1,3. Acceptance for using TWA in strongly occupied modes: <0.3 dB error at n_d>=4096 and s<=2 n_d^(1/6), with actual errors recorded. Check larger shears as failure controls. Fit errors; do not label all observables O(1/n) from a coherence test.
For coherent Kerr, tangent lambda=(sqrt(1+s^2)-s)^2 and sigma_max^2=1/lambda. Test curvature at fixed s=2,4,8: excess along tangent squeezed direction scales as n_d^-1 within exponent 1+-0.15 over 1e5..1e9; asymptotic term sigma_max^4/(8n_d) only claimed at s>>1. Test sigma_max^6/n_d={0.08,0.8,8,80}; boundary 0.8 predicts <10% relative excess (tolerance 15% to allow finite shear). Counts have exact Fano=1 for one mode.

## Sagnac/no-go
Two equal Kerr arms, input coherent pump plus vacuum, beam splitters 50:50. At a fixed coherent pump, the dark covariance equals the centered single-arm coherent Kerr covariance exactly. Test by two-mode Fock or independent Wigner beam-splitter propagation. Per-arm n_d=1e10, mean Phi={3,10,30,60}; power RMS epsilon={0,.02,sqrt(.0026),.1}. Use both fixed laboratory LO and an LO that follows each shot's output mean phase. Freeze both measurement definitions: cancellation of mean field is not a phase reference.
For the tracking LO at large Phi and small epsilon, test V_dark=V_coherent+epsilon^2 with relative tolerance 5% or absolute 2e-4 (larger), recording curvature separately. Use Dirichlet K=5,E'=.6 condensate draws, not a Gaussian surrogate; also report its actual epsilon. At Phi=30 compare with the claim's -25.9+-1 dB. Its zero-jitter -35.6 dB is tested against exact curvature.
For fixed LO and uniform pump phase, predict exact no squeezing, V=1+2<N_dark>; squeezing can be recovered only as a conditional/relational observable. Arbitrary Fock-diagonal input to a single-mode Kerr has V=1+2<N>, unchanged. Test finite geometric, Poisson and nonclassical number-state mixtures. Smooth super-Poissonian statistics alone do not establish a positive P representation; search for a counterexample/necessary condition.

## Limits
Monochromatic lossless scalar Kerr, no Raman or temporal grid; dt/window/aliasing inapplicable to closed moments. Fock cutoffs and floating-point cancellation are checked, with 60-digit moments. No claim about an actual thermalized condensate's exact quantum state is inferred from a chosen Gaussian input.
