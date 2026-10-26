#!/usr/bin/env python3
"""Independent serial Float64 RK4IP: gpt-d; model gpt-6-astra; family gpt.

FFT convention is positive-transform ifft, with a_w=tilde(A)/window.
No proposer script or solver implementation was read to write this code.
"""
from pathlib import Path
import argparse, csv, json, math, platform, subprocess, time
import numpy as np
from scipy.fft import fft, ifft, fftfreq

HERE=Path(__file__).resolve().parent
RAW=Path.home()/"analytical-nl-discovery-data"/HERE.name
IDENTITY=dict(agent="gpt-d",model="gpt-6-astra",family="gpt")
FREEZE="6df0927ef31369add037f36db21643b14d68bf51"
SOLVER="b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa"
C_UM_PS=299.792458

def memory_check():
    out=subprocess.check_output(["memory_pressure"],text=True)
    line=next(x for x in out.splitlines() if "free percentage" in x)
    print(line,flush=True)
    if int(line.split(":")[-1].strip().rstrip("%"))<35:
        raise RuntimeError("Free memory below 35%; wait and relaunch this case.")

def configs():
    silica=dict(material="SMF-28 local surrogate",lambda_um=1.55,n2_m2_W=2.6e-20,
        Aeff_um2=64.5,beta2_ps2_m=-.0217,beta3_ps3_m=.00012,fr=.18,
        oscillators=[dict(tau1_ps=.0122,tau2_ps=.032,fraction=1.)])
    cases=[]
    pairs=[("core",3,100,False),("h1_30",1,30,True),("h2_60",2,60,True),
        ("h4_150",4,150,True),("h5_225",5,225,True),("h6_300",6,300,True),
        ("h6_100",6,100,True),("h1_300",1,300,True)]
    for name,N,fwhm,held in pairs:
        T=fwhm/1000/(2*np.arccosh(np.sqrt(2)))
        LD=T*T/abs(silica["beta2_ps2_m"])
        L=LD*(2 if N==1 else 3/N)
        hmax=min(L/4000,LD/(60*N*N))
        steps=math.ceil(L/hmax)
        cases.append(dict(name=name,**silica,N=N,fwhm_fs=fwhm,T_ps=T,L_m=L,
            n=16384,dt_ps=.00075,steps=steps,held_out=held,alpha_m=0.))
    fl=dict(silica,material="ZBLAN published oscillator; surrogate dispersion",lambda_um=2.,
        n2_m2_W=4.7e-20,Aeff_um2=float(np.pi*(6.65/2)**2),
        beta2_ps2_m=-.04,beta3_ps3_m=.0001,fr=.3,
        oscillators=[dict(tau1_ps=.01667,tau2_ps=.02023,fraction=1.)])
    T=.180/(2*np.arccosh(np.sqrt(2))); LD=T*T/.04
    cases.append(dict(name="fluoride",**fl,N=3,fwhm_fs=180,T_ps=T,L_m=LD,n=16384,
        dt_ps=.00075,steps=4000,held_out=True,alpha_m=0.))
    core=cases[0]
    cases.extend([dict(core,name="core_half",steps=2*core["steps"],convergence_of="core"),
        dict(core,name="core_quarter",steps=4*core["steps"],convergence_of="core")])
    high=next(c for c in cases if c["name"]=="h6_100")
    cases.extend([dict(high,name="h6_100_half",steps=2*high["steps"],convergence_of="h6_100"),
        dict(high,name="h6_100_fine",n=32768,dt_ps=.000375,convergence_of="h6_100"),
        dict(high,name="h6_100_wide",n=32768,convergence_of="h6_100")])
    cases.extend([dict(core,name="loss",alpha_m=.2*np.log(10)/10,relaxation="uniform loss"),
        dict(core,name="mixture",oscillators=[dict(tau1_ps=.0122,tau2_ps=.032,fraction=.8),
            dict(tau1_ps=.02,tau2_ps=.05,fraction=.2)],relaxation="two passive oscillators")])
    return cases

