---
agent: pi-chatgpt
model: gpt-6-pro
family: gpt
date: 2026-10-18
filed_by: claude-interactive (claude-opus-5-5, family claude), 2026-10-19, task T-20261019-claude-interactive-01
targets: [C-20261008-claude-a-02, C-20261010-claude-a-01, C-20261010-claude-b-01]
run: 2026-10-18-pi-chatgpt-independent-verification
---

# Independent verification of the similariton and normal-dispersion squeezing claims (GPT 6 Pro)

**What this is.**
- **The report.** The PI ran a ChatGPT session (GPT 6 Pro) on 2026-10-18. It inspected repository snapshot `970bfe7`, wrote its own solvers, and returned a 26-page report plus a reproducibility archive.
- **Where it is.** The archive is committed as run [`2026-10-18-pi-chatgpt-independent-verification`](../runs/2026-10-18-pi-chatgpt-independent-verification/) (raw files at the `raw_location` in its `meta.yaml`). The report is [`archive/report/independent_verification_report.pdf`](../runs/2026-10-18-pi-chatgpt-independent-verification/archive/report/independent_verification_report.pdf); this file summarizes it.
- **Independence.** The verifier is family gpt; all three target claims are family claude. It imported no repository solver or numerical output.
- **Not a clean-context audit.** It read the claims' derivation notes and scripts (report section 1), so it supports `sim-verified`, not `audited` (AGENTS.md rule 2).

**Checks by claude-interactive before filing** (run [`2026-10-19-claude-interactive-gpt6pro-quick-repro`](../runs/2026-10-19-claude-interactive-gpt6pro-quick-repro/)):
- **Archive integrity.** All 82 archive checksums verify. All 44 inventoried repository files match snapshot `970bfe7` once one trailing newline (added by the fetch) is accounted for. Every script was read before running; none uses the network, subprocesses, or writes outside its own folder.
- **Quick reproduction on a second platform** (macOS, Python 3.9, NumPy 2.0, SciPy 1.13):
  - the weak-dispersion Fourier cross-check gives $\lambda_{\min}=0.0265400309069$ ($7\times10^{-13}$ relative to the archive);
  - the short-gain similariton counterexample gives $\lambda_{\rm LO}=0.8964864655$ (same digits, commutator error $7\times10^{-14}$);
  - the oscillator constants agree to $4\times10^{-12}$;
  - the symbolic $c_2(\Phi)$ derivation is identical.
- **Consistency with the repository's own numbers:**
  - The matched-LO table P4 of C-20261008-claude-a-02 has $\varepsilon_0^2C_{PP}/G=3.81, 61.8, 701$ at $gL=2,4,6$. That growth is consistent with the report's $G^{7/3}/\varepsilon_0^2$ and contradicts the card's $G/\varepsilon_0^2$.
  - The weak-dispersion ratios (measured/leading) at $\Phi=3$, $y=10^{-6}$ to $10^{-2}$ are 1.00099, 1.0031, 1.0099, 1.031, 1.094. The card's are 1.0010, 1.0031, 1.0098, 1.031, 1.094.
  - The strong-dispersion coefficients $\Lambda(0.75)=0.86284$, $\Pi(0.75)=2.18007$ and $\Lambda(1.5)\approx0.3625$ agree with the card's table.
- **Algebra re-derived by hand:**
  - the short-gain criterion $d\lambda_{\rm LO}/dz|_{0^+}=2n_{sp}g-2\gamma\int P^2/\int P$, with $\int P^2/\int P=4P_0/5$ for a parabola;
  - the large-$\Phi$ limit $c_2\to2\sqrt6/5$.

## C-20261008-claude-a-02: amplifier-similariton shape noise

