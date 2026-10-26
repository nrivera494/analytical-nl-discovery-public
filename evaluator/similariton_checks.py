#!/usr/bin/env python3
# agent: gpt-a; model: gpt-6-astra; family: gpt
"""Independent symbolic and ODE checks for T-20261008-gpt-a-01."""
from pathlib import Path
import json, platform, subprocess, time
import numpy as np
import sympy as s
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares
import yaml

ROOT = Path(__file__).resolve().parents[1]
RUN = "2026-10-08-gpt-a-similariton-checks"
OUT = ROOT / "runs" / RUN
RAW = Path.home() / "analytical-nl-discovery-data" / RUN
OUT.mkdir(exist_ok=True); RAW.mkdir(exist_ok=True)
started = time.monotonic()
tau, g, k, E, b0 = s.symbols("tau g k E b0", positive=True)
x = s.symbols("x", real=True)
b = s.Function("b")(tau)
P = 3*E*s.exp(g*tau)/(4*b)
T = s.symbols("T", real=True)
rho = P*(1-T**2/b**2)
v = s.diff(b,tau)*T/b
continuity = s.simplify(s.diff(rho,tau)+s.diff(rho*v,T)-g*rho)
momentum = s.simplify((s.diff(v,tau)+v*s.diff(v,T)+k*s.diff(rho,T)).subs(s.diff(b,tau,2),3*k*E*s.exp(g*tau)/(2*b**2)))
ss = s.symbols("ss", positive=True)
q = s.symbols("q", real=True)
accel = -2*q/3-ss/9+1/(9*ss**2)
V = q*q/2+ss*ss/18+1/(9*ss)
Vdot = s.simplify(s.diff(V,ss)*q+s.diff(V,q)*accel+2*q*q/3)
legendre = {}
for ell in range(1,9):
    pol = s.legendre(ell,x)
    legendre[str(ell)] = str(s.simplify(s.diff((1-x*x)*s.diff(pol,x),x)+ell*(ell+1)*pol))
# Differentiated Riemann invariant equation, including the gain source.
alpha, beta = s.symbols("alpha beta", real=True)
c = s.symbols("c", positive=True)
dal = -(3*alpha+beta)*alpha/4+g*(alpha-beta)/4
dc = g*c/2-c*beta/2
Q = (alpha+g)/s.sqrt(c)
Qdot = s.diff(Q,alpha)*dal+s.diff(Q,c)*dc
Qrhs = -s.Rational(3,4)*s.sqrt(c)*Q**2+3*g*Q/2-g*g/s.sqrt(c)
riemann = str(s.simplify(Qdot-Qrhs))
# A protected positive-density interval realizing the Riccati counterexample.
ell0=1/40; c0=1.; gain0=1.; grad0=c0/(2*ell0)
shock_bound=4/(3*(grad0-gain0))*np.sqrt(8/7)
domain_distance=10*c0/gain0*np.expm1(gain0*shock_bound/2)

def rhs(t,y):
    a,ap=y
    return [ap,-2*ap/3-a/9+1/(9*a*a)]

def fit_mode(t,y,yp):
    # Joint fit of width and its exact derivative; no finite differentiation.
    def model(p):
        decay,freq,A,B=p
        z=A*np.cos(freq*t)+B*np.sin(freq*t)
        dz=freq*(-A*np.sin(freq*t)+B*np.cos(freq*t))
        return np.exp(-decay*t)*z,np.exp(-decay*t)*(dz-decay*z)
    scale=max(np.max(np.abs(y)),1e-15)
    def residual(p):
        f,fp=model(p)
        return np.r_[(f-y)/scale,(fp-yp)/scale]
    init=[1/3,np.sqrt(2)/3,y[0],(yp[0]+y[0]/3)/(np.sqrt(2)/3)]
    fit=least_squares(residual,init,bounds=([0,0,-np.inf,-np.inf],[2,2,np.inf,np.inf]),
                      xtol=1e-13,ftol=1e-13,gtol=1e-13,max_nfev=10000)
    return dict(decay=float(fit.x[0]),angular_frequency=float(fit.x[1]),
                relative_joint_rms=float(np.sqrt(np.mean(fit.fun**2))))

