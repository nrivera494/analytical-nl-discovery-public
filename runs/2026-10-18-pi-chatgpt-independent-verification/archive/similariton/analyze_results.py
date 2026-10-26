#!/usr/bin/env python3
"""Summarize existing independently generated results; no repository imports."""
import json
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares

root=Path(__file__).parent
fv=json.loads((root/'results_fv.json').read_text())
data={'reduced_regression_slopes_12_26':fv['regression_slopes_12_26'],
      'period_matched_l2_slopes':fv['period_matched_l2_slopes'],
      'period_matched_l2':fv['period_matched_l2'],
      'full_shape_fits':[]}
for v in json.loads((root/'results_nlse_extended.json').read_text())['cases']:
    if v['tau']<6:continue
    t=np.array([x['tau'] for x in v['samples']])
    y=np.array([x['n_from_unit_eps_phase'] for x in v['samples']])
    for j,l in enumerate([2,3,4]):
        nu=np.sqrt(l*(l+1)/2-1)/3
        mask=t>=1
        def fun(c):
            return (np.exp(-c[0]*t[mask])*(c[2]*np.sin(c[1]*t[mask])+
                    c[3]*np.cos(c[1]*t[mask]))-y[mask,j])
        sol=least_squares(fun,[1/3,nu,-l*(l+1)/np.sqrt(18)/nu,0],
                          xtol=1e-12,ftol=1e-12,gtol=1e-12)
        exact=-l*(l+1)/np.sqrt(18)/nu*np.exp(-t/3)*np.sin(nu*t)
        data['full_shape_fits'].append(dict(ngrid=v['ngrid'],dt=v['dt'],l=l,
            interval=[1,6],decay=sol.x[0],frequency=sol.x[1],
            predicted_decay=1/3,predicted_frequency=nu,
            trajectory_relative_L2_error=float(np.linalg.norm(y[:,j]-exact)/
                                               np.linalg.norm(exact)),
            fit_relative_L2_residual=float(np.linalg.norm(fun(sol.x))/
                                          np.linalg.norm(y[mask,j]))))
data['linearization_examples']=[]
for tau in [6,12,18]:
    phi=(np.exp(2*tau/3)-1)/(2*np.sqrt(2)*.05)
    v=8*phi**2/9
    data['linearization_examples'].append(dict(eps=.05,tau=tau,
        Phi_NL=float(phi),leading_N0_times_Var_p0=float(v),
        phase_rms_at_N0_10000=float(np.sqrt(v/10000))))
data['short_time_derivative_Cmin_per_tau']=float(2-8/(5*.05*np.sqrt(18)))
(root/'analysis_summary.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(data,indent=2))
