#!/usr/bin/env python3
"""Independent frozen Raman quadrature and inequalities; gpt-d, gpt-6-astra, gpt."""
from pathlib import Path
import json, math, platform, subprocess, time
import numpy as np
import scipy.integrate as si
from scipy.fft import ifft, fftfreq
import mpmath as mp

HERE = Path(__file__).resolve().parent
RUN = HERE.name
RAW = Path.home()/"analytical-nl-discovery-data"/RUN
IDENTITY = dict(agent="gpt-d", model="gpt-6-astra", family="gpt")
FREEZE = "6df0927ef31369add037f36db21643b14d68bf51"
mp.mp.dps = 60

def exact_mp(x, r):
    x, r = mp.mpf(str(x)), mp.mpf(str(r))
    s = (r-1j)*x
    return mp.re((1+1j*r)*(1-s+s*s*mp.polygamma(1, 1+s/2)/2))

def weight(y, r):
    q = 1+r*r
    return 2*r*q*y*y/((q-y*y)**2+4*r*r*y*y)

def quad_rho(x, r):
    # Integrate v=Omega*T, independently of the trigamma expression.
    q = 1+r*r
    scale = max(1., x**3)
    def fn(v):
        u = math.pi*v/2
        sinc = 1. if u == 0 else (u/math.sinh(u))**2
        return scale*4*r*x/math.pi*v*v/((q*x*x-v*v)**2+4*r*r*x*x*v*v)*sinc
    points = sorted(set([0., 0.1*x, 0.5*x, x*math.sqrt(q), 2*x, 10*x, 1., 4., 16., 40.]))
    points = [v for v in points if v <= 40.]
    val, err = 0., 0.
    for lo, hi in zip(points[:-1], points[1:]):
        v, e = si.quad(fn, lo, hi, epsabs=2e-14, epsrel=3e-13, limit=200)
        val += v; err += e
    return val/scale, err/scale

def exponent(xs, ys):
    return float(np.polyfit(np.log(xs), np.log(np.abs(ys)), 1)[0])

def fit_summary(r, xs):
    c3 = 16*r/(15*(1+r*r)**2)
    d2 = 40*(1-r*r)/(7*(1+r*r)**2)
    xlong = np.array([40.,80.,160.])
    ylong = np.array([float(exact_mp(x,r)) for x in xlong])
    rel1 = np.array([float(exact_mp(x,r)/(mp.mpf(str(c3))/mp.mpf(str(x))**3)-1) for x in xlong])
    rel2 = np.array([float(exact_mp(x,r)/(mp.mpf(str(c3))/mp.mpf(str(x))**3)-1-mp.mpf(str(d2))/mp.mpf(str(x))**2) for x in xlong])
    xshort = np.array([.002,.004,.008,.016])
    gap = np.array([float(1-exact_mp(x,r)) for x in xshort])
    shortres = np.array([float(1-exact_mp(x,r)-2*mp.mpf(str(r))*mp.mpf(str(x))) for x in xshort])
    lc = np.polyfit(xlong**-2, ylong*xlong**3, 1)[-1]
    lc_fine = np.polyfit(xlong[-2:]**-2, (ylong*xlong**3)[-2:], 1)[-1]
    sc = np.polyfit(xshort, gap/xshort, 2)[-1]
    sc_fine = np.polyfit(xshort[:3], (gap/xshort)[:3], 2)[-1]
    out = dict(r=r, C3_predicted=c3, relative_Tminus2_coefficient=d2,
        C3_extrapolated=float(lc), C3_fit_window_difference=float(abs(lc-lc_fine)),
        short_linear_predicted=2*r, short_linear_extrapolated=float(sc),
        short_linear_fit_window_difference=float(abs(sc-sc_fine)),
        long_decay_exponent=-exponent(xlong,ylong),
        long_leading_relative_error_exponent=-exponent(xlong,rel1),
        long_corrected_relative_error_exponent=-exponent(xlong,rel2),
        short_gap_exponent=exponent(xshort,gap),
        short_linear_absolute_error_exponent=exponent(xshort,shortres),
        short_quadratic_coefficient=float(math.pi**2*(1-3*r*r)/12),
        long_x=xlong.tolist(), long_relative_error=rel1.tolist(),
        long_corrected_relative_error=rel2.tolist(),
        short_x=xshort.tolist(), short_linear_absolute_error=shortres.tolist())
    out["frozen_exponents_pass"] = bool(abs(out["long_decay_exponent"]-3)<.02 and
        abs(out["long_leading_relative_error_exponent"]-2)<.05 and
        abs(out["long_corrected_relative_error_exponent"]-4)<.15 and
        abs(out["short_gap_exponent"]-1)<.05 and
        abs(out["short_linear_absolute_error_exponent"]-2)<.08)
    return out

