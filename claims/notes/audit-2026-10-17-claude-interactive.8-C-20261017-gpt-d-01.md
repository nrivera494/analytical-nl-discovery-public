---
agent: claude-interactive.8
model: claude-opus-5-5
family: claude
claim: C-20261017-gpt-d-01
task: T-20261017-gpt-d-02
date: 2026-10-17
status: complete
verdict: pass
---

# Independent verification and audit: exact sech Raman loss ratio

**Verdict: pass.** The closed form, both asymptotic expansions with their error orders, and the
general-response moment expansion with its remainder bound are correct. I rederived each one and
checked it with my own code, at held-out points frozen before any check ran (commit f784fed). The
GNLSE launch-plane checks also pass. No blocker. The non-blocking concerns are model calibration for
real silica and the limited novelty of the exact integral representation.

Clean context: before this report was committed I read only the two claim cards, the problem card
P-20261016-claude-interactive-02, `evaluator/`, the solver documentation and source, and the
`config.yaml`, `meta.yaml` and `summary.json` of the four gpt-d runs the cards cite. I did not read
gpt-d's proof note, audit notes, logs, `docs/summary-*` files, PR description or scripts. All code
used here is my own.

Runs: S = `2026-10-17-claude-interactive.8-sech-tightness`; C = `2026-10-17-claude-interactive.8-concentration`
(propagation, Julia cross-check); H = `2026-10-17-claude-interactive.8-hc-relaxed`.

## Restatement and assumptions

For an intensity $I=E\,\mathrm{sech}^2(t/T)/(2T)$ at one plane of the lossless, constant-$A_{\rm eff}$,
photon-conserving shock GNLSE with the oscillator $h=(a^2+b^2)e^{-at}\sin(bt)/b$, the normalized loss
$\rho=|dE/dz|/(\kappa_UE^2)$ equals $\mathrm{Re}[(1+ir)\{1-s+\tfrac{s^2}{2}\psi_1(1+\tfrac s2)\}]$,
with $s=x(r-i)$, $r=\tau_1/\tau_2=a/b$ and $x=T/\tau_1$. It has a long-pulse expansion in $x^{-2}$,
a short-pulse Taylor expansion in $x$, and, for any response, a two-term moment expansion with an
explicit remainder.

The assumptions are the card's. I add three that it states only implicitly:
- $h(0^+)=0$ is used twice: in the energy identity, where a nonzero $h(0^+)$ would add $h(0^+)\int I^2$, and in the integration by parts behind the spectral form. The card lists it under regularity.
- The moment expansion's coefficients $8/15$, $16/63$, $16/225$ hold for the sech intensity only. Its generality is in the response, not the pulse shape.
- The identity needs no positive-frequency condition. It holds formally even when the spectrum reaches $\omega<0$, as at my 5 fs points.

## Derivation check (independent)

1. **Energy identity.** From $\partial_zA=iDA+i\gamma(1+\tfrac{i}{\omega_0}\partial_t)[AV]$, the dispersion and the instantaneous Kerr terms drop out of $dE/dz$. This leaves
   $dE/dz=-\frac{n_2f_R}{cA_{\rm eff}}\int_0^\infty h'(s)C(s)\,ds$, with $C$ the intensity autocorrelation.
   - Spectrally this is $-\frac{n_2f_R}{cA_{\rm eff}}\int W|\tilde I|^2\frac{d\Omega}{2\pi}$, with $W=\Omega\,\mathrm{Im}H$. This holds because the Fourier transform of $h'(|t|)$ is $2W$.
   - The sum rule $\int W\,d\Omega/2\pi=h'(0^+)/2$ gives $\rho\le1$.
   - The identity agrees with the card.
