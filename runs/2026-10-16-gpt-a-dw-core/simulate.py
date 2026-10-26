#!/usr/bin/env python3
"""Independent scalar GNLSE audit. agent=gpt-a model=gpt-6-astra family=gpt.

Positive Fourier transform: q=ifft(u), u=fft(q); physical frequency is +w.
Only the current field is held in memory. Configured outputs go to raw storage.
No proposer code is imported. The audit records a later diagnostic inspection
of the proposer's gate formula, after independent results were obtained.
"""
import argparse
import hashlib
import json
import os
import platform
import resource
import subprocess
import time
from pathlib import Path

import numpy as np
from scipy.fft import fft, ifft, fftfreq
from scipy.signal import find_peaks
import yaml

IDENTITY = dict(agent="gpt-a", model="gpt-6-astra", family="gpt")
SOLVER_COMMIT = "b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa"
SOURCE_SHA256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
S_PAPER = 835.0 / (2*np.pi*299.792458*50.0)


def clean_json(x):
    if isinstance(x, dict):
        return {k: clean_json(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [clean_json(v) for v in x]
    if isinstance(x, np.ndarray):
        return clean_json(x.tolist())
    if isinstance(x, (np.integer, np.bool_)):
        return x.item()
    if isinstance(x, (float, np.floating)):
        return float(x) if np.isfinite(x) else None
    return x


def write_json(path, value):
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(clean_json(value), indent=2)+"\n")
    temporary.replace(path)


def memory_check():
    while True:
        out = subprocess.check_output(["memory_pressure"], text=True)
        row = next(s for s in out.splitlines() if "free percentage" in s)
        free = int(row.split(":")[-1].strip().strip("%"))
        print(row, flush=True)
        if free >= 35:
            return free
        # Do not start a new propagation while the PI's threshold is unmet.
        time.sleep(30)


def response(w, model, dt, sampled=False):
    if model == "none":
        return None, 0.0, 1.0
    fr, t1, t2 = (0.18,12.2/50,32/50) if model == "M1" else (0.245,12/50,32/50)
    a,b = 1/t2,1/t1
    h = (a*a+b*b)/((a-1j*w)**2+b*b)
    if model == "roy":
        ab=50/96
        hb=2*ab/(ab-1j*w)-ab*ab/(ab-1j*w)**2
        h=.79*h+.21*hb
    dc=1.0
    if sampled:
        t=np.arange(len(w))*dt
        ht=(a*a+b*b)/b*np.exp(-a*t)*np.sin(b*t)
        if model == "roy":
            ht=.79*ht+.21*(2*ab-ab*ab*t)*np.exp(-ab*t)
        ht[0]*=.5
        h=ifft(ht)*len(w)*dt
        dc=float(h[0].real)
        if sampled == "normalized":
            h/=dc
    return h,fr,dc


def exact_breather(t,z):
    return (2*np.exp(.5j*z)*(np.cosh(3*t)+3*np.exp(4j*z)*np.cosh(t)) /
            (np.cosh(4*t)+4*np.cosh(2*t)+3*np.cos(4*z)))


def strip_fits(q,w):
    amp=np.abs(q)
    rel=amp/max(amp)
    output={}
    for side in [1,-1]:
        k=side*w
        for high,low in [(-3,-8),(-4,-9),(-5,-10),(-6,-11),(-7,-12)]:
            mask=(k>0)&(k<.75*max(w))&(rel<10.**high)&(rel>10.**low)
            xx=k[mask]
            yy=np.log(rel[mask])
            key=f"{'blue' if side==1 else 'red'}_{high}_{low}"
            if len(xx)<12 or np.ptp(xx)<5:
                output[key]=None
                continue
            matrix=np.column_stack([np.ones(len(xx)),-xx])
            c,d=np.linalg.lstsq(matrix,yy,rcond=None)[0]
            residual=yy-(c-d*xx)
            matrix3=np.column_stack([np.ones(len(xx)),-xx,np.log(xx)])
            c3,d3,p3=np.linalg.lstsq(matrix3,yy,rcond=None)[0]
            output[key]=dict(d=d,rms=np.sqrt(np.mean(residual**2)),
                w_low=min(xx),w_high=max(xx),points=len(xx),d_log=d3,
                log_power=p3,rms_log=np.sqrt(np.mean((yy-(c3-d3*xx+p3*np.log(xx)))**2)))
    return output


def metrics(q,q0,t,w,cfg):
    n=len(q); window=cfg["window"]; dt=window/n
    power=np.abs(q)**2; initial=np.abs(q0)**2
    E0=window*sum(initial); E=window*sum(power)
    u=fft(q)
    delta=cfg.get("delta3",0); order=cfg["N"]
    shock=cfg.get("shock",0)
    s=shock*S_PAPER
    D=-w*w/2+delta*w**3
    # Hamiltonian for the Kerr, no-shock model: -D is the linear contribution.
    H=window*sum(-D*power)-order**2/2*dt*sum(abs(u)**4)
    out=dict(energy=E,energy_relative_drift=E/E0-1,
        momentum=window*sum(w*power),hamiltonian=H,
        max_intensity=max(abs(u)**2),peak_time=t[np.argmax(abs(u)**2)],
        time_edge_fraction=dt*sum(abs(u[np.abs(t-cfg.get('center',0))>.45*window])**2)/E0,
        spectral_edge_fraction=window*sum(power[np.abs(w)>.8*max(w)])/E0)
    for label,weight_s in [("formal",s),("physical",S_PAPER)]:
        denom=1+weight_s*w
        valid=denom>0
        out[label+"_positive_frequency_norm"] = window*sum(power[valid]/denom[valid])
        out[label+"_norm_initial"] = window*sum(initial[valid]/denom[valid])
        out[label+"_norm_relative_drift"]=(out[label+"_positive_frequency_norm"]/
                                              out[label+"_norm_initial"]-1)
        out[label+"_negative_frequency_energy"]=window*sum(power[~valid])/E0
    if delta<=0:
        return out
    wz=1/(6*delta)
    wr=(1+4*delta**2*(2*order-1)**2)/(2*delta)
    broad=w>=wz
    resonant=(w>=.75*wr)&(w<=1.5*wr)
    out.update(w_z=wz,w_roy=wr,launch_band_leakage=sum(initial[broad])/sum(initial),
        eta_band=sum(power[broad])/sum(initial),eta_resonant=sum(power[resonant])/sum(initial))
    for radius in [15,20,25]:
        # Analytic two-edge gate. Unlike tanh(abs(t)-radius), it has no cusp.
        # expit form avoids subtracting two values close to one at the core.
        from scipy.special import expit
        gate=expit(2*(t-radius))+expit(-2*(t+radius))
        gq=ifft(u*gate); gp=abs(gq)**2
        out[f"eta_gate{radius}"]=sum(gp[broad])/sum(initial)
        out[f"eta_resonant_gate{radius}"]=sum(gp[resonant])/sum(initial)
        out[f"gate{radius}_total_energy"]=sum(gp)/sum(initial)
        out[f"gate{radius}_peak_ratio"]=max(gp[resonant])/max(initial) if any(resonant) else None
    indices=np.where((w>=max(wz,.65*wr))&(w<=1.8*wr))[0]
    indices=indices[np.argsort(w[indices])]
    peaks,_=find_peaks(power[indices])
    if len(peaks):
        j=indices[peaks[np.argmax(power[indices[peaks]])]]
        out.update(peak_ratio=power[j]/max(initial),peak_db=10*np.log10(power[j]/max(initial)),
                   peak_w=w[j],peak_cycles=w[j]/(2*np.pi),peak_is_local_maximum=True)
    else:
        j=indices[np.argmax(power[indices])]
        out.update(peak_ratio=None,peak_db=None,peak_w=None,peak_cycles=None,
                   peak_is_local_maximum=False,search_max_ratio=power[j]/max(initial))
    denom=1+s*w; valid=broad&(denom>0)
    out["eta_band_formal_weight"]=sum(power[valid]/denom[valid])/sum(initial[denom>0]/denom[denom>0])
    denom=1+S_PAPER*w; valid=broad&(denom>0)
    out["eta_band_photon"]=sum(power[valid]/denom[valid])/sum(initial[denom>0]/denom[denom>0])
    return out


def propagate(cfg,raw):
    began=time.monotonic()
    memory_free=memory_check()
    n=cfg["n"]; window=cfg["window"]; dt=window/n
    t=(np.arange(n)-n//2)*dt+cfg.get("center",0); w=2*np.pi*fftfreq(n,dt)
    u0=1/np.cosh(t) if cfg.get("shape","sech")=="sech" else np.exp(-t*t/2)
    q0=ifft(u0.astype(complex)); q=q0.copy()
    N=cfg["N"]; delta=cfg.get("delta3",0); s=cfg.get("shock",0)*S_PAPER
    zmax=cfg["zmax"]; steps=int(np.ceil(zmax/cfg["h"])); h=zmax/steps
    linear=1j*(-w*w/2+delta*w**3)
    half=np.exp(linear*h/2)
    rh,fr,dc=response(w,cfg.get("raman","none"),dt,cfg.get("sampled_kernel",False))
    pref=1j*N*N*(1+s*w)

    def nonlinear(v):
        u=fft(v); intensity=abs(u)**2
        potential=intensity if rh is None else (1-fr)*intensity+fr*fft(rh*ifft(intensity)).real
        return pref*ifft(u*potential)

    def split(v,step):
        ee=np.exp(linear*step/2)
        u=fft(ee*v); intensity=abs(u)**2
        potential=intensity if rh is None else (1-fr)*intensity+fr*fft(rh*ifft(intensity)).real
        return ee*ifft(u*np.exp(1j*N*N*step*potential))

    method=cfg.get("method","rk4ip")
    if method=="yoshida" and s:
        raise ValueError("Exact nonlinear split step does not apply with shock")
    outputs={}; strip=[]
    output_steps={int(round(z/h)):z for z in cfg.get("outputs",[zmax])}
    scan_stride=max(1,int(round(cfg.get("scan_stride",.005)/h)))
    initial_metrics=metrics(q,q0,t,w,cfg)
    for j in range(1,steps+1):
        if method=="rk4ip":
            v=half*q
            k1=half*nonlinear(q)
            k2=nonlinear(v+h*k1/2)
            k3=nonlinear(v+h*k2/2)
            k4=nonlinear(half*(v+h*k3))
            q=half*(v+h*(k1+2*k2+2*k3)/6)+h*k4/6
        else:
            c=1/(2-2**(1/3))
            q=split(split(split(q,c*h),(1-2*c)*h),c*h)
        if j%scan_stride==0 and cfg.get("strip",False):
            fits=strip_fits(q,w)
            strip.append(dict(z=j*h,fits=fits,max_intensity=float(max(abs(fft(q))**2))))
        if j in output_steps:
            z=output_steps[j]
            m=metrics(q,q0,t,w,cfg)
            m["hamiltonian_relative_drift"]=(m["hamiltonian"]-initial_metrics["hamiltonian"])/abs(initial_metrics["hamiltonian"])
            m["momentum_drift_per_initial_energy"]=(m["momentum"]-initial_metrics["momentum"])/initial_metrics["energy"]
            if delta==0 and N==2 and cfg.get("shape","sech")=="sech" and rh is None and s==0:
                exact=exact_breather(t,z)
                m["breather_relative_l2_error"]=np.linalg.norm(fft(q)-exact)/np.linalg.norm(exact)
            outputs[str(z)]=m
            np.savez(raw/(cfg["name"]+f"_z{z:g}.npz"),q=q,q0=q0,w=w,t=t,z=z)
        if j%max(1,steps//4)==0:
            print(cfg["name"],f"{j}/{steps}",f"elapsed={time.monotonic()-began:.1f}s",flush=True)
            if not np.all(np.isfinite(q)):
                raise RuntimeError("Nonfinite propagation")
    strip_min={}
    if strip:
        for key in strip[0]["fits"]:
            valid=[r for r in strip if r["fits"][key] is not None and
                   r["fits"][key]["d"]>0 and r["fits"][key]["rms"]<.10]
            if valid:
                best=min(valid,key=lambda r:r["fits"][key]["d"])
                strip_min[key]=dict(z=best["z"],**best["fits"][key])
        write_json(raw/(cfg["name"]+"_strip.json"),strip)
    return dict(config=cfg,dt_fs=dt*50,actual_h=h,steps=steps,
        memory_free_percent=memory_free,raman_kernel_dc=dc,initial=initial_metrics,
        outputs=outputs,strip_min=strip_min,wall_seconds=time.monotonic()-began,
        process_peak_rss_mb=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1024**2 if platform.system()=='Darwin' else 1024),
        implementation_sha256=SOURCE_SHA256)


def main():
    parser=argparse.ArgumentParser();parser.add_argument("config")
    parser.add_argument("--only",nargs="*")
    args=parser.parse_args()
    path=Path(args.config).resolve();config=yaml.safe_load(path.read_text())
    folder=path.parent;raw=Path(config["raw_location"]);raw.mkdir(parents=True,exist_ok=True)
    summary_path=folder/"summary.json"
    summary=json.loads(summary_path.read_text()) if summary_path.exists() else dict(
        **IDENTITY,run_id=folder.name,cases={})
    for cfg in config["cases"]:
        if args.only and cfg["name"] not in args.only:
            continue
        if cfg["name"] in summary["cases"]:
            print("already complete",cfg["name"],flush=True);continue
        print("BEGIN",cfg,flush=True)
        summary["cases"][cfg["name"]]=propagate(cfg,raw)
        write_json(summary_path,summary)
    meta=dict(**IDENTITY,run_id=folder.name,date="2026-10-16",task="T-20261016-claude-b-01",
        claim="C-20261016-claude-b-01",solver_commit=SOLVER_COMMIT,solver_dirty=False,
        implementation="independent scipy FFT RK4IP/Yoshida; pinned Julia solver is cross-checked separately",
        hardware=platform.platform(),raw_location=str(raw),
        wall_seconds=sum(c["wall_seconds"] for c in summary["cases"].values()))
    (folder/"meta.yaml").write_text(yaml.safe_dump(meta,sort_keys=False))


if __name__=="__main__":
    main()
