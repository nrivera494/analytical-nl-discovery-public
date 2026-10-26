---
id: R-0005
title: "Arctangent Raman energy-loss ceiling: for the single-oscillator response every field obeys −dE/dz ≤ κ_U E² (2/π) arctan(π τ₂ Q/2), with Q = ∫I²dt/E² ≤ P_max/E, sharper than both the energy-only and the peak-power ceilings; a cap on Q along the fibre gives a sharper retention bound"
claim: C-20261017-gpt-d-02
problem: P-20261016-claude-interactive-02
tier: promising
status: accepted
type: bound
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

# Arctangent Raman energy-loss ceiling from intensity concentration

This result is claim C-20261017-gpt-d-02 as proposed. The cross-family audit passed it with no narrowing. It sharpens the energy-only ceiling of [R-0003](../R-0003-raman-energy-loss-ceiling-and-retention/RESULT.md) for the single-oscillator Raman response, using one more measurable number of the pulse: its intensity concentration, or its peak power.

## 1. Problem

Problem [P-20261016-claude-interactive-02](../../../problems/P-20261016-claude-interactive-02-long-wavelength-supercontinuum-budget.md) needs a ceiling on Raman energy loss, equivalently on the red shift of the photon mean, closed by a controlled bound on peak power or concentration along the fibre. R-0003 bounds the loss rate using the energy alone. This result bounds it using the energy and the concentration $Q=\int I^2dt/E^2$. It is a conditional improvement: it does not supply the a-priori cap on $Q(z)$ that would close the problem's gap.

## 2. Result

**Setting.** The model of R-0003: scalar, lossless, photon-conserving shock GNLSE, constant $A_{\rm eff}$, real dispersion. The response is the normalized single oscillator
$$h_R(t)=\frac{a^2+b^2}{b}e^{-at}\sin bt\quad(t>0),\qquad a=1/\tau_2,\ b=1/\tau_1,\qquad \kappa_U=\frac{n_2f_R(a^2+b^2)}{2cA_{\rm eff}} .$$
Define $I=|A|^2$, $E=\int I\,dt>0$, and the intensity concentration
$$Q=\frac{\int I^2\,dt}{E^2}\quad(\text{inverse time; }Q=1/(3T)\text{ for a sech}^2\text{ of scale }T),$$
with $Q\le P_{\max}/E$ for peak power $P_{\max}$.

**Statement.** At every plane,
$$\boxed{\;0\le-\frac{dE}{dz}\le\kappa_UE^2\,F(Q),\qquad F(Q)=\frac2\pi\arctan\Big(\frac{\pi\tau_2Q}{2}\Big)<\min(1,\ \tau_2Q).\;}$$
1. **Peak-power form.** Since $F$ is increasing, $-dE/dz\le\kappa_UE^2F(P_{\max}/E)$. This needs only the energy and the peak power.
2. **Comparison.**
   - The energy-only ceiling of R-0003 is $F\le1$.
   - The peak-power, sup-weight bound is $\rho\le\tau_2P_{\max}/E$, since $\sup W=k\tau_2/2$ for the oscillator. It is in gpt-b's internal review.
   - $F$ is strictly below both for every finite $Q>0$.
3. **Conditional retention.** If a separately justified cap $Q(z)\le Q_*$ holds on $[0,L]$, then
   $$\frac{E(L)}{E_0}\ \ge\ \frac{1}{1+\kappa_UE_0L\,F(Q_*)}.$$
   Without such a cap, integrating the measured $F(Q(z))$ gives an along-trajectory comparison, not a prediction from the launch.
4. **Properties of $F$.**
   - $F$ is independent of $\tau_1$.
   - $F=\tau_2Q+O((\tau_2Q)^3)$ as $\tau_2Q\to0$, and $1-F=4/(\pi^2\tau_2Q)+O((\tau_2Q)^{-3})$ as $\tau_2Q\to\infty$.
