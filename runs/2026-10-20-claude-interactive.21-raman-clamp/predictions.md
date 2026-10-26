# Pre-registered predictions for the clamp test (frozen before any propagation in this folder)

Agent claude-interactive.21 (claude-opus-5-5), 2026-10-20, task T-20261020-claude-interactive-02 (starts
T-20261020-claude-interactive.21-04). Model `mmfieldM.py`, parameters `config.json`.

The toy is a three-group parabolic-fibre model: 6 Hermite–Gauss modes in groups of 1, 2 and 3, with exact overlaps. It has resonant inter-group Kerr exchange $g_0+g_2\leftrightarrow g_1+g_1$, white-noise $su(n)$ coupling inside groups 1 and 2, $\beta_2$ ($W_t=0.25$), Raman, and no shock. The launch has group populations 0.3/0.1/0.6 (RJ target with the same $N$ and $H_\perp$: 0.180/0.339/0.480), co-centred Gaussian spectra with $\sigma=20$ rad/ps, $L_{\rm NL}=0.1$ m, and $z$ up to 3 m $=30L_{\rm NL}$. The ensemble is 8 base realizations plus their mirrors, with a shared coupling path. Runs: $\lambda=-1,0,+1$.

**Operational kinetic length.** $L_{\rm kin}$ is the smallest saved $z$ at which the $\lambda=0$ mean group-1 fraction has covered $1-e^{-1}$ of the way from its launch value to its mean over the last five saved points ($z=2.6$–3.0 m). If $L_{\rm kin}>1$ m, test C3 is declared inconclusive.

Notation:
- $N_g(\lambda)$: pair-averaged group photon numbers;
- even part $E_g=[N_g(1)+N_g(-1)]/2-N_g(0)$;
- odd part $O_g=[N_g(1)-N_g(-1)]/2$;
- $\Delta c_{01}$: the $\lambda$-odd part of the difference between the energy centroids of mode 0 and of group 1 (power-weighted mean over the group's modes).

- **C0 (cheap, exact):** at $\lambda=0$ the pair-averaged energy centroids of every mode vanish to round-off ($<10^{-9}$ rad/ps), and $O_g<10^{-9}$ relative at every $z$.
- **C1 (relaxation exists):** the $\lambda=0$ group fractions move from 0.3/0.1/0.6 toward the RJ target. At $z=3$ m the group-1 fraction exceeds 0.25.
- **C2 (sign):** $E_0>0$ at $z=0.2$ and 0.3 m, and also at $z=3$ m: the fundamental gains from Raman at second order, before and after Kerr relaxation.
- **C3 (clamping conjecture), meaningful only if $L_{\rm kin}\le1$ m:**
  - (a) $|\Delta c_{01}|$ grows about linearly for $z<L_{\rm kin}/2$, but its local exponent $d\ln|\Delta c_{01}|/d\ln z$ over $z\in[2L_{\rm kin},3\,{\rm m}]$ is below 0.5. The no-Kerr Langmuir model would give 1.
  - (b) The local exponent of $E_0(z)$ over $z\in[2L_{\rm kin},3\,{\rm m}]$ is below 1.5, while over the first two saved points beyond 0.1 m it is 1.7–2.3.
  - If (a) and (b) hold, the conjecture is supported in this toy. If the late exponent of $E_0$ is $\ge1.7$, it is refuted here.

## Addendum: configuration `g4_weak` (written after the `main` outcome, before any `g4_weak` propagation)

The `main` configuration did not relax within $30L_{\rm NL}$ (C1 failed; it is in Garnier's strong-disorder regime with $L_{\rm kin}\propto\Delta\beta$).

**Setup.** Four groups (10 HG modes), weak coupling $D_d=1$ m⁻¹ ($L_d=10L_{\rm NL}$), $N=1024$, 6 mirror pairs, seed 61. Other parameters as `main`. Launch group fractions 0.3/0.1/0.5/0.1; RJ target 0.291/0.246/0.234/0.229.

**Operational $L_{\rm kin}$** (changed so that a slow drift cannot masquerade as a plateau): the smallest saved $z$ at which the $\lambda=0$ mean **group-2** fraction has covered $1-e^{-1}$ of the way from its launch value to its **RJ value 0.2341**. If none is reached by 3 m, or $L_{\rm kin}>1$ m, C3 is inconclusive.

- **C0:** as before.
- **C1:** the group-2 fraction at 3 m is below 0.40.
- **C2:** $E_0$ as before: positive at 0.2, 0.3 and 3 m. Note that the fundamental's RJ fraction (0.291) is close to its launch fraction, so the Kerr relaxation itself barely moves group 0.
- **C3 (a), (b):** as before, with this $L_{\rm kin}$.
