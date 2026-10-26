#!/usr/bin/env python3
"""gpt-b / gpt-6-astra / gpt; pinned RK4IP cross-check, no adjoint."""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'evaluator'))
from squeezing import *
from numpy.polynomial.hermite import hermgauss
RUN=Path(__file__).resolve().parent;DATA=RAW/RUN.name

def prepare():
    memory_gate();m=Model(5);a=m.launch(.6,4201);initial=[a]
    for eps in [1e-5,2e-5]:
      for d in np.r_[np.eye(m.M),1j*np.eye(m.M)]:initial.extend([a+eps*d,a-eps*d])
    x,w=hermgauss(9);initial1=(1+(x[:,None]+1j*x[None,:])/np.sqrt(2*4096)).reshape(-1)
    # Black-box one-step probe established that the pinned solver conjugates its fourth slot.
    np.savez(DATA/'squeezing_solver_input.npz',tensor=m.tensor,tensor_solver=np.transpose(m.tensor,(0,2,3,1)),initial=np.array(initial),initial1=initial1,weights=np.outer(w,w).reshape(-1)/np.pi)

def diagnose():
    import shutil
    m=Model(5);a=m.launch(.6,4201);rhs=m.rhs(a);probe=np.load(DATA/'squeezing_solver_probe.npz')
    errors={k:float(np.linalg.norm(probe[k]-rhs)) for k in probe.files};best=min(errors,key=errors.get)
    if errors[best]>1e-4:raise RuntimeError('No index convention matches one-step RHS: '+str(errors))
    orders={'conj_second':(0,1,2,3),'conj_third':(0,2,1,3),'conj_fourth':(0,2,3,1)}
    inp=dict(np.load(DATA/'squeezing_solver_input.npz'));inp['tensor_solver']=np.transpose(inp['tensor'],orders[best])
    np.savez(DATA/'squeezing_solver_input.npz',**inp)
    pilot=json.loads((RUN/'solver_check.json').read_text())
    if max(r['jacobian_max_error'] for r in pilot['rows'])>1e-5:
      if not (RUN/'solver_initial_convention.json').exists():shutil.copy2(RUN/'solver_check.json',RUN/'solver_initial_convention.json')
      if not (DATA/'squeezing_solver_initial_convention.npz').exists():shutil.copy2(DATA/'squeezing_solver_output.npz',DATA/'squeezing_solver_initial_convention.npz')
    save_json(RUN/'solver_convention.json',dict(**IDENTITY,one_step_dt=1e-5,errors=errors,selected=best,python_axes=orders[best],
       note='Initial unpermuted resonant tensor failed; the full HG tensor is permutation-symmetric but the beat-averaged tensor is not. Black-box probe, no proposer or solver source read.'))

def compare():
    inp=np.load(DATA/'squeezing_solver_input.npz');out=np.load(DATA/'squeezing_solver_output.npz');m=Model(5);a=m.launch(.6,4201)
    x=tangent_run(m,a,[0,5],dt=.01,sigma=0)[-1];r=tangent_observables(x);rows=[]
    for h in [.01,.005]:
      final=out[f'h{h}'];base=final[0]
      for j,eps in enumerate([1e-5,2e-5]):
        pairs=final[1+j*60:1+(j+1)*60];der=(pairs[::2]-pairs[1::2])/(2*eps)
        rr=tangent_observables(np.r_[base[None,:],der]);rows.append(dict(h=h,epsilon=eps,jacobian_max_error=float(np.max(abs(der-x[1:]))),
          field_error=float(np.linalg.norm(base-x[0])),quad_error_dB=10*np.log10(rr['lambda_quad']/r['lambda_quad']),count_error_dB=10*np.log10(rr['lambda_gen']/r['lambda_gen'])))
    a=inp['initial1'];w=inp['weights'];n=4096;z=5
    exact=a*np.exp(-1j*z*(abs(a)**2-1/n));sm=[]
    for h in [.01,.005]:
      f=out[f'single_h{h}']*np.exp(1j*z/n)
      def variance(b):
        mean=w@b;v=2*np.sqrt(n)*np.column_stack([(b-mean).real,(b-mean).imag]);return np.linalg.eigvalsh((v.T*w)@v)[0]
      sm.append(dict(h=h,field_error=float(np.max(abs(f-exact))),lambda_solver=variance(f),lambda_classical_map=variance(exact),variance_error=variance(f)-variance(exact)))
    save_json(RUN/'solver_check.json',dict(**IDENTITY,solver_commit='b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa',rows=rows,single_mode=sm))
if __name__=='__main__':getattr(sys.modules[__name__],sys.argv[1])()
