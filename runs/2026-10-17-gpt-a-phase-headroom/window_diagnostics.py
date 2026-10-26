#!/usr/bin/env python3
# agent: gpt-a; model: gpt-6-astra; family: gpt
"""Inspect saved fields only; distinguish mass stability from field stability."""
from independent import *
from scipy.optimize import minimize_scalar

rows=[]
for N in [3,4,5]:
    a=np.load(RAW/f'qualified_N{N}_step1.npz')
    b=np.load(RAW/f'qualified_N{N}_window.npz')
    t=a['t'];u=a['u'];offset=(len(b['u'])-len(u))//2;v=b['u'][offset:offset+len(u)]
    k=2*np.pi*fftfreq(len(t),t[1]-t[0]);V=fft(v)
    def aligned(shift):
        w=ifft(V*np.exp(1j*k*shift));phase=np.vdot(w,u)
        return w*phase/abs(phase)
    def objective(shift):return float(np.linalg.norm(u-aligned(shift))/np.linalg.norm(u))
    fit=minimize_scalar(objective,bounds=(-.5,.5),method='bounded',options={'xatol':1e-10})
    ui,_=initial(t,N,str(HERE/f'selected_N{N}_coef.csv'))
    vi,_=initial(b['t'],N,str(HERE/f'selected_N{N}_coef.csv'));vi=vi[offset:offset+len(u)]
    rows.append(dict(N=N,raw_field_error=float(np.linalg.norm(u-v)/np.linalg.norm(u)),
                     phase_aligned_error=objective(0.),phase_time_aligned_error=fit.fun,
                     fitted_time_shift_T0=fit.x,
                     intensity_relative_error=float(np.linalg.norm(abs(u)**2-abs(v)**2)/np.linalg.norm(abs(u)**2)),
                     input_field_difference=float(np.linalg.norm(ui-vi)/np.linalg.norm(ui))))
out=dict(agent='gpt-a',model='gpt-6-astra',family='gpt',run_id=HERE.name,cases=rows,
         note='Post-run diagnostic on unchanged saved fields. A small fraction discrepancy is not a claim of full complex-field convergence.')
(HERE/'window_diagnostics.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
