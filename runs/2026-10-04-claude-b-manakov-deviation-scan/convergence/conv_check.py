import json, sys, importlib, numpy as np
sys.path.insert(0, "~/agent-work/claude-b/runs/2026-10-04-claude-b-manakov-deviation-scan")
sys.path.insert(0, "/private/tmp/claude-502/-Users-user-agent-work-claude-b/76c587c8-f7e5-4a59-9fdd-b4b49e7b4393/scratchpad")
which = sys.argv[1]
lib = importlib.import_module("twomode_lib" if which == "halfdz" else "twomode_lib_wide")
t, w, TW = lib.t, lib.w, lib.TW
dz = 1e-3 if which == "halfdz" else 2e-3
C = [[1, 1], [1, 0.5]]; p2 = 0.30; p1 = 0.7; S = p1*p1 + 2*p1*p2 + 0.5*p2*p2
sech = 1/np.cosh(t); mask = (np.abs(w) < 0.8).astype(float)
d = 6 * 2*np.pi/40.0   # same physical walk-off as the scan (0.942)
Fs = lib.noise(sech+0j, 0*sech+0j, 5.0, dz, C, 0.0, mask, mask)["Fa"]
r = lib.noise(np.sqrt(p1/S)*sech+0j, np.sqrt(p2/S)*sech+0j, 5.0, dz, C, d, mask, mask)
out = {"which": which, "dz": dz, "N": int(lib.N), "TW": float(TW), "Fs": Fs, "case": r, "Ftot_dB_minus_Fs_dB": float(10*np.log10(r["Ftot"]/Fs))}
print(json.dumps(out)); json.dump(out, open(f"/private/tmp/claude-502/-Users-user-agent-work-claude-b/76c587c8-f7e5-4a59-9fdd-b4b49e7b4393/scratchpad/conv_{which}.json","w"))
