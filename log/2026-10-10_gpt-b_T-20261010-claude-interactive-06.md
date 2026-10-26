---
date: 2026-10-10
agent: gpt-b
model: gpt-6-astra
family: gpt
task: T-20261010-claude-interactive-06
duration_min: 225
---

## Did

Session start was 10:32:55 EDT; the wall-clock budget ends at 14:32:55.
Scientific calculations, registration and repository checks are complete.
The closing portion of the session is reserved for validation and PR delivery;
the final delivery time is recorded below.
No subagents were used. No original solver repository was modified. The
agents' solver remained clean at `b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa`.
Julia used at most two threads and one process at a time.

- Read the task/card and bounded prior-art search; derived the four-neutral-mode
  plus squared-Jost continuum correlator, an explicit centered-filter Gram
  formula, and the restricted covariance eigenvalues.
- Projected the symmetrized oscillator Raman source through that propagator.
  Derived exact cutoff source minorants, the positive-temperature long-pulse
  limit and higher-order coefficients, the zero-temperature law, and fixed-filter
  short- and long-distance asymptotes.
- Included deterministic Raman shift, shock and beta3 in physical checks with
  Float64 fixed-step RK4IP and explicit `adjoint_mode=:discrete_rk4ip`.
  Fetched the unmodified coth helper from private solver commit
  `d79f150c4dabac6f461f0302eb06b1ec7900bd4e`; no default half-zero-point/DC-zero
  source was used. Raman samples are at most 3 fs, with refinements below 1 fs.
- Froze the first physical prediction before its propagation, a second cutoff
  bound case in `57f1781`/`0fdee15`, and a sharper-source third case in
  `55d2da6`. Gaussian coherent-width predictions and the fission SSFS forecast
  were likewise frozen before their respective propagations.
- Tested Gaussian launches, a later one-soliton-plus-radiation case, and an N=2
  Gaussian Raman-fission case. Derived inherited scattering amplitude/frequency
  gradients and a local launch-mismatch Duhamel expansion.
- Reproduced the notebook's archived readout, searched broader binary masks,
  and checked selected masks with the native public discrete adjoint.
- Read the prior proposed multimode card and, only in the final hour, gpt-a's
  pushed readout note. Checked common bright/dark and uniform-phase limits;
  no other round-3 method or binary certificate was imported.

## Found

The usable proposed result is **C-20261010-gpt-b-01**, an exact lower bound
inside the frozen fundamental-soliton linear stochastic model. For
$T_R=2f_R\tau_1^2\tau_2/(\tau_1^2+\tau_2^2)$ and
$K_c=T_0\sqrt{2(\tau_1^{-2}-\tau_2^{-2})}$,

$$S_L(k)=(T_R/T_0)|k|\coth[\hbar|k|/(2k_BT T_0)]1_{|k|\le K_c}\le S_R(k),$$
$$B_L=\inf\operatorname{spec}(\mathcal R_q^*V_L\mathcal R_q)
\le\lambda_{\rm gen}(V_{\rm fr})\le\min_TF_{\rm fr}[T].$$

The complete neutral/continuum propagator and the source Gram are explicit;
no nonlinear longitudinal propagation is needed to evaluate this reduced
formula. Finite eigenvalues remain numerical approximations, not certified
continuum enclosures. The physical comparisons are in
$\zeta\le6$, $\zeta\max(T_R/T_0,|s|,|\delta_3|)\le0.06$, with fixed
$f_R=0.18$ and response-width ratio at most 0.256. **No one-sided physical
GNLSE remainder is proved.** Indeed, the full frozen amplitude eigenvalue
slightly exceeds the finest physical pilot eigenvalue.

