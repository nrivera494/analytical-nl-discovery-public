---
id: R-0004
title: "Exact Raman energy-loss ratio of a sech pulse for the single-oscillator response, ρ = Re[(1 + i a/b){1 − s + (s²/2)ψ₁(1 + s/2)}] with s = (a − ib)T, with its inverse-cube long-pulse and linear short-pulse expansions and a two-term moment expansion with explicit remainder for any response"
claim: C-20261017-gpt-d-01
problem: P-20261016-claude-interactive-02
tier: promising
status: accepted
type: asymptotic-solution
proposer: gpt-d
proposer_model: gpt-6-astra
proposer_family: gpt
verifier: claude-interactive.8
verifier_family: claude
auditor: claude-interactive.8
auditor_family: claude
solver_commit: b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa
promoted: 2026-10-19
pi_score: null
gates:
  G1: met
  G2: met
  G3: met
  G4: met
  G5: met
  G6: open
  G7: met
  G8: open
---

# Exact Raman energy-loss ratio of a sech pulse

This result is claim C-20261017-gpt-d-01 as proposed. The cross-family audit passed it with no narrowing. It gives the tightness of the ceiling of [R-0003](../R-0003-raman-energy-loss-ceiling-and-retention/RESULT.md) for sech pulses of every width. It replaces that claim's refuted inverse-square law with the exact curve and its $T^{-3}$ asymptote.

## 1. Problem

Problem [P-20261016-claude-interactive-02](../../../problems/P-20261016-claude-interactive-02-long-wavelength-supercontinuum-budget.md) needs the rate at which Raman scattering removes energy, and hence red-shifts photons, for pulses of any duration. R-0003 bounds that rate for every field by $\kappa_UE^2$. This result gives the exact rate for a sech intensity, the shape of a fundamental soliton, from the long-pulse (Gordon) regime to the impulsive limit. It also gives a controlled long-pulse expansion for any Raman response.

## 2. Result

**Setting.** The scalar, lossless, photon-conserving shock GNLSE with constant $A_{\rm eff}$, as in R-0003, with:
- $I=|A|^2$, $E=\int I\,dt$;
- $\kappa_U=n_2f_Rk/(2cA_{\rm eff})$ with $k=h_R'(0^+)$;
- the normalized loss $\rho\equiv|dE/dz|/(\kappa_UE^2)\in[0,1]$.

At a plane where the intensity is
$$I(t)=\frac{E}{2T}\,{\rm sech}^2\frac{t-t_0}{T}$$
(any energy, any phase, any $t_0$; $T$ is the sech scale, and the intensity FWHM is $2\,{\rm arccosh}\sqrt2\,T\approx1.763\,T$), the following hold.

**(i) Exact ratio for the single oscillator.** Take $h_R(t)=\frac{a^2+b^2}{b}e^{-at}\sin bt$ for $t>0$, with $a=1/\tau_2$ (damping) and $b=1/\tau_1$ (resonance). Then $k=a^2+b^2$ and
$$\boxed{\;\rho(T)={\rm Re}\Big[\Big(1+i\frac ab\Big)\Big\{1-s+\frac{s^2}{2}\,\psi_1\Big(1+\frac s2\Big)\Big\}\Big],\qquad s=(a-ib)\,T,\;}$$
where $\psi_1$ is the trigamma function. With $r=\tau_1/\tau_2=a/b$ and $x=T/\tau_1$, $s=x(r-i)$. Equivalently, for any response,
$$\rho=\frac2k\int W(\Omega)\Big[\frac{\pi\Omega T/2}{\sinh(\pi\Omega T/2)}\Big]^2\frac{d\Omega}{2\pi},\qquad W=\Omega\,{\rm Im}\,\tilde h_R .$$

**(ii) Long pulses**, $x^{-1}\to0$ at fixed $r$:
$$\rho=\frac{16r}{15(1+r^2)^2}\,x^{-3}\Big[1+\frac{40(1-r^2)}{7(1+r^2)^2}\,x^{-2}+O_r(x^{-4})\Big].$$

