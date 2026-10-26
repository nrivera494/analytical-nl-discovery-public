"""Frozen tables from C-20261008-claude-a-01 (P3, P5) and C-20261008-claude-a-02 (P3, P4, P5), as (in, ase) pairs."""
C01_P3 = {  # main case Gamma = sqrt(18): aL, apL, VarTc/sigTL^2, VarTcomp/T0^2, VarWc/sigWL^2, eps0*Cov
    2: dict(aL=1.4154, apL=2.2098, VarTc=(0.4991, 0.5964), VarTcomp=(0.2, 0.1242), VarWc=(0, 0.1051), Cov=(0, 0.1224)),
    4: dict(aL=3.3747, apL=6.2614, VarTc=(0.0878, 0.2529), VarTcomp=(0.2, 0.2484), VarWc=(0, 0.05348), Cov=(0, 0.4169)),
    6: dict(aL=7.5181, apL=11.6806, VarTc=(0.01769, 0.1073), VarTcomp=(0.2, 0.4557), VarWc=(0, 0.02294), Cov=(0, 0.7899)),
}
C01_P5 = {  # held out Gamma = 1
    2: dict(aL=4.4735, apL=2.8631, VarTc=(0.04997, 0.4347), VarTcomp=(0.2, 0.1815), VarWc=(0, 0.2435), Cov=(0, 0.8106)),
    4: dict(aL=11.5923, apL=4.2846, VarTc=(0.007441, 0.3484), VarTcomp=(0.2, 0.8832), VarWc=(0, 0.1808), Cov=(0, 2.465)),
    6: dict(aL=22.1913, apL=6.5861, VarTc=(0.002031, 0.2364), VarTcomp=(0.2, 3.923), VarWc=(0, 0.08558), Cov=(0, 4.124)),
}
C02_P3 = {  # main case spectral: N0 Var(s_l) (in, ase), lambda2/lambda1 (n_sp = 1)
    2: dict(s=[(0.4444, 0.3843), (0, 0.08407), (2.645, 1.486), (8.067, 7.783), (3.658, 14.36)], ratio=0.9868),
    4: dict(s=[(0.4444, 0.4363), (0, 0.04278), (0.1312, 0.2949), (0.481, 0.5688), (0.8996, 2.013)], ratio=0.3735),
    6: dict(s=[(0.4444, 0.4433), (0, 0.01835), (0.004664, 0.04164), (0.07037, 0.242), (0.4, 0.4685)], ratio=0.1095),
}
C02_P4 = {  # main case matched LO: eps0^2 C_PP / G (in, ase), 1 - r^2 (n_sp = 1)
    2: dict(CPP=(3.809, 2.258), omr2=0.07436),
    4: dict(CPP=(61.81, 55.32), omr2=0.01251),
    6: dict(CPP=(700.9, 685.3), omr2=0.004356),
}
C02_P5 = {  # held out Gamma = 1: s_0, s_2 (in, ase), lambda2/lambda1, 1 - r^2
    2: dict(s0=(0.4444, 0.3843), s2=(0.2596, 0.265), ratio=0.4257, omr2=0.06191),
    4: dict(s0=(0.4444, 0.4363), s2=(0.001834, 0.07332), ratio=0.1256, omr2=0.0211),
    6: dict(s0=(0.4444, 0.4433), s2=(0.01736, 0.03703), ratio=0.0757, omr2=0.007757),
}
C02_asym = dict(ratio={12: 3.03e-3, 15: 4.14e-4, 18: 6.07e-5}, omr2={12: 8.96e-5, 15: 9.59e-6, 18: 1.84e-6})
