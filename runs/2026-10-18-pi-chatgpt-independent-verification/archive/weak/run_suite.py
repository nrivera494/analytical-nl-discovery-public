#!/usr/bin/env python3
"""Reproduce all weak-dispersion tables; every completed case is checkpointed."""
import json
from pathlib import Path
from verify_weak import compute

HERE=Path(__file__).resolve().parent
results=[]

def run(label,**kw):
    result=compute(**kw)
    result['label']=label
    results.append(result)
    (HERE/'weak_results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(label, 'lambda=',result['lambda_min_upper'],'excess/leading=',result['ratio'],
          'width=',result['xrms'],'seconds=',round(result['runtime_seconds'],2),flush=True)

for phi in [3.,10.]:
    for y in [1e-6,1e-5,1e-4,1e-3,1e-2]:
        n=2048 if y<=1e-6 else 1024
        support=max(.3,7*(y/24)**.25)
        run(f'gaussian_phi{phi:g}_y{y:g}',phi=phi,y=y,n=n,support=support,
            rtol=2e-11,save_mode=str(HERE/f'mode_phi{phi:g}_y{y:g}.npz'))

for m in [2,3]:
    for y in [1e-6,1e-5,1e-4,1e-3,1e-2]:
        run(f'flat{2*m}_phi3_y{y:g}',phi=3,y=y,n=1024,m=m,
            support=max(.6,5*(y/6)**(1/(2*m+2))),rtol=2e-11)

# Spatial refinement at the most localized case and tolerance refinement.
run('grid_gaussian_fine',phi=3,y=1e-6,n=3072,support=.3,rtol=2e-11)
run('tolerance_gaussian',phi=10,y=1e-4,n=1024,support=.4,rtol=2e-12)
# Restriction and full symplectic reciprocity checks on the same discretization.
run('support_standard',phi=3,y=1e-3,n=512,support=.6,rtol=2e-11)
run('support_wide',phi=3,y=1e-3,n=512,support=1.2,rtol=2e-11)
run('full_tangent',phi=3,y=1e-3,n=512,support=4,full=True,rtol=2e-11)
# Larger physical window at identical spatial step size.
run('window_wide',phi=3,y=1e-3,n=1536,half_window=6,support=.8,rtol=2e-11)
# Exact dispersionless anchor on a grid that includes the peak.
run('zero_dispersion',phi=3,y=0,n=256,support=.4,rtol=2e-11)

print('Completed',len(results),'cases',flush=True)