The positive-temperature scale is $\rho_T=2k_BT T_R/\hbar$, which persists
as $T_0$ grows at fixed normalized length. Corrections on fixed regular
readouts start at $T_0^{-2}$; the zero-temperature source instead starts
at $T_R|k|/T_0$. The optimized white-source readout is the infimum of
$F_K[T]+\rho_T B[T]$, so its thermal dependence is nondecreasing and concave,
not a filter-independent additive constant. Unfitted next coefficients
leave measured amplitude-eigenvalue residual powers 4.0005 at 300 K and
2.9988 at zero temperature. A sharper polynomial-coth source minorant
leaves powers 4.0008 and 4.9984 in its eigenvalue gap to the full frozen
source. All are in `2026-10-10-gpt-b-soliton-raman`.

The original Kerr, 300 K physical pilot and three completed held-out scores
are tabulated below. Entries are dB; the three gaps are from the cutoff
formula (Kerr restriction in the Kerr row), directly propagated amplitude
minimum, and field minimum to the best achieved binary mask.

| Case | Field / passive / amplitude / binary | Formula / amplitude / field gaps | Run |
|---|---|---|---|
| Kerr, $\zeta=3\pi/2$ | -19.7728 / -10.8550 / -7.2639 / -6.5904 | 0.6735 / 0.6735 / 13.1824 | `2026-10-10-gpt-b-soliton-kerr` |
| Fundamental, 0.25 ps, 300 K, finest grid | -12.8910 / -6.8178 / -6.2229 / -5.6781 | 0.5484 / 0.5448 / 7.2129 | `2026-10-10-gpt-b-soliton-solver`, `pilot_finest` |
| Held out, 0.35 ps, 77 K, positive beta3 | -15.0510 / -7.4529 / -5.6875 / -5.2196 | 0.4711 / 0.4678 / 9.8314 | same run, `held_out` |
| Held out, 0.2 ps, 150 K, negative beta3 | -14.3972 / -7.2454 / -6.2227 / -5.7375 | 0.4899 / 0.4852 / 8.6597 | same run, `held_out_second` |
| Held out, 0.4 ps, 225 K, positive beta3, refined source | -14.2002 / -7.1652 / -6.6820 / -5.9130 | 0.7701 / 0.7690 / 8.2872 | same run, `held_out_third` |

The third case passes its frozen 0.003 absolute targets: the amplitude
eigenvalue error is 0.00005496 and the binary prediction error is 0.00062816.
Its native mask score agrees with the independent batch contraction.

The complete table is `runs/2026-10-10-gpt-b-soliton-solver/scored_cases.md`.
The main binary searches enumerate contiguous intervals, then use 64 seeded starts,
eigenvector-threshold masks, one-bit descent and four 10,000-flip annealing
sweeps. Selected mask values are re-contracted directly. No global binary
optimum is certified. Some fission/late-Gaussian eigenvalues are explicitly
Ritz values in constant-filter spectral-cell spaces; their gaps are not
whole-field certified gaps.

The notebook anchor has $N=1.968972$, outside the fundamental-soliton regime.
The archived mask gives about -5.252 dB with the shock-inclusive reservoir;
the archived -5.322 dB total used the source without that multiplier.
A broader searched mask reaches about -9.14 to -9.17 dB in the native
fine-grid/window checks. Its reservoir term now exceeds its input-vacuum
term. The 50-to-100 ps central mean changes by only $3.38\times10^{-9}$,
but the window check also changes frequency-bin spacing. These are achieved
values, not a new global optimum or a use of the fundamental bound outside
its regime (`2026-10-10-gpt-b-soliton-anchor`).

The N=2 Gaussian fission refinement reaches the finite-cell quartet
$(-16.1338,-15.8773,-12.0578,-11.0057)$ dB with cells of width 0.15.
Its native fixed-mask refinements give -11.03322 and -11.03933 dB,
with a final change of 0.00611 dB. The last variance consists of vacuum
0.02613622 and reservoir 0.05258052. The matched-grid amplitude/field gaps
are 1.0521/5.1281 dB; no fundamental-soliton formula is applied there.
Refining cells from 0.3 changed both eigenvalues and the best mask, so
whole-field/readout-basis convergence remains open
(`2026-10-10-gpt-b-soliton-gaussian`).

## What failed or was narrowed

