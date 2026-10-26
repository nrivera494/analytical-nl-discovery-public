#!/usr/bin/env python3
"""Input sensitivity of the largest Gaussian Zakharov-Shabat eigenvalue.

agent: gpt-b; model: gpt-6-astra; family: gpt.
This is a neutral-coordinate covariance diagnostic, not a filtered-Fano
formula. Complex Gaussian radiation correlations remain necessary.
"""
import json
from pathlib import Path
import sys
import numpy as np
from scipy.integrate import solve_ivp, cumulative_trapezoid
from scipy.special import gammaln
from soliton_gaussian_scattering import discrete_spectrum


def gradient(N,shape='gaussian',points=16385):
    eig=discrete_spectrum(N,shape=shape,half_window=20.,max_step=.02)
    eta=eig['eigenvalue_imaginary_parts'][0]
    x=np.linspace(-20,0,points)
    def base(x):return np.exp(-x*x/2) if shape=='gaussian' else 1/np.cosh(x)
    sol=solve_ivp(lambda xx,y:[N*base(xx)-eta*np.sin(2*y[0])],(-20,0),[0.],
                  rtol=1e-11,atol=1e-13,max_step=.01,t_eval=x)
    theta=sol.y[0];primitive=cumulative_trapezoid(np.cos(2*theta),x,initial=0)
    kernel=np.exp(-2*eta*(primitive[-1]-primitive))
    J=np.trapezoid(kernel*np.sin(2*theta),x);g=kernel/J
    norm2=2*np.trapezoid(g*g,x);derivative=2*np.trapezoid(g*base(x),x)
    # Frequency gradient is odd; on the negative half-line it is -g*cos(2theta).
    frequency_gradient=-g*np.cos(2*theta)
    frequency_norm2=2*np.trapezoid(frequency_gradient**2,x)
    carrier_response=2*np.trapezoid(frequency_gradient*x*N*base(x),x)
    eps=1e-4
    plus=discrete_spectrum(N+eps,shape)['soliton_amplitudes'][0]
    minus=discrete_spectrum(N-eps,shape)['soliton_amplitudes'][0]
    fd=(plus-minus)/(2*eps)
    row=dict(N=N,launch=shape,soliton_amplitude=2*eta,
        amplitude_gradient_norm_squared=float(norm2),coherent_sech_reference_norm_squared=4*eta,
        separated_soliton_energy_Fano=float(norm2/(4*eta)),
        da_dN_formula=float(derivative),da_dN_finite_difference=fd,
        derivative_relative_error=float(abs(derivative-fd)/abs(fd)),quadrature_points=points,
        frequency_gradient_norm_squared=float(frequency_norm2),
        frequency_carrier_shift_response=float(carrier_response),
        amplitude_frequency_cross_covariance=0.)
    if shape=='sech':
        amp=2*N-1
        exact=np.exp(np.log(2/(amp*np.sqrt(np.pi)))+gammaln(amp)
                     +2*gammaln(N+.5)-gammaln(amp+.5)-2*gammaln(N))
        row['sech_gamma_formula_F']=float(exact)
        row['sech_gamma_formula_error']=float(abs(norm2/(4*eta)-exact))
        row['sech_frequency_norm_formula']=float(2*amp*exact/(2*amp+1))
        row['sech_frequency_norm_formula_error']=float(abs(frequency_norm2-2*amp*exact/(2*amp+1)))
    return row


def main():
    rows=[gradient(n) for n in [1.,1.25,1.5,1.75,2.,3.]]
    controls=[gradient(n,shape='sech') for n in [1.,1.5,2.,2.7]]+[gradient(1.25,points=32769)]
    out=dict(agent='gpt-b',model='gpt-6-astra',family='gpt',points=rows,controls=controls,
        readout='energy of asymptotically separated largest classical Kerr soliton; not a binary spectral mask')
    Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))


if __name__=='__main__':main()
