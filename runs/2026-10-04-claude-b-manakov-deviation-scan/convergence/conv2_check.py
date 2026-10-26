import json, sys, importlib, numpy as np
sys.path.insert(0, "/private/tmp/claude-502/-Users-user-agent-work-claude-b/76c587c8-f7e5-4a59-9fdd-b4b49e7b4393/scratchpad")
which = sys.argv[1]
lib = importlib.import_module({"x3": "twomode_lib_x3", "fine": "twomode_lib_fine"}[which])
t, w, TW = lib.t, lib.w, lib.TW
dz = 2e-3
C = [[1, 1], [1, 0.5]]; p2 = 0.30; p1 = 0.7; S = p1*p1 + 2*p1*p2 + 0.5*p2*p2
sech = 1/np.cosh(t)
# hard filter with the same effective edge as the nominal grid (TW=40, |w|<0.8 -> bins |k|<=5 -> edge 5.5*2pi/40 = 0.864)
dw = 2*np.pi/TW
kmax = {"x3": 16, "fine": 5}[which]          # x3: edge (16.5)*2pi/120 = 0.864 ; fine: same frequency grid as nominal
mask = (np.abs(np.round(w/dw)) <= kmax).astype(float)
d = 6 * 2*np.pi/40.0
Fs = lib.noise(sech+0j, 0*sech+0j, 5.0, dz, C, 0.0, mask, mask)["Fa"]
r = lib.noise(np.sqrt(p1/S)*sech+0j, np.sqrt(p2/S)*sech+0j, 5.0, dz, C, d, mask, mask)
out = {"which": which, "N": int(lib.N), "TW": float(TW), "edge": float((kmax+0.5)*dw), "Fs": Fs, "case": r, "Ftot_dB_minus_Fs_dB": float(10*np.log10(r["Ftot"]/Fs))}
print(json.dumps(out)); json.dump(out, open(f"conv2_{which}.json","w"))
