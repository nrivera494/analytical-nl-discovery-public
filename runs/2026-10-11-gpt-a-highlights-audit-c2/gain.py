"""Independent gain-NLSE adjoint/moment audit; gpt-a, gpt-6-astra, gpt.

Second-order symmetric split-step; analytic tangent transpose; continuous ASE
integrated by the trapezoid rule. Physical frequency is -numpy FFT frequency.
"""
import argparse,json,time
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp,quad
from scipy.linalg import expm,eigh
from numpy.polynomial.legendre import legval,leggauss

PROVENANCE=dict(agent='gpt-a',model='gpt-6-astra',family='gpt')

def background(Gamma,U,q=0.):
    return solve_ivp(lambda z,y:[y[1],2*np.exp(Gamma*z)/y[0]**2,np.exp(Gamma*z)/y[0]],
        [0,U/Gamma],[1,q*Gamma,0],rtol=2e-12,atol=2e-13,dense_output=True)

def closed():
    out=dict(provenance=PROVENANCE,closed=[],transient=[],shape=[])
    for U in [0.,.01,2.,4.,6.,12.,24.]:
        for ns in [1.,1.5]:
            q=2*ns-1;freq=1+3*q*(1-np.exp(-U/3))
            T=(1+U/3)**2+q*(3+U*U/3-3*np.exp(-U/3))
            C=U*U/9+q*(U*U/3-2*U+6*(1-np.exp(-U/3)))
            # Direct convolution of W(s)=exp(2s/3)[[1,1/3],[1/3,1/9]].
            W0=np.array([[1,1/3],[1/3,1/9]])
            R=np.array([[1,U],[0,1.]])
            Cin=R@W0@R.T
            Case=np.array([[quad(lambda s,i=i,j=j: np.exp(-s/3)*(np.array([[1,U-s],[0,1.]])@W0@np.array([[1,0],[U-s,1.]]))[i,j],0,U,epsabs=1e-12)[0] for j in range(2)] for i in range(2)])
            cov=Cin+q*Case;v=np.array([1.,-3.])
            out['closed'].append(dict(gL=U,nsp=ns,frequency=freq,timing=T,compressed=C,
                 max_absolute_residual=float(max(abs(cov[0,0]-T),abs(9*cov[1,1]-freq),abs(v@cov@v-C)))))
    for Gamma in [np.sqrt(18),1.]:
      for U in [2.,4.,6.]:
        sol=background(Gamma,U);L=U/Gamma;a,ap,theta=sol.y[:,-1]
        def h(z):
            aa,ad,_=sol.sol(z);return aa+ad*(L-z-a/ap)
        ase=Gamma/5*quad(lambda z:np.exp(-Gamma*z)*h(z)**2,0,L,epsabs=1e-11)[0]
        out['transient'].append(dict(Gamma=Gamma,gL=U,aL=a,apL=ap,thetaL=theta,comp_input=h(0)**2/5,comp_ASE=ase))
    # Autonomous transformed Legendre system on the exact asymptote.
    Gamma=np.sqrt(18);ls=np.arange(5);H=np.zeros((10,10));Q=np.zeros((10,10))
    x,w=leggauss(80);P=np.array([legval(x,[0]*l+[1]) for l in ls]);c=(2*ls+1)/2
    B=(4/3)*c[:,None]*c[None,:]*((P*(w*(1-x*x)))@P.T)
    for l in ls:H[2*l,2*l+1]=-l*(l+1)/Gamma;H[2*l+1,2*l]=1/Gamma;H[2*l+1,2*l+1]=-2/3
    Q[::2,::2]=B
    S=np.zeros((5,10))
    for l in ls:S[l,2*l]=1.;S[l,2*l+1]=-3*l*(l+1)/Gamma
    conv=lambda u,cov:H@cov+cov@H.T+np.exp(-u)*Q
    sol=solve_ivp(lambda u,v:conv(u,v.reshape(10,10)).ravel(),[0,30],Q.ravel(),rtol=2e-11,atol=2e-13,dense_output=True)
    for U in [6.,9.,12.,15.,18.,21.,24.,27.,30.]:
        cov=sol.sol(U).reshape(10,10);d=np.sqrt(2/(2*ls+1));cs=(S@cov@S.T)*d[:,None]*d[None,:];ev=eigh(cs,eigvals_only=True)
        v=np.zeros(10);v[1]=1;v[5]=-1/5
        r2=float((cov[0]@v)**2/(cov[0,0]*(v@cov@v)))
        # Row-norm envelopes (the cosine/sine modulation remains explicit).
        M=expm(H[4:6,4:6]*U);ng=np.exp(U)*np.sum(M[0]**2);pg=np.exp(7*U/3)*np.sum(M[1]**2)
        out['shape'].append(dict(gL=U,eigenvalue_ratio=float(ev[-2]/ev[-1]),phase_residual=1-r2,
          s_variance_ratios=(np.diag(S@cov@S.T)/cov[0,0]).tolist(),intensity_gain=float(ng),phase_gain=float(pg),
          matched_phase_gain_coefficient=float(np.exp(7*U/3)*(v@cov@v))))
    out['shape_rates']=[dict(l=int(l),rates_real=np.linalg.eigvals(H[2*l:2*l+2,2*l:2*l+2]).real.tolist(),rates_imag=np.linalg.eigvals(H[2*l:2*l+2,2*l:2*l+2]).imag.tolist()) for l in ls]
    Path(__file__).with_name('closed.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))

def run(case='p8',eps=.05,U=4.,refine=1,gbw=0.,edge='e1',spectral=True):
    start=time.time()
    if case.startswith('p8'):
        beta=.025;gamma=0. if case=='p8_lin' else .005;g=1.9;L=3.2;window=12.;nt=2048*refine
        T0=.25/(2*np.sqrt(np.log(2)));P0=10/(np.sqrt(np.pi)*T0);steps=4000*refine
        hydro=None
    else:
        Gamma=1. if case=='heldout' else np.sqrt(18);q=1/3 if case=='asym' else 0.
        hydro=background(Gamma,U,q);a,ap,theta=hydro.y[:,-1]
        beta=gamma=T0=1.;P0=1/eps**2;g=Gamma/eps;L=U/g
        window=float(2*np.ceil(1.45*a+5));nt=int(2**np.ceil(np.log2(window*2.4*ap/eps/np.pi)))*refine
        steps=max(2000,int(np.ceil(theta/eps/.025)))*refine
    dt=window/nt;t=(np.arange(nt)-nt//2)*dt;w=-2*np.pi*np.fft.fftfreq(nt,dt)
    # Bound the largest linear phase increment, avoiding split-step resonance.
    steps=max(steps,int(np.ceil(L*beta*np.max(w*w)/2/.5)))
    h=L/steps;gprof=g*(1-gbw/(g*L)*(w/(ap/eps))**2) if gbw else np.full(nt,g)
    lin=np.exp((.5j*beta*w*w+gprof/2)*h/2)
    linear=lambda v:np.fft.ifft(lin[:,None]*np.fft.fft(v,axis=0),axis=0)
    if case.startswith('p8'):u=np.sqrt(P0)*np.exp(-t*t/(2*T0*T0))
    else:
        delta=.5*(eps if edge=='e1' else eps**(2/3))
        u=np.sqrt(P0*delta*np.logaddexp(0,(1-t*t)/delta))*np.exp(-1j*q*g*t*t/2)
    u=u.astype(complex);u0=u.copy();saved=np.empty((steps,nt),complex);W=[]
    def moments(v):
        rho=abs(v)**2;E=dt*rho.sum();tc=dt*np.sum(t*rho)/E
        Du=np.fft.ifft(w*np.fft.fft(v));wc=dt*np.vdot(v,Du).real/E
        return np.array([E,dt*np.sum((t-tc)**2*rho)/E,dt*np.vdot(Du-wc*v,Du-wc*v).real/E,
          dt*np.sum((t-tc)*np.real(v.conj()*(Du-wc*v)))/E,tc,wc])
    W.append(moments(u))
    for k in range(steps):
        v=linear(u[:,None])[:,0];saved[k]=v
        u=linear((v*np.exp(1j*gamma*h*abs(v)**2))[:,None])[:,0];W.append(moments(u))
    W=np.array(W);E0=W[0,0];EL=W[-1,0];m=W[-1];tc,wc=m[4:]
    grads=[u/EL,(t-tc)*u/EL,(np.fft.ifft(w*np.fft.fft(u))-wc*u)/EL,1j*u/np.sqrt(EL)]
    names=['relative_energy','Tc','Omega','LO_phase']
    if spectral:
        we=np.sqrt(5*m[2]);S0=.75*EL/we;core=abs(w-wc)<=we;xi=(w-wc)/we
        for l in range(5):
            weight=(2*l+1)/2/(we*S0)*legval(xi,[0]*l+[1])*core
            grads.append(np.fft.ifft(weight*np.fft.fft(u)));names.append('s'+str(l))
    v=np.column_stack(grads)
    def gram(v,noise=False):
        if noise and gbw:
            vf=np.fft.fft(v,axis=0,norm='ortho');return dt*np.einsum('ti,t,tj->ij',vf.conj(),abs(gprof/g),vf,optimize=False).real
        return dt*np.einsum('ti,tj->ij',v.conj(),v,optimize=False).real
    ase=.5*gram(v,True)
    for k in reversed(range(steps)):
        v=np.fft.ifft(lin.conj()[:,None]*np.fft.fft(v,axis=0),axis=0)
        mid=saved[k];phi=gamma*h*abs(mid)**2;rot=np.exp(1j*phi);a=rot*(1+1j*phi);b=rot*1j*gamma*h*mid*mid
        v=a.conj()[:,None]*v+b[:,None]*v.conj()
        v=np.fft.ifft(lin.conj()[:,None]*np.fft.fft(v,axis=0),axis=0)
        ase+=(.5 if k==0 else 1)*gram(v,True)
    Cin=E0*gram(v);Case=E0*g*h*ase
    z=np.linspace(0,L,steps+1);r=L-z
    f=np.array([W[:,1]+2*beta*r*W[:,3]+beta**2*r*r*W[:,2],W[:,2],W[:,3]+beta*r*W[:,2]])/W[:,0]*E0
    m_in=f[:,0];m_ase=g*np.trapezoid(f,z,axis=1)
    Dc=-m[3]/m[2];vcomp=np.array([1,Dc]);idx=[1,2]
    ti=float(vcomp@Cin[np.ix_(idx,idx)]@vcomp);ta=float(vcomp@Case[np.ix_(idx,idx)]@vcomp)
    ef=float(np.sum(abs(u[abs(t)>.4*window])**2)*dt/EL);fw=abs(np.fft.fft(u))**2
    out=dict(provenance=PROVENANCE,case=case,eps=eps,gL=g*L,refine=refine,gbw=gbw,edge=edge,nt=nt,window=window,steps=steps,
      parameters=dict(beta2=beta,gamma=gamma,g=g,L=L,P0=P0),names=names,C_in=Cin.tolist(),C_ASE=Case.tolist(),
      moment_input=m_in.tolist(),moment_ASE=m_ase.tolist(),seed_W=W[0].tolist(),output_W=W[-1].tolist(),
      compressed_input=ti,compressed_ASE=ta,Dc=Dc,energy_error=EL/(E0*np.exp(g*L))-1,
      time_edge_fraction=ef,frequency_edge_fraction=float(fw[abs(w)>.75*max(abs(w))].sum()/fw.sum()),wall_seconds=time.time()-start)
    assert np.isfinite(Cin).all() and np.isfinite(Case).all() and np.isfinite(W).all()
    out['all_covariance_and_moment_entries_finite']=True
    if hydro is not None:out['hydro']=dict(aL=a if np.isscalar(a) else float(hydro.y[0,-1]),apL=ap,thetaL=theta,Gamma=Gamma)
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode');p.add_argument('--case',default='p8');p.add_argument('--eps',type=float,default=.05);p.add_argument('--gL',type=float,default=4.);p.add_argument('--refine',type=int,default=1);p.add_argument('--gbw',type=float,default=0.);p.add_argument('--edge',default='e1');p.add_argument('--output');args=p.parse_args()
    if args.mode=='closed':closed()
    else:
        out=run(args.case,args.eps,args.gL,args.refine,args.gbw,args.edge);Path(args.output).write_text(json.dumps(out,indent=2));print(json.dumps({k:out[k] for k in ['case','eps','gL','nt','steps','compressed_input','compressed_ASE','energy_error','wall_seconds']}),flush=True)
