"""Independent audit solver: gpt-e / gpt-6-astra / gpt, 2026-10-19.

Fourth-order symplectic Fourier splitting of u_s=-i*d*u_tt/2+i*phi*|u|^2*u.
Exact real tangent and transpose of each subflow. No repository numerical code
is imported. Largest covariance eigenvalues give the reciprocal small ones.
"""
import numpy as np
from scipy.fft import fft, ifft, fftfreq
from scipy.sparse.linalg import LinearOperator, eigsh


def pack(z):
    return np.concatenate((z.real, z.imag))


def unpack(x):
    n = len(x)//2
    return x[:n]+1j*x[n:]


class Flow:
    def __init__(self, phi, dispersion, n=512, window=12., steps=40,
                 power=2, chirp=0., order=4, initial=None, gain=0.,save_noise_phases=False):
        self.n=n; self.window=window; self.steps=steps
        self.t=(np.arange(n)-n//2)*window/n
        self.w=2*np.pi*fftfreq(n, window/n)
        u=np.exp(-self.t**power/2-0.5j*chirp*self.t**2) if initial is None else initial(self.t).astype(complex)
        self.input=u.copy(); self.ops=[]
        c=1/(2-2**(1/3))
        coeffs=[c,1-2*c,c] if order==4 else [1.]
        # Gain uses positive-step Strang only. Tangent then conformally symplectic.
        if gain and order!=2:
            raise ValueError('Use order=2 with gain')
        for _ in range(steps):
            for coefficient in coeffs:
                h=coefficient/steps
                lin=np.exp(1j*dispersion*self.w**2*h/4+gain*h/4)
                u=ifft(fft(u)*lin)
                self.ops.append(('L',lin,np.exp(1j*np.angle(u))) if save_noise_phases else ('L',lin))
                q=np.exp(1j*phi*h*abs(u)**2)
                self.ops.append(('K',u.copy(),q,phi*h))
                u=q*u
                u=ifft(fft(u)*lin)
                self.ops.append(('L',lin,np.exp(1j*np.angle(u))) if save_noise_phases else ('L',lin))
        self.mean=u; self.gain=gain

    def forward(self,z):
        for op in self.ops:
            if op[0]=='L': z=ifft(fft(z,axis=0)*op[1][(...,)+(None,)*(z.ndim-1)],axis=0)
            else:
                _,a,q,k=op
                if z.ndim==2: a=a[:,None];q=q[:,None]
                z=q*(z+2j*k*a*np.real(np.conj(a)*z))
        return z

    def adjoint(self,z):
        for op in reversed(self.ops):
            if op[0]=='L': z=ifft(fft(z,axis=0)*np.conj(op[1])[(...,)+(None,)*(z.ndim-1)],axis=0)
            else:
                _,a,q,k=op
                if z.ndim==2: a=a[:,None];q=q[:,None]
                z=np.conj(q)*z
                z=z+2*k*a*np.imag(np.conj(a)*z)
        return z

    def covariance(self,x):
        return pack(self.forward(self.adjoint(unpack(x))))

    def spectrum(self,k=2,tol=2e-11):
        op=LinearOperator((2*self.n,2*self.n),matvec=self.covariance,dtype=float)
        rng=np.random.default_rng(191004)
        e,v=eigsh(op,k=k,which='LA',tol=tol,v0=rng.normal(size=2*self.n),ncv=max(30,2*k+1))
        ii=np.argsort(e)[::-1];e=e[ii];v=v[:,ii]
        small=np.concatenate((-v[self.n:],v[:self.n]),axis=0)
        # Exact M^T norm also checks symplectic reciprocity without cancellation.
        direct=np.array([np.linalg.norm(self.adjoint(unpack(small[:,j])))**2 for j in range(k)])
        return 1/e,small,direct

    def scaled_phase_spectrum(self,N,k=2):
        phase=np.exp(1j*np.angle(self.mean))
        def mv(x):
            a=np.real(self.adjoint(1j*phase*x))/N
            return np.imag(np.conj(phase)*self.forward(a.astype(complex)))/N
        e=eigsh(LinearOperator((self.n,self.n),matvec=mv,dtype=float),k=k,
                which='LA',tol=2e-10,v0=np.random.default_rng(191004).normal(size=self.n),return_eigenvectors=False)
        return 1/np.sort(e)[::-1]

    def diagnostics(self):
        rng=np.random.default_rng(191005)
        a=rng.normal(size=self.n)+1j*rng.normal(size=self.n)
        b=rng.normal(size=self.n)+1j*rng.normal(size=self.n)
        ma=self.forward(a);mb=self.forward(b)
        adj=abs(np.vdot(b,ma).real-np.vdot(self.adjoint(b),a).real)/np.linalg.norm(a)/np.linalg.norm(b)
        symp=abs(np.vdot(ma,mb).imag-np.exp(self.gain)*np.vdot(a,b).imag)/np.linalg.norm(a)/np.linalg.norm(b)
        spec=abs(fft(self.mean))**2
        high=float(spec[abs(self.w)>0.8*max(abs(self.w))].sum()/spec.sum())
        edge=float(np.sum(abs(self.mean[abs(self.t)>0.45*self.window])**2)/np.sum(abs(self.mean)**2))
        return dict(adjoint_defect=adj,symplectic_defect=symp,high_frequency_fraction=high,edge_energy_fraction=edge,
                    energy_relative_error=float(np.sum(abs(self.mean)**2)/np.sum(abs(self.input)**2)/np.exp(self.gain)-1))


def kerr_anchor(phi):
    return 1/(np.sqrt(1+phi*phi)+phi)**2
