---
agent: claude-interactive.8
model: claude-opus-5-5
family: claude
claim: C-20261017-gpt-d-02
task: T-20261017-gpt-d-03
date: 2026-10-17
status: complete
verdict: pass
---

# Independent verification and audit: conditional arctangent Raman energy-loss ceiling

**Verdict: pass.** The level-set (bathtub) proof is correct, and I found no hidden assumption
for the stated single oscillator. The arctangent is the exact maximum of the relaxed spectral
problem.
- **Attacks.** A shape-agnostic numerical bathtub, 315 positive-intensity profiles, a fixed-$Q$ optimizer over positive intensities, 26,507 propagation planes from 7 launches and a second solver all respect the bound.
- **No blocker.** The claim says so itself: the bound is not attained by physical intensities except as $\tau_2Q\to\infty$. At small $Q$ the best positive intensity I found reaches about $0.52F$.
- **Relaxing the oscillator.** With the multi-peak Hollenbeck–Cantrell response, the arctangent with the Blow–Wood $\tau_2$ is exceeded by strongly concentrated positive intensities. The claim already excludes multi-band responses, and the general bathtub bound $F_W$ still holds.

Clean context: as in the companion report. Before this report was committed I read only the claim
cards, the problem card, `evaluator/`, the solver documentation and source, and the `config.yaml`,
`meta.yaml` and `summary.json` of the cited gpt-d runs. All code is my own.

Runs: C = `2026-10-17-claude-interactive.8-concentration`; S = `2026-10-17-claude-interactive.8-sech-tightness`
(library, frozen predictions); H = `2026-10-17-claude-interactive.8-hc-relaxed`.

## Restatement and assumptions

In the lossless, constant-$A_{\rm eff}$, photon-conserving shock GNLSE with one damped oscillator, the
instantaneous loss satisfies $0\le-dE/dz\le\kappa_UE^2F(Q)$ at every plane. Here
$F=\frac2\pi\arctan(\pi\tau_2Q/2)$ and $Q=\int I^2/E^2$, and $Q\le P_{\max}/E$ gives a peak-power form.
Given a cap $Q\le Q_*$ on $[0,L]$, the retention bound $E(L)/E_0\ge1/(1+\kappa_UE_0LF(Q_*))$ follows.
Optimality is claimed only for the relaxed problem.

I checked whether the argument uses anything the card does not list:
- **Positivity of $I$.** Used once, to get $|\tilde I|\le E$, so $f=|\tilde I|^2/E^2\le1$. Intensities are always non-negative, so this costs nothing.
- **Sign of $W$.** $W\ge0$ is needed only for the lower bound $0\le-dE/dz$. The upper bound by the bathtub principle holds for any $W$.
- **Symmetry.** $W$ is even because $h$ is real. Both bands carry equal measure.
- **Shape of $W$.** For $\Omega\ne0$, $W=2a\omega_0^2/[(\Omega-\omega_0^2/\Omega)^2+4a^2]$ with $\omega_0^2=a^2+b^2$.
  - So $W$ depends only on $u=\Omega-\omega_0^2/\Omega$. This is monotone on each half-line, and $W$ decreases in $|u|$.
  - Each super-level set is therefore one interval per side, with $\Omega_+\Omega_-=\omega_0^2$ and $\Omega_+-\Omega_-=c$ (the width in $u$). Total measure $2c=2\pi Q$ gives $c=\pi Q$.
  - Unimodality on each side is thus proved for every $a,b>0$, not assumed.
- **The integral.** $\frac{d}{dc}\frac1\pi\int_{\Omega_-}^{\Omega_+}W\,d\Omega=\frac1\pi W_{\rm edge}=\frac{1}{\pi}\frac{2a\omega_0^2}{c^2+4a^2}$, because $d(\Omega_+-\Omega_-)/dc=1$. Integrating gives $\frac{\omega_0^2}{\pi}\arctan\frac{c}{2a}$, and with the prefactor $2/k$ this is $F$. It is independent of $b$.
- **Limits.** $F<\tau_2Q$ and $F<1$ follow from $\arctan y<\min(y,\pi/2)$. The stated asymptotes of $F$ are correct.
- **Retention.** $d(1/E)/dz\le\kappa_UF(Q_*)$ requires $F$ increasing, which holds.
- **Not covered by the claim.** No a-priori cap on $Q(z)$ is supplied, and the card says so. Every retention number below uses the observed $Q_{\max}$ or $P_{\max}$, so it is a consistency check, not a prediction.

Difference from the card's sketch: none in substance. The card states the level sets and the endpoint value. I obtained both from the variable $u$, which makes the "unimodal on each side" property a one-line proof.

## Attacks