**(iii) Short pulses**, $x\max(1,r)\to0$:
$$\rho=1-2rx+\frac{\pi^2(3r^2-1)}{12}\,x^2+2r(1-r^2)\,\zeta(3)\,x^3+O_r(x^4),$$
so $1-\rho=2T/\tau_2+O_r((T/\tau_1)^2)$.

**(iv) Any response.** Let $\mu_j=\int_0^\infty t^jh_R(t)\,dt$ and $\mu_{5,\rm abs}=\int_0^\infty t^5|h_R(t)|\,dt<\infty$. Then
$$\boxed{\;\rho=\frac{8\mu_1}{15kT^3}-\frac{16\mu_3}{63kT^5}+R,\qquad |R|\le\frac{16\,\mu_{5,\rm abs}}{225\,kT^7}.\;}$$
The leading equivalence $\rho\sim8\mu_1/(15kT^3)$ needs $\mu_1>0$. For the oscillator, $\mu_1=2a/(a^2+b^2)$ and $\mu_3/\mu_1=12(a^2-b^2)/(a^2+b^2)^2$, which reproduce (ii).

**Use.** Through R-0003's identity, $-dE/dz=\kappa_UE^2\rho(T)$ at that plane. When the photon number is conserved, the photon-mean frequency changes at $d\bar\omega/dz=-\bar\omega\,\kappa_UE\,\rho(T)$. The values of $r$ are:
- silica (Blow–Wood, $\tau_1=12.2$ fs, $\tau_2=32$ fs): $r=0.381$;
- the verifier's fluoride surrogate ($\tau_1=9.1$ fs, $\tau_2=40$ fs; assumed values, not sourced): $r=0.228$.

## 3. Regime of validity

| Dimensionless group | Definition | Lower bound | Upper bound | What fails outside |
|---|---|---|---|---|
| $x=T/\tau_1$ | Sech scale over inverse Raman resonance frequency | 0 | none | Exact at every $x$. (ii) needs $x\gg1$; (iii) needs $x\max(1,r)\ll1$ (the $\psi_1$ series converges for $\lvert s\rvert<2$) |
| $r=\tau_1/\tau_2$ | Damping over resonance frequency | 0 | none | The constants in (ii) and (iii) are not uniform as $r\to0$ or $r\to\infty$ |
| $\omega_0T$ | Carrier cycles per pulse | — | — | Not a hypothesis of the identity. At the 5 fs test points ($\omega_0T_0=1.9$ and 3.4) the envelope model is formal |

**Small parameters and error orders.**
- Long pulses: $x^{-1}$, with relative errors $O(x^{-2})$ after one term and $O(x^{-4})$ after two.
- Short pulses: $x$, with the error after $m$ terms $O(x^{m})$.
- The coefficients vanish at special points: the $x^2$ short coefficient at $r=1/\sqrt3$, and the long relative correction and the $x^3$ short coefficient at $r=1$. A fixed finite-window slope need not show the generic order near these points.

**Tested** (verifier): $7\times10^{-4}\le x\le600$ and $0.01\le r\le20$ for (i); GNLSE launches with FWHM 5–300 fs.

**Assumption ledger.**
- Scalar, single mode, deterministic, lossless.
- Constant $A_{\rm eff}$ and $n_2$, with the exact shock factor $\omega/\omega_0$; real dispersion.
- A real, causal, normalized response with $h_R(0^+)=0$ and $0<k<\infty$, with passive integrable $W$ and the sum rule of R-0003.
  - $h_R(0^+)=0$ is used twice: in the energy identity, where a nonzero value would add $h_R(0^+)\int I^2$, and in the integration by parts.
  - (i) and (iii) hold for the single oscillator only; (iv) holds for any response with a finite absolute fifth moment.
- The intensity is sech **at the plane of evaluation**.
  - The phase is arbitrary. Shape preservation during propagation is not assumed: a fission product need not stay sech.
  - The coefficients $8/15$, $16/63$ and $16/225$ belong to the sech shape; the generality of (iv) is in the response, not the pulse.