class Model:
    def __init__(self,cfg):
        self.cfg=cfg; n=cfg["n"]; self.n=n; dt=cfg["dt_ps"]; self.dt=dt
        self.window=n*dt; self.t=(np.arange(n)-n//2)*dt
        self.O=2*np.pi*fftfreq(n,dt)
        self.omega0=2*np.pi*C_UM_PS/cfg["lambda_um"]
        self.omega=self.omega0+self.O
        self.project=self.omega>.02*self.omega0
        self.photon_weight=np.divide(1.,self.omega,out=np.zeros(n),where=self.project)
        self.gamma=2*np.pi*cfg["n2_m2_W"]/(cfg["lambda_um"]*1e-6*cfg["Aeff_um2"]*1e-12)
        self.H=np.zeros(n,complex); self.k=0.
        for osc in cfg["oscillators"]:
            a=1/osc["tau2_ps"]; b=1/osc["tau1_ps"]; q=a*a+b*b; f=osc["fraction"]
            self.H+=f*q/((a-1j*self.O)**2+b*b); self.k+=f*q
        self.W=self.O*self.H.imag
        self.C=self.gamma*cfg["fr"]/self.omega0
        self.kappa=self.C*self.k/2
        self.D=1j*(cfg["beta2_ps2_m"]*self.O**2/2+cfg["beta3_ps3_m"]*self.O**3/6)-cfg["alpha_m"]/2
        self.pref=1j*self.gamma*(self.omega/self.omega0)*self.project
        self.h=cfg["L_m"]/cfg["steps"]; self.half=np.exp(self.D*self.h/2)
        T=cfg["T_ps"]; P=cfg["N"]**2*abs(cfg["beta2_ps2_m"])/(self.gamma*T*T)
        x=self.t/T
        initial=np.sqrt(P)*2*np.exp(-abs(x))/(1+np.exp(-2*abs(x)))
        self.aw0=ifft(initial)*self.project
        self.E0=self.window*np.sum(abs(self.aw0)**2)
        self.ph0=self.window*np.sum(abs(self.aw0)**2*self.photon_weight)
        self.maxima=dict(max_rho=-np.inf,max_spectral_rho=-np.inf,
            max_identity_residual_over_bound=0.,max_photon_drift=0.,
            max_time_edge_fraction=0.,max_spectral_edge_fraction=0.,
            max_low_optical_fraction=0.,max_conditional_ratio=0.,
            max_Q=0.,max_peak_W=0.)
        self.zmax=0.; self.max_field=None
        self.rows=[]; self.integrated_rate=0.; self.integrated_total=0.
        self.integrated_conditional=0.; self.min_retention_margin=np.inf
        self.min_lossaware_margin=np.inf;self.min_energy_step=np.inf;self.max_energy_step=-np.inf
        self.previous_E=self.E0; self.max_accepted_photon_drift=0.

    def nonlinear(self,aw,z,plane=False):
        A=fft(aw); I=abs(A)**2; iw=ifft(I)
        R=fft(self.H*iw).real
        V=(1-self.cfg["fr"])*I+self.cfg["fr"]*R
        nl=self.pref*ifft(A*V)
        E=self.window*np.sum(abs(aw)**2); bound=self.kappa*E*E
        rate_rhs=-2*self.window*np.real(np.vdot(aw,nl))
        rate_spec=self.C*self.window*np.sum(self.W*abs(iw)**2)
        rho=rate_rhs/bound; rhos=rate_spec/bound
        Q=self.dt*np.sum(I*I)/(E*E)
        ph=self.window*np.sum(abs(aw)**2*self.photon_weight)
        timeedge=self.dt*np.sum(I[abs(self.t)>.45*self.window])/E
        specedge=self.window*np.sum(abs(aw[abs(self.O)>.9*np.pi/self.dt])**2)/E
        lowopt=self.window*np.sum(abs(aw[self.omega<.1*self.omega0])**2)/E
        if len(self.cfg["oscillators"])==1:
            tau2=self.cfg["oscillators"][0]["tau2_ps"]
            F=2/np.pi*np.arctan(np.pi*tau2*Q/2)
        else:F=1.
        vals=dict(max_rho=rho,max_spectral_rho=rhos,
            max_identity_residual_over_bound=abs(rate_rhs-rate_spec)/bound,
            max_photon_drift=abs(ph/self.ph0*np.exp(self.cfg["alpha_m"]*z)-1),
            max_time_edge_fraction=timeedge,max_spectral_edge_fraction=specedge,
            max_low_optical_fraction=lowopt,max_conditional_ratio=rho/F,
            max_Q=Q,max_peak_W=np.max(I))
        for k,v in vals.items():self.maxima[k]=max(self.maxima[k],float(v))
        if plane:
            self.max_accepted_photon_drift=max(self.max_accepted_photon_drift,
                abs(ph/self.ph0*np.exp(self.cfg["alpha_m"]*z)-1))
            if not self.rows or rho>max(v[3] for v in self.rows[-1:]):
                # Separate running accepted-plane maximum; no O(nplanes^2) search.
                if not hasattr(self,"plane_max") or rho>self.plane_max:
                    self.plane_max=float(rho);self.zmax=z;self.max_field=aw.copy()
            lossless=1/(1+self.kappa*self.E0*z)
            alpha=self.cfg["alpha_m"]
            lossaware=lossless if alpha==0 else np.exp(-alpha*z)/(1+self.kappa*self.E0*(-np.expm1(-alpha*z))/alpha)
            self.min_retention_margin=min(self.min_retention_margin,E/self.E0-lossless)
            self.min_lossaware_margin=min(self.min_lossaware_margin,E/self.E0-lossaware)
            stepE=E-self.previous_E
            if self.rows:self.min_energy_step=min(self.min_energy_step,stepE);self.max_energy_step=max(self.max_energy_step,stepE)
            self.previous_E=E
            self.rows.append([z,E,ph,rho,rhos,rate_spec,Q,F,max(I),timeedge,specedge,lowopt,
                E/self.E0-lossless,E/self.E0-lossaware])
        return nl,rate_spec,rate_spec+self.cfg["alpha_m"]*E,F

    def run(self):
        aw=self.aw0.copy();h=self.h;eh=self.half
        nl0,r0,t0,f0=self.nonlinear(aw,0.,True)
        for j in range(self.cfg["steps"]):
            z=j*h
            v=eh*aw;k1=eh*nl0
            a2=v+h*k1/2;k2,r2,t2,f2=self.nonlinear(a2,z+h/2)
            a3=v+h*k2/2;k3,r3,t3,f3=self.nonlinear(a3,z+h/2)
            a4=eh*(v+h*k3);nl4,r4,t4,f4=self.nonlinear(a4,z+h)
            aw=eh*(v+h/6*(k1+2*k2+2*k3))+h/6*nl4
            self.integrated_rate+=h/6*(r0+2*r2+2*r3+r4)
            self.integrated_total+=h/6*(t0+2*t2+2*t3+t4)
            self.integrated_conditional+=h/6*(f0+2*f2+2*f3+f4)
            nl0,r0,t0,f0=self.nonlinear(aw,(j+1)*h,True)
            if (j+1)%1000==0:
                print(f"{self.cfg['name']}: {j+1}/{self.cfg['steps']} rho_max={self.maxima['max_rho']:.7g}",flush=True)
        E=self.rows[-1][1]; L=self.cfg["L_m"]
        meta=dict(**IDENTITY,run_id=HERE.name,case=self.cfg["name"],solver_commit=SOLVER,
            solver_dirty=False,implementation="Independent Float64 Python RK4IP",freeze_commit=FREEZE,
            h_m=h,gamma_Winv_minv=self.gamma,kappa_pJinv_minv=self.kappa,E0_pJ=self.E0,
            Eout_over_E0=E/self.E0,retention_lower_bound=1/(1+self.kappa*self.E0*L),
            min_retention_margin=self.min_retention_margin,min_lossaware_margin=self.min_lossaware_margin,
            integrated_identity_relative_mismatch=abs((self.E0-E)-self.integrated_total)/max(self.E0-E,1e-30),
            max_accepted_rho=self.plane_max,z_at_max_m=self.zmax,
            max_accepted_photon_drift=self.max_accepted_photon_drift,
            photon_diagnostic_note="max_photon_drift includes intermediate RK stages; max_accepted_photon_drift is invariant drift on the numerical trajectory",
            max_energy_increase_pJ=self.max_energy_step,**self.maxima,
            Qmax_conditional_retention_bound=None,path_conditional_retention_bound=None,
            positive_frequency_projection="omega > 0.02*omega0; orthogonal spectral projection of nonlinear RHS",
            sampled_weight_sum_over_continuum=float(self.W.sum()/self.window/(self.k/2)))
        if len(self.cfg["oscillators"])==1:
            tau2=self.cfg["oscillators"][0]["tau2_ps"]
            Fmax=2/np.pi*np.arctan(np.pi*tau2*self.maxima["max_Q"]/2)
            meta["Qmax_conditional_retention_bound"]=1/(1+self.kappa*self.E0*L*Fmax)
            meta["path_conditional_retention_bound"]=1/(1+self.kappa*self.E0*self.integrated_conditional)
        meta["frozen_numerical_checks_pass"]=bool(meta["max_rho"]<=1+1e-6 and
            meta["min_lossaware_margin"]>=-1e-6 and meta["max_identity_residual_over_bound"]<1e-5 and
            meta["integrated_identity_relative_mismatch"]<1e-3 and meta["max_accepted_photon_drift"]<1e-5 and
            meta["max_time_edge_fraction"]<1e-6 and meta["max_spectral_edge_fraction"]<1e-6)
        return meta,aw

def main():
    parser=argparse.ArgumentParser();parser.add_argument("cases",nargs="*");args=parser.parse_args()
    allcases=configs(); RAW.mkdir(parents=True,exist_ok=True)
    config=dict(**IDENTITY,run_id=HERE.name,freeze_commit=FREEZE,seeds=[],cases=allcases,
        raw_location=str(RAW),units=dict(time="ps",energy="pJ",length="m",power="W"))
    (HERE/"config.yaml").write_text(json.dumps(config,indent=2)+"\n")
    chosen=[c for c in allcases if not args.cases or c["name"] in args.cases]
    for c in chosen:
        path=RAW/(c["name"]+"_summary.json")
        if path.exists():
            print("Preserving completed case",c["name"],flush=True);continue
        memory_check();started=time.time();m=Model(c);summary,aw=m.run()
        summary.update(wall_time_s=time.time()-started,raw_location=str(RAW),hardware=platform.node())
        with (RAW/(c["name"]+"_planes.csv")).open("w") as f:
            writer=csv.writer(f);writer.writerow(["z_m","E_pJ","photon_norm","rho_rhs","rho_spec","rate_spec_pJ_m",
                "Q_psinv","F_Q","peak_W","time_edge","spectral_edge","low_optical","retention_margin","lossaware_margin"])
            writer.writerows(m.rows)
        np.savez(RAW/(c["name"]+"_fields.npz"),aw_initial=m.aw0,aw_final=aw,aw_max=m.max_field,
            t=m.t,Omega=m.O)
        path.write_text(json.dumps(summary,indent=2,allow_nan=False)+"\n")
        print(json.dumps(summary,indent=2),flush=True)
        summaries={p.stem.replace("_summary",""):json.loads(p.read_text()) for p in sorted(RAW.glob("*_summary.json"))}
        (HERE/"summary.json").write_text(json.dumps(dict(**IDENTITY,run_id=HERE.name,freeze_commit=FREEZE,cases=summaries),indent=2)+"\n")
        meta=dict(**IDENTITY,run_id=HERE.name,solver_commit=SOLVER,solver_dirty=False,
            solver_note="Python independent implementation; Julia cross-check uses this agents-copy commit.",
            seeds=[],hardware=platform.node(),raw_location=str(RAW),freeze_commit=FREEZE,
            wall_time_s=sum(s["wall_time_s"] for s in summaries.values()))
        (HERE/"meta.yaml").write_text(json.dumps(meta,indent=2)+"\n")

if __name__=="__main__":main()
