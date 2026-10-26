"""Independent functional symmetry and Kerr-limit tests."""
from propagate import *
base=Path(__file__).parent;f=Fibre('S28',loss_scale=0.);s=BoundSolver(f,n=8192,dt=.0015);Q=ifft(sech(s.t/.05));rows=[]
cases={'base':Q,'phase':Q*np.exp(.71j),'time':Q*np.exp(1j*s.Om*.31),'frequency':np.roll(Q,10),'amplitude':1.3*Q}
for name,q in cases.items():
 dq=s.nl(q);E=s.dt*s.n*np.sum(abs(q)**2)
 rows.append({'case':name,'E':float(E),'rate':float(s.current_rhs),'identity':float(s.current_identity),'ratio':float(-s.current_rhs/(s.kappa*E**2))})
f.fR=0.;k=BoundSolver(f,n=s.n,dt=s.dt);k.nl(Q)
dump(base/'symmetry_summary.json',{**IDENTITY,'cases':rows,'Kerr_only_energy_rate':float(k.current_rhs),'expected':'Translations/global phase leave rate unchanged; amplitude 1.3 multiplies E by 1.3^2 and rate by 1.3^4. No-Raman energy rate is zero.'})