| Statement | Verdict (GPT 6 Pro) | Evidence (in the run's `archive/`) |
|---|---|---|
| Shape powers $G^{1/3}$ (intensity), $G^{5/3}$ (phase) | **Verified** in leading hydrodynamics, as variance envelopes of photon-normalized fixed low-order shape variables; rms powers $G^{1/6}$, $G^{5/6}$; log-gain oscillating prefactors | `similariton/`: reduced-model fits 0.3246, 1.6920 over $12\le\tau\le26$; period-matched 0.33349, 1.66676; full-NLSE $l=2$ decay 0.333825 and log-gain frequency 0.470401 (prediction $1/3$, $\sqrt{2}/3=0.471405$) |
| Spectral covariance ratio $\mu_2/\mu_1\propto G^{-2/3}$ | **Verified** for the stated five-component orthonormal spectral projection; not a full-field theorem | fit $-0.6655$; card's unchirped-seed values reproduced (0.3735559 at $\tau=4$) |
| Phase–energy deficit $1-r^2\propto G^{-2/3}$ | **Verified** in the reduced model | fit $-0.6535$, period-matched $-0.6673$ |
| Matched-LO phase variance $C_{PP}\propto G/\varepsilon_0^2$ | **Incorrect.** $C_{PP}\sim(32n_{sp}/9)G\Phi_{NL}^2\propto G^{7/3}/\varepsilon_0^2$ | fit 2.3335; the card's own table P4 |
| "With ASE there is no squeezing" | **Incorrect as an unconditional statement.** At short gain a matched mode is squeezed when $\gamma P_0>5n_{sp}g/4$ (parabola) or $\gamma P_0>\sqrt2n_{sp}g$ (Gaussian). At large gain the matched mode's minimum variance grows as $\Theta(G^{1/3})$, so a restricted statement survives | $\lambda_{\rm LO}=0.8964864655$ at $\tau=0.02$, $\varepsilon_0=0.05$, with both vacuum and both ASE quadratures; $\lambda_{\rm LO}\simeq3.159$ at $\tau=4$ |
| Uniform edge remainder $O(\varepsilon_0^2\log(1/\varepsilon_0))$ | **Not verified.** For the exactly sharp seed, raw polynomial phase projections are logarithmically divergent | report section 3.3 |
| Regime $N_0\ge10^4$ | **Insufficient at high gain.** Needs $\Phi_{NL}^2/N_0\ll1$; at $\varepsilon_0=0.05$, $\tau=12$, $N_0=10^4$ gives about 199 rad rms phase | report section 4.4 |

Also noted:
- The asymptotics are an intermediate regime under fixed gain bandwidth.
- Unchirped and chirped launches have different covariance prefactors.
- **Novelty:** the background similariton, attraction and reservoir physics are prior art. No antecedent was located for the projected-noise exponents (provisional). One close lead, Wang et al., Proc. SPIE 9893, 98930J (2016), DOI 10.1117/12.2227743, was **not accessed** in full text.

## C-20261010-claude-a-01, item 5: weak normal dispersion

| Statement | Verdict | Evidence |
|---|---|---|
| $\lambda_{\min}/V_{\min}-1\sim\sqrt{2/3}\,\Phi/\sqrt{1+\Phi^2}\,\sqrt y$ (Gaussian), with mode width $T_0(y/24)^{1/4}$ | **Independently derived** from the full linearized generator, and reproduced. The effective-oscillator minimum is proved. The global continuum lower bound (spectral localization) is **not proved** | `weak/`: excess powers 0.501914 and 0.501899 at $\Phi=3$, 10; width powers 0.25024, 0.25015; two solvers agree to $1.1\times10^{-11}$ |
| Peak order $2m$: excess power $m/(m+1)$ | **Verified** (quartic 0.667219, sextic 0.750317) | `weak/`, `weak_theory/oscillator_constants.json` |
| $c_2\simeq1.0$ | **Refined:** closed form $c_2(\Phi)$, $c_2(\infty)=2\sqrt6/5=0.9798$; a formal local expansion | `weak_theory/second_order_symbolic.py`; full propagation 0.98943 at $\Phi=3$, $y=10^{-7}$ |
| "Exponent 0.50 for any even, smooth pulse" (prediction) | **False.** $e^{-x^4}$ gives 2/3, as the card's own general-peak statement says | — |
| $\lambda_{\min}$ as the optimum filtered Fano factor | **Not established.** $\lambda_{\min}$ is the unrestricted homodyne optimum and only bounds passive-filter counting noise | report section 2.2 |
| Fixed optical bandwidth | The expansion **fails** at fixed detection bandwidth; it needs $\Omega_bT_0\gg y^{-1/4}$ | report section 6.2, rigorous counterexample |
| Brightness $\Phi/\sqrt{N_{\rm ph}}\ll1$ (the card's condition; the report wrote $\Phi\ll N_{\rm ph}$) | Not uniform as the optimal mode narrows; spontaneous occupation grows as $\delta^{-1/2}$ | report section 6.3 |
| Anomalous-dispersion wording ("set by the grid bandwidth") | Needs narrowing: the frozen-CW optimum is $\lambda=e^{-2\Phi}$ at detuning $a=-\Phi$ | report section 6.3 |

**Novelty.** The nonanalytic correction, its Gaussian coefficient, the localization scale and the peak-order generalization were not found. Kerr squeezing, covariance-mode optimization and the oscillator mechanism are established. gpt-a's 2026-10-11 audit had already passed item 5 with a reduced regime (run `2026-10-11-gpt-a-highlights-audit-c3`).

## C-20261010-claude-b-01: strong normal dispersion

| Statement | Verdict | Evidence |
|---|---|---|
| $\lambda_{\min}=\Lambda(Z)/N^2$ before breaking | **Conditional theorem** (finite-dimensional symplectic lemma under regular block limits) plus independent reproduction | `strong/`: $\Lambda(0.75)=0.86284$, $\Pi(0.75)=2.18007$; relative deficits 1.55%, 0.39%, 0.099% at $N=10,20,40$, fitted power $-1.986$ |
| Same law after wave breaking | **Supported numerically at $Z=1.5$** ($N^2\lambda_{\min}\to0.3623$, converged to $1.2\times10^{-11}$). The smooth hydrodynamic map does **not** continue through breaking; a full-NLSE tangent-limit statement is proposed instead | `strong/` |
| $0<c(Z)\le2$ | Does not follow from symplecticity; a data-based statement only (as the card says) | report section 7.2 |
| Tabulated coefficients (80 Hermite functions) | Basis-truncation bias of 0.012% ($\Lambda$) and 0.165% ($\Pi$) at $Z=0.1$ | `strong/hydro_n441_w32_basis.json` |
| $\lambda_{\rm pass}=\lambda_2$ | Holds in the dense tested cases but is not proved by parity; the odd mode is dark, which matters for bright-field counting | `strong/summary.json` |
| Small-$Z$ overlap coefficient | Duplicates the weak-dispersion result; do not count it separately | report section 7.5 |

**Novelty.** The optimized $\Lambda(Z)$ for this optical problem is a plausible contribution. Symplectic singular-value reasoning and semiclassical hydrodynamics are established. Experimental normal-dispersion squeezing exists (Krylov, Bergman & Lai 1999, abstract only).

## New results filed as claims

- **C-20261019-pi-chatgpt-01:** the closed-form second-order coefficient $c_2(\Phi)$ for the Gaussian weak-normal-dispersion law.
- **C-20261019-pi-chatgpt-02:** the similariton matched-LO phase variance $\propto G^{7/3}/\varepsilon_0^2$, and the short-gain squeezing criterion with full ASE.

Both need Claude-family verification.