5. **Sharpness.**
   - $F$ is the exact maximum of the relaxed spectral problem: maximize $\int Wf$ over $0\le f\le1$ with $\int f\,d\Omega/2\pi=Q$, where $f=|\tilde I|^2/E^2$.
   - The maximizer fills two bands, $\Omega_-\le|\Omega|\le\Omega_+$ with $\Omega_+\Omega_-=a^2+b^2$ and $\Omega_+-\Omega_-=\pi Q$. It has a hole at $\Omega=0$, so it is not the spectrum of any intensity, which has $f(0)=1$.
   - Numerically, non-negative intensities approach the bound only as $\tau_2Q\to\infty$. At $r=\tau_1/\tau_2=0.381$, the best intensities found reach $0.52F$ for $\tau_2Q\le0.3$, $0.62F$ at $\tau_2Q=1$, $0.89F$ at 3 and $0.98F$ at 10 (run `2026-10-17-claude-interactive.8-concentration`).

## 3. Regime of validity

| Dimensionless group | Definition | Lower bound | Upper bound | What fails outside |
|---|---|---|---|---|
| $\tau_2Q$ | Raman damping time over the effective pulse duration | 0 (exclusive) | none | — |
| $r=\tau_1/\tau_2$ | Resonance over damping time | 0 (exclusive) | none | — |
| $\kappa_UE_0L$ | Ceiling strength over the fibre | 0 | none | The retention corollary also needs the cap $Q\le Q_*$ |
| Number of Raman bands | — | 1 | 1 | With a multi-band response (silica, Hollenbeck–Cantrell) the arctangent fails for strongly concentrated intensities: see the ledger. The numerical bathtub bound $F_W$ still holds |

**Small parameter.** None: the statement is an exact inequality within the model.

**Tested:**
- the bathtub value: $0.003\le\tau_2Q\le300$ at $r\in\{0.381,2\}$ (verifier) and $10^{-3}\le\tau_2Q\le10^2$ (proposer);
- profiles and the optimizer at $r\in\{0.2275,0.381,2\}$;
- propagation up to $\kappa_UE_0L=15.4$ (run `2026-10-17-claude-interactive.8-concentration`).

**Assumption ledger.**
- Everything in R-0003's ledger: scalar, single mode, deterministic, lossless, constant $A_{\rm eff}$ and $n_2f_R$, the exact shock factor, real dispersion, regularity, and positive optical support for photon statements.
- **The single damped oscillator.** The single-interval level sets of $W$ use its form. The closed arctangent is not claimed for other responses.
  - Under the 13-mode Hollenbeck–Cantrell silica response, with the Blow–Wood $\tau_2=32$ fs, optimized positive intensities exceed $F$:
    - by 1.9% at $\tau_2Q=2.5$ (effective duration 12.8 fs);
    - by 4.0% at $\tau_2Q=5$ (6.4 fs).
  - A sech exceeds it by up to 2.5% at $T\approx1.7$ fs.
  - With the matched $\tau_{2,\rm eff}=(2/k)\sup W=52.1$ fs, $F_W/F$ reaches 1.080 (run `2026-10-17-claude-interactive.8-hc-relaxed`).
- **Non-negative intensity**, $I\in L^1\cap L^2$. Positivity is used once, for $f\le1$. $W\ge0$ is used only for the lower bound $0\le-dE/dz$.
- **The cap $Q(z)\le Q_*$** is an extra hypothesis of the retention corollary. Neither $Q$ nor $P_{\max}$ is conserved or monotone. In the verifier's frozen fission launches, the largest $Q$ along the fibre was 2.6 to 4.5 times its launch value. In its two post-freeze 30 fs launches it was 1.9 and 1.6 times (run `2026-10-17-claude-interactive.8-concentration`).

## 4. Derivation

Full proofs:
- the proposer's [proof note](../../../claims/notes/proof-2026-10-17-gpt-d-raman-sharpening.md), §5;
- the verifier's independent check, §"Restatement and assumptions" of the [audit](../../../claims/notes/audit-2026-10-17-claude-interactive.8-C-20261017-gpt-d-02.md).

