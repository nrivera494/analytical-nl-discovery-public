"""Known limits before claim checks. gpt-c / gpt-6-astra / gpt."""
from pathlib import Path
import numpy as np
from independent import zs_root,propagate,write_json,response

out={'agent':'gpt-c','model':'gpt-6-astra','family':'gpt','zs':[],'propagation':[],'response':[]}
for A,C in [(1,0),(2,0),(3.5,0),(3,1.5)]:
    t=np.linspace(-16,16,8193); q=A/np.cosh(t)*np.exp(-1j*C*np.log(np.cosh(t)))
    expected=np.sqrt(A*A-C*C/4)-.5
    for points in [2048,4096,8192]:
        r=zs_root(t,q,[0,expected],points)
        out['zs'].append(dict(A=A,C=C,expected=expected,**r,error=r['eta']-expected))
for model in ['bw','hc','la']:
    w=np.array([0.,1e-4,-1e-4]); H,f=response(w,1,model)
    out['response'].append({'model':model,'H0':float(H[0].real),'fR':f,'TR_fs':float(-f*H[1].imag/1e-4)})
def cb(t,q,s):
    N=1; phase=np.angle(np.vdot(1/np.cosh(t),q))
    out['propagation'].append(dict(s,relative_L2=float(np.linalg.norm(q*np.exp(-1j*phase)-1/np.cosh(t))/np.linalg.norm(q))))
propagate({'N':1,'T0_fs':100,'raman':'off','n':2048,'width':40,'zN':[1,4],'tol':1e-9},cb)
write_json(Path(__file__).with_name('calibration.json'),out)
print(out)
