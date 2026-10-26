---
agent: gpt-f
model: gpt-6-astra
family: gpt
date: 2026-10-20
task: T-20261020-claude-interactive-01
---

# Ultrashort optical thermodynamics in disordered fibre

## Recommendation and limits of this review

File **one candidate**, [P-20261020-gpt-f-01](../problems/P-20261020-gpt-f-01-raman-drift-local-optical-equilibrium.md): a parameter-derived Raman drift and lifetime of a local classical optical equilibrium in weakly disordered GRIN silica fibre. Start away from condensation, with a specified spectral band and temporal gate. The requested output is a drift law for thermodynamic multipliers and measured modal fractions, together with a bound or asymptotic estimate for departure from that law.

Do **not** file separate cards for the shock-modified RJ distribution, a generic spatiotemporal RJ theory, or an unqualified claim that Raman favours the fundamental mode. These are respectively known, substantially addressed by the 2026 baseline and P-005, and false without restrictions. The new candidate has `literature_state: partial`, `novelty_confidence: low`, and priority 3: the constituent theories exist, but their compatible reduction and an experimentally accessible separation of rates remain to be established.

This is a first-family literature review, not a verification of a new claim. The only computation is the small symbolic/arithmetic run [2026-10-20-gpt-f-thermodynamic-ledger](../runs/2026-10-20-gpt-f-thermodynamic-ledger/summary.json). No propagation or kinetic simulation was run. Source access levels and remaining downloads are recorded below. “Not located” refers to the logged searches, not a proof of absence.

## 1. Definitions that prevent false conservation claims

Use $\Omega$ for detuning and $\omega=\omega_0+\Omega>0$ for physical optical frequency. Let $A_p$ be power-normalized envelopes and $\psi_p(\Omega)=\widetilde A_p(\Omega)/\sqrt{\omega_0+\Omega}$. Factors of $\hbar$ and the Fourier normalization can be restored consistently. Define

$$
N=\sum_p\int|\psi_p|^2\,d\Omega,\qquad
P=\sum_p\int\Omega|\psi_p|^2\,d\Omega,\qquad
\mathcal E=\sum_p\int|\widetilde A_p|^2\,d\Omega=\omega_0N+P.
$$

Here $\mathcal E$ is optical pulse energy; the propagation Hamiltonian $H$ is a different quantity. Write $H_2=\sum_p\int\epsilon_p(\Omega)|\psi_p|^2d\Omega$, where $\epsilon_p$ is the linear generator in the chosen $i\partial_z$ convention. Subtracting a carrier propagation constant or changing the retarded frame adds a multiple of $N$ or $P$; it must not change a physical conservation test.

For a stationary random wave, the analogous spectral integrals are ensemble densities per unit retarded time. For a finite pulse, integrate the local spectral density over the specified temporal gate before calling the result a pulse photon number or energy.

