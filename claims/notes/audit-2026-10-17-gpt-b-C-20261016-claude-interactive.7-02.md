---
agent: gpt-b
model: gpt-6-astra
family: gpt
date: 2026-10-17
claim: C-20261016-claude-interactive.7-02
task: T-20261016-claude-interactive.7-08
verdict: fail
status: completed-verification-failed
---

# Independent audit of the scrambling-length claim

**The claim is not verified as written.** Its exact one-mode Kerr limit has
the stated square-root collapse scaling, and the independent GRIN truncated-
Wigner data are compatible with a logarithmic trend. Neither establishes
Gaussianity until collapse. The prescribed all-mode dephased fluctuation
clock is ill-defined at the sparse launch, and a
coupled step-halving check leaves appreciable uncertainty in the coherent
crossing length. The distinction between global purity, Gaussianity,
coherence loss, intensity fluctuations and thermal equilibrium is essential.

All numbers in this report trace to **run `2026-10-17-gpt-b-scrambling`**.
Predictions were frozen at `f7e1a4f8d1c5c3544573c5cfad145a227624f52b`,
with training/holdout separation clarified at `4f27e39` and the common-path
step refinement committed at `d172b2a0529fb195805c614959929fe433d2492e`,
before production. No proposer run code, exploration, log or PR description
was read. The implementation is independent.

## Exact ballistic subcase and Gaussianity attack

For one mode with $\hat H=\chi\hat n(\hat n-1)/2$, initial coherent occupation
$n$, and $s=\chi n z$, direct evolution of Poisson Fock amplitudes gives

$$\langle a\rangle=\sqrt n\exp\{n(e^{-is/n}-1)\},\qquad
\langle a^2\rangle=n\exp\{-is/n+n(e^{-2is/n}-1)\}.$$

Hence the normalized coherence and first half-collapse length are exactly

$$C(s)=\frac{|\langle a\rangle|^2}{n}
=\exp[-4n\sin^2(s/(2n))],$$
$$s_{1/2}=2n\arcsin\sqrt{\frac{\ln2}{4n}}
=\sqrt{n\ln2}\left[1+\frac{\ln2}{24n}+O(n^{-2})\right].$$

An independent Fock-basis calculation at $n=16,64,256,1024,4096$, including
held-out 256 and 4096, agrees with the exact half-collapse formula to much
better than the frozen relative tolerance $10^{-6}$. The fitted exponent is
0.49971. This verifies the card's stated one-mode limiting case, not a
thermalizing or chaotic multimode system and not its Hartree–Fock coefficient.

For quadratures with vacuum variance $1/2$, the pure-state covariance obeys

$$\det V=(\tfrac12+n-|\langle a\rangle|^2)^2
-|\langle a^2\rangle-\langle a\rangle^2|^2.$$

A pure Gaussian has $\det V=1/4$. Expanding the exact expression at fixed $s$
gives $\det V=1/4+(2s^6+9s^4/2)/n+O(n^{-2})$. The measured inverse-photon-number
error powers at $s=1,2$ are 0.992 and 0.970. More directly, the held-out
$n=4096$ state at $s=4$ has $C=0.99610$ and $\det V=2.51318$, long before its
half-collapse at 53.28387. Unitary purity has survived; Gaussianity has not.
This attacks the asserted duration of Gaussianity in the card's own Kerr
limit. It is not a claim that a one-mode system thermalizes, nor a new
universal Gaussian-breakdown law for chaotic fibre light.

