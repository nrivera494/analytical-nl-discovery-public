"""Second pass of cw_sidebands.py at larger x, to locate the cutoff of the sideband growth band (same trajectory, seeds)."""
import json, warnings
warnings.filterwarnings('ignore')
import cw_sidebands as c
out = []
for mode in ['walkoff', 'gvd']:
    o = c.run(mode=mode, xs=(1.0, 2.0, 4.0, 8.0, 16.0)); out.append(o); print(json.dumps(o), flush=True)
json.dump(out, open('cw_sidebands_wide.json', 'w'), indent=1)