- Field regularity and decay for integration by parts. The identity needs no positive-frequency condition.
- **The single oscillator is a model of silica, not a calibration.** With the 13-mode Hollenbeck–Cantrell response and the same $f_R$, $\rho_{\rm HC}/\rho_{\rm BW}$ is:

  | $T$ | 5 fs | 10 fs | 100 fs | 300 fs | 1 ps |
  |---|---|---|---|---|---|
  | $\rho_{\rm HC}/\rho_{\rm BW}$ | 1.19 | 1.30 | 3.01 | 3.07 | 2.77 |

  (run `2026-10-17-claude-interactive.8-hc-relaxed`). A calibrated silica prediction must use the spectral form of (i) or (iv) with the measured response.

## 4. Derivation

Full proofs:
- the proposer's [proof note](../../../claims/notes/proof-2026-10-17-gpt-d-raman-sharpening.md), §§2–4;
- the verifier's independent derivation, §"Derivation check" of the [audit](../../../claims/notes/audit-2026-10-17-claude-interactive.8-C-20261017-gpt-d-01.md).

The crux:
1. **Energy identity in the time domain.** $-dE/dz=\frac{n_2f_R}{cA_{\rm eff}}\int_0^\infty h_R'(s)\,C(s)\,ds$, where $C(s)=\int I(t)I(t+s)\,dt$ is the intensity autocorrelation. Equivalently, $W$ is half the Fourier transform of $h_R'(\lvert t\rvert)$.
2. **The sech autocorrelation.** $C/E^2$ is the density of $T(U_1-U_2)$, where $U_1$ and $U_2$ are independent and have density ${\rm sech}^2u/2$. That density is $q(v)=(v\coth v-1)/\sinh^2v$ (in units of $T$).
3. **Laplace transform.** $\int_0^\infty e^{-sv}q(v)\,dv=\frac{1-s}{2}+\frac{s^2}{4}\psi_1(1+\frac s2)$.
   - gpt-d writes $q=\tfrac12(v\coth v)''$ and integrates by parts twice.
   - claude-interactive.8 uses the exponential series with a second-order subtraction anchored by $\int vq=\tfrac12$. Termwise integration without the subtraction is invalid: it gives $\int vq=0$.
   - With $h_R'(t)/k={\rm Re}[(1+ir)e^{-(a-ib)t}]$, $\rho=2\,{\rm Re}[(1+ir)L(s)]$, which is (i).
4. **(ii) and (iv).** Expand $\sin\Omega t$ under ${\rm Im}\,\tilde h_R$ with a Lagrange remainder and apply Parseval to derivatives of the normalized intensity $p$: $\int(p')^2=\frac{4}{15T^3}$, $\int(p'')^2=\frac{16}{21T^5}$ and $\int(p''')^2=\frac{64}{15T^7}$. The $1/(3s)$ term of $L$ contributes ${\rm Re}[i/x]=0$, so there is no $x^{-1}$ order.
5. **(iii).** Use $\psi_1(1+z)=\sum_k(-1)^k(k+1)\zeta(k+2)z^k$ for $\lvert z\rvert<1$. Equivalently, use the moments of $\lvert U_1-U_2\rvert$: $1$, $\pi^2/6$, $3\zeta(3)$ and $\pi^4/10$. Expanding at high frequency under the spectral integral would be invalid.

**Gate G2 is met:** a second family (claude) rederived every step before reading the proposer's note. The two routes differ only in how the Laplace transform is evaluated. The verifier's library, `ramanlib.py` (mpmath at 40 digits), reproduces each identity numerically.

**Gate G3 is met:**
- units: $\rho$ is dimensionless;
- invariance under energy scaling, phase and time translation;
- the limits $\rho\to1$ ($T\to0$) and the Gordon $T^{-3}$ law ($T\to\infty$);
- the Laplace transform against quadrature to $2.7\times10^{-32}$ (run `2026-10-17-claude-interactive.8-sech-tightness`).

## 5. Validation against numerics

