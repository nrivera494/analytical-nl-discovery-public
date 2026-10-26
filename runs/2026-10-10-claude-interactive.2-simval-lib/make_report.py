"""One line per result R1-R10 for the PR body and the hand-off message, from the same computed values as the note."""
import fill_note as F

v = F.main()
lines = [
    f"- R1 (width ODE, Lyapunov function, parabolic attraction): confirmed. max|s/s_ODE-1| over tau<=6: {v['R1_err01']} at eps0=0.1, "
    f"{v['R1_err005']} at 0.05, {v['R1_err0025']} at 0.025; slopes {v['R1_slopes']}. V is non-increasing for eps0<=0.05, and all launches approach s=1.",
    f"- R2 (linear spectrum): confirmed. Decay g/3 and frequencies sqrt2 g/3, sqrt5 g/3, g. {v['R2_smallest']} "
    f"l=0 neutral, l=1 Ehrenfest double root; inter-block mixing {v['R2_mixing']}.",
    f"- R3 (eps_eff ~ e^(-2gz/3)): confirmed. eps_eff slopes {v['R3_eeff']}. The transform-limited share decays at {v['R3_ftl']} "
    f"(predicted -4/3 plus log); its ratio to eps_eff^2 grows {v['R3_growth']}-fold over tau=2-6, approaching the edge-log value of about 2 as eps0 -> 0. "
    f"Edge-layer scaling (my frozen target, not a claim statement): slopes {v['R3_edge']} against -4/9, converging but outside the frozen 5% criterion.",
    f"- R4 (energy mapping 1/3, 2/3, 1/3, 0): confirmed. Extrapolated asymptotes {v['R4_asym']}; chirp g/(3 b2) to {v['R4_chirp']}.",
    f"- R5 (phase-sensitive shape gains G^(1/3), G^(5/3)): confirmed through gL=6. The scaled-variable generator is oscillatory, so the envelopes hold; "
    f"l=2 exponents at gL=6 are (1.7228, 0.2786) NLSE against (1.7232, 0.2768) from the reduced ODE. Determinants: {v['R5_det']} gL=12-24 not reached.",
    f"- R6 (exact moment structure): confirmed (exact). Energy law (1, 1-1/G) to 5e-4; n_sp = 2 n_s^2 + 1/2; adjoint = W(z) moment formula to "
    f"{v['R6B_MAX'].replace(chr(92)+'times10^{','e').replace('}','')}; Monte Carlo ASE scale factors {v['MC_b'].replace('$','').replace(chr(92)+'pm','+-').replace(chr(92)+chr(92)+'Omega_c','Omega_c')}.",
    f"- R7 (closed forms and frozen tables): closed forms confirmed (ASE parts within {v['R7_ase_small']}). P8 reproduced to all quoted digits "
    f"(ratio 3.5495, claim 3.55). P3/P5 ASE entries within {v['P3_ase_0025']} / {v['P5_ase_0025']}. Input-vacuum entries miss the claim's 5% band "
    f"at eps0=0.1 (main +23%, held out +313%); the cause is the seed's transform-limited bandwidth. At the smallest eps0 run the input entries are within {v['P3_in_small']} (main; passes my frozen criteria) and {v['P5_in_small']} (held out; fails at gL=4, 6).",
    f"- R8 (vacuum vs ASE share): confirmed for energy, Omega_c and T_comp (finite-G closed forms; MC split agrees). Not confirmed for shape-mode intensity: "
    f"the n_2 share oscillates ({v['R8_n2']}).",
    f"- R9 (spectral rank one): lambda2/lambda1 of the C-02 tables confirmed at gL=4, 6 (deviation at the smallest eps0 run: {v['R9_lam_small']}). "
    f"The individual N0 Var(s_l) entries of C-02 P3 are not all reproduced; off by more than 10%: {v['P3_entries_bad']} (s_1 ASE 14-19% high at every gL, not shrinking). At gL=2 the main-case ratio converges slowly "
    f"({v['R9_g2_lam']}) and the held-out ratio does not converge ({v['R9_h2_dev']}; effective exponent {v['R9_h2_exp']}), so the claim's own 10% criterion fails at gL=2; "
    f"moving the spectral-core cut changes the ratio by at most {v['R9_core_concl'].split('at most ')[1].split(',')[0] if 'at most' in v['R9_core_concl'] else 'n/a'}. Trend toward G^(-2/3) up to gL=8 "
    f"(asymptotic-seed ratios {v['R9_asym']}); gL=12-18 not tested.",
    f"- R10 (matched LO): C_AA = G + (2n_sp-1)(G-1) exact (to 5e-4); eps0^2 C_PP/G within 1% at eps0=0.05; 1-r^2 against C-02 P4 at the smallest eps0 run: {v['R10_omr2_short']}. G^(-2/3) law not tested "
    f"(asymptotic-seed 1-r^2 = {v['R10_asym']} at gL=2-8).",
]
def clean(l):
    for a, b in (("$", ""), ("\\varepsilon_0", "eps0"), ("\\tau", "tau"), ("\\in", " in "), ("\\Omega_c", "Omega_c"), ("\\pm", "+-"),
                 ("\\times10^{", "e"), ("}", ""), ("{", "")):
        l = l.replace(a, b)
    return l
print("\n".join(clean(l) for l in lines))
