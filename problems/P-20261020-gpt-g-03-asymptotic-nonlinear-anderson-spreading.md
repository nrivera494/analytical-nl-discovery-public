---
id: P-20261020-gpt-g-03
title: "Asymptotic spreading versus arrest in the standard local-Kerr nonlinear Anderson chain"
status: audited
priority: 3
literature_state: open
novelty_confidence: high
target_quantity: "An asymptotic spreading law or decisive probability/time bound for a finite-norm packet in the one-dimensional disordered DNLS at fixed linear hopping, resolving power-law spreading, sub-power transport and dynamical arrest."
model: "i dA_n/dz = v_n A_n - J(A_(n-1)+A_(n+1)) + g|A_n|^2 A_n, with static independent on-site disorder, constant J>0, local cubic Kerr response, conserved norm and Hamiltonian, and no bath or longitudinal noise."
oracle_ready: missing
last_audited: 2026-10-20
audited_by: [gpt, claude]
proposed_by: PI
provenance:
  agent: gpt-g
  model: gpt-6-astra
  family: gpt
claims: []
results: []
---

## Target quantity

Determine whether a typical finite-norm packet continues to spread indefinitely under the standard one-dimensional local-Kerr disordered DNLS, and at what asymptotic rate. Fix the probability measure over static disorder and random initial phases. A universal assertion for all initial states is excluded: localized quasiperiodic solutions and self-trapped components must be treated explicitly.

Use

$$i\partial_z A_n=v_nA_n-J(A_{n-1}+A_{n+1})+g|A_n|^2A_n,\qquad N=\sum_n|A_n|^2<\infty,$$

with a specified smooth bounded distribution of $v_n$, independent of $z$. Track three different observables:

$$p_n=|A_n|^2/N,\qquad m_2=\sum_n(n-\bar n)^2p_n,\qquad \mathcal P=(\sum_n p_n^2)^{-1},\qquad p_{\max}=\max_n p_n.$$

Also track the minimum interval containing a fixed norm fraction, and report its centre separately. The centred second moment can grow through remote tails while the bulk remains localized. The target is a controlled law or bound for bulk dilution and transport, including their relation, rather than a new finite-time fit to $m_2$.

The first scope is strong but finite disorder with fixed $J/W>0$ as the nonlinear density decreases. It does not replace the linear hopping by purely nonlinear intersite coupling. A successful result must specify its initial-condition measure, limiting order and parameter domain; it need not settle every disorder strength or every launch.

## Signal of hidden simplicity

Numerical packets often exhibit a simple subdiffusive scaling, while rare-resonance and normal-form analyses predict transport far slower than a fixed power at weak nonlinearity. Dilution reduces the nonlinear frequency shift, making the late dynamics approach the localized linear system. This supplies a moving small parameter and an identifiable competition between resonant transfer and the loss of effective chaos. The problem is precisely whether a simple coarse-grained law remains valid in that limit. Sources: Flach et al. 2009; Basko 2011; Fishman et al. 2012; De Roeck et al. 2024–2026.

## Literature state

### Longstanding evidence

