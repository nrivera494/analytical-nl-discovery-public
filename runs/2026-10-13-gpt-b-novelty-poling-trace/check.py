"""Audit check; agent gpt-b, model gpt-6-astra, family gpt.
Box potential normalization of Magland arXiv:0903.4363, Theorem 1.7.1.
Not a simulation of a new claim; no solver modifications.
"""
import json, pathlib, platform, time
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
import sympy as sp
base = pathlib.Path(__file__).resolve().parent
cfg = json.loads((base / 'config.json').read_text())
raw = pathlib.Path(cfg['raw_location']); raw.mkdir(parents=True, exist_ok=True)
t0 = time.perf_counter()
z, d, k = sp.symbols('z d k', real=True)
u, v = sp.symbols('u v')
# A1 = u exp(+i*d*z/2), A2 = v exp(-i*d*z/2).
gauge_u = sp.simplify(sp.I*k*v*sp.exp(-sp.I*d*z/2)*sp.exp(sp.I*d*z)*sp.exp(-sp.I*d*z/2)-sp.I*d*u/2)
gauge_v = sp.simplify(sp.I*k*u*sp.exp(sp.I*d*z/2)*sp.exp(-sp.I*d*z)*sp.exp(sp.I*d*z/2)+sp.I*d*v/2)
rows=[]
for coupling in cfg['kappa_L']:
    ys=[]
    for n in range(int(coupling/np.pi)+1):
        lo=(n+0.5)*np.pi
        hi=min((n+1)*np.pi,coupling)
        if hi<=lo: continue
        def ev(s): return np.cos(s)+np.sqrt(max(0,coupling**2-s*s))*np.sin(s)/s
        s=brentq(ev,lo+1e-12,hi,xtol=1e-14)
        ys.append(float(np.sqrt(coupling**2-s*s)))
    total=2*np.pi*coupling**2-8*np.pi*sum(ys)
    def integrand(delta):
        w=np.sqrt(coupling**2+(delta/2)**2)
        eta=(coupling*np.sin(w)/w)**2
        return -np.log1p(-eta)
    integrals=[]
    for cut in cfg['cutoffs']:
        edges=np.linspace(0,cut,int(np.ceil(cut/np.pi))+1)
        chunks=[quad(integrand,a,b,epsabs=1e-11,epsrel=1e-11,limit=150) for a,b in zip(edges[:-1],edges[1:])]
        val=2*sum(c[0] for c in chunks)
        corrected=val+4*coupling**2/cut
        integrals.append(dict(cutoff=cut,finite_integral=val,leading_tail=4*coupling**2/cut,tail_corrected=corrected,corrected_error=corrected-total,quad_error_estimate=2*sum(c[1] for c in chunks)))
    opa=[]
    def opa_log(delta):
        w2=coupling**2-(delta/2)**2
        if abs(w2)<1e-12: gain=1+coupling**2
        elif w2>0: gain=1+coupling**2*np.sinh(np.sqrt(w2))**2/w2
        else: gain=1+coupling**2*np.sin(np.sqrt(-w2))**2/(-w2)
        return np.log(gain)
    for cut in cfg['cutoffs']:
        edges=np.linspace(0,cut,int(np.ceil(cut/np.pi))+1)
        value=2*sum(quad(opa_log,a,b,epsabs=1e-11,epsrel=1e-11,limit=150)[0] for a,b in zip(edges[:-1],edges[1:]))
        opa.append(dict(cutoff=cut,finite_integral=value,tail_corrected=value+4*coupling**2/cut,corrected_error=value+4*coupling**2/cut-2*np.pi*coupling**2))
    ds=np.linspace(-cfg['cutoffs'][-1],cfg['cutoffs'][-1],cfg['raw_grid_points'])
    w=np.sqrt(coupling**2+(ds/2)**2)
    np.savez(raw/f'box_{coupling}.npz',delta=ds,eta=(coupling*np.sin(w)/w)**2)
    rows.append(dict(kappa_L=coupling,eigenvalue_imaginary_parts=ys,trace_prediction=total,energy_budget=2*np.pi*coupling**2,integrals=integrals,opa_integrals=opa))
summary=dict(agent='gpt-b',model='gpt-6-astra',family='gpt',run_id=base.name,gauge_u=str(gauge_u),gauge_v=str(gauge_v),rows=rows,wall_seconds=time.perf_counter()-t0,python=platform.python_version(),interpretation='Tail-corrected quadrature checks normalization only. Uniform-box OPA normalization also checked; no proof for arbitrary OPA profiles, depletion, finite-length optimum or loss extension.')
(base/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
