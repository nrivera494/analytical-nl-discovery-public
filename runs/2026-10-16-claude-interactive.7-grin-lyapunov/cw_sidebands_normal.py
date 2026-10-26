"""Third pass: GVD of the opposite sign (normal dispersion with this sign convention: x < 0), same trajectory and seeds."""
import json, warnings
warnings.filterwarnings('ignore')
import cw_sidebands as c
o = c.run(mode='gvd', xs=(0.0, -0.003, -0.01, -0.03, -0.1, -0.3, -1.0, -4.0))
print(json.dumps(o), flush=True)
json.dump([o], open('cw_sidebands_normal.json', 'w'), indent=1)
