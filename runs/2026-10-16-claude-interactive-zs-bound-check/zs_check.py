import numpy as np, math
rng=np.random.default_rng(7)
def zs_raw(qfun,n,T=24):
    t=np.linspace(-T,T,n,endpoint=False); dt=t[1]-t[0]
    k=2*np.pi*np.fft.fftfreq(n,dt)
    D=np.real(np.fft.ifft(1j*k[:,None]*np.fft.fft(np.eye(n),axis=0),axis=0))
    q=qfun(t); Q=np.diag(q)
    L=np.block([[1j*D,-1j*Q],[-1j*np.conj(Q),-1j*D]])
    ev=np.linalg.eigvals(L); return ev[ev.imag>0.02], q
def zs_conv(qfun):
    e1,q=zs_raw(qfun,384); e2,_=zs_raw(qfun,640)
    keep=[z for z in e1 if np.min(abs(e2-z))<2e-3]
    return np.array(keep), q
# sech check
for A in (1.0,2.5,3.0):
    ev,_=zs_conv(lambda t:A/np.cosh(t)); print("sech A=%.1f converged Im zeta:"%A, np.sort(ev.imag)[::-1].round(4))
# shaped Gaussians: fixed spectral amplitude of q0 = 3 exp(-t^2/2), random spectral phases
def shaped(seed):
    r=np.random.default_rng(seed); c=r.normal(0,1.5,4); amp=r.uniform(0,1)
    def f(t):
        q0=3.0*np.exp(-t**2/2); w=2*np.pi*np.fft.fftfreq(len(t),t[1]-t[0])
        phi=sum(c[j]*w**(j+2)/math.factorial(j+2) for j in range(4)) + amp*np.sin(1.7*w+seed)
        return np.fft.ifft(np.fft.fft(q0)*np.exp(1j*phi))
    return f
ratios=[];l4=[];emax=[]
for s in range(40):
    ev,q=zs_conv(shaped(s))
    m=ev.imag.max() if len(ev) else 0.0
    ratios.append(m/np.max(abs(q))); emax.append(m)
    l4.append(np.sum(abs(q)**4))
evtl,qtl=zs_conv(lambda t:3.0*np.exp(-t**2/2)+0j)
print("TL Gaussian (A=3): Im zeta_max=%.4f  ||q||inf=%.3f  ratio=%.4f"%(evtl.imag.max(),np.max(abs(qtl)),evtl.imag.max()/np.max(abs(qtl))))
print("shaped inputs: max Im zeta_max/||q||inf = %.4f ; max Im zeta_max/||q_TL||inf = %.4f ; TL Im zeta_max = %.4f"%(max(ratios),max(emax)/3.0, evtl.imag.max()))
print("shaped inputs: max int|q|^4 / TL = %.5f"%(max(l4)/np.sum(abs(qtl)**4)))
print("count shaped inputs with Im zeta_max > TL value:", sum(e>evtl.imag.max()+1e-3 for e in emax))
