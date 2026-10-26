#!/usr/bin/env python3
"""Classical sech-core diagnostics, kept separate from all noise predictions.
agent: gpt-b; model: gpt-6-astra; family: gpt.
No output covariance is reset or inferred from this fit.
"""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares
try:import tomllib
except ImportError:import tomli as tomllib


def fit_case(config,amplitude,batch='batch'):
    cfg=tomllib.loads(Path(config).read_text());path=Path(cfg['raw_location'])/(batch+'.npz')
    if not path.exists():return None
    data=np.load(path);u=data['mean'];n=len(u);window=cfg['window_over_T0']
    x=(np.arange(n)-n//2)*window/n;k=2*np.pi*np.fft.fftfreq(n,window/n)
    derivative=np.fft.fft(-1j*k*np.fft.ifft(u))
    peak=int(np.argmax(abs(u)));center=x[peak]
    use=abs(x-center)<6/amplitude
    carrier=-np.vdot(u[use],derivative[use]).imag/np.vdot(u[use],u[use]).real
    phase=np.angle(u[peak]);xx=x[use];observed=u[use]
    def model(p,xgrid):
        a=np.exp(p[0]);y=xgrid-p[1]
        return a/np.cosh(np.clip(a*y,-350,350))*np.exp(1j*(p[2]-p[3]*y))
    def residual(p):
        r=model(p,xx)-observed
        return np.r_[r.real,r.imag]
    fit=least_squares(residual,[np.log(amplitude),center,phase,carrier],
        bounds=([np.log(.4*amplitude),center-2/amplitude,-np.inf,-50],
                [np.log(1.8*amplitude),center+2/amplitude,np.inf,50]),
        xtol=1e-12,ftol=1e-12,gtol=1e-12,max_nfev=200)
    fitted=model(fit.x,x);energy=np.vdot(u,u).real
    return dict(config=str(config),raw_covariance=str(path),N=cfg.get('N',1.),
        z_over_LD=cfg['z_over_LD'],raman_fraction=cfg['raman_fraction'],
        reference_scattering_amplitude=amplitude,fitted_soliton_amplitude=float(np.exp(fit.x[0])),
        fitted_center_over_T0=float(fit.x[1]),fitted_carrier_times_T0=float(fit.x[3]),
        core_carrier_moment_times_T0=float(carrier),
        core_relative_field_error=float(np.linalg.norm((u-fitted)[use])/np.linalg.norm(u[use])),
        full_relative_field_error=float(np.linalg.norm(u-fitted)/np.linalg.norm(u)),
        core_energy_fraction=float(np.vdot(u[use],u[use]).real/energy),
        core_halfwidth_over_T0=6/amplitude,fit_success=bool(fit.success))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    root=Path(__file__).resolve().parents[1];base=root/'runs/2026-10-10-gpt-b-soliton-solver'
    rows=[]
    cases=[('gaussian_N1.25',1.3753906129146694,'batch'),('gaussian_N1.5',1.89815050,'batch'),
           ('gaussian_N1.25_Raman',1.3753906129146694,'batch'),('gaussian_N1.5_late',1.89815050,'batch'),
           ('gaussian_N2_Raman_fission',2.926210847337887,'batch_cells03'),
           ('anchor_50ps',2*1.9689720577167-1,'batch_cells03')]
    for name,a,batch in cases:
        row=fit_case(base/(name+'.toml'),a,batch)
        if row is not None:rows.append(row);print(json.dumps(row),flush=True)
    out=dict(agent='gpt-b',model='gpt-6-astra',family='gpt',points=rows,
        scope='Classical mean diagnostic only. Fitted widths/phases do not replace the inherited covariance.')
    Path(args.output).write_text(json.dumps(out,indent=2))


if __name__=='__main__':main()
