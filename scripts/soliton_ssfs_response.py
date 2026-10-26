#!/usr/bin/env python3
"""Full-response classical sech SSFS moment, without covariance resetting.

agent: gpt-b; model: gpt-6-astra; family: gpt.
This post-hoc diagnostic does not replace the frozen first-moment forecast.
"""
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.integrate import quad


def response_rate(amplitude, T0_ps, fr=.18, tau1_ps=.0122, tau2_ps=.032):
    tr = fr*2*tau1_ps**2*tau2_ps/(tau1_ps**2+tau2_ps**2)
    aR=1/tau2_ps;bR=1/tau1_ps
    cR=2*(bR*bR-aR*aR)/(aR*aR+bR*bR)**2
    def integrand(k):
        omega = amplitude*k/T0_ps
        response = (tau1_ps**-2+tau2_ps**-2)/((tau2_ps**-1-1j*omega)**2+tau1_ps**-2)
        h = 2. if k == 0 else np.pi*k/np.sinh(np.pi*k/2)
        return k*fr*response.imag*h*h/np.pi
    integral, error = quad(integrand, 0., 40., epsabs=1e-13, epsrel=1e-11)
    exact = -amplitude**3*integral/2
    first = -8*tr*amplitude**4/(15*T0_ps)
    return dict(full_response_rate=exact, first_moment_rate=first,
                response_correction_ratio=exact/first,
                relative_second_order_prediction=1+20*cR*amplitude**2/(7*T0_ps**2),
                relative_residual_after_second_order=exact/first-1-20*cR*amplitude**2/(7*T0_ps**2),
                quadrature_error_bound_estimate=amplitude**3*error/2,
                response_width_over_soliton_width=tau2_ps*amplitude/T0_ps)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--raw',required=True)
    args=ap.parse_args();raw=Path(args.raw);raw.mkdir(parents=True,exist_ok=True)
    rows=[]
    cases=[('fundamental',1.,.25,3*np.pi/2,None),
           ('Gaussian_N1.25',1.3753906129146694,.25,3.,-.03565469835588607),
           ('Gaussian_N2_fission',2.926210847337887,.125,8.,-4.781153981243761)]
    for name,a,t0,z,observed in cases:
        row=dict(case=name,amplitude=a,T0_ps=t0,z_over_LD=z,**response_rate(a,t0))
        row.update(full_response_no_formation_shift=z*row['full_response_rate'],
                   first_moment_no_formation_shift=z*row['first_moment_rate'],
                   fitted_core_carrier_times_T0=observed)
        if observed is not None:
            row['first_moment_relative_forecast_error']=abs(observed/row['first_moment_no_formation_shift']-1)
            row['posthoc_full_response_relative_error']=abs(observed/row['full_response_no_formation_shift']-1)
        rows.append(row)
    asymptotes=[]
    for width in [.125,.25,.5,1.,2.]:
        row=dict(T0_ps=width,**response_rate(1.,width))
        if asymptotes:
            row['relative_residual_power']=float(np.log2(abs(asymptotes[-1]['relative_residual_after_second_order']/row['relative_residual_after_second_order'])))
        asymptotes.append(row)
    result=dict(agent='gpt-b',model='gpt-6-astra',family='gpt',
        status='post-hoc diagnostic; original frozen forecast remains independently scored',
        scope='Instantaneous momentum derivative for a resting sech in the classical scalar Raman equation. Multiplication by distance neglects formation, changing shape, shock, beta3 and radiation.',
        points=rows,long_pulse_checks=asymptotes)
    (raw/'ssfs_response.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
