"""gpt-b / gpt-6-astra / gpt. Independent quantum-noise observables, vacuum=1."""
from thermalized_light import *
from scipy.special import ndtri
from scipy.stats import qmc

def sq_library():
    src=ROOT/'evaluator/squeezing_core.c';old=ROOT/'evaluator/thermalized_light_core.c'
    digest=hashlib.sha256(src.read_bytes()+old.read_bytes()).hexdigest()[:16]
    dest=Path('/private/tmp')/f'gpt-b-squeezing-{digest}.dylib'
    if not dest.exists():subprocess.run(['clang','-O3','-std=c11','-fPIC','-shared',str(src),'-o',str(dest)],check=True)
    lib=ct.CDLL(str(dest));ip=np.ctypeslib.ndpointer(np.int32,flags='C_CONTIGUOUS');dp=np.ctypeslib.ndpointer(np.float64,flags='C_CONTIGUOUS');zp=np.ctypeslib.ndpointer(np.complex128,flags='C_CONTIGUOUS')
    common=[ct.c_int,ct.c_int,ip,ip,ip,ip,dp,ip]
    lib.sq_tangent.argtypes=common+[zp,ct.c_double,ct.c_int,ct.c_double,ct.c_uint64,ct.c_int,ct.c_int,ip,zp]
    lib.sq_ensemble.argtypes=common+[zp,zp,ct.c_int,ct.c_double,ct.c_int,ct.c_double,ct.c_uint64,ct.c_int,ct.c_int,ip,zp,ct.c_double,ct.c_double,ct.c_uint64]
    return lib

def base_args(m):return [m.M,len(m.p),m.p,m.r,m.offset,m.column,m.value,m.q]
def tangent_run(m,a,zs,dt=.02,sigma=.3,seed=7601):
    if dt not in [.02,.01,.005,.0025,.00125,.000625]:raise ValueError('Nested dyadic Brownian grid rooted at .02')
    zs=np.array(zs);steps=np.rint(zs/dt).astype(np.int32);M=m.M
    x=np.zeros((1+2*M,M),complex);x[0]=a;x[1:1+M]=np.eye(M);x[1+M:]=1j*np.eye(M)
    out=np.zeros((len(zs),1+2*M,M),complex)
    cp=sq_library().sq_tangent(*base_args(m),x,dt,int(steps[-1]),sigma,seed,round(.02/dt),len(zs),steps,out)
    if cp!=len(zs):raise RuntimeError('Missing checkpoints')
    return out

def wigner_initial(a,n,power=9,seed=8701,nu=1):
    M=len(a);x=ndtri(qmc.Sobol(2*M,scramble=True,seed=seed).random_base2(power))
    return a+(x[:,:M]+1j*x[:,M:])*np.sqrt(nu)/(2*np.sqrt(n)),x

def ensemble_run(m,a,n,zs,dt=.02,sigma=.3,seed=7601,alpha=0,loss_seed=8901,weyl=True):
    zs=np.array(zs);steps=np.rint(zs/dt).astype(np.int32)
    a=np.ascontiguousarray(a,dtype=complex).copy();out=np.zeros((len(zs),len(a),m.M),complex)
    linear=np.ascontiguousarray(np.einsum('pqqs->ps',m.tensor)/n if weyl else np.zeros((m.M,m.M)),dtype=complex)
    cp=sq_library().sq_ensemble(*base_args(m),linear,a,len(a),dt,int(steps[-1]),sigma,seed,round(.02/dt),len(zs),steps,out,alpha,n,loss_seed)
    if cp!=len(zs):raise RuntimeError('Missing checkpoints')
    return out