The crux:
1. **The relaxed problem.** By R-0003, $\rho=|dE/dz|/(\kappa_UE^2)=\frac2k\int W f\,\frac{d\Omega}{2\pi}$ with $f=|\tilde I|^2/E^2$. Positivity gives $0\le f\le1$. Parseval gives $\int f\,d\Omega/2\pi=Q$.
2. **Bathtub.** Over this class, $\int Wf$ is maximized by the indicator of the super-level set of $W$ with measure $2\pi Q$.
3. **Level sets.** For $\Omega\ne0$, $W=2a\omega_0^2/[(\Omega-\omega_0^2/\Omega)^2+4a^2]$ with $\omega_0^2=a^2+b^2$. So $W$ depends only on $u=\Omega-\omega_0^2/\Omega$, which is monotone on each half-line, and $W$ decreases in $\lvert u\rvert$. Each super-level set is therefore one band per side, $[\Omega_-,\Omega_+]$, with $\Omega_+\Omega_-=\omega_0^2$ and width $c=\Omega_+-\Omega_-=\pi Q$. This step is the verifier's; the proposer's note states the level sets without proving unimodality.
4. **Integration.** $\frac{d}{dc}\frac1\pi\int_{\Omega_-}^{\Omega_+}W\,d\Omega=\frac1\pi W_{\rm edge}=\frac1\pi\frac{2a\omega_0^2}{c^2+4a^2}$. Integrating from $c=0$ and multiplying by $2/k$ gives $F=\frac2\pi\arctan\frac{c}{2a}=\frac2\pi\arctan\frac{\pi\tau_2Q}{2}$.
5. **Retention.** $d(1/E)/dz\le\kappa_UF(Q(z))\le\kappa_UF(Q_*)$, because $F$ is increasing.

**Gate G2 is met:** the verifier (claude) rederived the argument before reading the proposer's note and supplied the missing unimodality step.

**Gate G3 is met:** units ($Q$ in inverse time, $\tau_2Q$ and $F$ dimensionless), invariance under phase, time shift and energy scaling, and both asymptotes of $F$ (claim card Checks; audit).

## 5. Validation against numerics

All numbers in this section are from the verifier claude-interactive.8 (family claude), unless marked as proposer checks.

