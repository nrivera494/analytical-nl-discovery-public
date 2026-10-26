"""Independent auditor implementation. agent=gpt-d, model=gpt-6-astra, family=gpt.
Units ps,m,um,W,pJ. Forward Fourier transform uses exp(+i Omega t).
No proposer routines are imported. Analytical Raman transform avoids sampling bias.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
import json,time,subprocess,socket,sys
from pathlib import Path
import numpy as np
from scipy import special, optimize, interpolate, integrate, signal
from scipy.fft import fft,ifft,fftfreq
C=299.792458 # um/ps
HBAR=1.054571817e-10 # pJ ps
ROOT=Path(__file__).resolve().parents[2]
RAW=Path('~/analytical-nl-discovery-data')
IDENTITY={'agent':'gpt-d','model':'gpt-6-astra','family':'gpt'}
SOLVER='b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa'
def omega(lam): return 2*np.pi*C/np.asarray(lam)
def wavelength(w): return 2*np.pi*C/np.asarray(w)
def sech(x): return 2*np.exp(-np.abs(x))/(1+np.exp(-2*np.abs(x)))
def dump(path,obj):
    def conv(v):
        if isinstance(v,np.ndarray): return v.tolist()
        if isinstance(v,np.generic): return v.item()
        raise TypeError(type(v))
    Path(path).write_text(json.dumps(obj,indent=2,default=conv)+'\n')
def memory_ok():
    s=subprocess.check_output(['memory_pressure'],text=True)
    line=[x for x in s.splitlines() if 'free percentage' in x][0]
    print(line,flush=True)
    if int(line.split(':')[1].strip().rstrip('%'))<35: raise SystemExit('Memory below 35%; do not launch')

class Fibre:
    def __init__(self,material='Z75',area='constant',n2=None,dispersion='full',launch_um=None,
                 edge_B=None,edge_ref_um=None,edge_db=1.,loss_scale=1.,beta2=None):
        self.material=material; self.area=area; self.dispersion=dispersion
        if material=='Z75':
            a,na,sm=(3.75,.30,(1.235,.752,.090,14.47)); self.fR=.20; self.t1=.0209; self.t2=.053
            self.n2=2.1e-20 if n2 is None else n2
            self.launch_um=2.8 if launch_um is None else launch_um
            self.edge_B=92. if edge_B is None else edge_B
            self.edge_ref_um=4.2 if edge_ref_um is None else edge_ref_um
            lams=np.linspace(.65,8.,2401)
        else:
            a,na,sm=(4.1,.14,(1.1064,.7250,.091,9.11)); self.fR=.18; self.t1=.0122; self.t2=.032
            self.n2=2.6e-20 if n2 is None else n2
            self.launch_um=1.55 if launch_um is None else launch_um
            self.edge_B=48. if edge_B is None else edge_B
            self.edge_ref_um=2.3 if edge_ref_um is None else edge_ref_um
            lams=np.linspace(.45,4.5,2401)
        self.w0=float(omega(self.launch_um)); self.loss_scale=loss_scale; self.edge_db=edge_db
        V=2*np.pi*a*na/lams
        us=[]
        for v in V:
            def fun(u):
                ww=np.sqrt(max(v*v-u*u,1e-30))
                return u*special.j1(u)/special.j0(u)-ww*special.k1(ww)/special.k0(ww)
            us.append(optimize.brentq(fun,1e-9,min(v*(1-1e-13),2.4048255576-1e-10),xtol=1e-13))
        us=np.array(us); ws=np.sqrt(V*V-us*us)
        ncl2=1+sm[0]*lams*lams/(lams*lams-sm[2]**2)+sm[1]*lams*lams/(lams*lams-sm[3]**2)
        bet=np.sqrt((ncl2+na*na)*(2*np.pi/lams)**2-(us/a)**2)*1e6
        xs,gs=np.polynomial.legendre.leggauss(96)
        r=(xs+1)/2; gr=gs/2
        ae=[]
        for u,w in zip(us,ws):
            fi=special.j0(u*r)
            x=w+(xs+1)*15; gx=gs*15
            fo=special.j0(u)*special.k0(x)/special.k0(w)
            j2=np.sum(gr*r*fi**2)+np.sum(gx*x*fo**2)/w**2
            j4=np.sum(gr*r*fi**4)+np.sum(gx*x*fo**4)/w**2
            ae.append(2*np.pi*a*a*j2*j2/j4)
        om=omega(lams)[::-1]
        self.bs=interpolate.CubicSpline(om,bet[::-1]); self.As=interpolate.PchipInterpolator(om,np.array(ae)[::-1])
        self.A0=float(self.As(self.w0)); self.b2=float(self.bs(self.w0,2)) if beta2 is None else beta2
        self.b3=float(self.bs(self.w0,3)); self.g0=self.n2*1e18*self.w0/(C*self.A0)
        self.TR=self.fR*2*self.t1**2*self.t2/(self.t1**2+self.t2**2)
        self.wedge=2*np.pi*C/self.edge_B
    def b(self,w):
        x=np.asarray(w)-self.w0
        if self.dispersion=='quadratic': return .5*self.b2*x*x
        if self.dispersion=='cubic': return .5*self.b2*x*x+self.b3*x*x*x/6
        return self.bs(w)-self.bs(self.w0)-self.bs(self.w0,1)*x
    def b2at(self,w):
        if self.dispersion=='quadratic': return np.asarray(w)*0+self.b2
        if self.dispersion=='cubic': return self.b2+self.b3*(np.asarray(w)-self.w0)
        return self.bs(w,2)
    def A(self,w): return np.asarray(w)*0+self.A0 if self.area=='constant' else self.As(w)
    def gamma(self,w): return self.n2*1e18*np.asarray(w)/(C*self.A(w))
    def alpha(self,w): return self.loss_scale*self.edge_db*np.log(10)/10*np.exp(np.clip((omega(self.edge_ref_um)-np.asarray(w))/self.wedge,-700,50))
    def H(self,Om):
        aa=1/self.t2; bb=1/self.t1
        return (aa*aa+bb*bb)/(aa*aa+bb*bb-Om*Om-2j*aa*Om)
    def properties(self):
        return {**IDENTITY,'material':self.material,'A0_um2':self.A0,'beta2_ps2_m':self.b2,'beta3_ps3_m':self.b3,'gamma0_Winv_minv':self.g0,'TR_fs':self.TR*1000,'edge_w_rad_ps':self.wedge,'omega0':self.w0}
    def width(self,w,N): return 2*np.abs(self.b2at(w))/(self.gamma(w)*HBAR*w*N)
    def K(self,w): return self.TR*self.gamma(w)**4*(HBAR*w)**4/(30*np.abs(self.b2at(w))**3)
    def launch(self,T,order=1):
        P=order**2*abs(self.b2)/(self.g0*T*T)
        return P,2*P*T/(HBAR*self.w0)

def overlap_rate(f,w,N):
    T=float(f.width(w,N)); E=HBAR*w*N
    # Dimensionless sech-squared transform q(x)=pi*x/(2*sinh(pi*x/2)).
    def integrand(x):
        q=1. if abs(x)<1e-8 else (np.pi*x/2)/np.sinh(np.pi*x/2)
        Om=x/T
        return Om*f.H(Om).imag*q*q
    val=integrate.quad(integrand,0,35,epsabs=1e-9,epsrel=3e-9,limit=120)[0]/(np.pi*T)
    return -f.gamma(w)*f.fR*E*val

def reduced(f,T,L,order=1,full=True,spectral_loss=True,nplanes=241,initial=None):
    P,N0=f.launch(T,order)
    y0=[f.w0,0.] if initial is None else [initial[0],np.log(initial[1]/N0)]
    def rhs(z,y):
        w,n=y; N=N0*np.exp(n); Ts=float(f.width(w,N)); x=1/(f.wedge*Ts)
        al=float(f.alpha(w)); drift=0.
        if spectral_loss and abs(x)<3.0:
            al*=x/np.sin(x)
            drift=al*(f.wedge-1/Ts/np.tan(x))
            # d log M(s)/ds = 1/s - (1/T)cot(s/T); loss centroid shift = +alpha_avg*dlogM.
        dw=overlap_rate(f,w,N) if full else -float(f.K(w))*N**4
        return [dw+drift,-al]
    zs=np.linspace(0,L,nplanes)
    sol=integrate.solve_ivp(rhs,[0,L],y0,rtol=1e-8,atol=1e-10,t_eval=zs,max_step=max(L/100,1e-4))
    return {'z':sol.t,'omega':sol.y[0],'N':N0*np.exp(sol.y[1]),'N0':N0,'Ts':f.width(sol.y[0],N0*np.exp(sol.y[1]))}

def terminal(f,N0):
    def budget(w): return integrate.quad(lambda q:4*f.alpha(q)/(f.K(q)*N0**4),w,f.w0,epsabs=1e-9,epsrel=1e-8,limit=200)[0]
    lo=max(omega(7.5 if f.material=='Z75' else 4.),f.w0*.3)
    wi=optimize.brentq(lambda w:budget(w)-1,lo,f.w0)
    kappa=(np.log(f.K(wi+.05))-np.log(f.K(wi-.05)))/.1
    weff=1/(1/f.wedge+kappa)
    return {'omega_inf':wi,'lambda_inf_um':float(wavelength(wi)),'w_eff':weff,'alpha_inf':float(f.alpha(wi)),'terminal_condition_ratio':float(4*f.alpha(wi)*weff/(f.K(wi)*N0**4))}

def assess_reduced(f,r,cutoffs):
    out={'planes':[],'optima':{}}
    for z in [2,4,6,8,12]:
        if z<=r['z'][-1]: out['planes'].append({'z':z,'N_ratio':float(np.interp(z,r['z'],r['N'])/r['N0']),'lambda_um':float(wavelength(np.interp(z,r['z'],r['omega'])))})
    for lc in cutoffs:
        eta=(r['N']/r['N0'])*.5*(1+np.tanh(np.pi*r['Ts']/2*(omega(lc)-r['omega'])))
        j=np.argmax(eta); out['optima'][str(lc)]={'eta':float(eta[j]),'L_m':float(r['z'][j]),'boundary':bool(j==len(eta)-1)}
    return out

class GNLSE:
    def __init__(self,f,n=8192,dt=.003,carrier_um=None,raman='analytic',alias=False,shock=True,track_fission=False):
        self.f=f; self.n=n; self.dt=dt; self.t=(np.arange(n)-n//2)*dt
        self.Om=2*np.pi*fftfreq(n,dt); self.wref=float(omega(carrier_um)) if carrier_um else f.w0
        self.w=self.wref+self.Om; self.valid=(self.w>omega(7.8 if f.material=='Z75' else 4.4))&(self.w<omega(.66 if f.material=='Z75' else .46))
        ww=np.clip(self.w,omega(7.8 if f.material=='Z75' else 4.4),omega(.66 if f.material=='Z75' else .46))
        self.H=f.H(self.Om)
        self.kernel_info={'method':raman}
        if raman=='sampled':
            tt=np.arange(n)*dt; hh=(f.t1**2+f.t2**2)/(f.t1*f.t2**2)*np.exp(-tt/f.t2)*np.sin(tt/f.t1)
            integ=hh.sum()*dt; self.H=ifft(hh)*n*dt/integ
            self.kernel_info['raw_integral']=integ
        self.s=(f.A0/f.A(ww))**.25
        self.gamma_out=f.g0*(ww/f.w0 if shock else np.ones(n))*self.s*self.valid
        # Spectral projection is explicit; its occupied boundary mass is diagnosed.
        self.D=1j*f.b(ww)-np.minimum(f.alpha(ww),1e6)/2
        self.D[~self.valid]=-1e6
        if alias:
            # Filled in only when independently matching the documented solver window.
            self.gamma_out*=np.exp(-((self.Om)/(max(abs(self.Om))*.8))**36)
        self.alias=alias
        self.track_fission=track_fission
    def nl(self,Q):
        B=fft(self.s*Q); I=np.abs(B)**2
        R=(1-self.f.fR)*I+self.f.fR*fft(self.H*ifft(I)).real
        return 1j*self.gamma_out*ifft(B*R)
    def step(self,Q,h):
        ep=np.exp(self.D*(h/2)); U=ep*Q
        k1=ep*self.nl(Q); k2=self.nl(U+h*k1/2); k3=self.nl(U+h*k2/2); k4=self.nl(ep*(U+h*k3))
        return ep*(U+h*(k1+2*k2+2*k3)/6)+h*k4/6
    def measure(self,Q,N0,cutoffs,isolated=True):
        p=np.abs(Q)**2; iw=np.zeros(self.n); iw[self.valid]=1/(HBAR*self.w[self.valid]); factor=self.dt*self.n
        N=factor*np.sum(p*iw); E=factor*p.sum(); wm=E/(HBAR*N)
        A=fft(Q); I=np.abs(A)**2; j=int(np.argmax(I)); shift=self.n//2-j
        Ar=np.roll(A,shift); Ir=np.abs(Ar)**2
        # Photon waveform gives a windowed, positive norm; no negative-frequency singularity.
        photon_wave=fft(Q*np.sqrt(iw)); pr=np.abs(np.roll(photon_wave,shift))**2
        gate=np.abs(self.t)<1.5
        Qs=ifft(Ar*gate); ps=np.abs(Qs)**2
        Ns=factor*np.sum(ps*iw); Es=factor*np.sum(ps); ws=Es/(HBAR*Ns)
        peak=float(I.max()); Ts_est=Es/(2*peak)
        analytic_T=float(self.f.width(ws,Ns))
        alpha_z0=float(self.f.alpha(ws)*np.pi*analytic_T**2/(2*abs(self.f.b2at(ws))))
        dnQ=self.nl(Q)-np.minimum(self.f.alpha(np.maximum(self.w,1.)),1e6)*Q/2
        dspec=2*np.real(np.conj(Q)*dnQ); dN=factor*np.sum(dspec*iw); dE=factor*dspec.sum(); dw=(dE/HBAR-wm*dN)/N
        alavg=factor*np.sum(p*iw*self.f.alpha(np.maximum(self.w,1.)))/N
        cov=factor*np.sum(p*iw*(self.w-wm)*self.f.alpha(np.maximum(self.w,1.)))/N
        shape_gate=abs(self.t)<min(4*Ts_est,1.5)
        fitted=peak*sech(self.t/Ts_est)**2
        shape_residual=float(np.linalg.norm((Ir-fitted)[shape_gate])/np.linalg.norm(Ir[shape_gate]))
        return {'sech_intensity_residual':shape_residual,'fundamental_width_ratio':Ts_est/analytic_T,'dN_dz':float(dN),'domega_dz':float(dw),'alpha_avg':float(alavg),'filtering_domega_dz':float(-cov),'raman_domega_dz':float(dw+cov),'omega_energy_mean':float(np.sum(p*self.w)/p.sum()),'N':float(N),'N_ratio':float(N/N0),'E_pJ':float(E),'omega':float(wm),'lambda_um':float(wavelength(wm)),
                'Ns':float(Ns),'Ns_ratio':float(Ns/N0),'soliton_omega':float(ws),'soliton_lambda_um':float(wavelength(ws)),
                'Ts_est_fs':Ts_est*1000,'Ts_adiabatic_fs':analytic_T*1000,'alpha_z0':alpha_z0,
                'loss_bandwidth_parameter':float(1/(self.f.wedge*analytic_T)**2),'raman_longness':analytic_T/self.f.t1,
                'peak_W':peak,'peak_t_ps':float(self.t[j]),'time_edge_fraction':float(np.sum(Ir[np.abs(self.t)>.45*self.n*self.dt])/I.sum()),
                'outside_isolation_fraction':float(1-pr[gate].sum()/pr.sum()),
                'spectral_outer_fraction':float(p[np.abs(self.Om)>.8*np.pi/self.dt].sum()/p.sum()),
                'eta':{str(l):float(factor*np.sum((p*iw)[(self.w<omega(l))&self.valid])/N0) for l in cutoffs}}
    def fission_measure(self,Q,N0):
        A=fft(Q);I=abs(A)**2; peak=int(np.argmax(I));I=np.roll(I,self.n//2-peak);A=np.roll(A,self.n//2-peak)
        peaks,_=signal.find_peaks(I,height=.03*I.max(),distance=max(2,int(.06/self.dt)))
        iw=np.zeros(self.n);iw[self.valid]=1/(HBAR*self.w[self.valid]); candidates=[]
        for j in peaks:
            distances=np.minimum(abs(peaks-j),self.n-abs(peaks-j))*self.dt
            nearest=float(np.min(distances[distances>0])) if len(peaks)>1 else self.n*self.dt/2
            delta=(np.arange(self.n)-j+self.n//2)%self.n-self.n//2;tt=delta*self.dt
            gate=abs(tt)<min(.8,nearest/2);ql=ifft(A*gate);pp=abs(ql)**2
            N=self.dt*self.n*np.sum(pp*iw);E=self.dt*self.n*pp.sum()
            if N<.1*N0:continue
            w=E/(HBAR*N);T0=E/(2*I[j]);fitgate=abs(tt)<min(4*T0,nearest/2,.8)
            def residual(v):return (v[0]*sech(tt[fitgate]/v[1])**2-I[fitgate])/I[j]
            fit=optimize.least_squares(residual,[I[j],T0],bounds=([I[j]*.3,self.dt/2],[I[j]*2,1.]))
            err=float(np.linalg.norm(residual(fit.x))/np.linalg.norm(I[fitgate]/I[j]))
            Ts=float(fit.x[1]);candidates.append({'omega':float(w),'lambda_um':float(wavelength(w)),'N':float(N),'N_ratio':float(N/N0),'T_fit_fs':Ts*1000,'sech_residual':err,'nearest_separation_over_T':nearest/Ts,'isolated':bool(len(peaks)>=2 and N<.95*N0 and nearest/Ts>=8 and err<=.1),'t_ps':float(self.t[j])})
        candidates.sort(key=lambda x:x['omega'])
        return {'candidates':candidates,'selected':candidates[0] if candidates else None,'selection':'reddest candidate with at least 0.1 launch photons'}
    def run(self,T,L,h,order=1,cutoffs=(),save_every=.05,Q0=None,progress=True):
        P,_=self.f.launch(T,order)
        A0=np.sqrt(P)*sech(self.t/T)*np.exp(-1j*(self.f.w0-self.wref)*self.t)
        Q=ifft(A0)*self.valid if Q0 is None else Q0.copy()
        iw=np.zeros(self.n); iw[self.valid]=1/(HBAR*self.w[self.valid]); N0=self.dt*self.n*np.sum(abs(Q)**2*iw)
        nsteps=int(np.ceil(L/h)); h=L/nsteps; stride=max(1,int(round(save_every/h)))
        records=[]; tstart=time.monotonic(); initial=Q.copy()
        for k in range(nsteps+1):
            if k%stride==0 or k==nsteps:
                rr=self.measure(Q,N0,cutoffs); rr['z']=k*h; records.append(rr)
                if self.track_fission:rr['fission']=self.fission_measure(Q,N0)
                if not np.isfinite(rr['E_pJ']): raise FloatingPointError('nonfinite field')
                # Exact translation to keep the largest pulse centred. No interpolation.
                j=int(np.argmax(np.abs(fft(Q))**2)); offset=(j-self.n//2)*self.dt
                Q*=np.exp(-1j*self.Om*offset)
                if progress and (len(records)%40==0 or k==nsteps): print(json.dumps({'z':k*h,'lambda':rr['soliton_lambda_um'],'N':rr['Ns_ratio'],'alpha_z0':rr['alpha_z0'],'wall_s':time.monotonic()-tstart}),flush=True)
            if k<nsteps: Q=self.step(Q,h)
        out={'records':records,'wall_s':time.monotonic()-tstart,'steps':nsteps,'dz_m':h,'N0':N0,'properties':self.f.properties(),'kernel':self.kernel_info,'alias_window':self.alias,'optima':{}}
        for l in cutoffs:
            key=str(l); idx=np.argmax([r['eta'][key] for r in records]); rr=records[idx]
            out['optima'][key]={'eta':rr['eta'][key],'L_m':rr['z'],'boundary':bool(idx==len(records)-1)}
        return out,{'Q0':initial,'Qfinal':Q,'omega':self.w,'t':self.t}

def execute(config_path):
    cfg=json.loads(Path(config_path).read_text()); memory_ok()
    rid=cfg['run_id']; rd=ROOT/'runs'/rid; rd.mkdir(exist_ok=True); raw=RAW/rid; raw.mkdir(exist_ok=True)
    f=Fibre(**cfg['fibre']); s=GNLSE(f,**cfg.get('grid',{})); out,arrays=s.run(**cfg['propagation'])
    out.update(IDENTITY); out['run_id']=rid; out['config']=cfg
    np.savez_compressed(raw/'fields.npz',**arrays)
    dump(rd/'summary.json',out)
    (rd/'meta.yaml').write_text(f'run_id: {rid}\nagent: gpt-d\nmodel: gpt-6-astra\nfamily: gpt\nsolver_commit: {SOLVER}\nsolver_dirty: false\nimplementation: independent.py (auditor Python RK4IP)\nhardware: {socket.gethostname()}\nwall_time_s: {out["wall_s"]}\nraw_location: {raw}\n')
    print(json.dumps({'run_id':rid,'optima':out['optima'],'final':out['records'][-1]}),flush=True)
if __name__=='__main__': execute(sys.argv[1])