| Attack | Result | Run |
|---|---|---|
| Numerical bathtub with no level-set assumption (sorting $W$ on a 4,000,001-point log grid, both signs, fractional last cell), $r\in\{0.38125,2\}$, $\tau_2Q\in\{0.003,\dots,300\}$ | equals $F$ within $1.6\times10^{-10}$ (tolerance $10^{-6}$); selected band edges match $\Omega_\pm$ within $1.3\times10^{-5}$ (grid-limited) | C |
| 315 positive profiles at $r\in\{0.38125,0.2275,2\}$: sech, Gaussian, super-Gaussian, rectangle, triangle, Lorentzian², incoherent pairs, coherent pairs with offsets near $\omega_0$, chirped pairs, fission-like fields, random fields, resonant pulse trains, cosine envelopes | all $\rho/F\le0.99592$ (maximum: triangle, $\tau_2Q=58.6$) | C |
| Counterexample search: maximize $\rho$ at fixed $Q$ over positive intensities $p=s^2$ (L-BFGS, 4 starts, $M=4096$) | best $\rho/F$: $r=0.381$: 0.520, 0.527, 0.622, 0.894, 0.977 at $\tau_2Q=0.1,0.3,1,3,10$; $r=2$: 0.623, 0.661, 0.854, 0.940, 0.979. Never above 1 | C |
| Refined search at small $Q$ ($M=8192$, 5 starts each), $r=0.381$ | 0.5195, 0.5197, 0.5202, 0.5268 at $\tau_2Q=0.01,0.03,0.1,0.3$, the same from random, resonant-train and cosine starts | C |
| GNLSE, every step of 7 launches: SMF-28 surrogate $N=1$ 30 and 300 fs, $N=3$ 100 fs, and held out $N=4$ 200 fs, $N=6$ 100 fs, $N=5$ 300 fs; fluoride surrogate $N=4$ 150 fs (held out) | 26,507 planes, 0 violations of $\rho\le F(Q)\le1$; maximum $\rho/F=0.409$ ($N=3$); held-out maxima 0.368, 0.308, 0.342, 0.278 | C |
| Retention, both bounds | holds in all 7 launches, e.g. $N=3$: actual 0.9327 ≥ $Q_{\max}$-cap 0.6496 ≥ $P_{\max}$-cap 0.5758 ≥ energy-only 0.5048; fluoride: 0.7994 ≥ 0.1182 ≥ 0.0799 ≥ 0.0609 | C |
| Artefacts, $N=3$ case | half step: max ratio changes $3\times10^{-6}$ relative; half $dt$: $7\times10^{-14}$; double window: $2\times10^{-14}$; sampled kernel at 1 fs: $4.4\times10^{-5}$; at 3 fs: analytic $1.1\times10^{-5}$, sampled $3.4\times10^{-4}$ | C |
| Artefacts, $N=6$ and fluoride | $N=6$: half step $1.4\times10^{-7}$, half $dt$ $1.5\times10^{-14}$. Fluoride: the first window let $5\times10^{-3}$ of the energy reach the edges; a 4× window gives the same maximum ratio to $5\times10^{-14}$ (edge energy $9\times10^{-8}$; the wide-window run is used); its half step changes it by $2.8\times10^{-5}$ | C |
| Identity monitors | RHS vs spectral identity $\le4.5\times10^{-11}$ relative; integrated $E(L)-E_0$ vs $\int dE/dz$ $\le7\times10^{-6}$; photon drift $\le5.3\times10^{-7}$ | C |
| Second solver: agents' copy b9fa957 (`solve_mmgnlse`, sampled Blow–Wood kernel), $N=3$ case, 101 planes | $E(z)/E_0$ equal to my sampled-kernel run within $3.2\times10^{-15}$; my diagnostics on its fields: 0 violations, max $\rho/F=0.4087$, retention 0.93271 ≥ 0.6504 ≥ 0.5048 | C |
| Relaxed assumption: HC 13-mode silica response | see below | H |

The optimizer attack is stronger than optimizing launch pulses through the solver. The inequality is instantaneous and depends only on the intensity at the plane, and the optimizer searches all positive intensities, a superset of the intensities propagation can produce.

**Relaxed assumption: HC multi-peak response (run H).** Default amplitudes $A_i$; the $A_i/\omega_i$ variant gives the same conclusions.
- **Shape of $W$.** $W\ge0$ holds (sum rule $0.99998$), but $W$ has six local maxima on $\Omega>0$, so the single-interval level sets fail.
- **General bathtub.** The bound $F_W(Q)$ from sorting $W$ still holds:
  - in HC propagation of the $N=1$ 30 fs, $N=3$ and $N=6$ launches, max $\rho/F_W=0.36$, $0.41$ and $0.28$;
  - for sech at all widths, $\le0.987$.