- **C-20261010-gpt-b-02 is refuted:** resetting a Gaussian's soliton component
  to a fresh coherent sech is not a filtered-noise bound. The N=1.5 Kerr
  control gives an achieved $F=0.17647334$, below the frozen surrogate
  amplitude bound 0.34464482. The finite-distance field still contains
  radiation; no exactly isolated final sech is claimed. Native refinement
  preserves the physical-shock counterexample.
- The inherited amplitude/frequency gradients are useful neutral-coordinate
  formulas, but they do not replace the full inherited scattering covariance.
  The first launch-mismatch expansion has the predicted local quadratic
  error, yet fails badly at the full N=1.5 long-distance mismatch.
- The frozen first-moment SSFS forecast for N=2 Gaussian fission has 30.7%
  error relative to the prediction, failing its 20% target. A full-response
  momentum integral reduces the discrepancy to 2.94%, **post hoc**. The
  compressed response-width ratio is 0.749, outside a short-response limit.
- A stress test exposed cancellation/empty-mask handling in the initial
  incremental binary search. The failed output is retained as
  `launch_born_N1.5.json`, marked invalid. Direct recontraction, exclusion of
  empty masks and stable interval sums fixed it. All prior saved masks,
  99 distance-curve masks, and small exhaustive stress checks pass the
  arithmetic audit; no previously reported achieved main score changed.
- The first short-window notebook comparison was inconclusive and retained.
  The original window/filter convention is needed for an honest anchor.
- The exact elementary arbitrary-binary optimum was not obtained. A centered
  edge optimum is an achievable upper value, not the requested lower bound.
  Published Kerr optimum constants and the inaccessible Raman-floor formula
  were not recovered from unread full texts, and no novelty claim is made.

## Changed

Added the two claim cards, a detailed exploration with the assumption ledger,
research evaluators in `scripts/soliton_*`, registered configurations and
summaries in `runs/2026-10-10-gpt-b-soliton-*`, four inspected figures, the
required quartet/gap table, and follow-up tasks. Raw arrays, PDFs, means,
adjoints and masks remain in `~/analytical-nl-discovery-data/<run-id>/`.
The problem card, other agents' tasks, generated files and solver code were
not hand-edited. The own task remains open because its full physical and
Gaussian goals are not finished. No result folder is created or promoted.

## Not verified

All calculations are proposer checks, not independent-family verification.
The earlier source claim C-20261008-gpt-b-01 and the multimode law
C-20261008-claude-b-01 remain proposed and unverified. The latter was read
at `6c16dc1a0d8ecc348351dbe56a01d28249e1b8ff`; its no-Raman coefficients
cannot be reused for a physical Raman tensor. The common-reservoir Manakov
identity is a conditional model check, not a physical GRIN validation.

The final-hour readout cross-check used gpt-a's unverified work in progress
at `2a406511ac1f558fdbe87080dae67d00646299e5`. Our passive/global-phase and
amplitude conventions agree; the scalar DC phase-source null was checked
on our own covariance. The ideal passive limit allows arbitrary mode
mixing, not merely a spectral phase device.

Outstanding: a one-sided physical remainder, continuum lower enclosures,
global binary optimality, the full Gaussian scattering covariance,
physical multimode Raman coefficients, and priority against unavailable
primary full texts. The last item belongs with the orchestrator's literature
audit T-20261010-claude-interactive-02.

## Loose ends

- T-20261010-gpt-b-01: independent-family check of the cutoff bound and Gaussian refutation.
- T-20261010-gpt-b-02: controlled physical soliton remainder and continuum error.
- T-20261010-gpt-b-03: inherited Gaussian/fission covariance, readout-basis refinement and usable formula.
- T-20261010-gpt-b-04: physical Raman projection in the multimode second-order law.
- T-20261010-gpt-b-05: independent native check and refinement of the improved notebook-anchor mask.
- T-20261010-claude-interactive-02: existing literature audit, including inaccessible load-bearing filtering/Raman papers.

## Proposed card changes

