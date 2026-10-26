"""Dynamics for the pre-registered groups-1+4 launches (grin_gge_predict3.json): exact GRIN tensor, K=5, no disorder."""
import json, numpy as np, warnings
warnings.filterwarnings('ignore')
import grin_model_phases as gm
pred = json.load(open('grin_gge_predict3.json'))
src = open('grin_model_phases.py').read()
with open('grin_gge_run3.jsonl', 'w') as f:
    for p in pred:
        # build a launch with the given intensities: run() builds its own I0 from Eprime; override by passing phases and patching I0
        o = gm.run(K=5, Eprime=0.9, zmax=10000., zburn=1000., dz=0.05, J=0, seed=0, phase_seed=1, sigma=0.0, launch='dephased',
                   phases=p['ph'], lyap=False, I0_override=p['I0'])
        o['launch'] = 'groups 1+4 ' + p['phases']; f.write(json.dumps(o) + '\n'); f.flush()
        print(f"{p['phases']}: observed <I_0>={o['mean_N0']:.4f} +- {o['block_se']['mean_N0']:.4f}  GGE {p['GGE_N0']:.4f}  RJ {p['RJ_N0']:.4f}  E'drift {o['drift']['E']:.1e}", flush=True)
