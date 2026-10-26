#!/usr/bin/env python3
"""Tight-tolerance independent check of the newly derived Gaussian y term."""
import json
from pathlib import Path
import numpy as np
from verify_weak import compute

here=Path(__file__).resolve().parent
out=[]
for phi,y,n in [(3.,1e-6,3072),(3.,1e-7,4096),(10.,1e-7,4096)]:
    r=compute(phi=phi,y=y,n=n,support=.2 if y==1e-6 else .15,rtol=2e-13)
    S=np.sqrt(1+phi*phi)
    r['c2_predicted']=np.sqrt(6)*(45+81*phi**2+56*phi**4+40*phi**3*S)/(240*phi**2*(1+phi**2))
    r['c2_measured']=(r['ratio']-1)/np.sqrt(y)
    out.append(r)
    (here/'second_order_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(phi,y,r['c2_measured'],r['c2_predicted'],flush=True)
