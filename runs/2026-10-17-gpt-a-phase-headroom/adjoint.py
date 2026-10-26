#!/usr/bin/env python3
"""Independent checkpointed discrete RK4IP VJP. gpt-a/gpt-6-astra/gpt."""
from independent import *
from scipy.optimize import minimize
import gc, subprocess

def zs_terminal(t,u,N,refine=1):
    dt=t[1]-t[0];ip=np.argmax(abs(u)**2);hw=max(2.,12/(N*abs(u[ip])))
    inds=np.where(abs(t-t[ip])<=hw)[0];tt=t[inds];qpre=N*u[inds]
    k=2*np.pi*fftfreq(len(inds),dt);Q=fft(qpre);kc=np.sum(k*abs(Q)**2)/np.sum(abs(Q)**2)
    demod=np.exp(-1j*kc*tt);qbase=qpre*demod;q=qbase;work_t=tt
    if refine>1:
        # Odd input/output lengths make Fourier interpolation and its adjoint
        # exact transposes without an unpaired Nyquist mode. Zero-padding is
        # part of the linear map and its adjoint is the corresponding crop.
        pad=len(q)//2;right=pad+(1 if len(q)%2==0 else 0)
        qp=np.pad(q,(pad,right));nin=len(qp);nout=refine*nin+(1 if refine%2==0 else 0)
        q=resample(qp,nout);dt=dt*nin/nout
        work_t=tt[0]-pad*(t[1]-t[0])+np.arange(nout)*dt
    mid=(q[:-1]+q[1:])/2
    def transfer(z,grad=False):
        r=-z*z-abs(mid)**2;b=np.sqrt(r+0j);C=np.cosh(b*dt);S=np.sinh(b*dt)/b
        C1=dt*S/2;S1=(dt*C-S)/(2*r)
        T=np.empty((len(mid),2,2),complex);T[:,0,0]=C-1j*z*S;T[:,1,1]=C+1j*z*S
        T[:,0,1]=S*mid;T[:,1,0]=-S*mid.conj()
        U=np.empty_like(T);U[:,0,0]=C1-1j*z*S1;U[:,1,1]=C1+1j*z*S1
        U[:,0,1]=S1*mid;U[:,1,0]=-S1*mid.conj()
        Z=-2*z*U;Z[:,0,0]-=1j*S;Z[:,1,1]+=1j*S
        def inverse(mats):
            out=np.empty_like(mats)
            out[:,0,0]=mats[:,1,1];out[:,1,1]=mats[:,0,0]
            out[:,0,1]=-mats[:,0,1];out[:,1,0]=-mats[:,1,0]
            return out
        Ti=inverse(T);Zi=inverse(Z);split=len(mid)//2
        Y=np.zeros((len(q),2),complex);Y[0,0]=1
        R=np.zeros_like(Y);R[-1,1]=1
        yz=np.zeros(2,complex);rz=np.zeros(2,complex)
        for j in range(split):
            yz=T[j]@yz+Z[j]@Y[j];Y[j+1]=T[j]@Y[j]
        for j in range(len(mid)-1,split-1,-1):
            rz=Ti[j]@rz+Zi[j]@R[j+1];R[j]=Ti[j]@R[j+1]
        det=lambda v,w:v[0]*w[1]-v[1]*w[0]
        a=det(Y[split],R[split]);az=det(yz,R[split])+det(Y[split],rz)
        if not grad:return a,az
        X=-2*mid.real[:,None,None]*U;X[:,0,1]+=S;X[:,1,0]-=S
        V=-2*mid.imag[:,None,None]*U;V[:,0,1]+=1j*S;V[:,1,0]+=1j*S
        Xi=inverse(X);Vi=inverse(V)
        dx=np.zeros(len(mid),complex);dy=np.zeros(len(mid),complex)
        row=np.array([R[split,1],-R[split,0]])
        for j in range(split-1,-1,-1):
            dx[j]=row@X[j]@Y[j];dy[j]=row@V[j]@Y[j];row=row@T[j]
        row=np.array([-Y[split,1],Y[split,0]])
        for j in range(split,len(mid)):
            dx[j]=row@Xi[j]@R[j+1];dy[j]=row@Vi[j]@R[j+1];row=row@Ti[j]
        gm=(-dx/az).imag+1j*(-dy/az).imag;gq=np.zeros(len(q),complex)
        gq[:-1]+=gm/2;gq[1:]+=gm/2
        return a,az,gq
    solution=zs_shoot(work_t,q,np.max(abs(q))/2)
    if not (solution['root_ok'] and solution['eta']>0 and solution['evans_residual']<1e-8):
        candidates=[zs_shoot(work_t,q,factor*np.max(abs(q))/2) for factor in [.8,.6,1.2]]
        candidates=[r for r in candidates if r['root_ok'] and r['eta']>0 and r['evans_residual']<1e-8]
        if not candidates:raise ValueError(f'No leading ZS root: {solution}')
        solution=max(candidates,key=lambda r:r['eta'])
    z=solution['zeta_re']+1j*solution['eta']
    if not (0<z.imag<np.max(abs(q))*1.2):raise ValueError(f'ZS root out of range {z}')
    _,_,gq=transfer(z,True)
    if refine>1:gq=(nout/nin)*resample(gq,nin)[pad:pad+len(qbase)]
    dk=np.vdot(gq,-1j*tt*qbase).real
    gk=2*(ifft(k*Q)-kc*qpre)/np.sum(abs(qpre)**2)
    gt=np.zeros(len(t),complex);gt[inds]=2/N*(gq*demod.conj()+dk*gk)
    return 2*z.imag/N**2,gt,{'red_k':float(kc),'peak_t':float(t[ip]),'eta':float(z.imag),'gate_fraction':float((t[1]-t[0])*np.sum(abs(u[inds])**2)/2),'zs_refine':refine}

