#!/usr/bin/env python3
"""Two-polarization dispersionless Kerr model (isotropic fibre, instantaneous electronic Kerr, no Raman), circular basis:
    dA_+/dz = i (2 gamma/3)(|A_+|^2 + 2|A_-|^2) A_+ ,   and + <-> -.
|A_+|^2 and |A_-|^2 are z-invariant, so the linearized map is again a shear, now 2x2 per time slice:
    K = (4 Phi p/3) [[c+, 2 sqrt(c+ c-)], [2 sqrt(c+ c-), c-]],  c+- = (1 +- sin 2chi)/2 (ellipticity angle chi).
Readouts: (i) polarization-resolved spectral bins in the circular basis; (ii) polarization-insensitive bins (counts summed).
Strong linear birefringence (beat length << L_NL, no walk-off) is the same with linear axes, K = 2 Phi p [[cx, (2/3)sqrt(cx cy)], ...].
Usage: python polarization.py out.json"""
import json, sys, time, warnings
import numpy as np
from numpy.fft import fftfreq
warnings.filterwarnings("ignore")
from dlfano import gaussian_p, vmin_kerr, binary_search4

def model(p, dt, Phi, cplus, kind="isotropic"):
    n = len(p)
    cm = 1 - cplus
    if kind == "isotropic":           # circular basis
        a, b, d = (4 * Phi / 3) * cplus, (4 * Phi / 3) * 2 * np.sqrt(cplus * cm), (4 * Phi / 3) * cm
        ph = [(2 * Phi / 3) * (cplus + 2 * cm) * p, (2 * Phi / 3) * (cm + 2 * cplus) * p]
    else:                              # strong linear birefringence, linear axes
        a, b, d = 2 * Phi * cplus, 2 * Phi * (2 / 3) * np.sqrt(cplus * cm), 2 * Phi * cm
        ph = [Phi * (cplus + (2 / 3) * cm) * p, Phi * (cm + (2 / 3) * cplus) * p]
    P = np.diag(p)
    K = np.block([[a * P, b * P], [b * P, d * P]])
    I = np.eye(2 * n)
    V = np.block([[I, K.T], [K, I + K @ K.T]])        # ordering: X+, X-, Y+, Y-
    amps = [np.sqrt(cplus * p), np.sqrt(cm * p)]
    return V, ph, amps

def spectral2(V, ph, amps, dt, pad=4, thr=1e-6):
    n = len(amps[0]); ntot = pad * n
    t = (np.arange(ntot) - ntot // 2) * dt; i0 = ntot // 2 - n // 2
    w = 2 * np.pi * fftfreq(ntot, dt)
    Fm = np.exp(1j * np.outer(w, t)) / np.sqrt(ntot)
    rows, nbars, ws, chan = [], [], [], []
    vac = []
    for c in (0, 1):
        mean = np.zeros(ntot, complex); mean[i0:i0 + n] = amps[c] * np.exp(1j * ph[c])
        Ab = Fm @ mean; nb = np.abs(Ab) ** 2
        if nb.max() == 0:
            continue
        keep = nb >= thr * nb.max() if nb.max() > 0 else np.zeros(ntot, bool)
        psi = np.angle(Ab[keep])
        G = np.exp(-1j * psi)[:, None] * Fm[keep][:, i0:i0 + n] * np.exp(1j * ph[c])[None, :]
        B = np.zeros((keep.sum(), 4 * n))
        B[:, c * n:(c + 1) * n] = G.real                 # X_c
        B[:, 2 * n + c * n:2 * n + (c + 1) * n] = -G.imag  # Y_c
        rows.append(B); nbars.append(nb[keep]); ws.append(w[keep]); chan.append(np.full(keep.sum(), c))
        mask = np.ones(ntot, bool); mask[i0:i0 + n] = False
        Go = (np.exp(-1j * psi)[:, None] * Fm[keep])[:, mask]
        vac.append((Go @ Go.conj().T).real)
    B = np.vstack(rows); nb = np.concatenate(nbars); w = np.concatenate(ws); ch = np.concatenate(chan)
    Vamp = B @ V @ B.T
    off = 0
    for blk in vac:
        k = blk.shape[0]; Vamp[off:off + k, off:off + k] += blk; off += k
    return nb, Vamp, w, ch

def insensitive(nb, Vamp, w, ch):
    """Polarization-insensitive bins: n(w) = n+(w) + n-(w) on a common frequency grid (bins matched by frequency)."""
    s = np.sqrt(nb)
    Sig = s[:, None] * Vamp * s[None, :]
    freqs = np.unique(np.round(w, 10))
    M = np.zeros((len(freqs), len(nb)))
    for j, f in enumerate(freqs):
        M[j, np.abs(w - f) < 1e-9] = 1.0
    Sig2 = M @ Sig @ M.T; nb2 = M @ nb
    keep = nb2 > 0
    Sig2 = Sig2[np.ix_(keep, keep)]; nb2 = nb2[keep]
    s2 = np.sqrt(nb2)
    return nb2, Sig2 / s2[:, None] / s2[None, :], freqs[keep]

out = sys.argv[1] if len(sys.argv) > 1 else "polarization.json"
rows = []
Phi = 10.0; dt = 0.04; t = np.arange(-7, 7, dt); p = gaussian_p(t)
for kind, label, cplus in [("isotropic", "linear", 0.5), ("isotropic", "elliptical chi=pi/8", (1 + np.sin(np.pi / 4)) / 2),
                           ("isotropic", "circular", 1.0), ("birefringent", "45deg", 0.5), ("birefringent", "on axis", 1.0)]:
    t0 = time.time()
    V, ph, amps = model(p, dt, Phi, cplus, kind)
    lm = float(np.linalg.eigvalsh(V)[0])
    if kind == "isotropic":
        cc = cplus * (1 - cplus); Phi_eff = (Phi / 3) * (1 + np.sqrt(1 + 12 * cc))
    else:
        cc = cplus * (1 - cplus); Phi_eff = (Phi / 2) * (1 + np.sqrt(1 - (20 / 9) * cc))
    nb, Va, w, ch = spectral2(V, ph, amps, dt, pad=4)
    lg_res = float(np.linalg.eigvalsh(Va)[0])
    rb_res = binary_search4(nb, Va, w)
    nbi, Vai, wi = insensitive(nb, Va, w, ch)
    lg_ins = float(np.linalg.eigvalsh(Vai)[0])
    rb_ins = binary_search4(nbi, Vai, wi)
    row = {"kind": kind, "input": label, "c_plus": float(cplus), "Phi": Phi, "lam_min": lm,
           "Phi_eff_formula": float(Phi_eff), "Vmin_of_Phi_eff": float(vmin_kerr(Phi_eff)),
           "lam_gen_resolved": lg_res, "binary_resolved": rb_res["F"],
           "lam_gen_insensitive": lg_ins, "binary_insensitive": rb_ins["F"], "wall_s": round(time.time() - t0, 1)}
    rows.append(row); print(json.dumps(row), flush=True)
    json.dump({"rows": rows}, open(out, "w"), indent=1)