For the autonomous, lossless instantaneous Kerr model with the correct frequency prefactor and symmetric overlap vertex, $N,P,H$ are conserved. Thus $\mathcal E$ is conserved too, but is not a fourth independent invariant. Weak-wave kinetics conserves $H_2$ to its order of approximation; the full field equation conserves $H_2+H_4$, not generally $H_2$ separately. A bare first spectral moment of $|\widetilde A|^2$ is not the canonical momentum once shock is retained. These distinctions are supported by [Barviau et al. 2009](https://doi.org/10.1103/PhysRevA.79.063840), [Picozzi et al. 2014, §5.4.4](https://doi.org/10.1016/j.physrep.2014.03.002), and [Zanaglia et al. 2026](https://doi.org/10.1103/mqzh-w2gh).

For a passive, frequency-preserving random linear step $\partial_z\psi=-iC(z,\Omega)\psi$, $C=C^\dagger$, the total occupation at **each** frequency is conserved. Therefore $N,P,\mathcal E$ survive regardless of modal degeneracy. Its contribution to propagation energy is

$$
\partial_zH_2=i\int\psi^\dagger[C,\epsilon]\psi\,d\Omega.
$$

It vanishes for all inputs precisely when $[C(z,\Omega),\epsilon(\Omega)]=0$. Exactly degenerate symmetry partners satisfy this across the band if the symmetry persists. Members of an approximate GRIN group generally do not: their entire $\beta_p(\omega)$ curves matter. Inter-group coupling between non-degenerate modes does not conserve $H_2$. Moreover, even commuting **linear** disorder does not establish conservation of the complete nonlinear Hamiltonian: the disorder can rotate the Kerr vertex, and $z$-dependent forcing makes the instantaneous Hamiltonian non-autonomous. The commutator identity and the unitary covariance check are recorded in the symbolic run.

## 2. Mechanism map: what mixes, at what rate, and with which invariants?

| Platform/mechanism | Derived or measured result | Rate information and broadband limitation |
|---|---|---|
| Weak random birefringence in GRIN silica; Fusaro/Garnier 2019 | Polarization decorrelation permits resonant Kerr exchange between spatial modes and discrete-wave RJ condensation. Their principal disorder is a random Hermitian polarization matrix for each spatial mode. | $\Delta\beta=\sigma_\beta^2\ell_\beta$, $L_d=1/\Delta\beta$, with $\ell_\beta\ll L_d\ll L_{\rm NL}$ and group spacing $\gg\Delta\beta$. In the discrete CW limit $L_{\rm kin}\sim L_{\rm NL}^2/(L_d\overline{\lvert S\rvert^2})$. Numerical prefactors and the relaxation eigenvalue depend on the quartet network and populations. |
| Full random coupling inside exact spatial groups, as used in this repository | A useful explicit mixing model, but not identical to the preceding polarization-noise model. It preserves group power in each linear step. | Calibrate the covariance and its spectral dependence. Commutation preserves the linear $H_2$ in each step; it does not supply a measured kinetic rate or automatically preserve nonlinear resonant invariants. |
| Strong disorder coupling non-degenerate groups; Berti 2022 | Kerr RJ relaxation competes with linear power equipartition. A transient RJ state can occur before the eventual disorder-driven distribution. | The linear rate is $\Gamma_{pq}=2\operatorname{Re}\int_0^\infty\langle C_{pq}(0)C_{qp}(s)\rangle e^{i(\epsilon_p-\epsilon_q)s}ds$. Its graph gap defines $L_{\rm eq}^{-1}$. Require $L_{\rm kin}\ll L_{\rm eq}$ for an RJ plateau. Optical energy survives lossless mixing, but $H_2$ generally does not. |
| Random-coupling-assisted cleaning; Sidelnikov 2019 | Compares all-mode and degenerate-mode coupling in a spatial coupled-mode model. Supports sensitivity of cleaning to the coupling structure. | It is not a broadband pulsed thermodynamic closure or a universal relaxation-rate formula. Its random-segment parameters must be translated into a covariance before comparison. |
| Strongly coupled single degenerate group; Mecozzi 2012 | Haar averaging gives an isotropic multicomponent Manakov equation when common dispersion and negligible frequency-dependent coupling are imposed. | Fast orientation mixing does not imply RJ thermalization. The leading equation is integrable. Unequal group dispersions and coupled-group coefficients remove that implication. |
| Multiple strongly coupled groups / multicore fibre; Mecozzi 2012, Mumtaz 2013 | Averaged vector equations and coupling coefficients exist. Coupled-core implementations offer controllable linear coupling and delays. | Constant core coupling belongs in the autonomous linear Hamiltonian and preserves the full conservative $H$; it does not by itself redistribute occupations of its own eigenmodes. Random coupling preserves $H_2$ only under the same commutator test. Inter-core supermodes are usually non-degenerate. |
| Static spatial disorder in nonlinear photonic lattices | Localization can inhibit nonlinear thermalization; increasing disorder need not accelerate mixing. | A static disordered Hamiltonian is conserved, unlike a longitudinally random drive. Rates depend on resonant overlaps/localization and cannot be imported from polarization scrambling. |
| Chaotic D-shaped fibre; Ermann et al., 2026 journal / 2025 preprint | Nonlinear dynamics above a chaos threshold approaches RJ; below it, nearly integrable behaviour persists. | Linear ray chaos supplies complicated eigenfunctions, not irreversible modal thermalization. Autonomous Kerr dynamics preserves $N,P,H$ with appropriate broadband normalization; the cited study is spatial. No calibrated ultrashort mixing rate was established here. |

Primary references for this table: [Fusaro 2019](https://doi.org/10.1103/PhysRevLett.122.123902), [Garnier 2019](https://doi.org/10.1103/PhysRevA.100.053835), [Berti 2022](https://doi.org/10.1103/PhysRevLett.129.063901), [Sidelnikov 2019](https://arxiv.org/abs/1908.07745), [Mecozzi 2012](https://arxiv.org/abs/1203.6275), [Mumtaz 2013](https://arxiv.org/abs/1207.6645), [localization-hindered thermalization](https://doi.org/10.1038/s42005-023-01309-7), [D-shaped fibre](https://arxiv.org/abs/2506.06534). The source ledger distinguishes full-text and abstract access.

**Two qualifications are essential.** First, perfectly common polarization noise on all modes does not provide the decorrelation assumed by the weak-disorder kinetic derivation; partially decorrelated noise can. Second, the discrete CW rate above must not simply be pasted onto a temporal frequency continuum. Disorder-broadened resonances can change $H_2$ when off-resonant channels matter. Garnier 2019, Eqs. (22)–(32), distinguishes an energy-conserving discrete spatial regime from a spatial continuum regime tending toward equipartition. That is a warning for a pulsed extension, not a theorem about its temporal continuum: the extension must compare resonance width with dispersion-dependent mismatch, and calculate or bound any extra drift. This is one reason the candidate is conditional.

### The January 2026 non-uniform-disorder paper

[Zitelli, arXiv:2601.16998](https://arxiv.org/abs/2601.16998), full text of model, experiments and discussion, reports non-uniform modal distributions from linear disorder, using field-coupling calculations, power-flow equations, classical measurements and single-photon measurements. It separately estimates mode-dependent losses. This is relevant contrary evidence, not something to omit.

It does not establish that an arbitrary closed, lossless, reciprocally mixed modal system has a non-uniform equilibrium. Its field model includes output-index-dependent normalization of coupling coefficients and a total-power correction after coupling steps; its power-flow discretization has asymmetric group flows. Experiments observe a subset of supported groups. These details require audit in a common flux-normalized basis.

**Independent consistency test:** a lossless unitary channel maps a covariance $nI$ to itself. A mixture of such channels is also unital. Therefore a universal departure from equal **per-mode** occupation, starting with that covariance over the complete guided space, requires a different assumption. Group degeneracy, unobserved/radiative channels, loss correction, coherence of the launch and normalization must be resolved before interpreting the reported weighted-BE law as a universal equilibrium. Also, a small fractional change in $\sum\beta_p n_p$ dominated by the common carrier $\beta$ does not establish conservation of the modal excitation energy: that test changes under an arbitrary common shift of $\beta$. These are audit questions, not a refutation of the experiments.

## 3. Spatial thermodynamics and what pulsed experiments actually test

The spatial weak-Kerr framework already has RJ occupations, entropy maximization, equations of state, condensation and negative-temperature states for a bounded modal spectrum. With the convention $n_p=T/(\epsilon_p-\mu)$, the elementary state equation is $H_2-\mu N=MT$. Optical temperature refers to propagation eigenvalues, not the thermal temperature of silica. [Wu et al. 2019](https://doi.org/10.1038/s41566-019-0501-8) develops thermodynamic processes; [Baudin et al. 2020](https://doi.org/10.1103/PhysRevLett.125.244101) tests condensation and heat capacity; [Baudin et al. 2023](https://arxiv.org/abs/2301.02796) tests inverted negative-temperature populations.

| Experiment | Pulse/platform and observed quantity | Treatment of time and limitation |
|---|---|---|
| Baudin et al. 2023 negative temperatures | Subnanosecond Nd:YAG pulses near 1.06 µm; near/far-field reconstruction and an ensemble of speckle launches. | A bounded spatial mode spectrum is the thermodynamic system. The theory omits temporal dispersion and uses modal power. This does not establish a joint mode–frequency negative-temperature state. |
| Pourbeyram et al. 2022 | 200-fs, 1040-nm pulses; GRIN fibre, predominantly 50-µm core; spectrally resolved holographic modal decomposition, both polarizations. | Spatial modal fractions are compared with RJ. Short fibres suppress Raman; weak coupling and gradual normal-dispersion broadening are discussed explicitly. Reported $L_D\sim0.5$ m and $L_{\rm NL}\sim0.05$ m at the highest energy do not justify neglecting all temporal evolution. Supplement §§6–8 distinguishes participating groups and late Raman asymmetry. |
| Mangini et al. 2022 | Sech-like pulses: 174 fs, 1 ps, 7.6 ps at 1030 nm, plus 435 ps at 1064 nm; camera-based modal decomposition. | The derivation expressly uses monochromatic waves. Similar RJ fits over these durations demonstrate robustness of a measured spatial distribution, not equilibration of the full $n_p(t,\Omega)$. Different coupling conditions change fitted multipliers. |
| Ferraro et al. 2024 calorimetry | Two differently launched/polarized photon gases; 2-ps, 1030-nm pulses; modal populations give thermodynamic parameters. | Polarization-resolved spatial exchange is the thermodynamic object. The setup includes output spectral filtering. It does not derive a temporal kinetic closure or the photon-weighted shock correction. |
| Liu et al. 2016 | Approximately 80-fs, 1030-nm pulses in 62.5-µm GRIN fibre; Kerr cleaning. | A beam-profile experiment with simulations; it is not a measurement of joint spatiotemporal equilibrium. Only its publisher abstract was read here. |
| Zitelli, Mangini & Wabnitz 2024 | 250-fs, 1400-nm input; long OM4 fibre; delayed mode-group pulses permit decomposition. | Derives a weighted-BE law by entropy extremization, then fits group distributions. It assumes appropriate conservation or small variation and separates regimes with/without observed Raman shift. Group delay separates pulses; it is not a continuing equilibrium of a mutually overlapping finite pulse. |

Sources: [Baudin](https://doi.org/10.1103/PhysRevLett.130.063801), [Pourbeyram](https://doi.org/10.1038/s41567-022-01579-y), [Mangini](https://doi.org/10.1364/OE.449187), [calorimetry](https://doi.org/10.1103/PhysRevX.14.021020), [Liu](https://doi.org/10.1364/OL.41.003675), [weighted BE](https://doi.org/10.1038/s41467-024-45185-3). The [2025 Physica D review](https://doi.org/10.1016/j.physd.2025.134758), especially §§2–3, explicitly discusses time integration and narrow output filters. Neither a time-integrated RJ fit nor a weighted-BE fit independently proves an ergodic microscopic state. Zitelli's later [weighted-BE state-equation formulation](https://arxiv.org/abs/2404.00480), DOI:10.1002/lpor.202400714, also fits thermodynamic multipliers across powers; it does not derive the longitudinal perturbative Raman law sought here.

## 4. Spatiotemporal and single-mode baselines

**Required baseline, read in full:** [Zanaglia et al., PRL 136, 053802 (2026), arXiv:2506.23536v2](https://arxiv.org/abs/2506.23536). It treats stationary, temporally incoherent waves; spatial modes and continuous frequencies jointly enter the four-wave kinetic equation. It derives a generalized unidirectional model, canonical frequency-weighted amplitudes, collision invariants, an H-theorem, and the generalized RJ family. Its treatment includes shock and higher-order dispersion. Spectral expansion produces a moving local equilibrium and adiabatic cooling, not a final classical state over an infinite frequency continuum. The appendices derive the asymptotic front/cooling powers for the specified symmetric, quadratic-dispersion regime. These exponents must not be transferred to Raman, finite envelopes or arbitrary dispersion. Degenerate modes are excluded from that kinetic derivation; the numerical examples use lifted degeneracy, and avoid soliton competition through their chosen dispersion/nonlinearity signs.

**Quantum companion:** [arXiv:2512.07784](https://arxiv.org/abs/2512.07784), full text of model and relevant equilibrium/discussion sections, supplies the BE equilibrium and its classical RJ limit. In its convention $\widetilde\beta_m=\beta_m-\kappa\Omega^2$, anomalous dispersion admits positive-temperature states, whereas normal dispersion selects negative-temperature states with inverted spatial occupation. This is an equilibrium analysis of stationary incoherent waves, not a finite-pulse relaxation law. Its discussion identifies adding structural disorder and controlling Raman as future issues.

**Single-mode prior art is substantial.** Barviau–Kibler–Picozzi 2009 already treats self-steepening, higher-order dispersion, spectral fission and equilibrium spectra in supercontinuum. The [2014 Physics Reports review](https://doi.org/10.1016/j.physrep.2014.03.002), selected passages in §§3, 5.4, 6 and 7, covers kinetic/Vlasov limits, anomalous thermalization, spectral incoherent solitons, truncated thermalization and driven cavities. In the scalar quadratic-dispersion NLSE, the ordinary resonant four-wave collision term is too restrictive to provide generic RJ relaxation. Suret–Picozzi–Randoux's refined kinetic treatment nevertheless predicts spectral relaxation in the integrable system; integrability does not mean that every ensemble observable is frozen. Additional invariants and the kinetic ordering matter. Their stationary spectra must not be identified with generic RJ equilibrium.

Spatiotemporal GRIN experiments on multimode solitons, geometric parametric instability and supercontinuum supply competing mechanisms, not interchangeable thermodynamic evidence. [Wright–Christodoulides–Wise 2015](https://doi.org/10.1038/nphoton.2015.61) studies anomalous-dispersion ultrashort dynamics. [Krupa et al. 2017](https://arxiv.org/abs/1603.02972) uses 900-ps pulses, explicitly comparing their duration with about 12 ps of modal broadening over 12 m, and filters the observed pump band; its simulations use a different, shorter pulse for computational scaling. [Lopez-Galmiche et al. 2016](https://doi.org/10.1364/OL.41.002553) attributes visible supercontinuum to intermodal mixing and spatiotemporal breathing. Coherent soliton capture, Raman locking and weighted-BE descriptions of their modal distributions are already neighbouring topics, especially P-002 and P-008.

## 5. Self-steepening, integrability and other conservative corrections

For the restricted scalar equation

$$
iA_z=dA_{tt}+g|A|^2A+i s\,\partial_t(|A|^2A),
$$

the change $A=e^{i(kt+\ell z)}q(z,t+vz)$ with $k=g/s$, $v=2dk$, $\ell=dk^2$ removes the cubic term and gives a Kaup–Newell derivative NLS. The substitution is checked symbolically in the registered run. It is a mathematical statement for this constant-coefficient equation; the frequency shift is not a physical prescription to move a positive-frequency envelope outside its validity range. The scalar Kerr-plus-simple-shock model is consequently not a generic thermalizer. The integrable multicomponent Manakov limit likewise needs isotropic nonlinearity and common dispersion. Coupled generalized Manakov equations for several unequal groups are not automatically integrable. The scalar substitution also does not certify an arbitrary shock-corrected vector vertex; the averaged broadband equation must be checked explicitly.

Generic third-order dispersion breaks these special structures. The Hirota and Sasa–Satsuma exceptions require matching **nonlinear derivative terms and coefficients**, not just adding a dispersion coefficient; see [Sasa–Satsuma](https://doi.org/10.1143/JPSJ.60.409) and the [integrable hierarchy](https://doi.org/10.1063/1.5030604). Nonintegrability alone still does not give a usable thermalization length. Real, autonomous higher-order dispersion preserves canonical $N,P,H$ while changing resonance geometry, allowed temperature signs, group-velocity matching and ultraviolet behaviour.

There is a stronger warning than mere rate uncertainty: the scalar TOD kinetic model in Picozzi et al. 2014, §6.2, retains **frequency-local collision invariants** and relaxes to a nonstandard spectrum. Thus even an integrability-breaking correction can leave more than three kinetic constraints. The candidate must test the collision null space before projecting onto three multipliers.

Frequency-dependent mode profiles require a four-frequency overlap vertex or a justified reduction. Multiplying an otherwise fixed cubic term by an arbitrary $\gamma(\Omega)$ need not conserve physical photons. [Bonetti et al. 2020](https://doi.org/10.1364/JOSAB.377891), full text of conservation/model sections, demonstrates this and constructs a photon-conserving modification. Lægsgaard 2007 and Poletti–Horak 2008 are foundational must-reads for profile dispersion and multimode normalization. [Arduin–Lægsgaard 2021](https://doi.org/10.1364/JOSAB.432276), abstract only, proposes an efficient overlap-dispersion approximation benchmarked against quadrature in step-index and parabolic fibres. The newly located [Timmerkamp–Fallnich 2026](https://doi.org/10.1364/JOSAB.603100) is directly relevant; its full text was not retrieved, so no result beyond its bibliographic subject is attributed here.

[Blow–Wood 1989](https://doi.org/10.1109/3.40655) remains a primary-source access gap for the underlying transient Raman formulation; its photon-conservation role is identified by Bonetti's full text, not independently certified here. [Hult 2007](https://doi.org/10.1109/JLT.2007.909373), model/algorithm sections read, supplies the interaction-picture integration method and a GNLSE including shock and Raman. It is not a derivation of a new thermodynamic equilibrium.

[Ho–Kahn 2011](https://doi.org/10.1109/JLT.2011.2165316) derives group-delay statistics under strong mixing: delay spread grows diffusively with independent sections, whereas weakly coupled differences grow ballistically. This reduces some walk-off but cannot be used to erase delays between groups that the proposed disorder intentionally does not mix. Correlation bandwidth also matters for a broad pulse. Vector Kerr preserves total conservative invariants with the correct tensor; component powers, polarization and angular momentum require additional symmetries and generally do not survive arbitrary disorder.

## 6. Raman: known kinetics and the narrower remaining question

[Garnier–Picozzi 2010](https://doi.org/10.1103/PhysRevA.81.033831) develops kinetic theory for a noninstantaneous response. [Kibler et al. 2011](https://doi.org/10.1103/PhysRevE.84.066605) treats Raman spectral incoherent solitons. [Xu et al. 2014](https://doi.org/10.1103/PhysRevA.90.013828), full model text, includes the shock factor in Raman kinetic evolution and studies spectral shocks/singularities. Thus neither “Raman kinetic theory” nor “shock plus Raman statistics” is an empty field.

[Baudin et al. 2022](https://doi.org/10.1103/PhysRevA.105.013528), full text of derivation and relevant discussion, is especially close. Strong mixing of all modal/polarization components homogenizes linear coefficients and averages the Raman tensor. Its weak-Langmuir kinetic reduction produces drifting spectral structures. The leading instantaneous Kerr contribution vanishes in that ordering. This is not the proposed regime of fast inter-group Kerr RJ relaxation followed by weak Raman drift. Its no-shock normalization conserves optical power; that invariant must not be silently reinterpreted as exact broadband photon number.

Modal Raman gain is already described by overlap competition, including [Terry–Alley–Russell 2007](https://doi.org/10.1364/OE.15.017509) and [Antonelli–Mecozzi–Shtaif 2013](https://doi.org/10.1364/OL.38.001188). Raman laser cleanup also involves pump depletion, filtering and cavity gain/loss; [Babin et al. 2021](https://doi.org/10.1038/s41598-021-01491-0) is an example. Such driven steady states must not be labelled passive RJ equilibria. [Dupiol et al. 2018](https://arxiv.org/abs/1801.03649) explicitly reports competition between Kerr pump cleaning and Raman Stokes cleanup.

Raman-assisted concentration can mean several different things: low-mode Stokes gain, red-moving incoherent spectral concentration, coherent soliton attraction, or a driven laser condensate. None by itself establishes adiabatic motion on a Kerr RJ manifold. The 2024 weighted-BE paper supplies a statistical description with conservation assumptions, not a parameter-derived slow longitudinal drift. [Gemechu–Zitelli 2026](https://doi.org/10.1364/AO.585354) reports Raman depletion of the fundamental toward higher modes in a few-mode setting; it directly rules out an unrestricted claim of low-mode preference.

For a scalar constant-overlap test, let $I=|A|^2$, $Q=R*I$, and

$$
A_z=i\gamma AQ-\frac{\gamma}{\omega_0}\partial_t(AQ).
$$

With decaying temporal boundaries, direct integration gives

$$
\frac{d\mathcal E}{dz}=-\frac{\gamma}{\omega_0}\int I\,\partial_tQ\,dt.
$$

Using $Q=I-T_RI_t+\cdots$ gives $d\mathcal E/dz=-(\gamma T_R/\omega_0)\int I_t^2dt+\cdots$, while physical $N$ survives. This limiting identity is checked in the run; it is not a new Raman theory. A multimode drift requires the cross-mode Raman tensor and correlations, not the sum of isolated-soliton redshift formulas. The reduced optical subsystem is open to phonons; an enlarged light–matter Hamiltonian is compatible with this optical dissipation.

**Search-bounded gap:** the searches below did not locate a coefficient-derived drift of the three canonical local-equilibrium moments, with a transverse-to-equilibrium error/lifetime criterion, for weak intra-group disorder in a finite GRIN pulse. Existing scalar Langmuir kinetics, all-mode strong-coupling Raman theory and coherent multimode-soliton moment models substantially limit the novelty. The missing full texts may narrow it further.

## 7. Verdicts on the orchestrator's leads

| Lead | Verdict |
|---|---|
| **L1** | **Correct in a restricted photon-conserving model, substantially prior art.** $N,\mathcal E,H$ survive instantaneous Kerr plus simple shock; $P=\mathcal E-\omega_0N$ is the canonical momentum. The generalized RJ family in photon variables is known. A universal first-order change in band-integrated modal fractions is wrong: an odd first-order spectral tilt integrates to zero on a symmetric band when the leading spectrum and constraints have the corresponding symmetry. Frequency-dependent vertices need additional care. |
| **L2** | **Restricted integrability statements largely correct; the platform conclusion needs qualification.** Scalar quadratic-dispersion Kerr plus simple shock maps to derivative NLS; isotropic common-dispersion Manakov is integrable. Multiple unequal groups, frequency-dependent profiles/coupling and generic HOD are different. Raman drives an optical nonequilibrium process, not equilibrium thermalization. Weakly disordered GRIN with independently calibrated inter-group leakage is the clearest starting platform among those reviewed, but its broadband invariant/rate window must be demonstrated. |
| **L3** | **Plausible conditional reduction, not an established general law.** Photon-conserving Raman transfers optical energy to matter, so a passive, nontrivial fixed RJ distribution is generally not stationary. Slow multiplier drift requires a fast collision gap, weak Raman residual, controlled band/gate flux and negligible extra invariants. Neither the sign of optical temperature drift nor growth of fundamental occupation follows from redshift alone. |
| **L4** | **Correct ultraviolet obstruction, with sign and model qualifications.** A quadratic one-frequency RJ tail has finite norm but divergent propagation-energy integral on an unbounded continuum. Use a moving local equilibrium or an explicitly open measured band, not an FFT cutoff declared physical. The dispersion-sign convention affects positive/negative temperatures and which spatial group is favoured. Quantum BE occupation supplies a different ultraviolet completion, not validation of a classical finite-pulse fixed point. |

The scalar UV integrals and symmetry cancellation were checked in the registered symbolic run. With photon normalization, the finite RJ “norm” is $N$, not automatically optical energy: formally extending $n_\psi\sim\Omega^{-2}$ to arbitrarily large positive frequencies also makes $\int(\omega_0+\Omega)n_\psi d\Omega$ logarithmically divergent. The first-order shock envelope model is not valid in that limit anyway. Normal-dispersion silica should not be promised fundamental-mode **joint** condensation merely because its spatial-only experiment cleans a beam.

## 8. A concrete derivation handoff

Take the photon-normalized equilibrium $n_{\theta,p}(\Omega)=1/[\theta_0+\theta_1\Omega+\theta_2\epsilon_p(\Omega)]$ on a stated band and a central temporal gate over which the local multipliers are approximately uniform. A mixture of substantially different local RJ states need not itself be RJ; in that case retain $t$-dependent transport under P-005 instead of forcing a single ODE. This is the known three-multiplier RJ family in a nonsingular parameterization. For $q=(1,\Omega,\epsilon)$, define $Q_i=\sum_p\int q_i n_p$ and $\chi_{ij}=\sum_p\int q_iq_j n_{\theta,p}^2$. If the fast conservative collision operator has the required gap on the complement of these moments, projection gives the **starting ansatz**

$$
-\chi(\theta)\,\partial_z\theta
=F_R(\theta)+F_{\rm disorder}(\theta)-\Phi_{\rm band}-\Phi_{\rm gate}.
$$

Here $F_i=\sum_p\int q_i\,\mathcal C[n_\theta]_p$ must be derived from the correct response/coupling model. The non-equilibrium correction should solve

$$
\delta n=-\mathcal L_K^{-1}(I-\Pi)\big(\mathcal C_R+\mathcal C_{\rm disorder}\big)[n_\theta]+\cdots,
$$

with explicit norm, null space and boundary conditions. These formulas are a proposed organization of the work, not a verified closure. Calculate the leading band modal-fraction derivative and a validity length; a successful result must beat independently refitting RJ at every distance. If the collision gap closes or disorder drives $H_2$ as fast as Kerr relaxation, report that failure rather than assigning a temperature.

The ratio $T_R/T_0$ alone is misleading: the comparison is approximately $(L_{\rm kin}/L_{\rm NL})(T_R/t_c)$ for a spectral-drift scale, with $t_c$ the fluctuation/coherence time and $T_{\rm env}$ the pulse-envelope scale. The run gives $T_R=1.462$ fs for the specified single-oscillator silica response, not a universal Raman time. For illustrative $L_{\rm kin}/L_{\rm NL}=10$–100 and $t_c=100$ fs the resulting screening ratio is about 0.15–1.46. That arithmetic warns that “small Raman” at one nonlinear length need not remain small over equilibration. It does not measure a physical rate. Longer pulses or faster experimentally verified mixing may provide a window.

## 9. Repository boundaries and oracle audit

P-005 should eventually cite the 2026 baseline and explicitly distinguish isolated finite envelopes from stationary incoherent waves; this review does not change its status. P-010 retains detector-defined self-cleaning thresholds. P-20261016-claude-interactive.7-01 retains quantum states and counting statistics. If the only progress obtained is a general finite-envelope collision closure, it belongs in P-005 rather than the new card.

R-0007–R-0010 and the thermalization-statistics manuscript were inspected for scope. R-0007 is a conditional classical shell identity with restricted dynamical evidence; the other results concern restricted squeezing statements. The manuscript distinguishes its scalar spatial-group Brownian model from published polarization disorder. **C-20261016-claude-interactive.7-03 is not a verified general GGE endpoint:** its status is `cheap-checks-passed`, and the independent audit leaves convergence unresolved. Preserved resonant invariants and phase memory must be retained as a risk, but not converted into an accepted endpoint theorem.

At agents-copy solver commit `b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa`:

- Deterministic multimode shock **already exists**: `src/mmgnlse_solver.jl:448–450` constructs the factor `omega + parameters.omega0`; lines 591–603 apply it to the Kerr/Raman cubic. Legacy/CP propagation uses the same frequency dependence. The orchestrator's word-search inference was incorrect.
- `AgarwalRaman` and `AnisotropicRaman` exist in `src/mmgnlse_types.jl`; vector/component overlap and modal dispersion support are present. The public linear operator is diagonal in components.
- No random linear mode-coupling operator was found in `src/` or `docs/`, after searches for random coupling, birefringence, Hermitian coupling and coupling matrices, plus inspection of the linear RHS. Raman Langevin noise is not random linear mode mixing.
- The public overlap object is a fixed modal/component tensor, not a general four-frequency vertex. The deterministic frequency damping window also modifies the formal prefactor near the grid edge; invariants must be tested in a resolved interior band and under bandwidth refinement.
- Missing oracle work: calibrated Hermitian colored coupling, correct vector covariance, broadband photon/energy diagnostics, a Raman kinetic evaluator and band/gate flux accounting. These are future additions to the agents' copy only. No solver file was changed.

## 10. Source ledger

Access was checked on **2026-10-20**. `full text` means the indicated full-text passages were read, not necessarily the entire paper. `abstract only` means no derivation is independently certified. `not accessed` means a bibliographic record or citation was located but neither the paper's derivation nor its abstract was read from an accepted primary source. The required Zanaglia baseline is the exception explicitly read **in its entirety**, including appendices. There are no direct quotations in this review.

PDFs, extracted text and download logs are outside git in `~/analytical-nl-discovery-data/lit-T-20261020-claude-interactive-01/`. The file stems below identify the local copies. A download alone is not counted as reading. Publisher pages, arXiv, author pages and institutional repositories supplied the evidence; search-engine snippets from other sites were used only to discover legitimate sources.

### Spatial thermodynamics, pulsed evidence and the spatiotemporal baseline

| Source and persistent identifier | Access and reading extent | What it establishes; limit for this task |
|---|---|---|
| Wu, Hassan & Christodoulides 2019, [DOI:10.1038/s41566-019-0501-8](https://doi.org/10.1038/s41566-019-0501-8), arXiv:1912.08270 | **full text**, `wu2019`, main pp. 1–5 | Entropy, RJ equation of state and thermodynamic processes for finite spatial modes under weak nonlinearity and assumed ergodicity; CW/broad-pulse premise. |
| Baudin et al. 2020, [DOI:10.1103/PhysRevLett.125.244101](https://doi.org/10.1103/PhysRevLett.125.244101) | **abstract only**, publisher | Experimental RJ condensation and thermodynamic characterization, including heat capacity. No independent audit of its supplemental pulse treatment here. |
| Baudin et al. 2023, [DOI:10.1103/PhysRevLett.130.063801](https://doi.org/10.1103/PhysRevLett.130.063801), arXiv:2301.02796 | **full text**, author PDF `baudin2023`, main pp. 1–3 | Subnanosecond spatial negative-temperature populations; ensemble reconstruction and bounded spatial eigenvalues. |
| Pourbeyram et al. 2022, [DOI:10.1038/s41567-022-01579-y](https://doi.org/10.1038/s41567-022-01579-y), arXiv:2012.12110 | **full text**, `pourbeyram2022`, main experiment and supplemental temporal/model passages, including §§6–8 | Femtosecond modal RJ measurements with spectral resolution; documents normal-dispersion evolution and later Raman asymmetry. |
| Mangini et al. 2022, [DOI:10.1364/OE.449187](https://doi.org/10.1364/OE.449187), arXiv:2111.08063 | **full text**, `mangini2022`, theory and pulse/measurement sections | Monochromatic statistical derivation compared with spatial measurements across femtosecond, picosecond and longer pulses. |
| Ferraro et al. 2024, [DOI:10.1103/PhysRevX.14.021020](https://doi.org/10.1103/PhysRevX.14.021020), arXiv:2212.12781 | **full text**, `ferraro2024`, experiment and appendices on source/filtering | Photon-gas calorimetry with polarization-resolved spatial populations and picosecond excitation. |
| Ferraro et al. 2025 review, [DOI:10.1016/j.physd.2025.134758](https://doi.org/10.1016/j.physd.2025.134758), arXiv:2505.11299v1 | **full text**, `2505.11299v1`, abstract and selected §§2–3, particularly PDF pp. 19–20 and 38–41 | Reviews kinetic disorder regimes, equilibrium experiments, detector integration and limitations of spatial thermalization evidence. |
| Zanaglia et al. 2026, PRL 136, 053802, [DOI:10.1103/mqzh-w2gh](https://doi.org/10.1103/mqzh-w2gh), [arXiv:2506.23536v2](https://arxiv.org/abs/2506.23536) | **full text, all 18 PDF pages**, `2506.23536v2`; equation page also visually inspected | Joint stationary mode–frequency kinetics, canonical shock weighting, generalized RJ, spectral-front expansion and cooling. It already solves much of L1 and the stationary baseline of L4. |
| Zanaglia et al. quantum companion, [arXiv:2512.07784v1](https://arxiv.org/abs/2512.07784) | **full text**, `2512.07784v1`, model, BE/RJ and conclusion passages | Quantum equilibrium completion; positive/negative-temperature branches depend on dispersion sign. No disorder-assisted finite-pulse Raman drift is derived. |
| Picozzi et al. 2014 review, [DOI:10.1016/j.physrep.2014.03.002](https://doi.org/10.1016/j.physrep.2014.03.002) | **full text**, author PDF `picozzi2014`, selected §§3, 5.4, 6, 7; PDF pp. 20–22, 27–29, 74–77, 86, 93–94, 99–100, 102 and reference trails | Derives delayed-response kinetics, shock canonical variables, restricted spectral relaxation, and driven-cavity distinctions. The whole 132-page review was not read. |
| Zitelli, Mangini & Wabnitz 2024, [DOI:10.1038/s41467-024-45185-3](https://doi.org/10.1038/s41467-024-45185-3), arXiv:2306.15995 | **full text**, `zitelli2024`, entropy, experiment and group-delay sections, pp. 3–6 | Weighted-BE modal statistics and long-fibre pulse-group measurements; coherent/quasi-soliton and Raman regimes require separate interpretation. |
| Zitelli, online 2024 / journal-volume 2025 formulation, [DOI:10.1002/lpor.202400714](https://doi.org/10.1002/lpor.202400714), [arXiv:2404.00480v1](https://arxiv.org/abs/2404.00480) | **full text**, local stem `zitelli2025` contains the **2024 v1 preprint**, pp. 1, 3–4; published institutional record also located | Weighted-BE state equation and entropy/error metric; comparison of cleaning and soliton data, not a derived slow Raman flow. |
| Kabat et al. 2026, [arXiv:2602.13161](https://arxiv.org/abs/2602.13161) | **abstract only**, arXiv | Extends optical thermodynamics beyond weak nonlinearity; relevant boundary on weak-wave assumptions, not a solution of this pulsed disorder/Raman question. |

### Disorder, averaging and modal delays

| Source and persistent identifier | Access and reading extent | What it establishes; limit for this task |
|---|---|---|
| Fusaro et al. 2019, [DOI:10.1103/PhysRevLett.122.123902](https://doi.org/10.1103/PhysRevLett.122.123902), arXiv:2011.05111 | **full text**, author PDF `fusaro2019`, main model/rate/experiment passages | Weak-disorder acceleration of spatial thermalization and condensation; not an ultrashort rate measurement. |
| Garnier et al. 2019, [DOI:10.1103/PhysRevA.100.053835](https://doi.org/10.1103/PhysRevA.100.053835), arXiv:2011.03918 | **full text**, `garnier2019`, pp. 1–9 and correlated-noise discussion | Polarization covariance, closure, discrete versus spatial-continuum kinetic equations, rate scaling and correlation dependence. |
| Berti et al. 2022, [DOI:10.1103/PhysRevLett.129.063901](https://doi.org/10.1103/PhysRevLett.129.063901), arXiv:2207.08680 | **full text**, `berti2022`, main pp. 1–3 | Competition of nonlinear RJ relaxation with disorder-driven power equipartition; transient rather than automatic permanent RJ. |
| Zitelli 2026, [arXiv:2601.16998v1](https://arxiv.org/abs/2601.16998) | **full text**, `2601.16998v1`, model and experimental/discussion pp. 1–3, 7–10 | Reports non-uniform linear-disorder distributions and weighted-BE interpretation. Normalization, completeness and losses are explicit audit questions in §2. |
| Sidelnikov et al. 2019, [DOI:10.1016/j.yofte.2019.101994](https://doi.org/10.1016/j.yofte.2019.101994), arXiv:1908.07745 | **full text**, `sidelnikov2019`, abstract and coupled-mode model pp. 1–3 | Tests random all-mode versus degenerate-mode coupling in cleaning; spatial model. |
| Mecozzi, Antonelli & Shtaif 2012, strong coupling, [DOI:10.1364/OE.20.011673](https://doi.org/10.1364/OE.20.011673), arXiv:1203.6275 | **full text**, `mecozzi2012`, pp. 1–3 | Isotropic generalized Manakov equation and averaging coefficient for a common strongly mixed group; explicitly restricted dispersion model. |
| Mecozzi, Antonelli & Shtaif 2012, coupled groups, [DOI:10.1364/OE.20.023436](https://doi.org/10.1364/OE.20.023436) | **abstract only**, Tel Aviv University record; publisher returned a wait page | Coupled Manakov equations for quasi-degenerate groups and nonlinear modal-delay compensation. Its full coefficients were not checked here. |
| Mumtaz, Essiambre & Agrawal 2013, [DOI:10.1109/JLT.2012.2231401](https://doi.org/10.1109/JLT.2012.2231401), arXiv:1207.6645 | **full text**, `mumtaz2013`, introductory/model/averaging passages and multicore discussion | Vector equations under weak and strong mixing, fixed overlaps and coupled-core applications. Averaging is not proof of thermodynamic relaxation. |
| Ho & Kahn 2011, [DOI:10.1109/JLT.2011.2165316](https://doi.org/10.1109/JLT.2011.2165316), arXiv:1104.4527 | **full text**, author PDF `ho2011`, pp. 1–3 | Random-matrix modal group-delay statistics and square-root length scaling in strong coupling. |
| Antonelli, Mecozzi & Shtaif 2013, group coupling, [DOI:10.1364/OE.21.009484](https://doi.org/10.1364/OE.21.009484) | **abstract only**, plus publisher introduction/conclusion excerpts | Linear inter-group coupling depends on propagation mismatch and correlation scales; useful covariance calibration context. |
| Ermann, Chepelianskii & Shepelyansky, 2025 preprint / 2026 journal, [arXiv:2506.06534v3](https://arxiv.org/abs/2506.06534), DOI:10.1088/1751-8121/ae3ebe | **full text**, `ermann2026`, abstract and introductory model pp. 1–2 | D-shaped nonlinear-wave thermalization above a chaos threshold; spatial simulations, no broadband disorder covariance or measured pulsed rate. |
| Localization-hindered thermalization, 2023, [DOI:10.1038/s42005-023-01309-7](https://doi.org/10.1038/s42005-023-01309-7) | **abstract only**, publisher | Static disorder/localization can obstruct thermalization. It cannot be identified with longitudinal polarization noise. |

### Shock, Raman, integrability and broadband field equations

| Source and persistent identifier | Access and reading extent | What it establishes; limit for this task |
|---|---|---|
| Barviau, Kibler & Picozzi 2009, [DOI:10.1103/PhysRevA.79.063840](https://doi.org/10.1103/PhysRevA.79.063840) | **abstract only**, publisher; derivation read through the authors' 2014 review | Shock/HOD wave-turbulence treatment and modified equilibrium spectra. Original full text requested from PI. |
| Blow & Wood 1989, [DOI:10.1109/3.40655](https://doi.org/10.1109/3.40655) | **not accessed**; bibliographic identification in Hult/Bonetti and IEEE locator; IEEE verification page blocked reading | Foundational transient Raman model. Exact original assumptions await full text; no independent derivation is attributed from this session. |
| Hult 2007, [DOI:10.1109/JLT.2007.909373](https://doi.org/10.1109/JLT.2007.909373) | **full text**, Cambridge author PDF `hult2007`, pp. 1–2 | Interaction-picture RK method and a GNLSE with Raman/shock. Numerical method, not new thermodynamic variables. |
| Lægsgaard 2007, [DOI:10.1364/OE.15.016110](https://doi.org/10.1364/OE.15.016110) | **not accessed**, DTU bibliographic record only; attempted PDF was non-PDF | Mode-profile-dispersion formulation located; its rescaling and invariant details remain a required check. |
| Poletti & Horak 2008, [DOI:10.1364/JOSAB.25.001645](https://doi.org/10.1364/JOSAB.25.001645) | **abstract only**, publisher and Southampton record; repository PDF returned HTTP 401 | Multimode vector GNLSE with HOD, shock, Raman and frequency-dependent coefficients; original symmetry derivation remains unread. |
| Bonetti et al. 2020, [DOI:10.1364/JOSAB.377891](https://doi.org/10.1364/JOSAB.377891) | **full text**, institutional PDF `bonetti2020`, conservation/model pp. 2–3 | Photon-conserving replacement for arbitrary frequency-dependent nonlinearity; explains why a naive output-frequency coefficient can fail. |
| Arduin & Lægsgaard 2021, [DOI:10.1364/JOSAB.432276](https://doi.org/10.1364/JOSAB.432276) | **abstract only**, publisher and institutional manuscript excerpt; PDF download HTTP 403 | Efficient overlap-dispersion approximation versus fixed overlap and quadrature. No invariant proof inferred from abstract. |
| Timmerkamp & Fallnich 2026, [DOI:10.1364/JOSAB.603100](https://doi.org/10.1364/JOSAB.603100) | **not accessed**, University of Münster metadata; OA designation, but publisher retrieval failed | Directly relevant multimode photon-conserving extension. Highest-priority missing normalization/novelty check. |
| Garnier & Picozzi 2010, [DOI:10.1103/PhysRevA.81.033831](https://doi.org/10.1103/PhysRevA.81.033831) | **abstract only**, publisher; related derivation read in the 2014 review | Unified kinetic description for noninstantaneous response, with regime-dependent kinetic/Vlasov limits. |
| Kibler, Michel et al. 2011, [DOI:10.1103/PhysRevE.84.066605](https://doi.org/10.1103/PhysRevE.84.066605) | **abstract only**, publisher; 2014 review provides context | Raman spectral incoherent solitons in supercontinuum, rather than static Kerr equilibrium. |
| Xu et al. 2014, [DOI:10.1103/PhysRevA.90.013828](https://doi.org/10.1103/PhysRevA.90.013828) | **full text**, author PDF `xu2014shock`, pp. 1–2 | Shock-weighted Raman kinetic equation; photon weighting and spectral-shock dynamics are already studied. |
| Baudin et al. 2022, [DOI:10.1103/PhysRevA.105.013528](https://doi.org/10.1103/PhysRevA.105.013528), arXiv:2111.05744 | **full text**, `baudin2022raman`, model/averaging/kinetic pp. 1–5 and relevant discussion | Weak Langmuir turbulence after strong all-mode mixing, including averaged Raman contractions. Different ordering from fast Kerr equilibration plus slow Raman. |
| Terry, Alley & Russell 2007, [DOI:10.1364/OE.15.017509](https://doi.org/10.1364/OE.15.017509) | **abstract only**, Air Force Institute of Technology author repository | Overlap-gain competition explains GRIN Stokes cleanup and its absence in the studied step-index case. |
| Antonelli, Mecozzi & Shtaif 2013, Raman amplification, [DOI:10.1364/OL.38.001188](https://doi.org/10.1364/OL.38.001188) | **abstract only**, publisher | Group-averaged Raman gain and equalization within strongly mixed groups. Full tensor derivation requested. |
| Dupiol et al. 2018, [arXiv:1801.03649](https://arxiv.org/abs/1801.03649) | **abstract only**, arXiv | Kerr pump cleaning and Raman Stokes cleanup can compete. |
| Babin et al. 2021, [DOI:10.1038/s41598-021-01491-0](https://doi.org/10.1038/s41598-021-01491-0) | **abstract only**, publisher | Raman-laser spatio-spectral control with filtering and Kerr cleaning; driven cavity context. |
| Gemechu & Zitelli 2026, [DOI:10.1364/AO.585354](https://doi.org/10.1364/AO.585354), arXiv:2510.14782 | **abstract only**, downloaded preprint `gemechu2026` | Raman can deplete fundamental occupation in a few-mode platform; counterexample to universal fundamental-mode preference. |
| Suret, Randoux, Jauslin & Picozzi 2010, [DOI:10.1103/PhysRevLett.104.054101](https://doi.org/10.1103/PhysRevLett.104.054101) | **not accessed**, identified in 2014 review; publisher retrieval failed | Local kinetic invariants and anomalous relaxation are described in the review; original derivation not independently read. |
| Suret, Picozzi & Randoux 2011, [DOI:10.1364/OE.19.017852](https://doi.org/10.1364/OE.19.017852) | **not accessed** from an allowed primary page; identified in 2014 review, publisher wait page | The review's §6.3 derives transient spectral relaxation of integrable NLS. No claim that integrability freezes all statistics. |
| Barviau et al. 2013, [DOI:10.1103/PhysRevA.87.035803](https://doi.org/10.1103/PhysRevA.87.035803) | **abstract only**, publisher; selected §6 of 2014 review read | HOD can restrict kinetic resonances and produce a bounded thermalized spectrum. This is distinct from an arbitrary computational cutoff. |
| Kaup & Newell 1978, [DOI:10.1063/1.523737](https://doi.org/10.1063/1.523737) | **not accessed**, author publication list and 2014 review locate it; publisher retrieval failed | Integrable derivative NLS reference. The mixed-NLS substitution itself was checked in this task's symbolic run. |
| Hirota 1973, [DOI:10.1063/1.1666399](https://doi.org/10.1063/1.1666399) | **not accessed**, located in primary-paper bibliographies; publisher retrieval failed | Fine-tuned higher-order integrable equation, not arbitrary cubic NLS plus TOD. |
| Sasa & Satsuma 1991, [DOI:10.1143/JPSJ.60.409](https://doi.org/10.1143/JPSJ.60.409) | **abstract only**, J-STAGE publisher | Inverse-scattering solvability of a particular higher-order optical equation. |
| Bandelow et al. 2018, [DOI:10.1063/1.5030604](https://doi.org/10.1063/1.5030604) | **abstract only**, AIP publisher | Lax-pair hierarchy with matched nonlinear/dispersive terms; substantiates why the exception is structured. |

### Competing pulse dynamics

| Source and persistent identifier | Access and reading extent | What it establishes; limit for this task |
|---|---|---|
| Wright et al. 2015, multimode solitons, [DOI:10.1364/OE.23.003492](https://doi.org/10.1364/OE.23.003492) | **abstract only**, Cornell author-group page | Real spatiotemporal soliton dynamics; belongs to the coherent-soliton neighbours. |
| Wright, Christodoulides & Wise 2015, [DOI:10.1038/nphoton.2015.61](https://doi.org/10.1038/nphoton.2015.61) | **abstract only**, publisher | Launch-dependent ultrashort anomalous-dispersion dynamics, dispersive waves and supercontinuum. |
| Krupa et al. 2017, [DOI:10.1038/nphoton.2017.32](https://doi.org/10.1038/nphoton.2017.32), arXiv:1603.02972 | **full text**, `krupa2017`, introduction and Methods pp. 1, 8 | Kerr self-cleaning; pulse-width versus modal-delay argument and pump-band filtering. |
| Liu et al. 2016, [DOI:10.1364/OL.41.003675](https://doi.org/10.1364/OL.41.003675) | **abstract only**, publisher | Femtosecond Kerr cleaning; does not by itself establish thermodynamic equilibrium. |
| Lopez-Galmiche et al. 2016, [DOI:10.1364/OL.41.002553](https://doi.org/10.1364/OL.41.002553) | **abstract only**, publisher | Low-DGD normal-dispersion multimode supercontinuum and intermodal mixing. |

### Forward citation checks and what was not established

The 2014 review's delayed-response and shock references were followed to the 2022 disordered Raman theory, then to the 2025 review and 2026 spatiotemporal papers. The normalization trail runs from Blow–Wood/Lægsgaard/Poletti–Horak through Bonetti 2020 and Arduin–Lægsgaard 2021 to the **August 2026** Timmerkamp–Fallnich record. The modal-statistics trail reaches weighted-BE state equations, the **January 2026** disorder preprint, and the **2026** few-mode Raman counterexample. Searches also found the 2026 strong-nonlinearity thermodynamics preprint. This is a search through the session date, not an exhaustive citation-index export.

No primary full text was established for a generic “Raman-assisted condensation” law applicable to the proposed passive pulse. The phrase searches returned driven laser, spectral-soliton and coherent modal-attraction work; these are recorded above without merging their meanings. Candidate abstracts concerning 2026 Raman depolarization and a 2025 random-birefringence ultrashort model were discovered but not verified from a primary full text and are not used as evidence for novelty or equations.

## 11. PI download list and tracked follow-up

The first four requests need institutional retrieval or an authorized author manuscript. A technical retrieval failure is not by itself proof that the paper is paywalled. **Do not sign in on the PI's behalf or circumvent access controls.**

| Priority/read | URL and reason | Current obstacle | Follow-up |
|---|---|---|---|
| Blow–Wood 1989 | [DOI:10.1109/3.40655](https://doi.org/10.1109/3.40655): check original photon/energy balance and Raman approximation | IEEE verification page; full text not read | [T-20261020-gpt-f-01](../tasks/T-20261020-gpt-f-01-obtain-and-audit-blow-wood-1989-photon-a.md) |
| Barviau et al. 2009 | [DOI:10.1103/PhysRevA.79.063840](https://doi.org/10.1103/PhysRevA.79.063840): pin down the already-known shock/HOD equilibrium and invariant assumptions | Publisher abstract available; HAL attempts failed | [T-20261020-gpt-f-02](../tasks/T-20261020-gpt-f-02-obtain-and-audit-barviau-2009-shock-and-.md) |
| Poletti–Horak 2008 | [DOI:10.1364/JOSAB.25.001645](https://doi.org/10.1364/JOSAB.25.001645): multimode vertex, polarization and broadband normalization | Publisher access required; legitimate repository PDF returned 401 | [T-20261020-gpt-f-03](../tasks/T-20261020-gpt-f-03-obtain-poletti-horak-2008-broadband-mult.md) |
| Antonelli–Mecozzi–Shtaif 2013 | [DOI:10.1364/OL.38.001188](https://doi.org/10.1364/OL.38.001188): derive the proper group-averaged Raman gain tensor | Publisher full text unavailable without access | [T-20261020-gpt-f-04](../tasks/T-20261020-gpt-f-04-obtain-antonelli-2013-group-averaged-ram.md) |
| Lægsgaard 2007 — OA retrieval help | [DOI:10.1364/OE.15.016110](https://doi.org/10.1364/OE.15.016110): profile-dispersion rescaling and approximation limits | Bibliography located; publisher returned non-PDF | [T-20261020-gpt-f-05](../tasks/T-20261020-gpt-f-05-retrieve-laegsgaard-2007-mode-profile-di.md) |
| **Timmerkamp–Fallnich 2026 — highest-priority OA retrieval help** | [DOI:10.1364/JOSAB.603100](https://doi.org/10.1364/JOSAB.603100): may change the multimode photon-conserving model used for derivation | Münster marks it OA; only metadata and a publisher wait page obtained | [T-20261020-gpt-f-06](../tasks/T-20261020-gpt-f-06-retrieve-timmerkamp-fallnich-2026-photon.md) |

Other loose ends are [T-20261020-gpt-f-07](../tasks/T-20261020-gpt-f-07-establish-a-broadband-disorder-window-fo.md), for the broadband collision/leakage window and flux-normalization audit; [T-20261020-gpt-f-08](../tasks/T-20261020-gpt-f-08-specify-the-missing-random-coupling-and-.md), for a concrete oracle plan; and [T-20261020-gpt-f-09](../tasks/T-20261020-gpt-f-09-reconcile-p-005-with-the-2026-spatiotemp.md), for the P-005 literature boundary. The existing **T-20261020-claude-interactive-02** remains the second-family review and preliminary derivation task; no replacement was created.

## 12. Search and access record

The literal query list and access-attempt inventory below are part of the reproducibility record. All queries were issued on 2026-10-20 through the web search service; a `site:` term is an explicit domain restriction. Repeated queries are retained, including unsuccessful searches.

### Literal web queries

| Query | Site/scope | Literal text |
|---|---|---|
| Q001 | Web search, unrestricted domains | `Zanaglia Spatio temporal thermalization adiabatic cooling guided light waves 2506.23536` |
| Q002 | Web search, unrestricted domains | `arxiv 2512.07784 quantum thermalization` |
| Q003 | Web search, unrestricted domains | `arxiv 2601.16998 disorder non uniform distributions` |
| Q004 | Web search, unrestricted domains | `Ferraro Wave turbulence thermalization multimode locking optical fibers 2505.11299` |
| Q005 | Web search, unrestricted domains | `Fusaro 2019 Garnier 2019 thermalization disorder multimode fiber 123902 053835` |
| Q006 | Web search, unrestricted domains | `self steepening photon number Hamiltonian conservation Blow Wood 1989 Hult 2007 Laegsgaard 2007 Poletti Horak 2008` |
| Q007 | Web search, unrestricted domains | `Picozzi Garnier Michel Kibler Raman spectral incoherent solitons kinetic theory multimode 013528` |
| Q008 | Web search, unrestricted domains | `Sidelnikov 2019 random mode coupling beam self cleaning` |
| Q009 | Web search, unrestricted domains | `"self-steepening" "incoherent" "013828"` |
| Q010 | Web search, unrestricted domains | `"Blow" "Wood" "1989" "picosecond" theory transient` |
| Q011 | Web search, unrestricted domains | `"Hult" "2007" "interaction picture" "fourth-order"` |
| Q012 | Web search, unrestricted domains | `"Laegsgaard" "2007" "Mode profile dispersion"` |
| Q013 | Web search, unrestricted domains | `"Blow" "Wood" "Theoretical description of transient stimulated Raman scattering" 1989` |
| Q014 | Web search, unrestricted domains | `"Mode profile dispersion" "Laegsgaard" pdf` |
| Q015 | Web search, unrestricted domains | `"Description of ultrashort pulse propagation in multimode optical fibers" 2008` |
| Q016 | Web search, unrestricted domains | `"Weak Langmuir turbulence in disordered multimode optical fibers" arxiv` |
| Q017 | Web search, unrestricted domains | `"self steepening" "Kaup Newell" "modified nonlinear Schrodinger"` |
| Q018 | Web search, unrestricted domains | `"mixed nonlinear Schrödinger" "Kaup" integrable cubic derivative` |
| Q019 | Web search, unrestricted domains | `"Raman-assisted" "condensation" optical` |
| Q020 | Web search, unrestricted domains | `"thermalization" "Raman" multimode 2025 2026` |
| Q021 | Web search, unrestricted domains | `"Direct observations of thermalization" "200" "femtosecond"` |
| Q022 | Web search, unrestricted domains | `"Statistical mechanics of beam self-cleaning" "174" "7.6"` |
| Q023 | Web search, unrestricted domains | `"Calorimetry of photon gases" "pulse" arxiv` |
| Q024 | Web search, unrestricted domains | `"Thermodynamic theory of highly multimoded nonlinear optical systems" arxiv` |
| Q025 | Web search, unrestricted domains | `Pourbeyram Sidorenko Wu Wright thermalization Rayleigh Je​ans 2022 arxiv` |
| Q026 | Web search, unrestricted domains | `Ferraro Mangini Calorimetry photon gases 2024 arxiv` |
| Q027 | Web search, unrestricted domains | `Ho Kahn statistics group delays multimode fiber strong coupling 2011 arxiv` |
| Q028 | Web search, unrestricted domains | `thermalization chaotic D shaped optical fiber coupled core multicore mixing rate` |
| Q029 | Web search, unrestricted domains | `"Raman-assisted" "optical" "condensation" fiber` |
| Q030 | Web search, unrestricted domains | `"Raman" "condensation" "kinetic" optical fibers` |
| Q031 | Web search, unrestricted domains | `"chaotic" "D-shaped" "thermalization" fiber` |
| Q032 | Web search, unrestricted domains | `"coupled-core" "thermalization" nonlinear` |
| Q033 | Web search, unrestricted domains | `"Dynamical thermalization, Rayleigh" "Ermann" arxiv` |
| Q034 | Web search, unrestricted domains | `"Raman-accelerated power depletion" few-mode 2026` |
| Q035 | Web search, unrestricted domains | `"multicore fiber" "thermalization" Kerr` |
| Q036 | Web search, unrestricted domains | `"self-steepening" "thermalization" optical kinetic` |
| Q037 | Web search, explicit domain in query | `"Mode profile dispersion in the generalised nonlinear" site:orbit.dtu.dk` |
| Q038 | Web search, explicit domain in query | `"Theoretical description of transient stimulated Raman" site:ieeexplore.ieee.org` |
| Q039 | Web search, unrestricted domains | `"Self-steepening" "higher-order dispersion" "Barviau" 2009` |
| Q040 | Web search, unrestricted domains | `"Raman beam cleanup" "Terry" "Rogers" 2007` |
| Q041 | Web search, unrestricted domains | `"Raman beam cleanup" fiber Terry Rogers 2007` |
| Q042 | Web search, unrestricted domains | `"Raman beam cleanup" statistical theory multimode` |
| Q043 | Web search, unrestricted domains | `"Raman assisted condensation" fiber` |
| Q044 | Web search, unrestricted domains | `"Zitelli" "Statistics of modal condensation" 45185` |
| Q045 | Web search, unrestricted domains | `"Multimode photon-conserving nonlinear Schrödinger equation for frequency-dependent nonlinearities"` |
| Q046 | Web search, unrestricted domains | `"Photon conserving" "Timmerkamp" Fallnich` |
| Q047 | Web search, unrestricted domains | `"Description of ultrashort pulse propagation" "pdf" Poletti Horak` |
| Q048 | Web search, unrestricted domains | `"Raman beam cleanup in multimode optical fibers" Terry Rogers 2007` |
| Q049 | Web search, unrestricted domains | `"10.1364/JOSAB.603100"` |
| Q050 | Web search, unrestricted domains | `"Timmerkamp" "photon-conserving" arxiv` |
| Q051 | Web search, unrestricted domains | `"Photon-conserving generalized nonlinear" "Bonetti" 2020` |
| Q052 | Web search, unrestricted domains | `"Wave-turbulence approach of supercontinuum generation" pdf` |
| Q053 | Web search, unrestricted domains | `"Coupled Manakov equations" "2012" arxiv` |
| Q054 | Web search, unrestricted domains | `"An explanation of SRS beam cleanup" doi` |
| Q055 | Web search, unrestricted domains | `"Spatio-spectral beam control" "2021" doi` |
| Q056 | Web search, unrestricted domains | `"Impact of random birefringence on nonlinear ultrashort"` |
| Q057 | Web search, unrestricted domains | `"Coupled Manakov equations in multimode fibers with strongly coupled groups of modes" Mecozzi` |
| Q058 | Web search, unrestricted domains | `"Kerr self-cleaning of femtosecond-pulsed beams" Liu 2016` |
| Q059 | Web search, unrestricted domains | `"Spatiotemporal dynamics of multimode optical solitons" Wright 2015` |
| Q060 | Web search, unrestricted domains | `"Lopez-Galmiche" "2016" "supercontinuum"` |
| Q061 | Web search, explicit domain in query | `Coupled Manakov strongly coupled groups modes Mecozzi Antonelli Shtaif 23436 site:opg.optica.org` |
| Q062 | Web search, explicit domain in query | `Kerr self cleaning femtosecond pulsed beams Liu Wright 2016 site:opg.optica.org` |
| Q063 | Web search, explicit domain in query | `Lopez Galmiche 2016 2553 multimode fiber site:opg.optica.org` |
| Q064 | Web search, explicit domain in query | `Geng random birefringence 576472 site:opg.optica.org` |
| Q065 | Web search, unrestricted domains | `"Raman" "condensation" "Picozzi" "2010"` |
| Q066 | Web search, unrestricted domains | `"Raman-assisted condensation" photons` |
| Q067 | Web search, unrestricted domains | `"Raman" "modal attraction" "Zitelli"` |
| Q068 | Web search, unrestricted domains | `"negative temperature" "thermalization" multimode fiber 2025 2026` |
| Q069 | Web search, unrestricted domains | `"Theoretical description of transient stimulated Raman scattering" Blow Wood` |
| Q070 | Web search, unrestricted domains | `"Raman amplification in multimode fibers with random mode coupling"` |
| Q071 | Web search, unrestricted domains | `"Mode profile dispersion in the generalised nonlinear Schrödinger equation" Laegsgaard` |
| Q072 | Web search, unrestricted domains | `"Multimode photon-conserving" Timmerkamp Fallnich 603100` |
| Q073 | Web search, unrestricted domains | `"Classical Rayleigh-Jeans Condensation" Baudin 2020 arxiv` |
| Q074 | Web search, unrestricted domains | `"Optical kinetic theory of nonlinear multimode photonic networks" arxiv` |
| Q075 | Web search, unrestricted domains | `"Thermalization" "Raman" "Rayleigh-Jeans" drift` |
| Q076 | Web search, unrestricted domains | `"Raman" "optical thermodynamics" 2026` |
| Q077 | Web search, unrestricted domains | `"Suret" "Randoux" "Anomalous thermalization" optical 2010` |
| Q078 | Web search, unrestricted domains | `"Truncated thermalization" "2013" Barviau Garnier` |
| Q079 | Web search, unrestricted domains | `"Optical thermodynamics beyond the weak nonlinearity limit" 2026 arxiv` |
| Q080 | Web search, explicit domain in query | `"Mode profile dispersion" site:backend.orbit.dtu.dk` |
| Q081 | Web search, explicit domain in query | `"An explanation of SRS beam cleanup" site:scholar.afit.edu` |
| Q082 | Web search, unrestricted domains | `"Approximation of mode profile dispersion" Arduin Lægsgaard` |
| Q083 | Web search, unrestricted domains | `"Controllable spatiotemporal nonlinear effects in multimode fibres"` |
| Q084 | Web search, unrestricted domains | `"Visible supercontinuum generation" "Lopez-Galmiche" 2553` |
| Q085 | Web search, unrestricted domains | `Kaup Newell 1978 exact solution derivative nonlinear Schrodinger 798 DOI` |
| Q086 | Web search, unrestricted domains | `Sasa Satsuma higher order nonlinear Schrodinger equation 1991 409 integrability` |
| Q087 | Web search, unrestricted domains | `Hirota 1973 exact envelope soliton nonlinear wave equation 805 809` |
| Q088 | Web search, unrestricted domains | `Mecozzi Antonelli Shtaif coupled Manakov 2012 23436 abstract` |
| Q089 | Web search, explicit domain in query | `"An exact solution for a derivative nonlinear" site:pubs.aip.org` |
| Q090 | Web search, explicit domain in query | `"Exact envelope-soliton solutions" site:pubs.aip.org` |
| Q091 | Web search, explicit domain in query | `"Coupled Manakov equations" site:arxiv.org` |
| Q092 | Web search, explicit domain in query | `"Spatial beam self-cleaning in multimode fibres" site:arxiv.org` |
| Q093 | Web search, unrestricted domains | `"Mecozzi" "23436"` |
| Q094 | Web search, unrestricted domains | `"Timmerkamp" "603100" pdf` |
| Q095 | Web search, unrestricted domains | `"Lægsgaard" "16110" pdf` |
| Q096 | Web search, unrestricted domains | `"Poletti" "Horak" "1645" pdf soton` |
| Q097 | Web search, unrestricted domains | `"Anomalous thermalization of nonlinear wave systems"` |
| Q098 | Web search, unrestricted domains | `"Wave turbulence in integrable systems" Suret Picozzi Randoux` |
| Q099 | Web search, unrestricted domains | `"Truncated thermalization" "035803"` |
| Q100 | Web search, unrestricted domains | `"A New Thermodynamic Approach" Zitelli 2025` |
| Q101 | Web search, explicit domain in query | `"10.1103/PhysRevLett.104.054101" site:link.aps.org` |
| Q102 | Web search, explicit domain in query | `"10.1364/OE.19.017852" site:opg.optica.org` |
| Q103 | Web search, explicit domain in query | `"10.1103/PhysRevA.87.035803" site:link.aps.org` |
| Q104 | Web search, explicit domain in query | `"Blow" "Wood" "40655" site:ieeexplore.ieee.org` |

**Search outcomes and failures:** Q001–Q008 located the baseline/disorder/Raman families; Q009–Q018 checked normalization and integrability; Q019–Q044 explored alternative mixing, pulsed evidence and Raman/condensation terminology; Q045–Q072 followed normalization and multimode Raman references forward; Q073–Q080 checked thermodynamics and integrable-spectrum trails; Q081–Q100 verified bibliographic identities, pulse assumptions and original references. The Q101–Q104 domain-restricted batch returned **no search results**; direct publisher opens subsequently recovered the Barviau 2013 abstract, while the other accesses remained blocked or incomplete. Several earlier queries returned irrelevant records, especially unqualified “Raman-assisted condensation” and multicore searches; those records were excluded, not treated as evidence of absence.

### Direct page requests

| Requested page | Outcome / evidence used |
|---|---|
| [Page 1](https://arxiv.org/html/2506.23536v2) | Requested baseline HTML; full reading used the matching 18-page PDF. |
| [Page 2](https://arxiv.org/html/2512.07784v1) | Requested quantum-companion HTML; selected full-text reading used the matching PDF. |
| [Page 3](https://arxiv.org/html/2601.16998v1) | Requested disorder-preprint HTML; model and discussion read from PDF. |
| [Page 4](https://arxiv.org/html/2505.11299v1) | Requested review HTML; selected full-text reading used PDF. |
| [Page 5](https://opg.optica.org/josab/abstract.cfm?uri=josab-25-10-1645) | Publisher abstract available; full text inaccessible. |
| [Page 6](https://orbit.dtu.dk/en/publications/mode-profile-dispersion-in-the-generalised-nonlinear-schr%C3%B6dinger-/) | Tool access failed; later search recovered the DTU bibliographic record. |
| [Page 7](https://eprints.soton.ac.uk/65472/) | Initial tool access failed; ordinary HTTP later returned the public record and its PDF link. |
| [Page 8](https://doi.org/10.1109/3.40655) | DOI request inaccessible in tool. |
| [Page 9](https://opg.optica.org/josab/abstract.cfm?doi=10.1364/JOSAB.603100) | Publisher DOI-form request inaccessible; metadata located at Münster. |
| [Page 10](https://www.nature.com/articles/s41467-024-45185-3) | Publisher article located; detailed reading used arXiv PDF. |
| [Page 11](https://pmc.ncbi.nlm.nih.gov/articles/PMC8578583/) | Verification/captcha response; no bypass. Publisher abstract used instead. |
| [Page 12](https://opg.optica.org/josab/abstract.cfm?uri=josab-43-8-1819) | Publisher wait page; no article text. |
| [Page 13](https://opg.optica.org/oe/abstract.cfm?uri=oe-15-24-16110) | Publisher access did not yield the article PDF. |
| [Page 14](https://eprints.soton.ac.uk/65472/1/1658.pdf) | Attempted repository locator failed; later observed actual G.pdf link returned 401. |
| [Page 15](https://opg.optica.org/oe/abstract.cfm?uri=oe-20-21-23436) | Publisher redirected to a wait page; university abstract used. |
| [Page 16](https://doi.org/10.1063/1.523737) | Publisher DOI request inaccessible. |
| [Page 17](https://doi.org/10.1063/1.1666399) | Publisher DOI request inaccessible. |
| [Page 18](https://www.nature.com/articles/nphoton.2015.61) | Publisher abstract and subscription notice available. |
| [Page 19](https://link.aps.org/doi/10.1103/PhysRevLett.104.054101) | APS redirect failed with inaccessible/500 response. |
| [Page 20](https://opg.optica.org/oe/abstract.cfm?uri=oe-19-18-17852) | Publisher wait page. |
| [Page 21](https://link.aps.org/doi/10.1103/PhysRevA.87.035803) | APS abstract available; full article requires authorization. |
| [Page 22](https://ieeexplore.ieee.org/document/40655) | JavaScript/robot-verification page; no bypass. |

### PDF and repository retrieval attempts

The first four arXiv PDFs were downloaded before the structured download logs: saved versions `2506.23536v2`, `2512.07784v1`, `2601.16998v1` and `2505.11299v1`, all from arXiv. Subsequent attempts are enumerated below. Only PDF responses were saved as PDFs. A failed optional `requests` import caused no HTTP request; the download batch was rerun with Python's standard library.

| Local item | Requested URL | Result |
|---|---|---|
| `fusaro2019` | [josselin-garnier.org](https://josselin-garnier.org/wp-content/uploads/2019/06/fusaro19.pdf) | downloaded |
| `garnier2019` | [arxiv.org](https://arxiv.org/pdf/2011.03918) | downloaded |
| `berti2022` | [arxiv.org](https://arxiv.org/pdf/2207.08680) | downloaded |
| `baudin2022raman` | [josselin-garnier.org](https://josselin-garnier.org/wp-content/uploads/2022/02/pra22a.pdf) | downloaded |
| `xu2014shock` | [josselin-garnier.org](https://josselin-garnier.org/wp-content/uploads/2014/08/pra_selfsteepening.pdf) | downloaded |
| `sidelnikov2019` | [arxiv.org](https://arxiv.org/pdf/1908.07745) | downloaded |
| `mecozzi2012` | [arxiv.org](https://arxiv.org/pdf/1203.6275) | downloaded |
| `mumtaz2013` | [arxiv.org](https://arxiv.org/pdf/1207.6645) | downloaded |
| `hult2007` | [laser.ceb.cam.ac.uk](https://laser.ceb.cam.ac.uk/system/files/documents/pdf-a-fourth-order-runge-kutta-in-the-interaction-picture-method-for-simulating-supercontinuum-generation-in-optical-fibres.pdf) | downloaded |
| `picozzi2014` | [josselin-garnier.org](https://josselin-garnier.org/wp-content/uploads/2014/08/physrep14.pdf) | downloaded |
| `pourbeyram2022` | [arxiv.org](https://arxiv.org/pdf/2012.12110) | downloaded |
| `mangini2022` | [arxiv.org](https://arxiv.org/pdf/2111.08063) | downloaded |
| `ferraro2024` | [iris.uniroma1.it](https://iris.uniroma1.it/retrieve/718dbe77-3a47-42bc-9e27-b7985f52b6b9/Ferraro_Calorimetry_2024.pdf) | HTTP Error 403: Forbidden |
| `wu2019` | [arxiv.org](https://arxiv.org/pdf/1912.08270) | downloaded |
| `ho2011` | [ee.stanford.edu](https://ee.stanford.edu/~jmk/pubs/MMF.GD.statistics.JLT.pdf) | downloaded |
| `ermann2026` | [arxiv.org](https://arxiv.org/pdf/2506.06534) | downloaded |
| `gemechu2026` | [arxiv.org](https://arxiv.org/pdf/2510.14782) | downloaded |
| `ferraro2024` | [arxiv.org](https://arxiv.org/pdf/2212.12781) | OK |
| `zitelli2024` | [arxiv.org](https://arxiv.org/pdf/2306.15995) | OK |
| `barviau2009` | [hal.science](https://hal.science/hal-00449139/document) | HTTP Error 404: Not Found |
| `laegsgaard2007` | [opg.optica.org](https://opg.optica.org/oe/viewmedia.cfm?uri=oe-15-24-16110&seq=0) | non-PDF response |
| `timmerkamp2026` | [opg.optica.org](https://opg.optica.org/josab/viewmedia.cfm?uri=josab-43-8-1819&seq=0) | non-PDF response |
| `bonetti2020` | [ri.itba.edu.ar](https://ri.itba.edu.ar/bitstreams/c884d094-31f2-47ae-baf2-27d64a618e54/download) | OK |
| `barviau2009` | [hal.science](https://hal.science/hal-00447568/document) | HTTP Error 404: Not Found |
| `arduin2021` | [backend.orbit.dtu.dk](https://backend.orbit.dtu.dk/ws/files/266885825/OSA_template.pdf) | HTTP Error 403: Forbidden |
| `baudin2023` | [josselin-garnier.org](https://josselin-garnier.org/wp-content/uploads/2023/03/baudin23a.pdf) | 200; saved baudin2023.pdf |
| `krupa2017` | [arxiv.org](https://arxiv.org/pdf/1603.02972) | 200; saved krupa2017.pdf |
| `zitelli2025` | [arxiv.org](https://arxiv.org/pdf/2404.00480) | 200; saved zitelli2025.pdf |
| `soton-record` | [eprints.soton.ac.uk](https://eprints.soton.ac.uk/65472/) | 200; public metadata and PDF link only |
| `poletti2008` | [eprints.soton.ac.uk](https://eprints.soton.ac.uk/id/eprint/65472/1/G.pdf) | HTTP Error 401: Unauthorized |

The first HAL locator for Barviau 2009 was an incorrect lead; the corrected locator also failed. Neither is used as a citation to the paper. No credentials were entered, no paywall was bypassed, and no PDF/raw text was added to git.

### Repository screening

The requested local problem search used `raman|thermaliz|rayleigh|self-steep` over `problems/*.md`. Solver searches included `random.{0,30}(linear|mode|coupl)|birefringen|Hermitian|coupling_matrix`, Raman type names, shock/self-steepening terms and the frequency prefactor, followed by inspection of the actual linear and nonlinear RHS. `rg` was unavailable, so `grep` and Python were used. The specified results and manuscript were read only for their model and evidence scope; no claim, result or generated index was edited. No conversations or files from another project clone were accessed.
