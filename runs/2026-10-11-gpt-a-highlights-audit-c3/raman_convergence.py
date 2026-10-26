"""Raman band-edge counterexample/convergence audit; gpt-a/gpt-6-astra/gpt."""
import json,gc
from pathlib import Path
from raman_band import calculate,PROVENANCE
out=dict(provenance=PROVENANCE,rows=[])
cases=[dict(T0=200.,Phi=10.,temp=300.,band=B,refine=r,padding=p) for B in [30.,44.] for r,p in [(2,16.),(1,32.)]]
cases += [dict(T0=T,Phi=10.,temp=300.,band=44.) for T in [2000.,5000.]]
for case in cases:
 out['rows'].append(calculate(**case));Path(__file__).with_name('raman_convergence.json').write_text(json.dumps(out,indent=2));gc.collect()