Non-Gaussian coherent-state Kerr evolution is established prior art:
Kitagawa and Yamamoto, DOI
[10.1103/PhysRevA.34.3974](https://doi.org/10.1103/PhysRevA.34.3974)
(**abstract only**, located and read). The numerical and algebraic attack
here does not rely on that paper's derivation.

## Multimode truncated-Wigner test

The classical trajectory is the independent scalar resonant HG model with
$K=5$, $M=15$, $N=1$, $E=0.6$, and excitation in groups one and two. Disorder
has $\sigma=0.3$ under the full spatial-group GUE convention defined in the
Dirichlet run. Two quenched realizations, seeds 7501 and 7502, are tested.
All quantum shots within a realization share **the same disorder path**.
Redrawing the path between shots would instead add classical disorder noise.

The coherent initial field receives independent complex noise
$(\xi+i\eta)/(2\sqrt n)$ per mode. The Weyl force correction
$-(1/n)\sum_qS_{pqqr}a_r$ is included. The scan holds the normalized classical
trajectory fixed as $n$ changes: it varies the effective semiclassical
parameter. Changing physical power at fixed Kerr coefficient would also
change $L_{\rm NL}$ and is not the same experiment.

Each ensemble has 256 trajectories, processed serially in eight batches.
We subtract the finite-shot bias in the squared sample mean and the symmetric-
order half-quantum from intensity. The clock is the first downward crossing
of one half by the mean of individual modal coherence fractions after
$s=10$. Power-weighted and ground-referenced relative coherence are recorded
as separate diagnostics; their crossing times need not agree exactly.
The normalized vacuum energy is $20/n$, well below $E=0.6$ over the tested
$n\ge10^4$, although many input modes initially have no coherent occupation.

The prespecified fitted form is $s_{1/2}=a\ln n+b$. Only core
$n=10^6,10^8,10^{10}$ are used in that fit. $n=10^7,10^{12}$ are held out.
Independent tangent-separation
runs use common disorder, repeated separations $10^{-6},10^{-7},10^{-8}$,
and long-time block errors. Their exponents agree across separations.

| Disorder seed | $\lambda_1L_{\rm NL}$ | Predicted $a=1/(2\lambda_1L_{\rm NL})$ | Measured $a$ | Largest held-out residual |
|---|---|---|---|---|
| 7501 | $0.02027\pm0.00067$ | 24.66 | $18.30\pm4.29$ | 29.14 |
| 7502 | $0.01877\pm0.00112$ | 26.65 | $20.95\pm2.37$ | 2.21 |

Length and slope units are $L_{\rm NL}$. Slope errors in this table are the
regression errors from scatter of the three core points, not precise
population confidence intervals. Quantum-shot jackknife errors are much
smaller; realization dependence and departures from an affine curve dominate.
Both slopes meet the frozen 30% criterion and both holdouts meet the frozen
30-length-or-three-SE criterion. A separate post-hoc free fit to all five
points, $b+a(\ln n)^p$, gives
$p=1.06\pm1.08$ and $0.736\pm0.451$. This is compatible with exponent one,
but does not measure that exponent precisely.

The early scaled-dephasing prediction does work in this semiclassical test. For $n\ge10^6$, $n[-\ln C(s)]$ varies across photon number by less than 0.2% at $s=10,25,50$, and by at most about 7% at $s=100$ for these two realizations. The lower $n=10^4$ case is already approaching saturation and does not collapse onto that curve. This checks the early $1/n$ factor, not Gaussianity of the full quantum state.

The step-0.02 run is a Brownian-bridge refinement of the same step-0.04
increments. At $n=10^8$, seed 7501, its crossing changes from 331.05 to
382.61, while the quantum-shot uncertainty is much smaller. This is a
15.6% change. Long chaotic evolution amplifies discretized-path differences;
a single path pair cannot establish convergence of the disorder ensemble.
In addition, changing only the middle of three equally spaced log-n training
points cannot test the fitted slope itself. Thus this check does **not**
justify a converged numerical coefficient or a `sim-verified` status for
the full scrambling law. Final trajectory power/energy drifts are below
$2\times10^{-8}$, so invariant accuracy alone does not resolve this issue.

## Dephased launch: onset is not equilibrium

**Analysis correction after the first committed report.** The original code
used the normally ordered excess $g^{(2)}-1$ under a relative-variance label.
That diagnostic gave 1.13, 0.20 and 0.22 at $n=10^4,10^8,10^{12}$, but its
failed 20% comparison is not a valid refutation of the stated photon-number
relative-variance prediction. The raw moments are retained. With normalized
Wigner moments $I=\langle|\alpha|^2\rangle$ and $J=\langle|\alpha|^4\rangle$,
the actual photon-number relative variance is

$$R_n=\frac{J-I^2-1/(4n^2)}{[I-1/(2n)]^2}
=(g^{(2)}-1)+\frac{1}{n[I-1/(2n)]}.$$

Nine excited modes are initially vacuum: their photon relative variance is
undefined, while raw Wigner vacuum intensity already has relative variance
one. The all-mode photon statistic is above threshold at the first nonzero
sample for the first two photon numbers, and crosses at 0.221 for the third.
Finite-shot initial vacuum ratios and first-cell interpolation do not define
a reliable onset clock. We therefore withdraw the earlier unqualified
dephased-clock failure, preserving it as an analysis-definition error in
`variance_clocks.json` and this audit trail.

As a diagnostic selected after examining this definition, the actual photon
variance median over the five *initially occupied* excited modes crosses at
2.09285, 2.09241, 2.09237, with shot-jackknife SE 0.0373, 0.0350, 0.0350.
This supports classical n-independence of phase-seeded fluctuations in this
specific diagnostic. It does not replace the frozen all-mode observable or
establish thermal equilibrium. At $s=2$ the mean
condensate fraction is about 0.563, still far from RJ's 0.739; it approaches
that value only at much greater lengths in this ensemble.

## Verdict, scope and remaining work

The whole claim is **refuted as written** by the Gaussian-state assertion
in its stated Kerr limit. Separately, the all-mode dephased onset test is
inconclusive because of its initial support and observable-definition issue,
while the multimode coherence coefficient remains unverified because it lacks
sufficient stochastic convergence. The exact
Kerr square-root law is verified as a known limiting subcase; the logarithmic
TWA trend is partial positive evidence. No exact chaotic many-mode quantum
calculation, reduced-state Fock diagonalization, entropy equilibration, or
universal minimum-of-two-lengths law has been established. The displayed
Kerr formulas and tested TWA trend do not constitute a new proposed claim.

The relaxation of TWA to exact Fock evolution is limited to the ballistic
one-mode case. A physical multimode Hartree–Fock coefficient, finite temporal
cells, dispersion/walk-off, polarization, loss and Raman were not tested.
No temporal grid or Raman kernel exists in this spatial model, so a ≤3 fs
Raman-grid check is inapplicable. No adjoint was used. Further work must
separate Gaussianity from coherence, establish stochastic ensemble convergence,
and compare a genuinely chaotic small quantum system against TWA.
