"""Independent rescaled BdG/Duhamel calculation of Gaussian weak-GVD terms.

No repository implementation imported.  Uses exact polynomial action on the
harmonic ground state and symbolic z integrals.  eps=sqrt(y), x=sqrt(eps)*q.
Mean: rho=1-eps*q**2+eps**2*(q**4/2-s**2)+O(eps**3).
"""
import json
from pathlib import Path
import sympy as sp

q, s, t, F, r = sp.symbols('q s t F r', real=True, positive=True)
b=sp.sqrt(6)
e=sp.Matrix([1,-r])
ep=sp.Matrix([r,1])

def simp(x):
    return x.applyfunc(sp.expand) if isinstance(x,sp.MatrixBase) else sp.expand(x)
def M(z):
    return sp.Matrix([[1,0],[2*F*z,1]])
def deriv(p):
    return sp.diff(p,q)-b*q*p
def D(p):
    return -sp.diff(p,q,2)+2*b*q*sp.diff(p,q)+(b-b*b*q*q)*p
def G1(v):
    return simp(sp.Matrix([-D(v[1])/(2*F),D(v[0])/(2*F)-2*F*q*q*v[0]]))
def G2(v,z):
    dilation=lambda p: -z*(2*q*deriv(p)+p)
    return simp(sp.Matrix([dilation(v[0])+v[1]/(2*F),dilation(v[1])+(F*q**4-2*F*z*z-1/(2*F))*v[0]]))
def avg(p):
    poly=sp.Poly(sp.expand(p),q)
    out=0
    for (n,),c in poly.terms():
        if n%2==0:
            out+=c*sp.factorial2(n-1)/(2*b)**(n//2) if n else c
    return sp.simplify(out)
def integ(v,var,lo,hi):
    return v.applyfunc(lambda p: sp.integrate(sp.expand(p),(var,lo,hi)))
def dot(v,w):
    return (v.T*w)[0]

f0=M(1).T*e
term2=integ(M(1-s)*G2(M(s)*f0,s),s,0,1)
term11=integ(integ(M(1-s)*G1(M(s-t)*G1(M(t)*f0)),t,0,s),s,0,1)
S2f0=simp(term2+term11)
# S1^dagger acting on unnormalized squeezed direction.
S1dag_e=simp(sp.Matrix([-D(e[0])/2+(1/(2*F)-F/3)*D(e[1])-2*F*q*q*e[1],-D(e[0])/(2*F)-D(e[1])/2]))
V2exp=avg(2*dot(e,S2f0)+dot(S1dag_e,S1dag_e))/(1+r*r)

# Explicit first-order covariance operator.
def V1(v):
    B=sp.Matrix([[-1,-4*F/3],[-4*F/3,1-4*F*F/3]])
    C=sp.Matrix([[0,-2*F],[-2*F,-8*F*F]])
    return simp(B*sp.Matrix([D(v[0]),D(v[1])])+q*q*C*v)
cross=sp.expand(dot(ep,V1(e)))/(1+r*r)
cross2=avg(cross*cross)/(r**-2-r*r)
coeff2=sp.factor((V2exp-cross2).subs(F,(1-r*r)/(2*r)))
coeff1=r*r*(1-r*r)/(1+r*r)*sp.sqrt(sp.Rational(2,3))
first_direct=sp.factor((avg(dot(e,V1(e)))/(1+r*r)).subs(F,(1-r*r)/(2*r)))
assert sp.simplify(first_direct-coeff1)==0
c2=sp.factor(coeff2/coeff1)
print('coefficient eps^2 in lambda:',coeff2)
print('relative correction c2 in excess:',c2)
out={'epsilon':'sqrt(y)','r':'sqrt(1+Phi**2)-Phi',
     'lambda_epsilon2_coefficient_in_r':str(coeff2),
     'c2_in_r':str(c2),'table':{}}
for FF in [2,3,5,10,20,40]:
    rr=sp.sqrt(1+FF*FF)-FF
    value=float(c2.subs(r,rr).evalf(20))
    out['table'][str(FF)]=value
    print(FF,value)
Path(__file__).with_name('second_order_symbolic.json').write_text(json.dumps(out,indent=2)+'\n')