class DiscreteAdjoint:
    def __init__(self,N,T0,nt=8192,width=80.,hfac=1.,M=30,stride=32,zs_refine=1):
        self.N=N;self.T0=T0;self.nt=nt;self.dt=width/nt;self.width=width;self.M=M;self.stride=stride
        self.zs_refine=zs_refine
        self.t=(np.arange(nt)-nt//2)*self.dt;self.k=2*np.pi*fftfreq(nt,self.dt)
        self.Q=fft(1/np.cosh(self.t));self.wc=2*np.pi # keep the physical mask fixed across window checks
        self.B=basis(self.k,M,self.wc)
        self.z=4/N;self.steps=int(np.ceil(self.z/(.4/(N*(2*N-1))**2*hfac)));self.h=self.z/self.steps
        self.E=np.exp(-.25j*self.k**2*self.h);a=T0/32;b=T0/12.2
        self.H=(a*a+b*b)/((a+1j*self.k)**2+b*b);self.H[nt//2]=self.H[nt//2].real
        self.pref=1j*N*N
    def nl(self,V,cache=False):
        u=ifft(V);p=abs(u)**2;R=.82*p+.18*ifft(self.H*fft(p)).real
        out=self.pref*fft(u*R)
        return (out,(u,R)) if cache else out
    def vjp(self,lam,cache):
        u,R=cache;v=ifft(np.conj(self.pref)*lam)
        r=(v.conj()*u).real;ct=.82*r+.18*ifft(self.H.conj()*fft(r)).real
        return fft(R*v+2*u*ct)
    def step(self,U,cache=False):
        h=self.h;E=self.E;V=E*U
        a,ca=self.nl(U,True);k1=h*E*a
        a,cb=self.nl(V+k1/2,True);k2=h*a
        a,cc=self.nl(V+k2/2,True);k3=h*a
        a,cd=self.nl(E*(V+k3),True);k4=h*a
        out=E*(V+(k1+2*k2+2*k3)/6)+k4/6
        return (out,(ca,cb,cc,cd)) if cache else out
    def reverse(self,lam,cache):
        ca,cb,cc,cd=cache;h=self.h;Ec=self.E.conj()
        lv=Ec*lam;lk1=lv/6;lk2=lv/3;lk3=lv/3
        lc=h*self.vjp(lam/6,cd);lv=lv+Ec*lc;lk3=lk3+Ec*lc
        lb=h*self.vjp(lk3,cc);lv+=lb;lk2=lk2+lb/2
        la=h*self.vjp(lk2,cb);lv+=la;lk1=lk1+la/2
        return h*self.vjp(Ec*lk1,ca)+Ec*lv
    def evaluate(self,c,gradient=True):
        if hasattr(self,'failure_state'):del self.failure_state
        U0=self.Q*np.exp(1j*np.sum(self.B*c,axis=1));U=U0.copy();checkpoints={0:U.copy()}
        edge=abs(self.t)>.45*self.width
        input_edge=float(self.dt*np.sum(abs(ifft(U)[edge])**2)/2);max_edge=input_edge
        if input_edge>1e-6:
            self.failure_state=(ifft(U),dict(kind='input window',edge_mass=input_edge,step=0))
            raise ValueError(f'Unresolved input time-window edge: {input_edge}')
        for j in range(self.steps):
            U=self.step(U)
            if (j+1)%self.stride==0:
                checkpoints[j+1]=U.copy()
                max_edge=max(max_edge,float(self.dt*np.sum(abs(ifft(U)[edge])**2)/2))
                if max_edge>1e-6:
                    self.failure_state=(ifft(U),dict(kind='propagation window',edge_mass=max_edge,step=j+1))
                    raise ValueError(f'Unresolved propagation time-window edge: {max_edge}')
        u=ifft(U)
        try:f,gt,diag=zs_terminal(self.t,u,self.N,self.zs_refine)
        except ValueError:
            self.failure_state=(u,dict(kind='ZS root',step=self.steps));raise
        diag.update(input_edge=input_edge,max_propagation_edge=max_edge,
                    output_alias=float(np.sum(abs(U[abs(self.k)>.8*np.pi/self.dt])**2)/np.sum(abs(U)**2)),
                    mass_drift=float(self.dt*np.sum(abs(u)**2)/2-1))
        if not gradient:return f,None,diag,u
        lam=fft(gt)/self.nt
        # Segment boundaries match saved multiples even for a final short chunk.
        ends=list(range(0,self.steps,self.stride))+[self.steps]
        for idx in range(len(ends)-1,0,-1):
            a,b=ends[idx-1],ends[idx];v=checkpoints[a].copy();caches=[]
            for j in range(a,b):v,cs=self.step(v,True);caches.append(cs)
            for cs in reversed(caches):lam=self.reverse(lam,cs)
        g=np.sum((lam.conj()*(1j*U0))[:,None]*self.B,axis=0).real
        return f,g,diag,u

def run(N,T0,start,maxiter=200,nt=8192,hfac=1.,mode='opt',warm=None,precondition=False,method='L-BFGS-B',zs_refine=1,stop_gradient=0.,width=80.,max_seconds=0.):
    if start=='polish' and max_seconds==0:max_seconds={3:420,4:600,5:1200}[int(N)]
    engine=DiscreteAdjoint(N,T0,nt=nt,width=width,hfac=hfac,zs_refine=zs_refine);M=engine.M;c=np.zeros(M)
    if warm is not None:c=np.loadtxt(warm,delimiter=',')
    elif start=='B':c[:15]=coefficients('B')
    elif start.startswith('r'):
        rng=np.random.default_rng(2026101700+int(start[1:]));c=rng.normal(size=M)*({'r1':.2,'r2':.7,'r3':1.5}[start])
    tag=f'pyopt_N{int(N)}_T{int(T0)}_{start}';began=time.time();rows=[];best=-np.inf;best_gradient=None;last=None;rejected=0
    def fun(c):
        nonlocal best,best_gradient,last,rejected
        try:f,g,d,u=engine.evaluate(c)
        except ValueError as exc:
            rejected+=1;stem=f'{tag}_rejected_{rejected:03d}'
            np.savetxt(RAW/(stem+'_coef.csv'),c,delimiter=',')
            failure=dict(agent='gpt-a',model='gpt-6-astra',family='gpt',error=str(exc),elapsed_s=time.time()-began,
                         successful_evaluations=len(rows),rejected_evaluations=rejected,action='reject unresolved trial; never treat penalty as physical objective')
            if hasattr(engine,'failure_state'):
                fu,fd=engine.failure_state;failure.update(fd)
                np.savez_compressed(RAW/(stem+'_field.npz'),t=engine.t,u=fu,c=c)
            (RAW/(stem+'.json')).write_text(json.dumps(failure,indent=2));print('REJECTED',json.dumps(failure),flush=True)
            if last is None:raise
            delta=c-last[0]
            return 1e3+float(delta@delta),2*delta
        elapsed=time.time()-began;last=(c.copy(),g.copy())
        row={'evaluation':len(rows)+1,'total_evaluation':len(rows)+rejected+1,'elapsed_s':elapsed,'f_zs':f,'gradient_norm':float(np.linalg.norm(g)),**d};rows.append(row)
        with open(RAW/(tag+'_history.jsonl'),'a') as file:file.write(json.dumps(row)+'\n')
        if f>best:
            best=f;best_gradient=float(np.linalg.norm(g));np.savetxt(RAW/(tag+'_bestcoef.csv'),c,delimiter=',');np.savez_compressed(RAW/(tag+'_bestfield.npz'),t=engine.t,u=u,c=c)
        print(tag,json.dumps(row),flush=True)
        return -f,-g
    if mode in ['check','checkopt']:
        f,g,d,u=engine.evaluate(c);rng=np.random.default_rng(2026101704);v=rng.normal(size=M);v/=np.linalg.norm(v);eps=1e-5
        fd=(engine.evaluate(c+eps*v,False)[0]-engine.evaluate(c-eps*v,False)[0])/(2*eps);pred=float(g@v)
        check={'f':f,'gradient':g.tolist(),'fd':fd,'adjoint':pred,'relative_error':abs(fd-pred)/max(abs(fd),abs(pred)),
               'elapsed_s':time.time()-began,'N':N,'T0_fs':T0,'h':engine.h,'nt':nt,'width':engine.width,'ZS_min_halfwidth':2.,'zs_refine':zs_refine}
        (RAW/(tag+'_check.json')).write_text(json.dumps(check,indent=2));print('CHECK',json.dumps(check),flush=True)
        np.savez_compressed(RAW/(tag+'_checkfield.npz'),t=engine.t,u=u)
        # Near a stationary point the directional derivative can approach zero;
        # a relative-only comparison then amplifies Float64 differencing noise.
        check['absolute_error']=abs(fd-pred)
        check['tolerance']=1e-9+1e-4*max(abs(fd),abs(pred))
        check['passed']=bool(check['absolute_error']<=check['tolerance'])
        (RAW/(tag+'_check.json')).write_text(json.dumps(check,indent=2))
        if not check['passed']:raise ValueError('Gradient mismatch')
        if mode=='check':return
    transform=np.eye(M)
    if precondition:
        weight=abs(engine.Q)**2;weight/=weight.sum()
        gauges=np.column_stack([np.ones(engine.nt),engine.k])
        projection=np.linalg.solve(np.einsum('ni,n,nj->ij',gauges,weight,gauges),
                                   np.einsum('ni,n,nj->ij',gauges,weight,engine.B))
        physicalB=engine.B-np.einsum('ni,ij->nj',gauges,projection)
        gram=np.einsum('ni,n,nj->ij',physicalB,weight,physicalB)
        if not np.isfinite(gram).all():raise ValueError('Nonfinite phase preconditioner')
        eig,vec=np.linalg.eigh(gram)
        transform=vec/np.sqrt(np.maximum(eig,0)+1e-4)[None,:]
    def transformed(x):
        val,grad=fun(transform@x)
        return val,transform.T@grad
    def callback(x):
        if max_seconds>0 and time.time()-began>=max_seconds:raise StopIteration
        if (stop_gradient>0 and last is not None and np.allclose(transform@x,last[0],rtol=0,atol=1e-12)
                and np.linalg.norm(last[1])<=stop_gradient):raise StopIteration
    options={'maxiter':maxiter,'gtol':1e-6,'ftol':1e-14,'maxls':30,'maxcor':20} if method=='L-BFGS-B' else {'maxiter':maxiter,'gtol':1e-6,'norm':2}
    result=minimize(transformed,np.linalg.solve(transform,c),jac=True,method=method,options=options,callback=callback)
    if method=='BFGS':
        np.savez_compressed(RAW/(tag+'_BFGS_state.npz'),x=result.x,inverse_hessian=np.asarray(result.hess_inv),
                            transform=transform,agent='gpt-a',model='gpt-6-astra',family='gpt')
    final_c=transform@result.x
    f,g,d,u=engine.evaluate(final_c);np.savetxt(RAW/(tag+'_finalcoef.csv'),final_c,delimiter=',')
    summary={'agent':'gpt-a','model':'gpt-6-astra','family':'gpt','N':N,'T0_fs':T0,'start':start,'f_zs':f,'best_f_zs':best,
             'gradient_norm':float(np.linalg.norm(g)),'best_gradient_norm':best_gradient,'gradient_max':float(np.max(abs(g))),'iterations':int(result.nit),'calls':len(rows),'rejected_calls':rejected,'total_calls':len(rows)+rejected,
             'converged':bool(np.linalg.norm(g)<=1e-5),
             'optimizer_reported_success':bool(result.success),'raw_gradient_stopping_target':stop_gradient,
             'termination':str(result.message),'coefficients':M,'nt':nt,'width':engine.width,
             'dt_fs':engine.dt*T0,'h':engine.h,'elapsed_s':time.time()-began,'wall_clock_limit_s':max_seconds,'diag':d,'preconditioned':precondition,'optimization_method':method,'zs_refine':zs_refine}
    (RAW/(tag+'_summary.json')).write_text(json.dumps(summary,indent=2));print('SUMMARY',json.dumps(summary),flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('N',type=float);p.add_argument('T0',type=float);p.add_argument('start');p.add_argument('--mode',default='opt')
    p.add_argument('--maxiter',type=int,default=200);p.add_argument('--nt',type=int,default=8192);p.add_argument('--hfac',type=float,default=1.);p.add_argument('--warm');p.add_argument('--precondition',action='store_true');p.add_argument('--method',default='L-BFGS-B',choices=['L-BFGS-B','BFGS'])
    p.add_argument('--zs-refine',dest='zs_refine',type=int,default=1)
    p.add_argument('--stop-gradient',dest='stop_gradient',type=float,default=0.)
    p.add_argument('--width',type=float,default=80.)
    p.add_argument('--max-seconds',dest='max_seconds',type=float,default=0.)
    args=p.parse_args();budget_path=HERE/'training_budget.json'
    if budget_path.exists():
        budget=json.loads(budget_path.read_text());key=f'N{int(args.N)}_T{int(args.T0)}_{args.start}'
        if key in budget['deferred_starts']:
            print('DEFERRED BEFORE PROPAGATION',key,budget['reason'],flush=True)
            raise SystemExit(75)
    run(**vars(args))