1. Distinguish an exact bound in a frozen stochastic model from an asymptotic
   physical prediction; the deterministic remainder is a separate obligation.
2. State that the notebook launch is an N approximately 1.969 sech, not a
   fundamental soliton. Its archived mask is not the optimum over the broader
   binary class tested here. Record both source conventions and the new achieved
   mask values, with the finite-cell eigenvalue qualification.
3. A Gaussian with N near two can contain two discrete solitons under the
   stated launch-width convention. A sech-looking core retains launch/radiation
   covariance; its classical fitted width does not determine the quantum noise.
4. The long-pulse thermal scale at fixed normalized length is
   $2k_BT T_R/\hbar$. The floor depends on distance/readout and is not a single
   material-only additive penalty. Cooling retains zero-point noise.
5. Require the Raman overlap tensor for a multimode extension. Deterministic
   Manakov symmetry does not by itself prove a reservoir first-order null.
6. Ensure the PI input list includes nonlinear and Raman response data,
   temperature and input-noise assumptions; the linear index profile alone
   does not specify these.

## Literature and access

The initial search was kept below forty minutes. Queries included the supplied
author/year/page strings, the supplied arXiv identifiers, “Raman noise and
soliton squeezing pdf”, “Perturbation theory of quantum solitons dB”, and
“Klaus Shaw Gaussian pulse number solitons area pi Zakharov Shabat single lobe”.
Publisher/PubMed, arXiv, author-hosted, MIT OCW and indexed preview copies
were checked. This is not an exhaustive absence-of-theory search.
Source-reported numerical values and access records are registered under
`2026-10-10-gpt-b-soliton-literature`.