def real_matrix(x):return np.concatenate([x.real,x.imag],axis=-1)
def tangent_observables(x):
    a=x[0];M=len(a);S=real_matrix(x[1:]).T
    U,s,v=np.linalg.svd(S,full_matrices=False);V=S@S.T
    phase=np.angle(a);P=np.zeros((M,2*M));P[np.arange(M),np.arange(M)]=np.cos(phase);P[np.arange(M),M+np.arange(M)]=np.sin(phase)
    amp=P@V@P.T;e,c=np.linalg.eigh(amp)
    # Exact tangent minimum from singular values, not subtracting large eigenvalues.
    R=np.array([[np.cos(phase[0]),np.sin(phase[0])],[-np.sin(phase[0]),np.cos(phase[0])]])
    own=R@V[np.ix_([0,M],[0,M])]@R.T
    ev=np.linalg.eigvalsh(own);det=np.linalg.det(own)
    J=np.block([[np.zeros((M,M)),np.eye(M)],[-np.eye(M),np.zeros((M,M))]])
    return dict(a=a,S=S,V=V,lambda_quad=s[-1]**2,quad_direction=U[:,-1],sigma_max=s[0],
        lambda_gen=e[0],count_direction=c[:,0],P=P,own=own,lambda_own=ev[0],
        own_approx=det/own[1,1],nu=np.sqrt(max(0,det)),f0=abs(a[0])**2,
        symplectic_error=float(np.max(abs(S@J@S.T-J))),reciprocal_error=float(np.max(abs(s*s[::-1]-1))),
        Fano_N=float(abs(a)@amp@abs(a)/np.sum(abs(a)**2)))

def sample_observables(fields,n,tan,initial_noise=None):
    M=fields.shape[1];mean=fields.mean(axis=0);d=2*np.sqrt(n)*real_matrix(fields-mean);V=np.cov(d,rowvar=False,ddof=1)
    pow=abs(fields)**2;counts=n*pow-.5;mean_count=counts.mean(axis=0)
    # Center counts before covariance: avoids n^2 cancellation at n=1e10.
    dc=n*(pow-pow.mean(axis=0));C=np.cov(dc,rowvar=False,ddof=1)-np.eye(M)/4
    safe=np.maximum(mean_count,1e-300);F=C/np.sqrt(safe[:,None]*safe[None,:]);e=np.linalg.eigvalsh(F)
    direction=tan['quad_direction'];c=tan['count_direction'];phase=np.angle(mean[0]);R=np.array([[np.cos(phase),np.sin(phase)],[-np.sin(phase),np.cos(phase)]])
    own=R@V[np.ix_([0,M],[0,M])]@R.T
    frozen_weights=c/np.maximum(abs(tan['a']),1e-150)
    scalar=(pow-pow.mean(axis=0))@frozen_weights
    denominator=float(np.sum(frozen_weights**2*mean_count/n))
    frozen_variance=(n*np.var(scalar,ddof=1)-np.sum(frozen_weights**2)/(4*n))/denominator
    out=dict(count_frozen_weights=float(frozen_variance),count_frozen_shot_denominator=denominator,
        min_mean_photons=float(np.min(mean_count)),max_mean_photons=float(np.max(mean_count)),
        condensate_coherence=float(abs(mean[0])**2/(mean_count[0]/n)),
        total_coherent_fraction=float(np.sum(abs(mean)**2)/(np.sum(mean_count)/n)),
        lambda_quad=np.linalg.eigvalsh(V)[0],quad_fixed=float(direction@V@direction),
        lambda_gen=e[0],count_fixed=float(c@F@c),lambda_own=np.linalg.eigvalsh(own)[0],own=own,
        Fano_N=float(C.sum()/mean_count.sum()),mean_photons=mean_count,V=V,F=F)
    if initial_noise is not None:
        # Paired tangent control: subtract its finite-sample variance, add analytic variance.
        lin=initial_noise@tan['S'].T
        vl=np.cov(lin,rowvar=False,ddof=1)
        out['quad_fixed_control']=out['quad_fixed']-float(direction@vl@direction)+tan['lambda_quad']
        cl=c@tan['P'];out['count_frozen_weights_control']=out['count_frozen_weights']-(float(cl@vl@cl)-tan['lambda_gen'])/denominator
        # A fixed condensate tangent eigenvector avoids fitted-angle bias in the 1/n residual.
        _,evec=np.linalg.eigh(tan['own']);angle=np.angle(tan['a'][0]);R0=np.array([[np.cos(angle),np.sin(angle)],[-np.sin(angle),np.cos(angle)]])
        v0=R0.T@evec[:,0];full=np.zeros(2*M);full[[0,M]]=v0
        out['own_fixed']=float(full@V@full)
        out['own_fixed_control']=out['own_fixed']-float(full@vl@full)+tan['lambda_own']
    return out
