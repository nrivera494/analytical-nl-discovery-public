---
id: T-20261004-claude-b-02
title: "Read the gated full texts behind the multimode soliton noise cards"
type: literature
status: open
priority: 3
problem: P-20261004-root-03
claim: null
family_required: any
lease_hours: 8
created_by: claude-b
created: 2026-10-04
---

## Goal

Read the full texts that the Claude-family review (T-20261004-root-02) could not reach, and update P-20261004-root-03, P-20261004-claude-interactive-01 and P-20261004-claude-interactive-02 if they change anything.

## Context

On 2026-10-04, from claude-b's environment, the Optica pages returned a CAPTCHA (not bypassed). The APS full texts needed a login, and only some had author copies. Each item below is recorded on the cards as **abstract only** or **not accessed**. They probably need institutional access through the PI.

Load-bearing first:
1. **Hirosawa, Kannari, Takeoka & Sasaki, PRA 76, 043817 (2007)**, DOI 10.1103/PhysRevA.76.043817. A soliton plus a trapped pulse, with photon-number correlations from cross-phase modulation. Does its correlation structure map onto the weak-admixture problem of -01 (reduction 1 there)? Does it vary the group-velocity mismatch? Konyukhov, PRA 111, 013508 (2025) was read in full on arXiv (2412.09208) and does not cover this.
2. **Birefringence-mediated timing jitter.** Extract the exact jitter formula, its power of $z$, and whether passive launch-noise partition jitter ($z^2$) appears. This bears on -02 (reduction 1 there).
   - Mollenauer & Gordon, OL 19, 375 (1994), DOI 10.1364/OL.19.000375.
   - Baker & Elgin, Quantum Semiclass. Opt. 10 (1998), DOI 10.1088/1355-5111/10/1/028.
   - Baker, Elgin & Harvey, Opt. Commun. 165, 27 (1999), DOI 10.1016/S0030-4018(99)00197-2.
   - Elgin, Silmon-Clyde, Baker & Harvey, "Soliton jitter and collisions in birefringent fibres," Springer (1998), DOI 10.1007/978-94-011-5141-2_2. A helper's search snippet suggests it derives an arrival-time variance with ASE-perturbed polarization; unverified.
   - Doktorov & Kuten, Nonlinear Phenom. Complex Syst. 4, 1 (2001): timing jitter of the Manakov soliton.
3. **Gordon & Haus, OL 11, 665 (1986)**, DOI 10.1364/OL.11.000665; **Moores, Wong & Haus, Opt. Commun. 113, 153 (1994)**, the Gordon–Haus plus self-frequency-shift $z^5$ term.
4. **Levandovsky, Vasilyev & Kumar, OL 24, 43 (1999)**, DOI 10.1364/OL.24.000043; **Mecozzi & Kumar, OL 22, 1232 (1997)**. These are the single-mode filtered baseline.
5. **Menyuk, JOSA B 5, 392 (1988)**, DOI 10.1364/JOSAB.5.000392: soliton trapping.
6. **For P-20261004-root-01:**
   - **Provost et al., Opt. Express 15, 5100 (2007)**, DOI 10.1364/OE.15.005100. The HAL copy returned a bot check, which was not bypassed. Extract the normalized design map, and the scaling of the plateau power with length, $N$ and filter offset.
   - **König et al., J. Mod. Opt. 45, 2425 (1998)**, DOI 10.1080/09500349808230495: the measured power dependence of normal-dispersion filtered squeezing.
   - **Nishizawa et al., Jpn. J. Appl. Phys. 38, 1961 (1999)**, DOI 10.1143/JJAP.38.1961: the role of GVD in filtered squeezing.
   - **Anderson et al., JOSA B 9, 1358 (1992)**: wave breaking.

   Then add a row to root-01 stating whether its part 1 (location of the minimum) is already a classical design rule.

## Deliverables

- Access levels upgraded on the three cards, with what each paper derives.
- An audit-trail row on each card that changes.
- A session log and a pull request.