- **Arctangent form under HC.** It does not transfer:
  - with the matched sup-weight $\tau_{2,\rm eff}=(2/k)\sup W=52.1$ fs, $F_W$ exceeds $F(\tau_{2,\rm eff}Q)$ by up to 8.0%, at $\tau_{2,\rm eff}Q\approx4$;
  - with the Blow–Wood $\tau_2=32$ fs, optimized positive intensities exceed $F$ by 1.9% at $\tau_2Q=2.5$ (effective duration 12.8 fs) and 4.0% at $\tau_2Q=5$ (6.4 fs);
  - a plain sech exceeds it by up to 2.5% at $T\approx1.7$ fs;
  - in realistic HC propagation the planes stay at $\tau_2Q\lesssim1$, where $\rho/F(32\,{\rm fs})\le0.51$.

**Prior work.**
- No source found for the arctangent or concentration bound, or for the $\kappa_UE^2$ ceiling as a bound. Searched by subagent claude-interactive.8.1: "bathtub principle" or "Lieb-Loss" or "level-set" with Raman or SSFS; upper bound on Raman energy loss or SSFS rate with "peak power" or "sum rule"; Raman response "initial slope" sum rule; maximum or upper limit of SSFS with impulsive saturation.
- arXiv:2607.05244 has no bound. Access: full text by the subagent; HTML targeted extraction by me.
- arXiv:2603.21734 Eq. (3c) and arXiv:2511.04013 Eq. (8) give the ceiling value only as a $\tau\to0$ limit. Access: full text by the subagent.
- The weaker peak or sup-weight inequality is attributed by the card to gpt-b's internal review, which I did not read.

**Fine-tuning.** None.

## Blockers

None.

## Non-blocking concerns

1. **Not sharp for physical intensities at small or moderate $Q$.** The best positive intensities reach $0.52F$ for $\tau_2Q\le0.3$ ($r=0.381$), $0.62F$ at $\tau_2Q=1$ and $0.89F$ at 3. The arctangent is the relaxed optimum. The sharp constant for non-negative intensities is open.
2. **Oscillator-specific.** For silica modeled with HC, use $F_W$ or a measured gain spectrum. The arctangent with Blow–Wood $\tau_2$ is not a valid ceiling for intensities concentrated to about 15 fs or less.
3. **Retention needs an a-priori cap.** Neither $Q$ nor $P_{\max}$ is monotone. In my fission launches the observed $Q_{\max}$ was 2.6 to 4.5 times the launch value (1.0 for the fundamental solitons), so the corollary is not predictive from launch data (run C).

## Regime I sign off on

As stated: $0<\tau_2Q<\infty$, $0<\tau_1/\tau_2<\infty$, $0\le\kappa_UE_0L<\infty$, for the single
Blow–Wood-type oscillator, constant $A_{\rm eff}$, lossless photon-conserving model. Tested on
$10^{-3}\le\tau_2Q\le300$ (bathtub) and $r\in\{0.2275,0.381,2\}$ (profiles, optimizer), and in
propagation up to $\kappa_UE_0L=15.4$. No narrowing needed. The retention corollary applies only with an independently justified cap.

## Post-audit note (after commit 6320014)

After the report above was committed, I read gpt-d's proof note §5. It changes nothing in the verdict.
- **Same proof.** The note uses the same bathtub argument, band edges and endpoint value. Its $D$-derivative $4a/[\pi(D^2+4a^2)]$ equals my $(2/k)W_{\rm edge}/\pi$.
- **Level sets.** The note states the single-interval level sets without proving unimodality. The variable $u=\Omega-\omega_0^2/\Omega$ above supplies that step.
- **Physical attainability.** The note says the relaxed optimizer is not a physical spectrum, since $f(0)=1$. My optimizer quantifies this: about $0.52F$ is reachable at small $\tau_2Q$ for $r=0.381$.

Post-freeze addition (after commit 6320014): I ran two further launches at the short end of the requested range. They were not frozen in advance, so they are not held out (run C, `postfreeze_propagation`).
- **Launches.** SMF-28 surrogate, 30 fs: $N=3$ over $3L_D$ and $N=6$ over $1L_D$, 14,002 planes in total.
- **Result.** No violations. Max $\rho/F=0.434$ ($N=3$), at $\tau_2Q$ up to 1.18; $0.383$ for $N=6$.
- **Convergence.** Half step changes the max ratio by $2.4\times10^{-10}$ ($N=3$) and $5.4\times10^{-8}$ ($N=6$).
- **Verdict.** Unchanged.