| Label | Run id |
|---|---|
| C | `2026-10-17-claude-interactive.8-concentration` (bathtub, profiles, optimizer, propagation, second solver) |
| H | `2026-10-17-claude-interactive.8-hc-relaxed` (Hollenbeck–Cantrell response) |
| P, Q, M | `2026-10-17-gpt-d-raman-propagation`, `2026-10-17-gpt-d-raman-conditional` and `2026-10-17-gpt-d-raman-sharpening` (proposer's checks) |

The verifier froze its tolerances and launches in commit f784fed.

![rho against tau2 Q at GNLSE planes and for optimized intensities](../../../runs/2026-10-17-claude-interactive.8-concentration/fig_summary.png)
*Figure 1. $\rho=|dE/dz|/(\kappa_UE^2)$ against $\tau_2Q$.*
- *Circles: 60 planes per launch of the verifier's own photon-conserving GNLSE. Filled: the SMF-28 surrogate launches. Open: held-out launches (blue, SMF-28 surrogate; green, fluoride surrogate).*
- *Diamonds: the optimizer's best non-negative intensities at fixed $Q$.*
- *Solid: the bound $F$. Dashed: the earlier ceilings $\min(1,\tau_2Q)$.*
- *Run C. The verifier's solver is its own code; the second-solver check uses the agents' solver at commit b9fa957.*

**The bound itself** (run C).
- A bathtub computation that does not assume the level-set shape, on a 4,000,001-point grid, matches $F$ within $1.6\times10^{-10}$, at $r\in\{0.381,2\}$ and $\tau_2Q\in\{0.003,0.03,0.3,3,30,300\}$. The band edges match within $1.3\times10^{-5}$, the grid limit.
- 315 non-negative profiles at $r\in\{0.2275,0.381,2\}$ give at most $\rho/F=0.99592$ (a triangle at $\tau_2Q=58.6$).
- The fixed-$Q$ optimizer over non-negative intensities (four starts) gives:

  | $\tau_2Q$ | 0.1 | 0.3 | 1 | 3 | 10 |
  |---|---|---|---|---|---|
  | best $\rho/F$, $r=0.381$ | 0.520 | 0.527 | 0.622 | 0.894 | 0.977 |
  | best $\rho/F$, $r=2$ | 0.623 | 0.661 | 0.854 | 0.940 | 0.979 |

  A refined search (five starts) gives 0.5195 to 0.5268 for $\tau_2Q=0.01$ to 0.3 at $r=0.381$. The bound is never exceeded.

**Propagation** (run C).
- **Launches.** Seven launches:
  - SMF-28 surrogate: $N=1$ at 30 and 300 fs, $N=3$ at 100 fs;
  - held out: $N=4$ at 200 fs, $N=6$ at 100 fs, $N=5$ at 300 fs, and a fluoride-surrogate $N=4$ at 150 fs.
- **Result.** 26,507 planes with no violation of $\rho\le F(Q)\le1$. The maximum $\rho/F$ is 0.409 ($N=3$); the held-out maxima are 0.368, 0.308, 0.342 and 0.278.
- **Post-freeze launches.** Two 30 fs fission launches, $N=3$ and $N=6$, were added after the freeze, so they are not held out. Over 14,002 planes there was no violation, with a maximum of 0.434 at $\tau_2Q\le1.18$.
- **Retention**, always with the observed $Q_{\max}$, so these are consistency checks:
  - $N=3$: actual 0.9327 ≥ $Q_{\max}$ cap 0.6496 ≥ $P_{\max}$ cap 0.5758 ≥ energy-only bound 0.5048;
  - fluoride: 0.7994 ≥ 0.1182 ≥ 0.0799 ≥ 0.0609.
- **Identity monitors.** RHS against the spectral identity $\le4.5\times10^{-11}$ (relative); integrated balance $\le7.2\times10^{-6}$; photon drift $\le5.3\times10^{-7}$.
- **Artefacts** ($N=3$; relative change of the maximum ratio):

  | Change | Effect |
  |---|---|
  | Half step | $3\times10^{-6}$ |
  | Half $dt$ | $7\times10^{-14}$ |
  | Double window | $2\times10^{-14}$ |
  | Sampled kernel at 1 fs | $4.4\times10^{-5}$ |
  | At 3 fs, analytic / sampled kernel | $1.1\times10^{-5}$ / $3.4\times10^{-4}$ |

  The fluoride case was rerun in a 4× window after $5\times10^{-3}$ of its energy reached the first window's edges. The wide-window run is the one used.
- **Second solver.** The agents' solver (b9fa957, `solve_mmgnlse`, sampled Blow–Wood kernel) on the $N=3$ case at 101 planes:
  - $E(z)$ equals the verifier's sampled-kernel run within $3.2\times10^{-15}$;
  - the verifier's diagnostics on its fields find no violation, maximum $\rho/F=0.4087$, and retention $0.93271\ge0.6504\ge0.5048$.

**Relaxed assumption** (run H, Hollenbeck–Cantrell response).
- $W\ge0$ still holds (sum rule 0.99998), but $W$ has six local maxima on $\Omega>0$, so the single-band level sets fail.
- The numerical bathtub $F_W$ still holds in propagation: maximum $\rho/F_W$ is 0.36, 0.41 and 0.28 for the $N=1$ 30 fs, $N=3$ and $N=6$ launches.
- The arctangent itself is exceeded for strongly concentrated intensities (section 3). In the realistic propagations, planes stay at $\tau_2Q\lesssim1$, where $\rho/F\le0.51$.

**Proposer's checks** (gpt-d, family gpt).
- Level-set integral against quadrature: $1.33\times10^{-13}$ (runs M, Q).
- 82 frozen profiles: largest $\rho/F=0.98012330$ (runs M, Q).
- 36,011 propagation planes: largest $\rho/F=0.50200193$ (runs P, Q).
- Core retention: universal bound 0.632137, observed-$Q$ cap 0.755777, observed-path comparison 0.840231, actual 0.952963 (run Q).

## 6. Adversarial audit

[audit-2026-10-17-claude-interactive.8.md](audit/audit-2026-10-17-claude-interactive.8.md): claude-interactive.8 (family claude, model claude-opus-5-5); proposer gpt-d (family gpt). **Verdict: pass, no blockers, no narrowing.**

**Clean context.** By the report's own description, before its commit (6320014) the auditor read only:
- the claim cards and the problem card;
- `evaluator/`, and the solver documentation and source;
- the `config.yaml`, `meta.yaml` and `summary.json` of the cited gpt-d runs.

All code is its own. The tolerances and launches were frozen in f784fed. **G5 is met.**

**Attacks.**
- a hidden-assumption check of the proof;
- a shape-agnostic bathtub;
- 315 profiles, including resonant pulse trains and fission-like fields;
- a counterexample optimizer over all non-negative intensities at fixed $Q$. This is a superset of what propagation can produce, since the inequality is instantaneous;
- 7 propagated launches, 4 held out;
- step, grid, window and kernel artefacts;
- a second solver;
- the Hollenbeck–Cantrell relaxation;
- prior work;
- fine-tuning: none needed.

**Non-blocking concerns.**
1. The bound is not sharp for physical intensities at small and moderate $Q$: about $0.52F$ is reachable at $\tau_2Q\le0.3$ for $r=0.381$.
2. The arctangent is oscillator-specific.
3. The retention corollary needs an a-priori cap on $Q$, which nobody has supplied.

## 7. Novelty

Two families searched:
- gpt-d (gpt), run `2026-10-17-gpt-d-raman-literature`;
- claude-interactive.8.1 (claude), with search strings including "bathtub principle", "Lieb-Loss" and "level-set" with Raman or SSFS, and upper bounds on Raman energy loss or SSFS rate with "peak power" or "sum rule".

Closest prior work:
- **gpt-b's internal review** (`docs/review-2026-10-16-gpt-b-supercontinuum-literature.md`) gives the weaker peak-power, sup-weight inequality, which in this notation is $\rho\le\tau_2P_{\max}/E$.
- **Chen et al., arXiv:2603.21734, Eq. (3c)** (§3 of v2 full text, claude-interactive.8.1) and **Nie et al., arXiv:2511.04013, Eq. (8)** (full text, claude-interactive.8.1 and gpt-d) give the ceiling value only as a $\tau\to0$ limit.
- **Huang et al., arXiv:2607.05244** (full text, energy sections) has no bound.
- **Not found:** no source for the arctangent, or for any concentration-dependent bound.

**G6 is open.** T-20261017-gpt-d-04 still has to compare the concentration arctangent with the original texts of Gordon 1986 (DOI 10.1364/OL.11.000662) and Herrmann & Nazarkin 1994 (DOI 10.1364/OL.19.002065), both read only at abstract level.

## 8. Experimental test

- **Measurement.**
  - In a fibre whose Raman response is well described by one band, measure at one plane the pulse energy $E$, the intensity concentration $Q=\int I^2/E^2$ (from a FROG retrieval or an intensity autocorrelation), and the energy-loss rate. The rate comes from a short cutback around that plane, corrected for linear loss.
  - The peak-power form needs only $E$ and $P_{\max}$.
- **Prediction.** $-dE/dz\le\kappa_UE^2F(Q)$, with $\kappa_U$ and $\tau_2$ from the measured response.
- **Expected signal.** For launches like those tested, the measured rate sits at no more than about 0.4–0.5 of the bound (runs C and P). The bound comes within a few percent of the rate only for strongly concentrated intensities, $\tau_2Q\gtrsim10$.
- **Falsification.** A rate above $\kappa_UE^2F(Q)$, beyond the measurement error, for a single-band response.
  - For silica, use the numerical $F_W$ from the measured response instead. The arctangent with the Blow–Wood $\tau_2$ is already known to fail for intensities concentrated below about 13 fs (section 3), so such a violation would not refute this result.

## 9. Open questions

- **The sharp ceiling over non-negative intensities.** The verifier's numerics converge to about $0.52F$ at small $\tau_2Q$ for $r=0.381$: T-20261017-claude-interactive.8-01.
- **Realistic multi-band responses**, and an a-priori cap on $Q$ or $P_{\max}$ for a bounded launch class: T-20261017-gpt-d-05; loss-aware closure, T-20261016-gpt-b-03.
- **G6** (original-text prior art): T-20261017-gpt-d-04.
- **G8 is open**: nothing is formalized. The bathtub argument and the arctangent integral are elementary: T-20261019-claude-interactive.15-03.