def profiles():
    rng = np.random.default_rng(20261017)
    rows=[]
    r=12.2/32
    for x in [.1,1.,10.]:
        n=32768; window=max(80*x,80/r); dt=window/n
        t=(np.arange(n)-n//2)*dt
        om=2*np.pi*fftfreq(n,dt)
        z=t/x
        sech = lambda v: 2*np.exp(-np.abs(v))/(1+np.exp(-2*np.abs(v)))
        shapes={"sech":sech(z)**2,"gaussian":np.exp(-z*z),
          "rectangle":(abs(z)<1).astype(float),"supergaussian":np.exp(-z**8),
          "incoherent_pair":sech(z-3)**2+0.6*sech(z+3)**2,
          "coherent_pair":abs(sech(z-1)*np.exp(.3j*z*z)+.8*sech(z+1)*np.exp(-.2j*z*z+1j))**2}
        if x==1:
            for j in range(64):
                I=np.zeros(n)
                for _ in range(6):
                    I+=rng.uniform(.1,1)*np.exp(-((t-rng.uniform(-6,6))/rng.uniform(.4,2))**2)
                shapes[f"positive_mixture_{j:02d}"]=I
        for name,I in shapes.items():
            E=dt*sum(I); Q=dt*sum(I*I)/E**2
            rho=2/(1+r*r)*window*sum(weight(om,r)*abs(ifft(I))**2)/E**2
            cap=2/np.pi*np.arctan(np.pi*Q/(2*r))
            peakcap=2/np.pi*np.arctan(np.pi*max(I)/(2*r*E))
            rows.append(dict(profile=name,x=x,rho=float(rho),Q=float(Q),
                cap=float(cap),peak_cap=float(peakcap),ratio_to_cap=float(rho/cap)))
    return rows

def main():
    started=time.time(); RAW.mkdir(parents=True,exist_ok=True)
    xs=[.002,.004,.008,.016,.03,.1,.3,1.,3.,10.,20.,40.,80.,160.]
    rs=[12.2/32,16.67/20.23,.2,.6,1.4]
    config=dict(**IDENTITY,freeze_commit=FREEZE,units="tau1=1",x=xs,r=rs,seed=20261017,
        held_out_r=[.2,.6,1.4],raw_location=str(RAW),precision_digits=60)
    (HERE/"config.yaml").write_text(json.dumps(config,indent=2)+"\n")
    rows=[]
    for r in rs:
        for x in xs:
            exact=float(exact_mp(x,r)); numeric,error=quad_rho(x,r)
            rows.append(dict(r=r,x=x,exact=exact,quadrature=numeric,quadrature_error=error,
                relative_difference=abs(exact-numeric)/exact,held_out=r in [.2,.6,1.4]))
    levels=[]
    for r in rs:
        for u in [.001,.01,.1,1.,10.,100.]:
            Q=u*r; D=np.pi*Q; q=1+r*r
            lo=(np.sqrt(D*D+4*q)-D)/2; hi=lo+D
            quad=2/(np.pi*q)*si.quad(lambda om:weight(om,r),lo,hi,epsabs=1e-12,epsrel=1e-12)[0]
            exact=2/np.pi*np.arctan(np.pi*u/2)
            levels.append(dict(r=r,tau2_Q=u,quadrature=quad,exact=exact,
                relative_difference=abs(quad/exact-1)))
    shape_rows=profiles()
    fits=[fit_summary(r,xs) for r in rs]
    summary=dict(**IDENTITY,run_id=RUN,freeze_commit=FREEZE,
        max_quadrature_relative_difference=max(v["relative_difference"] for v in rows),
        max_levelset_relative_difference=max(v["relative_difference"] for v in levels),
        max_profile_ratio_to_conditional_bound=max(v["ratio_to_cap"] for v in shape_rows),
        fits=fits,quadrature=rows,levelsets=levels,profiles=shape_rows)
    (HERE/"summary.json").write_text(json.dumps(summary,indent=2,allow_nan=False)+"\n")
    curve_x=np.geomspace(.001,200,401)
    np.savez(RAW/"analytic_curves.npz",x=curve_x,r=np.array(rs),
        rho=np.array([[float(exact_mp(x,r)) for x in curve_x] for r in rs]))
    meta=dict(**IDENTITY,run_id=RUN,solver_commit=None,solver_dirty=False,
        solver_note="Independent quadrature, special functions and algebra; no propagation solver.",
        seeds=[20261017],hardware=platform.node(),wall_time_s=time.time()-started,
        raw_location=str(RAW),freeze_commit=FREEZE)
    (HERE/"meta.yaml").write_text(json.dumps(meta,indent=2)+"\n")
    print(json.dumps({k:v for k,v in summary.items() if k not in ["quadrature","profiles","levelsets"]},indent=2))

if __name__=="__main__":main()
