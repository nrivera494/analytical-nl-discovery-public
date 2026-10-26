#!/usr/bin/env python3
"""Small-temperature law for the optimized centered soliton passband.
agent: gpt-b; model: gpt-6-astra; family: gpt.
An achievable filter optimum is not a lower bound on arbitrary masks.
"""
import json,sys,time
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from soliton_jost_filter import bandpass


def main():
    started=time.monotonic();order=320
    fun=lambda x,rho=0.:bandpass(x[0],x[1],order=order,rho=rho)
    opt=minimize(fun,[4.75,.736],method='Nelder-Mead',options={'xatol':1e-6,'fatol':1e-10})
    x=opt.x;h=np.array([.002,.0005]);H=np.zeros((2,2));gradB=np.zeros(2)
    bf=lambda y:bandpass(y[0],y[1],order=order,include_checks=True)['Raman_per_rho']
    for i in range(2):
        d=np.eye(2)[i]*h[i]
        H[i,i]=(fun(x+d)-2*fun(x)+fun(x-d))/h[i]**2
        gradB[i]=(bf(x+d)-bf(x-d))/(2*h[i])
        for j in range(i):
            e=np.eye(2)[j]*h[j]
            H[i,j]=H[j,i]=(fun(x+d+e)-fun(x+d-e)-fun(x-d+e)+fun(x-d-e))/(4*h[i]*h[j])
    correction=np.linalg.solve(H,gradB)
    baseline=bandpass(x[0],x[1],order=640,include_checks=True)
    c0=baseline['F_Kerr'];c1=baseline['Raman_per_rho'];c2=-.5*gradB@correction
    rows=[]
    for rho in [.01,.02,.029475502239748363,.05741980955795136,.11483961911590272]:
        fit=minimize(lambda y:fun(y,rho),x-rho*correction,method='Nelder-Mead',
                     options={'xatol':1e-6,'fatol':1e-10})
        result=bandpass(fit.x[0],fit.x[1],order=640,rho=rho,include_checks=True)
        rows.append(dict(rho=rho,z_over_LD=float(fit.x[0]),edge=float(fit.x[1]),
                         F=result['F'],F_series=float(c0+c1*rho+c2*rho*rho)))
    out=dict(agent='gpt-b',model='gpt-6-astra',family='gpt',
        quantity='best centered passband over distance near its first minimum; upper bound on arbitrary binary optimum',
        Kerr_optimum=dict(z_over_LD=float(x[0]),edge=float(x[1]),F=c0),
        coefficients_in_rho=[c0,c1,float(c2)],first_order_optimum_shift_per_rho=(-correction).tolist(),
        Hessian=H.tolist(),gradient_B=gradB.tolist(),points=rows,
        order_for_optimization=order,order_for_values=640,wall_time_s=time.monotonic()-started)
    Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))


if __name__=='__main__':main()
