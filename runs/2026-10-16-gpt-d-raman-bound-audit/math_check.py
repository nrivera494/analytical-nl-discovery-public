"""Independent Raman-bound algebra and quadrature. gpt-d/gpt-6-astra/gpt."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'2026-10-16-gpt-d-loss-edge-audit'))
from independent import *
base=Path(__file__).parent;t0=time.monotonic();out={**IDENTITY,'responses':{}}

def sech_transform(x):
 y=abs(np.pi*x/2)
 return 1. if y<1e-7 else 2*y*np.exp(-y)/(-np.expm1(-2*y))

def rho(r,A):
 # y=Omega*T resolves the intensity bandwidth at both asymptotic ends.
 def fn(y):
  x=y/r;den=(1+A*A-x*x)**2+4*A*A*x*x
  return 4*A/(np.pi*r)*x*x/den*sech_transform(y)**2
 points=sorted(set(x for x in [r*.2,r*.5,r,r*2,r*5,1.,5.,15.] if 0<x<40))
 return integrate.quad(fn,0,40,points=points,epsabs=2e-12,epsrel=2e-11,limit=300)[0]
for mat in ['S28','Z75']:
 f=Fibre(mat,loss_scale=0.);a=1/f.t2;b=1/f.t1;A=f.t1/f.t2;hp=a*a+b*b;coef=f.g0*f.fR/f.w0;k=coef*hp/2
 wfun=lambda x:2*A*(1+A*A)*x*x/((1+A*A-x*x)**2+4*A*A*x*x)
 sm=integrate.quad(wfun,0,np.inf,epsabs=1e-11,epsrel=1e-12,limit=200)[0]/(np.pi*f.t1*f.t1)
 rs=[.001,.002,.004,.008,.016,.04,.08,.16,.4,.8,1.,2.,4.,10.,20.,40.,80.,160.]
 rows=[{'T_over_tau1':r,'T_fs':1000*f.t1*r,'ratio':rho(r,A),'long_prediction':16*A/(15*(1+A*A)**2*r**3),'short_gap_prediction':2*A*r} for r in rs]
 exps={}
 for name,sel,val in [('long_10_80',lambda r:10<=r['T_over_tau1']<=80,lambda r:r['ratio']),('long_40_160',lambda r:40<=r['T_over_tau1']<=160,lambda r:r['ratio']),('short_1e3_8e3',lambda r:.001<=r['T_over_tau1']<=.008,lambda r:1-r['ratio'])]:
  rr=[r for r in rows if sel(r)];slope=float(np.polyfit(np.log([r['T_over_tau1'] for r in rr]),np.log([val(r) for r in rr]),1)[0]);exps[name]=-slope if name.startswith('long') else slope
 out['responses'][mat]={'tau1_fs':1000*f.t1,'tau2_fs':1000*f.t2,'fR':f.fR,'Aeff_um2':f.A0,'n2_m2_W':f.n2,'kappa_pJinv_minv':k,'sum_rule_integral_psinv2':sm,'hprime_half_psinv2':hp/2,'sum_rule_relative_error':sm/(hp/2)-1,'passivity_min_sample':float(np.min(np.linspace(-1000,1000,20001)*f.H(np.linspace(-1000,1000,20001)).imag)),'cases':rows,'exponents':exps}
out['wall_s']=time.monotonic()-t0;dump(base/'math_summary.json',out);print(json.dumps({m:{k:v for k,v in d.items() if k!='cases'} for m,d in out['responses'].items()},indent=2))
