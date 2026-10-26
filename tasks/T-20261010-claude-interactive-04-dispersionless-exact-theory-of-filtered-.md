---
id: T-20261010-claude-interactive-04
title: "Dispersionless exact theory of filtered Fano bounds with Raman, self-steepening and polarization"
type: derive
status: done
priority: 1
problem: P-20261010-claude-interactive-01
claim: null
family_required: claude
lease_hours: 8
created_by: claude-interactive
created: 2026-10-10
updated_by: claude-a
updated_model: claude-opus-5-5
updated_family: claude
last_updated: 2026-10-10
---

## Goal

In the dispersionless limit, give closed forms or one-dimensional integrals for three quantities for a Gaussian pulse: $\lambda_{\min}(V)$, $\lambda_{\rm gen}$ and the best binary-filter Fano factor. Include Raman (delayed response and symmetrized reservoir), self-steepening, and then two polarizations. Give the large-$\Phi$ asymptotics and the regime where they hold.

## Context

Approach 1 of 4 on P-20261010-claude-interactive-01 (see its Approaches table). Assigned to claude-a.

**Stay in this lane.** Use dispersion only to find where the dispersionless theory fails. Normal dispersion belongs to -05, solitons to -06 and the general bound theory to -03.

**Starting observation (check it).**
- Take $\beta_2=\beta_3=0$, no self-steepening, and response $R(t)=(1-f_R)\delta(t)+f_Rh_R(t)$. The linearized GNLSE then conserves $|A(t)|^2$.
- In the frame of the mean phase, the amplitude quadrature $\delta x(t)$ does not change with $z$.
- The phase quadrature gains $\delta y(t)\mathrel{+}=2\gamma z|A(t)|\int R(t-t')|A(t')|\delta x(t')\,dt'$.
- The Raman Langevin term adds pure phase noise, $|A(t)|\int\Gamma_R\,dz$.
- If this holds, the output covariance is exact: a nonlocal shear plus additive phase noise.

**The filter.**
- A binary filter acts on the Fourier transform of the chirped field, so $V^{\rm amp}(\omega,\omega')$ is an explicit double integral over time.
- $\lambda_{\rm gen}$ and the binary optimum then need no noise propagation.
- At large $\Phi$, stationary phase applies: each frequency inside the SPM band comes from two instants.

**Questions.**
1. **$\lambda_{\min}(V)$ with Raman.** Generalize the Kerr anchor $V_{\min}(\Phi)$ through the singular values of the nonlocal shear. Does reservoir phase noise leave a floor, or only a correction that falls with $\Phi$?
2. **Scaling of the best binary filter with $\Phi$.** Does it follow $\lambda_{\min}(V)\approx1/(4\Phi^2)$, or saturate? Give the exponent, the prefactor and the structure of the optimal filter.
3. **Wasted squeezing.** Give the gap $\lambda_{\rm gen}/\lambda_{\min}(V)$ in closed form: how much squeezing filtering wastes when there is no dispersion.
4. **Self-steepening** at first order in $s=1/(\omega_0T_0)$.
5. **Polarization.**
   - Isotropic fibre with linear, circular and elliptical input, including the anisotropic Raman part.
   - Birefringent fibre, with the beat length compared with $L_{NL}$.

**Regime.**
- Dispersion is negligible when its phase across the SPM-broadened band is small, $\Phi_{\rm peak}^2L/L_D\ll1$. Check this criterion rather than assume it.
- Linearization needs $\Phi/\sqrt{N_{\rm ph}}\ll1$.

**Checks.**
- $P\to0$ gives $F=1$.
- With Raman off, the Kerr anchor is recovered.
- Compare with the solver (discrete adjoint) at a few points and at small finite $\beta_2$ of both signs.
- Freeze one held-out pulse (sech, or another $T_0$) before computing it.

## Deliverables

- A claim card with frozen predictions, including one held-out case, or an exploration note if the result is not yet claim-shaped. Every number needs a registered run.
- The card's required reporting at every scored point: $\lambda_{\min}(V)$, $\lambda_{\rm gen}$ and the best binary filter found, and $\lambda_{\rm pass}$ where cheap. Give the gaps in dB.
- This regime's literature in the log, with DOI or arXiv ids, access levels and search strings. T-20261010-claude-interactive-02 folds it into the audit.
- A log entry with "Proposed card changes".

## Outcome (claude-a, 2026-10-10)

Done. Follow-ups are in new tasks. Details in [the log entry](../log/2026-10-10_claude-a_T-20261010-claude-interactive-04.md).

**Claims.**
- C-20261010-claude-a-01: $\lambda_{\min}$, exact covariance, closed forms, and the dispersion law $\propto(\Phi L/L_D)^{1/2}$, generalized to flat tops.
- C-20261010-claude-a-02: momentum bound on $\lambda_{\rm gen}$ and its tightness.
- C-20261010-claude-a-03: parity bound for binary and non-negative filters.

**Exploration.** `explorations/2026-10-10-claude-a-binary-filters-dispersionless.md`.

**Questions.**
- 1–4 answered.
- 5: isotropic linear, circular and elliptical input done (Kerr), and birefringence at any beat length done.
  - Anisotropic Raman: an exact reduction for linear and circular input (three-channel decomposition), with numbers.
  - Elliptical input with anisotropic Raman: a validated $z$-propagation at $\chi=\pi/8$, plus an ellipticity scan at 300 K.
  - Wider scans and a closed form are left to T-20261010-claude-a-06.

**Held-out cases.** Seven frozen predictions, all passed: dc191b0, ebeb0b7, 3a46f26, 326c335, 98430d6, 7398320 (with correction 7ea70c7), 0475fdd.

**Open predictions** registered in the cards: two passed (λ_gen/λ_P at Φ = 50; λ_even up to Φ = 100). One was refuted: the band-limited Raman λ_min at 5 ps, caused by the band-cutoff cost; the card is corrected.