| Source | Access in this session | What it establishes here |
|---|---|---|
| Levandovsky, Vasilyev & Kumar, DOI [10.1364/OL.24.000043](https://doi.org/10.1364/OL.24.000043) | **Abstract only** at publisher/PubMed; indexed partial full-text preview and figure captions also inspected, but the full PDF could not be fetched | Complete analytical amplitude-quadrature correlator including continuum and numerical filter optimization are prior art. Square filters are approximately optimal up to three soliton periods; disconnected passbands improve longer-distance filtering. The full numerical Kerr optimum and their complete formula were not read. |
| Mecozzi & Kumar, DOI [10.1364/OL.22.001232](https://doi.org/10.1364/OL.22.001232) | **Abstract only**, PubMed; publisher full text not accessed | Soliton-bandwidth/photon-number correlation and continuum-induced oscillations/finite filtering limit are prior art. A specific parabolic-filter closed form is attributed to this paper by Raginsky–Kumar; the primary formula itself was not accessed. |
| Werner & Friberg, [arXiv:quant-ph/9904104](https://arxiv.org/abs/quant-ph/9904104) | **Full text**, including the filter convention and Fig. 4 | A symmetric passband for a sech input is optimized in cutoff and distance. For $T_0=1$ ps and 300 K the paper reports 4.8 dB, cutoff $125\pm12.5$ GHz, and $3\pm0.2$ soliton periods. In the angular-frequency convention here the central cutoff is $a=\pi/4$, not 0.125. This is not a global optimum over arbitrary binary masks. Source-reported numbers are transcribed in the literature run. |
| Kärtner, Dougherty, Haus & Ippen, DOI [10.1364/JOSAB.11.001267](https://doi.org/10.1364/JOSAB.11.001267) | **Abstract only**; publisher marks full text unavailable | Quantized Raman phonons, thermal/quantum excess noise, and limits for subpicosecond soliton squeezing are prior art. No particular numerical floor or analytic coefficient is attributed to the unread full text. |
| Drummond & Corney, [arXiv:quant-ph/9912095](https://arxiv.org/abs/quant-ph/9912095), DOI 10.1364/JOSAB.18.000139 | **Full text available**, sections on Raman coupling and symmetric/Wigner noise read closely | Scalar Raman noise is proportional to $(n_{\rm th}+1/2)\alpha_R=|\operatorname{Im}h|\coth$, including zero-point noise. A measured multi-Lorentzian response is distinguished from the single oscillator. A numerical discrepancy with Werner's material model cannot be interpreted as a theory discrepancy without matching the response. |
| Corney & Drummond, [arXiv:quant-ph/9912096](https://arxiv.org/abs/quant-ph/9912096) | **Full text available**, bright-soliton perturbation and source projections read closely; equations visually checked | Projection of multiplicative Raman noise and integrated frequency-to-timing diffusion are established. The paper treats deterministic redshift as a small correction in its analytic reduction and retains it in numerical checks. This does not establish a spectral-filter noise floor from neutral modes alone. |
| Raginsky & Kumar, [arXiv:quant-ph/0104120](https://arxiv.org/abs/quant-ph/0104120) | **Full text** | Confirms the soliton-plus-continuum/filtering conventions and prior analytical correlator. Its parabolic attenuation and cascaded stages are different readouts from one binary mask. |
| Kärtner, MIT 6.977 lecture notes, chapter 3, [official course PDF](https://ocw.mit.edu/courses/6-977-ultrafast-optics-spring-2005/c439bcfab7826300aec0017e7de1f2fd_chapter3.pdf) | **Full text available**, soliton perturbation section read | Source for continuum/discrete-mode completeness and adjoint conventions; educational source, no DOI/arXiv identifier. The primary filtering papers above carry the priority attribution. |
| Klaus & Shaw, DOI [10.1103/PhysRevE.65.036607](https://doi.org/10.1103/PhysRevE.65.036607) | **Abstract only** | Real single-hump Zakharov–Shabat potentials have imaginary discrete eigenvalues. Used only to motivate a separate Gaussian soliton-content check. |
| Uddin et al., DOI [10.1038/s41566-025-01677-2](https://doi.org/10.1038/s41566-025-01677-2), [arXiv:2311.05535](https://arxiv.org/abs/2311.05535) | **Full main text** from the latest arXiv PDF; supplement not accessed | Programmable spectral filtering of a Raman-shifted soliton and pump, including disconnected filters and noisy inputs, is already demonstrated. The displayed launch is a sech pulse. This session's Gaussian tests are related regime tests, not a reproduction of that experiment. |
| Uddin et al., [arXiv:2503.12646](https://arxiv.org/abs/2503.12646) | **Full text**; model and noise-source sections read closely | Power-dependent Raman-soliton and pump correlations are calculated from input-to-output sensitivities. The authors explicitly omit the phonon Langevin contribution after estimating it to be small in their setting. That omission does not establish a symmetrized-reservoir floor for the present readout. |
| Werner, DOI [10.1103/PhysRevA.60.R781](https://doi.org/10.1103/PhysRevA.60.R781) | **Abstract only** | The connection between long-fibre edge-filtered squeezing and Raman self-frequency shift is prior art. A fixed-mask frozen-mean distance asymptote must not be substituted for the moving Raman-soliton calculation in that work. |


## Validation and delivery

Both required checks passed: `python scripts/validate.py` and
`python scripts/check_generated.py origin/main`. `git diff --check` is clean.
All 28 Python evaluators compile; the Julia evaluator parses. The final native
metadata guard rejects a dirty solver checkout instead of hard-coding a clean
status. This metadata-only change does not change the completed calculations.
Registered evaluator hashes match the final files, and relative artifact links
resolve. The final saved-mask, distance-curve and small exhaustive arithmetic
checks pass. Four generated figures were visually inspected. GitHub's
`validate` check passed on the evidence commit `4f59d28`.

`origin/main` was refreshed and is already an ancestor of this task branch.
PR #27 merged during the session; this task's PR targets main and states the
original stack. PR: [#32](https://github.com/nrivera494/analytical-nl-discovery/pull/32).
Final session record: 2026-10-10 14:18:13 EDT (225 minutes, rounded).
This is after the three-hour-forty-five-minute minimum; unfinished questions
remain explicit in the task and continuation records. No pull request was
merged by this agent.
