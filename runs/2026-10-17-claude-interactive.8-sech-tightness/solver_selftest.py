"""Self-tests of gnlse_pc.py (verifier's own solver) before production runs."""
import json, time, numpy as np
import mpmath as mp
from gnlse_pc import GNLSE, sech_launch
from ramanlib import rho_closed
t0 = time.time()
out = {}
ps, fs = 1e-12, 1e-15
A = dict(lam0=1550e-9, beta2=-21.7e-27, beta3=0.127e-39, n2=2.6e-20, Aeff=80e-12)
# 1. pure NLSE fundamental soliton (fR=0, no shock): shape and energy over 5 soliton periods
sim = GNLSE(2**13, 2*fs, A["lam0"], A["beta2"], 0.0, A["n2"], A["Aeff"], 0.0, 12.2*fs, 32*fs)
sim.shock[:] = 1.0
A0, T0, P0 = sech_launch(sim, 1, 100*fs, A["beta2"])
LD = T0**2/abs(A["beta2"]); z0 = np.pi/2*LD
for nst in [500, 1000]:
    rec, AL = sim.run(A0, 5*z0, nst, record_every=nst)
    out[f"nlse_soliton_nsteps{nst}"] = {"shape_err": float(np.max(np.abs(np.abs(AL)-np.abs(A0)))/np.sqrt(P0)),
                                        "energy_drift": float(rec[-1]["E"]/rec[0]["E"]-1)}
# 2. Kerr+shock, no Raman: energy conserved (continuum identity) and photon number
sim2 = GNLSE(2**14, 1*fs, A["lam0"], A["beta2"], A["beta3"], A["n2"], A["Aeff"], 0.0, 12.2*fs, 32*fs)
A0, T0, P0 = sech_launch(sim2, 3, 100*fs, A["beta2"])
rec, AL = sim2.run(A0, 0.25, 4000, record_every=400)
out["kerr_shock_N3"] = {"energy_drift": float(rec[-1]["E"]/rec[0]["E"]-1), "photon_drift": float(rec[-1]["Nph"]/rec[0]["Nph"]-1),
                        "max_abs_dEdz_rhs_over_kappaE2": float(max(abs(r_["dEdz_rhs"]) for r_ in rec)/(1.0))}
# 3. with Raman: photon conservation, identity residual, launch-plane rho vs closed form
sim3 = GNLSE(2**14, 1*fs, A["lam0"], A["beta2"], A["beta3"], A["n2"], A["Aeff"], 0.18, 12.2*fs, 32*fs)
A0, T0, P0 = sech_launch(sim3, 3, 100*fs, A["beta2"])
rec, AL = sim3.run(A0, 0.25, 4000, record_every=40)
x = T0/(12.2*fs); r = 12.2/32
out["raman_N3"] = {"photon_drift": float(rec[-1]["Nph"]/rec[0]["Nph"]-1), "energy_ratio": float(rec[-1]["E"]/rec[0]["E"]),
                   "max_identity_rel": float(max(abs(r_["dEdz_rhs"]-r_["dEdz_spec"])/abs(r_["dEdz_spec"]) for r_ in rec)),
                   "rho0_rhs": float(rec[0]["rho_rhs"]), "rho0_spec": float(rec[0]["rho_spec"]), "rho0_closed": float(rho_closed(r, x)),
                   "max_negfreq_frac": float(max(r_["negfrac"] for r_ in rec)), "max_edge": float(max(r_["edge"] for r_ in rec))}
out["wall_s"] = time.time()-t0
print(json.dumps(out, indent=1))
json.dump(out, open("summary_solver_selftest.json", "w"), indent=1)
