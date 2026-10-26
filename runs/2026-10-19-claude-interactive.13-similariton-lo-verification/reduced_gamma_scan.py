"""(i)/(iii) at other Gamma (edge of the 'Gamma of order 1' regime): unchirped and chirp-Gamma/3 parabolic seeds.
claude-interactive.13."""
import json, numpy as np
from reduced import run, lo_quantities
taus = np.arange(0.005, 60.0025, 0.005)
out = {}
for Gam in (0.5, 2.0, 10.0):
    for lab, ap in (("unchirped", 0.0), ("chirp_Gamma_over_3", Gam / 3)):
        o = run(Gam, ap0_zeta=ap, taus=taus)
        r = lo_quantities(o, taus, 1.0, eps0=0.05)
        lnC = np.log(r["e2CPP"]); m1 = (taus >= 12) & (taus <= 26); m2 = (taus >= 26) & (taus <= 40); m3 = (taus >= 40) & (taus <= 60)
        gl = r["lam_lead"] * np.exp(-taus / 3)
        d = dict(power_12_26=float(np.polyfit(taus[m1], lnC[m1], 1)[0]), power_26_40=float(np.polyfit(taus[m2], lnC[m2], 1)[0]),
                 power_40_60=float(np.polyfit(taus[m3], lnC[m3], 1)[0]),
                 ratio_12_26=[float(r["ratio_i"][m1].min()), float(r["ratio_i"][m1].max())], ratio_40_60=[float(r["ratio_i"][m3].min()), float(r["ratio_i"][m3].max())],
                 Gm13_lam_12_26=[float(gl[m1].min()), float(gl[m1].max())], Gm13_lam_26_60=[float(gl[(taus >= 26)].min()), float(gl[(taus >= 26)].max())])
        out[f"Gamma{Gam}_{lab}"] = d
        print(Gam, lab, {k: (np.round(v, 5) if not isinstance(v, list) else [round(x, 4) for x in v]) for k, v in d.items()})
json.dump(out, open("reduced_gamma_scan.json", "w"), indent=1)