2. **Sech autocorrelation.** $C/E^2$ is the density of $T(U_1-U_2)$, where $U$ has density $\mathrm{sech}^2u/2$ (a logistic law with scale 1/2). Its density is $q(v)=(v\coth v-1)/\sinh^2v$, with $q(0)=1/3$ and $q''(0)=-4/15$. This agrees with the card.
3. **Laplace transform.** I expanded $q=4\sum_n(vn^2-n)e^{-2nv}$.
   - Termwise integration is not valid. The partial sums carry a spike at $v\to0$ that contributes at order $s$. Integrated termwise, the series gives $\int vq=0$, although $q>0$.
   - Subtracting through second order, $\int(e^{-sv}-1+sv)q$, is legitimate. Combined with $L(0)=1/2$ and $L'(0)=-\tfrac12E|U_1-U_2|=-\tfrac12$ (the logistic Gini mean difference is $2\sigma=1$), it gives $L(s)=\tfrac{1-s}{2}+\tfrac{s^2}{4}\psi_1(1+\tfrac s2)$. This is the card's formula.
   - The large-$s$ expansion reproduces $q(0)/s+q''(0)/s^3$.
   - With $h'(t)/k=\mathrm{Re}[(1+ir)e^{-(a-ib)t}]$ and $\rho=2\,\mathrm{Re}[(1+ir)L(s)]$, the boxed formula follows.
4. **Short pulses.** $\psi_1(1+z)=\sum_k(-1)^k(k+1)\zeta(k+2)z^k$ converges for $|s|<2$. It gives $\rho=1-2rx+\frac{\pi^2(3r^2-1)}{12}x^2+2r(1-r^2)\zeta(3)x^3+O(x^4)$, identical to the card.
5. **Long pulses.** I expanded $\sin\Omega t$ under $\mathrm{Im}H$ with the Lagrange remainder and applied Parseval: $\int(p')^2=4/(15T^3)$, $\int(p'')^2=16/(21T^5)$, $\int(p''')^2=64/(15T^7)$.
   - This gives $8\mu_1/(15kT^3)-16\mu_3/(63kT^5)$, with $|R|\le16\mu_{5,\rm abs}/(225kT^7)$, identical to the card.
   - For the oscillator, $\mu_1=2a/(a^2+b^2)$ and $\mu_3/\mu_1=12(a^2-b^2)/(a^2+b^2)^2$. These give the card's $16r/[15(1+r^2)^2]$ and $40(1-r^2)/[7(1+r^2)^2]$.
   - Independently, the $1/(3s)$ term of $L$ contributes $\mathrm{Re}[i/x]=0$, so the $x^{-1}$ order vanishes identically.

Difference from the card's derivation sketch: none in substance. My route to the Laplace transform
(series with second-order subtraction, fixed by the first moment) may differ from the proposer's.
The card's warning against expanding at high frequency under the spectral integral is consistent with my
step 4, which expands the closed form instead.

## Attacks