- **Earliest explicit open statement located:** Pikovsky and Shepelyansky, PRL 100, 094101 (2008), DOI [10.1103/PhysRevLett.100.094101](https://doi.org/10.1103/PhysRevLett.100.094101), [arXiv:0708.3315](https://arxiv.org/abs/0708.3315). **Full text**, model and final discussion. They report apparently unlimited spreading above a threshold, but state: “The question about the exact value of the exponent remains open.” The conclusion also leaves extremely slow subthreshold Arnold diffusion possible. Finite-time evidence is not an all-time conclusion.
- Fishman, Krivolapov and Soffer, *The nonlinear Schrödinger equation with a random potential: results and puzzles*, Nonlinearity 25, R53 (2012), DOI [10.1088/0951-7715/25/4/R53](https://doi.org/10.1088/0951-7715/25/4/R53), [arXiv:1108.2956](https://arxiv.org/abs/1108.2956). **Full text**, analytic/numerical comparison and Sec. 5.1. Its explicit open list asks: “What is the asymptotic time scale?” It also asks how experiments can reach the asymptotic regime and whether the numerical scaling can be derived.
- De Roeck, Huveneers and Prośniak, PRE 109, 044207 (2024), DOI [10.1103/PhysRevE.109.044207](https://doi.org/10.1103/PhysRevE.109.044207), [arXiv:2308.10572](https://arxiv.org/abs/2308.10572). **Full text**, introduction, model and theorem. The paper explicitly revisits the conflict between numerical power-law spreading and nonperturbatively slow analytical relaxation. Its actual theorem concerns equilibrium decorrelation in a KG chain.
- **Most recent explicit restatement located:** De Roeck, Giacomin, Hannani and Huveneers, *Sub-power law decay of the wave packet maximum in disordered anharmonic chains*, Nonlinearity 39, 045002 (2026), DOI [10.1088/1361-6544/ae56ad](https://doi.org/10.1088/1361-6544/ae56ad), [arXiv:2502.02344](https://arxiv.org/abs/2502.02344). **Full text of 2025 preprint**, introduction, model and result. It states that “the exact nature and rate of this spreading remain elusive”. Its advance and its different coupling structure are distinguished below; the quotation is from the accessed preprint, not an assumed identical journal text.

### Resolution audit

| Work and access | What is established | Why it does not close this card |
|---|---|---|
| Kopidakis et al. (2008), DOI [10.1103/PhysRevLett.100.084103](https://doi.org/10.1103/PhysRevLett.100.084103), [arXiv:0710.2621](https://arxiv.org/abs/0710.2621); **abstract only**, primary publisher/arXiv | Analytic obstruction to complete dilution at sufficiently strong nonlinearity, plus numerical bounded participation despite increasing second moment. | The proof is conditional on the strong-nonlinearity regime; extrapolation to arbitrary launches is stated as an assumption. It motivates measuring bulk participation and separating self-trapping, rather than claiming universal spreading. |
| Flach, Krimer and Skokos (2009), DOI [10.1103/PhysRevLett.102.024101](https://doi.org/10.1103/PhysRevLett.102.024101), [arXiv:0805.4693](https://arxiv.org/abs/0805.4693); **full text**, scaling mechanism/model; erratum [10.1103/PhysRevLett.102.209903](https://doi.org/10.1103/PhysRevLett.102.209903) also read in full | Resonance-based weak-chaos spreading picture and subdiffusive numerical scaling. | Does not control the self-consistency of stochastic forcing at arbitrarily small density or exclude a later crossover. |
| Johansson, Kopidakis and Aubry (2010), DOI [10.1209/0295-5075/91/50001](https://doi.org/10.1209/0295-5075/91/50001), [arXiv:1007.1912](https://arxiv.org/abs/1007.1912); **full text**, abstract and discussion | Empirical arguments and numerical evidence for KAM-like regular states constrain universal spreading assertions. | Evidence for nonspreading states, including a proposed finite-probability set, does not determine the fate of the specified broad random-phase ensemble. The proposed problem must report probabilities, not discard these states. |
| Basko (2011), DOI [10.1016/j.aop.2011.02.004](https://doi.org/10.1016/j.aop.2011.02.004), [arXiv:1005.5033](https://arxiv.org/abs/1005.5033); **full text**, introduction, scope and Appendix B, pp. 96–98 | Rare chaotic spots and macroscopic transport; Appendix B explicitly predicts finite-packet size $L(t)\sim\exp[(c^{-1}\log t)^{1/3}]$ in its weak-chaos regime. | This is an existing asymptotic proposal, not just a finite-density result. Appendix B acknowledges that the local-equilibration length grows faster than the packet, then argues that fluctuations only change a coefficient. Controlling that extrapolation and its ensemble dependence remains essential. Its finite-resource condition is argued to improve at long times; finite norm alone is not a refutation. Re-deriving the predicted functional form without resolving these issues would not be novel. |
| Vakulchyk, Fistul and Flach (2019), DOI [10.1103/PhysRevLett.122.040501](https://doi.org/10.1103/PhysRevLett.122.040501), [arXiv:1806.06345](https://arxiv.org/abs/1806.06345); **full text**, abstract/model/conclusion | Greatly extended numerical time horizons in a nonlinear discrete-time quantum-walk model support continuing subdiffusion. | A unitary map is not the same fixed-Hamiltonian DNLS, and finite horizons cannot settle all-time asymptotics. This is important contrary evidence, not an ignored result. |
| De Roeck et al. (2024), above; rigorous companion (2025), DOI [10.1007/s00220-025-05336-z](https://doi.org/10.1007/s00220-025-05336-z), [arXiv:2308.11243](https://arxiv.org/abs/2308.11243); **full text**, introduction/model and stated bounds | KG equilibrium decorrelation/transport times grow faster than any inverse power of anharmonicity as it vanishes, including fixed harmonic hopping. | Equilibrium weak-anharmonicity bounds do not themselves give a finite-packet DNLS spreading law, nor infinite-time arrest. The papers' use of asymptotic localization must not be interpreted as permanent localization at fixed nonlinearity. |
| De Roeck et al. (2025 preprint/2026 journal), above | An all-time sub-power bound on packet-maximum decay for chains with on-site harmonic disorder and quartic nearest-neighbour coupling. | The displayed model suppresses harmonic hopping. Its DNLS-type extension has nonlinear intersite coupling, not standard linear hopping plus on-site Kerr. The observable is also peak decay, not a complete width law. Extending a bound mechanically is not the full target. |
| Milovanov and Iomin (2025), DOI [10.1103/svxt-wsk7](https://doi.org/10.1103/svxt-wsk7), [arXiv:2502.08463](https://arxiv.org/abs/2502.08463); **full text**, journal Secs. II–VI and preprint | Proposes dielectric screening, finite localization length, and a further self-screening scenario. | The main result uses a spatially nonlocal/dispersive nonlinear kernel, then an effective superquadratic on-site power. The self-screening claim for the original problem additionally assumes a nearest-mode Cayley-tree reduction, a Boltzmann chaos probability and a percolative conductivity. These are not a controlled derivation for the fixed local-Kerr chain or the ensemble here. |

The last assessment is this scout's inference from the published equations, not a claim that the screening paper is incorrect in its stated medium. In particular, its Sec. VI genuinely addresses a self-screening possibility; it cannot be dismissed simply by saying that every part of the paper adds an external bath. A future derivation must either justify such a reduction for the present model or distinguish its predictions experimentally/numerically.

### Kill search

On 2026-10-20, screened the 2021–2026 forward citations of Pikovsky–Shepelyansky and followed the 2024–2026 mathematical and screening papers. Targeted queries included:

- `"nonlinear Anderson" "open problem" 2024 2025 2026`
- `"nonlinear Anderson" "asymptotic" "2026" -site:researchgate.net -site:scribd.com`
- `"wave packet maximum" "2025" "2026" De Roeck`
- `"Asymptotic localization" "10.1103/svxt-wsk7"`
- `"nonlinear" "Anderson" "fiber loops" experiment`

Exact submitted strings and API date filters are preserved in the [review](../docs/review-2026-10-20-gpt-g-longstanding-optical-thermalization.md). No accepted closure of the specified fixed-hopping finite-norm local-Kerr problem was found. **High provisional novelty confidence** follows from the explicit open problem and the inspected limitations of the strongest apparent resolutions. It does not mean the derivation is likely to be easy. *Added by claude-interactive.23 (2026-10-20): the independent Claude-family search agrees, for a controlled or rigorous result; see below.*

### Second-family review (added by claude-interactive.23, claude, 2026-10-20)

This is the cross-family novelty review, task T-20261020-claude-interactive-05; the full assessment is in [the review](../docs/review-2026-10-20-claude-interactive.23-cross-family-novelty-gpt-g-cards.md). An independent Claude-family search (claude-interactive.23 and helper .23.3) found no asymptotic result for the chain with linear hopping $J>0$. The three longstanding-evidence quotations above are verbatim, and the description of De Roeck, Huveneers and Prośniak (2024) is accurate (arXiv full texts). The target is open. High novelty is defensible for a controlled or rigorous result. Additions:

- **The rigorous route is not a modest adaptation.**
  - De Roeck, Huveneers and Prośniak (CMP 406, 155 (2025), [arXiv:2308.11243](https://arxiv.org/abs/2308.11243); passage read in **full text**) state that their approach "would thus not have worked" for the nonlinear Schrödinger equation. The reason: DNLS small denominators are combinations of Anderson eigenvalues, whose correlations are not controlled beyond pairs.
  - The light-cone lemma behind the 2026 peak bound uses an energy current bounded by $C(H_{x-1}^2+H_x^2)$, which has no analogue when the hopping is linear.
  - The 2026 authors nevertheless expect their method to extend to a broader class of chains, so this route has a likely competitor.
- **A maximum bound would itself meet the bar.** A sub-power lower bound on $p_{\max}$ for the standard chain would rule out asymptotic power-law dilution, and that is enough for high novelty. This sharpens the statement above that "Extending a bound mechanically is not the full target": the extension is not mechanical. It agrees with the scouting review's criterion of "a bound that rules out one of the competing asymptotes".
- **Missing from the resolution audit:**
  - Cong, Shi and Zhang, J. Stat. Phys. (2021), [arXiv:2006.04332](https://arxiv.org/abs/2006.04332), and Cong, Shi and Wu (2024). These are the only rigorous long-time localization results for the DNLS with linear hopping, valid for small hopping and nonlinearity up to finite, super-polynomial times (helper .23.3, theorem statement).
  - Aubry (2023), [arXiv:2212.05771](https://arxiv.org/abs/2212.05771), conjectures that typical chaotic packets do not spread; it is rigorous only for hard-core models (helper .23.3, full text).
  - Recent numerics: Cheong et al., Chaos (2026); Many Manda et al. (2023); Kati, Yu and Flach (2020) (abstracts).
- **A heuristic answer exists.** Basko (2011), Eq. (3.8), gives $L(t)\sim\exp\{[(\ln t)/C']^{1/3}\}$, with $C'$ and the exponent $p$ of his Eq. (3.6) only bounded. A new heuristic derivation is medium novelty unless it fixes those constants or decides between arrest and slow spreading.
- **Platform numbers** (helper .23.3):
  - Lahini et al. (2008) used 99 AlGaAs waveguides on 5 mm samples.
  - Vatnik et al. (2017) report agreement up to 80–120 round trips on about 104 positions, in the linear regime.
  - Vakulchyk et al. (2019) state that experiments reach less than a thousandth of their computational horizon.
  - Transverse-Anderson fibres show a thermal, nonlocal nonlinearity (Leonetti et al. 2014).
  - No nonlinear disordered fibre-loop experiment was found.

## Sharpest statement of the gap

Can deterministic rare resonances keep transferring norm after a spreading packet becomes arbitrarily dilute, and what replaces the finite-time diffusion law if the available chaotic background ceases to act as a bath? A theory must connect local resonant dynamics, the distribution of bottlenecks, and global finite-norm dilution without assuming the answer through a stochastic forcing model.

Solving this would matter to Anderson localization, nonlinear wave turbulence, weak chaos, and optical transport. The problem is substantially older than the particular fibre implementation. A new optical geometry alone would not make its solution novel.

## Analytical foothold and first derivation target

Work in the exponentially localized linear-eigenmode basis. The nonlinear overlap tensor decays with mode separation, while frequency mismatches generate a sparse hierarchy of resonant clusters. Use a resonant normal form for a small chaotic cluster and perturbative elimination of the surrounding nonresonant modes, building on Basko and the newer normal-form bounds.

**First derivation target:** bound or derive the distribution of the action-transfer time from such a cluster across one localization volume as the nonlinear shift/level-spacing ratio tends to zero at fixed $J/W$. Keep the cluster's finite energy and norm budget and the receiving modes' backreaction; do not impose stationary white noise. Resolve the roles of rare small denominators and rare long barriers, and distinguish median from disorder-averaged rates.

Then test whether a local transport closure survives the packet's dilution time. If it does, derive a self-consistent growth law with its crossover scale. If it does not, obtain a probability/time bound or a constructive mechanism deciding whether bulk spreading can continue. Merely re-establishing the KG decorrelation bound for a nearby Hamiltonian, or obtaining a fitted weak-chaos exponent, is an insufficient final result.

*Added by claude-interactive.23 (2026-10-20):* Two sharper first targets, one for each route.
- **Rigorous route.** For 1D Anderson eigenmodes within one localization volume, quantify the probability that $|E_\nu+E_\mu-E_\kappa-E_\lambda|<\delta$. This is the correlation that De Roeck, Huveneers and Prośniak (2025) name as the obstacle. Then decide numerically whether a Minami-type bound is plausible for quadruples, using exact diagonalization only (task T-20261020-claude-interactive.23-03).
- **Physics route.** Compute Basko's undetermined $C'$ and $p$ for one disorder strength. That turns his functional form into a quantitative prediction for long-time numerics (task T-20261020-claude-interactive.23-04).

## Assumptions, dimensionless groups and regime

- One-dimensional infinite chain as the mathematical target; large finite chains with negligible boundary occupation for the oracle. Static independent bounded continuous disorder, constant hopping, on-site Kerr only, no longitudinal randomness, dissipative bath, external phase noise, Raman, gain or nonlocal dielectric response.
- Disorder scale $W$ and $\kappa=J/W$ with $0<\kappa_{\min}\le\kappa\le\kappa_{\max}\ll1$. Hold $\kappa$ fixed when taking the dilute limit. The atomic limit $J\to0$ is a comparison, not the claimed domain.
- Let $V_\xi$ be the linear localization volume and $d_\xi$ its typical linear level spacing, both defined for the occupied spectral interval. For local occupation scale $n$, use $\epsilon=|g|n/d_\xi\ll1$ and $\nu=|g|n/W\ll1$. Their evolution must be determined rather than kept artificially fixed.
- Initial packet width $L_0/V_\xi\gg1$, independent uniform phases, prescribed finite total norm and bounded local nonlinear shift below the linear bandwidth. Specify the distribution of amplitudes and conserved energy; separately report any self-trapped component. The disorder/launch ensemble is part of the result.
- At fixed finite propagation length require boundary distance much larger than the measured fixed-mass radius, $\alpha z_{\rm obs}\ll1$, and external-noise decorrelation time much greater than the predicted transfer time. Synthetic-loop step size must approach the continuous Hamiltonian limit before transferring conclusions to this equation. These conditions can be demanding and may limit the lab to testing the mechanism rather than the eventual asymptote.

## Conjectures

None. Continued subdiffusion, sub-power spreading and ensemble-dependent arrest remain competing possibilities at the scope stated here.

## Oracle

**Missing.** The present solver has modal Kerr and dispersion but lacks a ready static disordered core-hopping lattice evaluator and a validated transverse-disorder mode generator. Its lack of random linear mode coupling must not be confused with the present requirement for *quenched* disorder and fixed hopping. A small dedicated Hamiltonian DNLS code is the appropriate initial oracle.

First check the resonant-cluster transfer-time distribution, using exact linear Anderson eigenmodes for each disorder realization. Then compare packet evolution at held-out disorder strengths and launches using $m_2$, $\mathcal P$, $p_{\max}$, fixed-mass radius and local action decorrelation. Enforce norm/energy convergence, step-size and precision checks, finite-chain convergence, and independence of the reported distribution from the integration method. Deliberately add weak dephasing as an assumption-relaxation control and show how it cuts off or changes the deterministic law. No simulation campaign was performed for this card.

## Lab test

Prefer a one-dimensional coupled-core fibre with independently calibrated propagation-constant disorder, or a programmable fibre-loop mesh with static phase disorder and a verified small-step DNLS limit. Vary input norm at fixed disorder and packet shape; record the core/bin-resolved power and coherent field where available. Test the predicted density dependence of local decorrelation and transfer events, together with bulk participation and width. A finite experiment can reject a proposed rate or crossover; it cannot by itself prove perpetual localization.

Mafi and Ballato's fibre review, DOI [10.3389/fphy.2021.736774](https://doi.org/10.3389/fphy.2021.736774), **full text**, Secs. 1 and 4.2–4.3, documents disordered fibres and warns that nonlocal thermal nonlinearities also occur. Vatnik et al., *Anderson localization in synthetic photonic lattices*, DOI [10.1038/s41598-017-04059-z](https://doi.org/10.1038/s41598-017-04059-z), is a located linear fibre-loop platform demonstration; this scout accessed its abstract/indexed conclusion, while PMC full-text retrieval was blocked by a CAPTCHA and was not bypassed. Neither is evidence that the nonlinear asymptotic question has already been tested.

A transverse-Anderson-localization fibre is a valuable later two-dimensional extension, but neither its dimension nor its potentially nonlocal response is interchangeable with this one-dimensional local-Kerr target. The dedicated platform check must precede promises of an asymptotic fibre experiment.

## How a solution would be recognized

A theory for the specified ensemble decides a nontrivial asymptotic alternative, or supplies a bound that excludes one, at fixed linear hopping. It predicts the relation between bulk dilution and transport, gives a usable rate or crossover dependence on dimensionless disorder/nonlinearity, and survives independent numerical tests without relying on a finite-time slope alone. A measurable cluster-transfer or decorrelation prediction must distinguish it from the existing weak-chaos and screening explanations.

## Risks and must-reads

- Rare events may make the mean unrepresentative; both typical and tail behaviour matter.
- A local-equilibrium closure can fail as the packet dilutes. This is part of the unknown, not a permitted hidden assumption.
- KAM states and self-trapping invalidate universal-for-all-launches statements.
- The asymptotic regime may be beyond feasible experiments and direct simulation. A useful bound and an experimentally discriminating local mechanism are required, rather than promising an infinite-time test.
- Read the full technical proof of the 2026 peak bound and the full high-order calculation in Basko before choosing the derivation route; this scout read selected relevant sections, not every proof.
- Milovanov–Iomin's self-screening reduction is a serious competing explanation to audit, not a citation to omit.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-20 | gpt-g (gpt; gpt-6-astra) | Created candidate; high novelty provisional, GPT literature review only | Explicit 2008/2012 open statements; 2024–2026 restatements and bounds; full-text model comparison with the 2025 screening claim; documented kill search |
| 2026-10-20 | claude-interactive.23 (claude; claude-opus-5-5) | Second-family novelty review (T-20261020-claude-interactive-05). Agrees that the target is open and that high novelty is defensible for a controlled or rigorous result; a heuristic sub-power law is not new (Basko 2011). candidate → audited; audited_by [gpt] → [gpt, claude]; novelty_confidence high, priority 3 and literature_state unchanged. Added the second-family subsection and sharper first targets | De Roeck et al. 2026 (arXiv full text); De Roeck–Huveneers–Prośniak, CMP 2025 (quoted passage); Basko 2011, Eqs. 3.6–3.8; [review](../docs/review-2026-10-20-claude-interactive.23-cross-family-novelty-gpt-g-cards.md); helper search .23.3 |
