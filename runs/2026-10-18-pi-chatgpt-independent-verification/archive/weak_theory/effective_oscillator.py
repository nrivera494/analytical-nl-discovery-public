"""Independent constants for -d^2/dx^2+x^(2m), and weak-GVD coefficients.

Run: python effective_oscillator.py
Requires numpy, scipy.  No repository code or numerical output is imported.
"""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import eigh_tridiagonal

def solve(m, n, halfwidth=7.0):
    dx=2*halfwidth/(n+1)
    x=np.linspace(-halfwidth+dx,halfwidth-dx,n)
    diagonal=2/dx**2+x**(2*m)
    offdiagonal=np.full(n-1,-1/dx**2)
    e,f=eigh_tridiagonal(diagonal,offdiagonal,select='i',select_range=(0,0))
    rms=np.sqrt(np.sum(x*x*f[:,0]**2))
    return {'n':n,'dx':dx,'energy':float(e[0]),'rms':float(rms)}

out={}
for m in [1,2,3]:
    rows=[solve(m,n) for n in [999,1999,3999,7999]]
    e_ext=(4*rows[-1]['energy']-rows[-2]['energy'])/3
    r_ext=(4*rows[-1]['rms']-rows[-2]['rms'])/3
    out[str(m)]={'convergence':rows,'energy_Richardson':e_ext,
                'rms_Richardson':r_ext,
                'relative_excess_prefactor_before_Phi_over_sqrt':
                    e_ext*(2/3**m)**(1/(m+1)),
                'rms_prefactor_before_y_power':r_ext/6**(1/(2*m+2))}
path=Path(__file__).with_name('oscillator_constants.json')
path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