| Attack | Result | Run |
|---|---|---|
| Laplace transform and moment of $q$ by quadrature | 5 complex $s$ agree to $2.7\times10^{-32}$; $\int_0^\infty vq=0.5$ | S |
| Closed form vs two independent quadratures (spectral, positive integrand; autocorrelation) at 48 frozen held-out points, $r\in\{0.1,0.2275,0.45,1,2.5,5\}$, $x\in[7\times10^{-4},600]$ | max relative difference $3.3\times10^{-25}$ (spectral, all 48) and $2.2\times10^{-25}$ (autocorrelation, the 36 points with $x\le33$; tolerance $10^{-9}$) | S |
| Edge of regime $r=0.01$ and $r=20$, $x\in\{0.01,1,100\}$ | $5\times10^{-28}$ | S |
| Long-pulse exponents, $x\in[50,400]$ | decay $-3.0009$ to $-2.9999$; leading relative error $-2.0004$ to $-1.9999$ for $r\ne1$; at $r=1$, $-3.999999$; two-term error $-3.9989$ to $-4.0010$; $C_3$ extrapolations within $7.4\times10^{-13}$. All within the frozen tolerances | S |
| Short-pulse exponents, $x\in[10^{-4},10^{-2}]$ | $(1-\rho)/(2rx)-1$: $0.9914$ to $0.99998$; cubic residual: $2.9926$ to $3.0028$ ($r\ne1$), $3.9976$ at $r=1$ ($c_3=0$); quartic residual: $3.993$ to $4.001$; measured $c_3$ matches within $4\times10^{-4}$. All pass | S |
| General remainder bound, oscillator $r\in\{0.2275,1,5\}$, $x\in\{3,10,30\}$ | holds at all 9 points; $R$/bound up to $0.9985$ at $r=5$, so the bound is nearly tight for a nearly one-signed $h$ | S |
| GNLSE nonlinear RHS at the sech launch plane, 16 launches, FWHM 5–300 fs, SMF-28 and fluoride surrogates (11 held out) | max relative difference $1.7\times10^{-11}$ (tolerance $10^{-6}$) | S |
| Real short propagation: Richardson $dE/dz$ from $E(h),E(2h),E(4h)$ | max relative difference $4.1\times10^{-9}$ (tolerance $10^{-4}$) | S |
| Raman kernel sampled instead of exact transfer | $8.1\times10^{-6}$ and $2.3\times10^{-5}$ at $dt=2.5$ fs; $7.9\times10^{-4}$ and $2.2\times10^{-3}$ at $dt=7.5$ fs | S |
| Solver self-test | NLSE soliton shape error $7.2\times10^{-9}\to4.5\times10^{-10}$ on halving the step (order 4); photon drift $4.4\times10^{-9}$ for $N=3$ with Raman; identity residual $1.6\times10^{-12}$ | S |
| Second solver (agents' copy b9fa957), N=3 100 fs case | $E(z)/E_0$ equal to my sampled-kernel run within $3.2\times10^{-15}$ at 101 planes | C |
| Propagated $N=1$ solitons: $\rho(z)$ against the closed form at $T_{\rm eff}=1/(3Q)$ | 30 fs: ratio in $[0.991,1.056]$ while the soliton reshapes and shifts; 300 fs: $[0.999998,1.0010]$ | S (uses C raw data) |
| Relaxed assumption: 13-mode Hollenbeck–Cantrell response | see below | H |
| Prior work | see below | — |

One check was rerun after a bug in my own code: the first short-pulse execution used the wrong
sign for the $c_2x^2$ subtraction and reported slope 2. I fixed the sign and reran without changing
the frozen prediction.

**Relaxed assumption (HC multi-peak silica response, run H).** I used amplitudes $A_i$, as gnlse-python
and Luna.jl do, and also tried $A_i/\omega_i$.
- **Exact formula.** The closed form does not apply; it is oscillator-specific, as the card says.
- **Moment expansion.** It survives:
  - leading relative error slope $-1.962$ and two-term slope $-4.110$ over $600\le T\le3000$ fs;
  - remainder bound satisfied at all 10 widths from 150 fs to 3 ps;
  - the expansion is only asymptotic there: the two-term relative error is $-0.42$ at 150 fs.
- **Short-pulse gap.** It generalizes as $1-\rho\simeq-h''(0^+)T/k$. The ratio is $1.023$ at $T=0.02$ fs and tends to 1. This is my extension, not part of the claim.
- **Quantitative silica prediction.**
  - With the same $f_R$, HC gives $\rho_{\rm HC}/\rho_{\rm BW}=1.19$ at $T=5$ fs, $1.30$ at 10 fs, $3.01$ at 100 fs, $3.07$ at 300 fs and $2.77$ at 1 ps.
  - $h'(0^+)$ itself differs, $4.75\times10^{27}$ against $7.70\times10^{27}$ s⁻², so $\kappa_U$ is response-dependent.
  - The Blow–Wood closed form is therefore not a calibrated silica prediction beyond about 10 fs.

**Prior work.**
- arXiv:2607.05244 (Huang et al.):
  - Eq. (17) of the current version gives $E'=-4\tau_R\epsilon_\omega E^2/(15\rho^3)$ in the first-moment $T_R$ approximation, which equals the claimed leading law.
  - It contains no all-duration form, no polygamma function and no bound.
  - Access: full text, HTML, read by me with targeted extraction; the main body of v1 and v2 was read in full by my literature subagent claude-interactive.8.1.
- arXiv:2603.21734 (Chen, Wang, Hou, Antonio-Lopez, Amezcua-Correa, Xu, Wise):
  - Eq. (2) gives an exact sech-ansatz time kernel for arbitrary $R$. Its $\tau_0\to0$ limit, Eq. (3c), is the $\kappa_UE^2$ ceiling without the dephasing correction.
  - The kernel as transcribed, $B=\frac{15}{8}\mathrm{csch}^4u\,[4u+2u\cosh2u-3\sinh2u]$, equals $\frac{15}{4}(-q'(u))$ to $2\times10^{-35}$ (run S). It is the same autocorrelation kernel as the claim's derivation.
  - Access: §3 of v2 read in full by subagent claude-interactive.8.1; the abstract by me.
- The exact integral representation is therefore prior work. Gordon, DOI 10.1364/OL.11.000662, also has an all-width integral over the gain spectrum: abstract only, plus a secondary account in DOI 10.1109/JSTQE.2008.915526 (full text, subagent).
- Chen, Taylor and Efimov, DOI 10.1364/JOSAB.27.001022 (abstract only): full gain spectrum, arbitrary durations.
- Herrmann and Nazarkin, DOI 10.1364/OL.19.002065 (abstract only): a short-pulse shift $\propto1/T$, independent of the molecular frequency, consistent with $\rho\to1$.
- Nie et al., arXiv:2511.04013 (full text, subagent): an approximate non-adiabatic oscillator formula with no special functions.
- No source found gives the trigamma closed form or the short-pulse coefficients.
- Searches by the subagent: "self-frequency shift" with trigamma, polygamma, digamma or Hurwitz zeta; sech with full Raman response and saturation; plus direct reads of the Optica abstract pages listed.

**Fine-tuning.** None. The $r=1/\sqrt3$ and $r=1$ cancellations are special points of the error terms, not requirements.

## Blockers

None.

## Non-blocking concerns

1. **Calibration.** For real silica the Blow–Wood closed form misestimates $\rho$ by up to a factor of 3 against HC (run H). A measurable silica prediction should use the general-response quadrature, or the moment expansion with measured $\mu_j$, and a measured $h'(0^+)$.
2. **Novelty.** It is limited to the closed-form evaluation and the explicit expansion coefficients. The exact sech integral for arbitrary response (arXiv:2603.21734 Eq. 2) and the leading law (arXiv:2607.05244 Eq. 17) are published.
3. **Short-pulse regime.** It is formal model sharpness, as the card states. My 5 fs points have $\omega_0T_0=1.9$–3.4.

## Regime I sign off on

As stated on the card: the exact identity for $0<x<\infty$ and $0<r<\infty$, tested on
$7\times10^{-4}\le x\le600$ and $0.01\le r\le20$; long asymptotics as $x^{-1}\to0$ at fixed $r$; short asymptotics as $x\max(1,r)\to0$; within the single-oscillator, constant-$A_{\rm eff}$, lossless
photon-conserving model. No narrowing needed.

## Post-audit note (after commit 6320014)

After the report above was committed, I read gpt-d's proof note
(`claims/notes/proof-2026-10-17-gpt-d-raman-sharpening.md`). It changes nothing in the verdict.
- **Laplace transform.** gpt-d writes $g=\tfrac12(u\coth u)''$ and integrates by parts twice, so the exponential series is integrated only after multiplication by $u$. My route uses the series with a second-order subtraction anchored by $\int vq=1/2$. Same result.
- **Short-pulse coefficients.** gpt-d takes them from the moments of $|U-V|$ ($1$, $\pi^2/6$, $3\zeta(3)$, $\pi^4/10$). I took them from the Taylor series of $\psi_1$. Same coefficients.
- **Retained finite-window failure.** I confirmed its explanation independently (run S, `summary_cancellation.json`):
  - at $r=0.6$ the gap-ratio slope is $1.080$ in $x\in[0.002,0.016]$ and $1.0005$ in $[10^{-5},10^{-4}]$;
  - at $r=1/\sqrt3$ it is $1.9986$, since $c_2=0$.
  - So the proposer's 2.082 residual slope is a pre-asymptotic window effect near the cancellation, not an error in the expansion.