All numbers in this section are from the verifier claude-interactive.8 (family claude), unless marked as proposer checks.

| Label | Run id |
|---|---|
| S | `2026-10-17-claude-interactive.8-sech-tightness` (closed form, exponents, GNLSE launch planes) |
| C | `2026-10-17-claude-interactive.8-concentration` (propagation data and the second-solver check) |
| H | `2026-10-17-claude-interactive.8-hc-relaxed` (Hollenbeck–Cantrell response) |
| M | `2026-10-17-gpt-d-raman-sharpening` (proposer's checks, gpt-d) |

The verifier froze its held-out points and tolerances in commit f784fed before any check ran.

![GNLSE launch-plane rho against the closed form](../../../runs/2026-10-17-claude-interactive.8-sech-tightness/fig_summary.png)
*Figure 1. $\rho=|dE/dz|/(\kappa_UE^2)$ from the nonlinear right-hand side of the verifier's own photon-conserving GNLSE at the launch plane of 16 sech pulses, FWHM 5–300 fs (circles; open = held out).*
- *Curves: the closed form (i) for the SMF-28 surrogate ($r=0.381$) and the fluoride surrogate ($r=0.228$).*
- *Dashed: the leading long- and short-pulse terms of (ii) and (iii) at $r=0.381$.*
- *Run S. The verifier's solver is its own code (no solver commit); the second-solver check against the agents' solver at commit b9fa957 is in run C.*

**Exact formula** (run S).
- Against two independent quadratures, at 48 held-out points ($r\in\{0.1,0.2275,0.45,1,2.5,5\}$, $7\times10^{-4}\le x\le600$), the maximum relative difference is:
  - spectral quadrature: $3.3\times10^{-25}$;
  - autocorrelation quadrature: $2.2\times10^{-25}$, at the 36 points with $x\le33$.
- At $r=0.01$ and $r=20$: $5\times10^{-28}$.

**Error-scaling exponents** (run S).

| Quantity | Window | Measured slope | Predicted |
|---|---|---|---|
| Long-pulse decay | $x\in[50,400]$ | $-3.0009$ to $-2.9999$ | $-3$ |
| Leading relative error, $r\ne1$ | $x\in[50,400]$ | $-2.0004$ to $-1.9999$ | $-2$ |
| Leading relative error, $r=1$ | $x\in[50,400]$ | $-3.999999$ | $-4$ (correction vanishes) |
| Two-term relative error | $x\in[50,400]$ | $-3.9989$ to $-4.0010$ | $-4$ |
| Short pulses, $(1-\rho)/(2rx)-1$ | $x\in[10^{-4},10^{-2}]$ | 0.9914 to 0.99998 | 1 |
| Cubic residual, $r\ne1$ | $x\in[10^{-4},10^{-2}]$ | 2.9926 to 3.0028 | 3 |
| Cubic residual, $r=1$ | $x\in[10^{-4},10^{-2}]$ | 3.9976 | 4 ($c_3=0$) |
| Quartic residual | $x\in[10^{-4},10^{-2}]$ | 3.993 to 4.001 | 4 |

The $C_3$ extrapolations match within $7.4\times10^{-13}$.

**General remainder (iv)** (run S). The bound holds at all 9 test points ($r\in\{0.2275,1,5\}$, $x\in\{3,10,30\}$). $R$ reaches 0.9985 of the bound at $r=5$, so the bound is nearly tight for a nearly one-signed $h_R$.

**GNLSE** (runs S and C).
- At the launch plane, the RHS equals the closed form for 16 sech launches (5–300 fs, SMF-28 and fluoride surrogates, 11 held out) to $1.7\times10^{-11}$ relative.
- A Richardson estimate of $dE/dz$ from real propagation agrees to $4.1\times10^{-9}$.
- With a sampled kernel instead of the exact transfer function, the difference is $8.1\times10^{-6}$ and $2.3\times10^{-5}$ at $dt=2.5$ fs, and $7.9\times10^{-4}$ and $2.2\times10^{-3}$ at $dt=7.5$ fs.
- The agents' solver (b9fa957) reproduces $E(z)$ of the $N=3$, 100 fs case within $3.2\times10^{-15}$ at 101 planes (run C).

**Propagated fundamental solitons** (run S, using C's raw data). $\rho(z)$ divided by the closed form at the instantaneous width $T_{\rm eff}=1/(3Q)$ stays in:
- $[0.991,1.056]$ for 30 fs, while the soliton reshapes and shifts;
- $[0.999998,1.0010]$ for 300 fs.

**Relaxed assumption** (run H, Hollenbeck–Cantrell response). The closed form does not apply, as stated. The moment expansion (iv) survives:
- slopes $-1.962$ and $-4.110$ over $600\le T\le3000$ fs;
- the remainder bound holds at all 10 widths from 150 fs to 3 ps.

It is only asymptotic: the two-term relative error is $-0.42$ at 150 fs.

**Proposer's checks** (gpt-d, family gpt, run M).
- Closed form against quadrature: $7.83\times10^{-16}$.
- Silica exponents: decay 3.00158; leading and corrected relative-error exponents 2.00170 and 4.00091.
- Coefficients: $C_3$ 0.30999923 extrapolated against 0.30999947 exact; the short coefficient 0.762500043 against the exact $2r=0.7625$.
- Direct GNLSE RHS: $9.05\times10^{-12}$.

**Retained failure.** One frozen proposer tolerance failed: at $r=0.6$ the linear short residual had slope 2.08200, outside $2\pm0.08$ (run M). The verifier traced it to the fit window near the $r=1/\sqrt3$ cancellation:
- the gap-ratio slope is 1.080 for $x\in[0.002,0.016]$ and 1.0005 for $x\in[10^{-5},10^{-4}]$;
- at $r=1/\sqrt3$ it is 1.9986, as predicted, since $c_2=0$ (run S, `summary_cancellation.json`).

The failure is a finite-window effect, not an error in (iii).

## 6. Adversarial audit

[audit-2026-10-17-claude-interactive.8.md](audit/audit-2026-10-17-claude-interactive.8.md): claude-interactive.8 (family claude, model claude-opus-5-5); proposer gpt-d (family gpt). **Verdict: pass, no blockers, no narrowing.**

**Clean context.** By the report's own description, before its commit (6320014) the auditor read only:
- the two claim cards (C-20261017-gpt-d-01 and -02);
- the problem card;
- `evaluator/`, and the solver documentation and source;
- the `config.yaml`, `meta.yaml` and `summary.json` of the four gpt-d runs the cards cite.

It did not read gpt-d's proof note, audit notes, logs, `docs/summary-*` files, PR description or scripts, and all its code is its own. The held-out predictions were frozen in f784fed. **G5 is met.**

**Attacks.**
- an independent derivation;
- two quadratures at frozen held-out points;
- the edge of regime ($r=0.01$, $r=20$);
- six error exponents, including the $r=1$ cancellation. The $r=1/\sqrt3$ case was checked after the audit commit, in the post-audit note;
- the general remainder bound;
- GNLSE launch planes and real propagation;
- sampled-kernel artefacts;
- a second solver;
- a relaxed response;
- prior work;
- fine-tuning: none needed.

**Non-blocking concerns.**
1. For silica, the Blow–Wood closed form misestimates $\rho$ by up to a factor of 3 against Hollenbeck–Cantrell.
2. Novelty is limited (section 7).
3. The shortest test points have $\omega_0T\approx1.9$–3.4, so the short-pulse limit is formal model sharpness.

## 7. Novelty

Two families searched:
- gpt-d (gpt), run `2026-10-17-gpt-d-raman-literature`;
- claude-interactive.8 and its subagent claude-interactive.8.1 (claude), audit §"Prior work".

| Source | Access | What it has |
|---|---|---|
| Chen, Wang, Hou, Antonio-Lopez, Amezcua-Correa, Xu & Wise, arXiv:2603.21734, Eq. (2) | §3 of v2 full text (claude-interactive.8.1); abstract (claude-interactive.8) | An exact sech-ansatz time kernel for arbitrary response. It equals $\frac{15}{4}(-q'(u))$, the autocorrelation kernel of step 2, to $2\times10^{-35}$ (run S). **The exact integral representation is prior work.** |
| Huang et al., arXiv:2607.05244 | full text, energy sections (gpt-d, v1; claude-interactive.8, current version) | The leading inverse-cube energy law: Eq. (18) in v1, Eq. (17) in the current version. No all-width form, no polygamma, no bound |
| Gordon 1986, DOI 10.1364/OL.11.000662 | abstract only; secondary account in DOI 10.1109/JSTQE.2008.915526, full text (claude-interactive.8.1) | An all-width integral over the Raman gain spectrum |
| Chen, Taylor & Efimov 2010, DOI 10.1364/JOSAB.27.001022 | abstract only | Full gain spectrum, arbitrary durations |
| Herrmann & Nazarkin 1994, DOI 10.1364/OL.19.002065 | abstract only (both families) | A short-pulse frequency-shift rate $\propto1/T$, consistent with $\rho\to1$ |
| Nie et al., arXiv:2511.04013 | full text (claude-interactive.8.1; gpt-d) | An approximate non-adiabatic oscillator formula without special functions |

**Not found in either search:**
- the trigamma closed form (i);
- the short-pulse coefficients of (iii), including $1-\rho\simeq2T/\tau_2$;
- the two-term moment expansion with explicit remainder (iv).

Searches included "self-frequency shift" with trigamma, polygamma, digamma or Hurwitz zeta, and sech with the full Raman response and saturation.

**G6 is open.** Herrmann & Nazarkin (the short-pulse coefficient) and Gordon (the all-width integral) were read only at abstract level, so the difference from them cannot yet be stated. T-20261017-gpt-d-04 covers this. Novelty is at most the closed-form evaluation and the expansion coefficients.

## 8. Experimental test

- **Measurement.**
  - Launch near-sech pulses of known width $T$ and energy $E$ (fundamental solitons are the natural choice) into a fibre segment short enough that the width changes little.
  - Measure the energy loss, or the photon-mean-frequency shift, per unit length. Then $\rho_{\rm meas}=|\Delta E/\Delta z|/(\kappa_UE^2)$, or equivalently $|\Delta\bar\omega/\Delta z|/(\bar\omega\,\kappa_UE)$ for a fundamental soliton.
  - Do this over $T$ from well above to near $\tau_1$ (about 10–300 fs).
- **Prediction.**
  - For any fibre, $\rho(T)$ follows the spectral form of (i) with the measured Raman response, and approaches $8\mu_1/(15kT^3)$ at long widths.
  - For a fibre whose response is well described by one damped oscillator, $\rho(T)$ follows the trigamma curve, which crosses from $C_3(\tau_1/T)^3$ to $1-2T/\tau_2$. A fluoride fibre is the better candidate; the test's fluoride parameters are a surrogate.
- **Falsification.**
  - A measured $\rho(T)$ that departs from the spectral form computed with the measured response, beyond the uncertainty in $\kappa_U$, $T$ and the pulse shape.
  - Or a long-pulse exponent different from $-3$, which is $-4$ for the frequency-shift rate of fundamental solitons, since $E\propto1/T$.

  The closed form is an identity within the oscillator model, so a mismatch with it alone falsifies the model of the fibre, not the algebra.

## 9. Open questions

- **G6** (Herrmann & Nazarkin and Gordon full texts, exact-overlap citations): T-20261017-gpt-d-04.
- **A calibrated silica prediction** with a measured multiband response: T-20261017-gpt-d-05; the Hollenbeck–Cantrell amplitude convention, T-20261017-claude-interactive.8-02.
- **The short-pulse regime with a carrier-resolved model** and a sourced broadband response: T-20261016-gpt-d-06.
- **G8 is open**: nothing is formalized. The trigamma identity needs Mathlib's special-function support. Task: T-20261019-claude-interactive.15-03.
