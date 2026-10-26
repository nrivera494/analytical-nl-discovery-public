#!/usr/bin/env python3
"""Exact identities and independent quadrature checks for the soliton kernels.
agent: gpt-b; model: gpt-6-astra; family: gpt.
"""
import json
from pathlib import Path
import sys
import numpy as np
import sympy as sp
from scipy.integrate import quad
from soliton_jost_filter import white_source_gram, even_coefficient, C


def main():
    t,k=sp.symbols('t k',real=True)
    u=(k+sp.I*t)**2/(1+k*k);v=(1-t*t)/(1+k*k)
    def d(f):return (1-t*t)*sp.diff(f,t)+sp.I*k*f
    huu=-d(d(u))/2+(sp.Rational(1,2)-2*(1-t*t))*u-(1-t*t)*v
    hvv=d(d(v))/2+(-sp.Rational(1,2)+2*(1-t*t))*v+(1-t*t)*u
    residues=[str(sp.factor(huu-(1+k*k)/2*u)),str(sp.factor(hvv-(1+k*k)/2*v))]
    assert residues==['0','0']
    values=[]
    for kval,lval in [(0.,0.),(.7,-.2),(1.3,2.1),(-2.5,.3)]:
        def integrand(x):
            q=1/np.cosh(x);tt=np.tanh(x)
            ss=lambda kk: ((kk+1j*tt)**2+q*q)/(1+kk*kk)*np.exp(1j*kk*x)
            return q*q*ss(kval)*ss(lval).conjugate()
        numerical=quad(lambda x:integrand(x).real,-25,25,epsabs=1e-12)[0]+1j*quad(lambda x:integrand(x).imag,-25,25,epsabs=1e-12)[0]
        exact=white_source_gram(np.array([kval,lval]))[0,1]
        values.append({'k':kval,'l':lval,'quadrature':float(numerical.real),'formula':float(exact),'absolute_error':float(abs(numerical-exact))})
    coefficients=[]
    a=.7368
    j1=quad(lambda p:p*np.tanh(C*p),-a,a,epsabs=1e-12)[0]
    for kval in [-1.3,-.2,.31,1.1]:
        if abs(kval)<a:
            def smooth(p):
                d=p-kval
                return -p/C if abs(d)<1e-10 else d*p/np.tanh(-C*d)
            j2=quad(smooth,-a,a,weight='cauchy',wvar=kval,epsabs=1e-12)[0]
        else:j2=quad(lambda p:p/np.tanh(C*(kval-p)),-a,a,epsabs=1e-12)[0]
        direct=np.pi/np.cosh(C*kval)/(1+kval*kval)*((kval*kval-1)*(abs(kval)<a)-j1-j2)
        analytic=even_coefficient(np.array([kval]),a)[0]
        coefficients.append({'k':kval,'edge':a,'quadrature':float(direct),'formula':float(analytic),'absolute_error':float(abs(direct-analytic))})
    normf=quad(lambda x:(1/np.cosh(x)*(1-x*np.tanh(x)))**2,-30,30,epsabs=1e-12)[0]
    normqf=quad(lambda x:(1/np.cosh(x)**2*(1-x*np.tanh(x)))**2,-30,30,epsabs=1e-12)[0]
    out={'agent':'gpt-b','model':'gpt-6-astra','family':'gpt','Jost_symbolic_residuals':residues,
         'white_source_Gram_checks':values,'edge_primitive_checks':coefficients,
         'phase_dual_norm2':normf,'phase_dual_norm2_formula':2/3+np.pi**2/18,
         'phase_source_norm2':normqf,'phase_source_norm2_formula':2/3+np.pi**2/45}
    path=Path(sys.argv[1]);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