ode=[]
for name,a,qq in [("small_width",1.001,1/3),("narrow_compressive",0.5,-1.),
                  ("broad_expanding",2.,1.),("heldout_inward",1.6,-0.6)]:
    ts=np.linspace(0,42,4201)
    sol=solve_ivp(rhs,[0,42],[a,a*(qq-1/3)],method="DOP853",t_eval=ts,rtol=2e-12,atol=2e-14)
    width,wp=sol.y
    energy=wp*wp/2+width*width/18+1/(9*width)
    fits={}
    for start,end in [(12.,30.),(18.,36.),(24.,42.)]:
        mask=(ts>=start)&(ts<=end)
        fits[f"{start:g}-{end:g}"]=fit_mode(ts[mask]-start,width[mask]-1,wp[mask])
    ode.append(dict(label=name,s0=a,q0=qq,min_width=float(min(width)),
                    final_width=float(width[-1]),final_width_derivative=float(wp[-1]),
                    initial_lyapunov=float(energy[0]),final_lyapunov=float(energy[-1]),
                    largest_sampled_lyapunov_increase=float(max(np.diff(energy))),fits=fits))
    np.savez(RAW/f"{name}.npz",tau=ts,width=width,width_derivative=wp,lyapunov=energy)

# Nonlinear quantile-map inequality, beyond the parabolic family.
from numpy.polynomial.legendre import leggauss
aa,weights=leggauss(512)
r=(1-aa*aa)/18; rp=-aa/9
rng=np.random.default_rng(18491)
cases=[]
for j in range(80):
    slope=rng.uniform(.5,2.); shift=rng.uniform(-1,1); h=rng.uniform(-.12,.12)
    X=slope*aa+shift+h*(aa**3-aa)
    Xa=slope+h*(3*aa*aa-1); Xaa=6*h*aa
    vel=rng.normal(0,.2,3); U=vel[0]+vel[1]*aa+vel[2]*(aa*aa-1/5)
    grad=X/9+rp/Xa**2-r*Xaa/Xa**3
    F=np.sum(weights*(r*r/(2*Xa)+r*X*X/18))
    Fstar=np.sum(weights*(r*r/2+r*aa*aa/18))
    Y=X-aa; W=U+Y/3
    H=F-Fstar+.5*np.sum(weights*r*W*W)
    Hdot=np.sum(weights*r*(grad*U+W*(-U/3-grad)))
    cases.append(dict(min_jacobian=float(min(Xa)),H=float(H),Hdot=float(Hdot),
                      inequality_residual=float(Hdot+H/3)))

summary=dict(agent="gpt-a",model="gpt-6-astra",family="gpt",run_id=RUN,
    symbolic=dict(continuity=str(continuity),momentum=str(momentum),width_lyapunov=str(Vdot),
                  legendre=legendre,riemann_gradient_identity=riemann),
    predicted=dict(decay_per_gain_length=1/3,breathing_frequency_per_gain_length=float(np.sqrt(2)/3),
                   density_semiclassical_exponent=-2/3,
                   conditional_modulated_energy_exponent=-1/3,
                   conditional_transport_exponent=-1/6),
    width_ode=ode,quantile_inequality=dict(cases=len(cases),
        largest_residual=max(c["inequality_residual"] for c in cases),
        smallest_jacobian=min(c["min_jacobian"] for c in cases)),
    parity=dict(normalized_even_odd_overlap=0.,equal_mass_field_distance_squared=2.),
    protected_shock_example=dict(c0=c0,gain=gain0,ell=ell0,R=1.,
        initial_negative_riemann_gradient=grad0,chi=gain0*ell0/c0,
        upper_breaking_gain_length=shock_bound,required_protected_radius=domain_distance,
        radius_condition_satisfied=bool(domain_distance<1)),
    caveat="ODE checks and exact identities; no full-NLSE global convergence proof")
(RAW/"quantile_cases.json").write_text(json.dumps(cases,indent=2)+"\n")
(OUT/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
config=dict(agent="gpt-a",model="gpt-6-astra",family="gpt",script="evaluator/similariton_checks.py",
            task="T-20261008-gpt-a-01",seed=18491,ode_rtol=2e-12,ode_atol=2e-14,
            gain_length_max=42,quantile_quadrature_points=512)
(OUT/"config.yaml").write_text(yaml.safe_dump(config,sort_keys=False))
commit=subprocess.check_output(["git","-C",str(ROOT/"solver"),"rev-parse","HEAD"],text=True).strip()
meta=dict(run_id=RUN,agent="gpt-a",model="gpt-6-astra",family="gpt",task="T-20261008-gpt-a-01",
          exploration="explorations/2026-10-08-gpt-a-similariton-attraction.md",
          solver_commit=commit,solver_dirty=False,solver_used=False,
          hardware=platform.platform(),hostname=platform.node(),wall_seconds=time.monotonic()-started,
          raw_location=str(RAW),purpose="Independent symbolic residuals, nonlinear width rates, transport Lyapunov checks")
(OUT/"meta.yaml").write_text(yaml.safe_dump(meta,sort_keys=False))
print(json.dumps(summary,indent=2))
