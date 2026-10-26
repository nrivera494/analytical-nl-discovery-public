"""Three-group (6-mode) GRIN toy: does fast Kerr relaxation clamp the second-order Raman modal drift?
usage: python run_clamp.py LAM [tag]   (LAM = -1, 0 or 1; s = 0). Mirror-closed ensemble (R/2 base + mirrors),
shared coupling path. Saves group photon numbers per realization at every save point to the raw-data folder.
"""
import json
import os
import sys
import time

import numpy as np

from mmfieldM import ModelM, launch, mirror

RUN_ID = "2026-10-20-claude-interactive.21-raman-clamp"
RAW = os.path.expanduser("~/analytical-nl-discovery-data/" + RUN_ID)
os.makedirs(RAW, exist_ok=True)
os.makedirs("results", exist_ok=True)
cfg = json.load(open("config.json"))
lam = float(sys.argv[1])
tag = sys.argv[2] if len(sys.argv) > 2 else "main"
c = dict(cfg["main"])
c.update(cfg.get(tag, {}))
m = ModelM(G=c["G"], N=c["N"], dt=c["dt_ps"], gamma=c["gamma_perWm"], fR=c["fR"], tau1=c["tau1_ps"], tau2=c["tau2_ps"],
           omega0=c["omega0_radps"], dbeta=c["dbeta_perm"], beta2=c["beta2_ps2perm"], s=c["s"], lam=lam, Dd=c["Dd_perm"])
rng = np.random.default_rng(c["seed"])
B0 = launch(rng, c["R_base"], m, c["powers_W"], c["sigma_radps"])
B = np.concatenate([B0, mirror(B0)], axis=0)
g = np.random.default_rng(c["seed"] + 1).standard_normal((c["nsteps"], m.ngen))
def moments(B):
    P = np.abs(B) ** 2
    Ptot = P.sum(-1)
    c1 = (P * m.W).sum(-1) / Ptot                     # energy centroid per mode (rad/ps)
    c2 = (P * m.W ** 2).sum(-1) / Ptot - c1 ** 2      # energy-spectrum variance per mode
    return c1, c2
rec = [m.photon(B)]
mom = [moments(B)]
t0 = time.time()
for n in range(c["nsteps"]):
    B = m.step(B, c["dz_m"], g[n])
    if (n + 1) % c["save_every"] == 0:
        rec.append(m.photon(B))
        mom.append(moments(B))
rec = np.array(rec)                       # (nsave+1, 2R, M)
np.save(os.path.join(RAW, "%s_lam%g_photon.npy" % (tag, lam)), rec)
np.save(os.path.join(RAW, "%s_lam%g_centroid.npy" % (tag, lam)), np.array([x[0] for x in mom]))
np.save(os.path.join(RAW, "%s_lam%g_variance.npy" % (tag, lam)), np.array([x[1] for x in mom]))
json.dump(dict(tag=tag, lam=lam, wall_s=time.time() - t0, M=m.M, groups=m.grp.tolist(), cfg=c),
          open("results/%s_lam%g_meta.json" % (tag, lam), "w"), indent=1)
grp = m.grp
Ng = np.stack([rec[:, :, grp == k].sum(-1) for k in range(c["G"])], axis=-1)   # (nz, 2R, G)
frac = Ng / Ng.sum(-1, keepdims=True)
print("lam", lam, "wall %.0f s" % (time.time() - t0))
for i in range(0, rec.shape[0], max(1, rec.shape[0] // 15)):
    print("z=%.2f m group fractions %s" % (i * c["save_every"] * c["dz_m"], np.round(frac[i].mean(0), 4)))
