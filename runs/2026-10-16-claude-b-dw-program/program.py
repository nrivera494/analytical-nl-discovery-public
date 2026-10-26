"""H1: the conservation-law program of card sketch 1, made two-sided, on a window |w| <= W; plus the explicit
three-point construction showing vacuity on the whole line; plus the normal-dispersion reduction (Cantelli).

Per-photon units (normalized output spectrum p(w) >= 0, sum p = 1). Model M0 invariants for a launch u0:
  Nn = int|u|^2,  wbar = <w>,  h = H/Nn = <K> - (N^2/(2 Nn)) int|u|^4,  K(w) = -D(w) = w^2/2 - d3 w^3.
Valid constraints on any reachable output (Kerr energy >= 0 and sharp 1-D Gagliardo-Nirenberg, C = 1/sqrt(3),
applied to u exp(i wbar tau)):   h <= <K> <= h + a*sigma,  a = N^2 Nn / (2 sqrt 3),  sigma^2 = <(w - wbar)^2>.
Program: maximise P(w >= wz) subject to the above, <1> = 1, <w> = wbar; solved as linear programs at fixed
variance v (constraint <w^2> = v + wbar^2) and maximised over v.
"""
import numpy as np, json
from scipy.optimize import linprog

C_GN = 1/np.sqrt(3)

def launch_invariants(kind, N, d3):
    if kind == 'gauss':
        Nn = np.sqrt(np.pi); K2 = 0.5*np.sqrt(np.pi)/2; U4 = np.sqrt(np.pi/2)   # int w^2 n /2 ; int|u|^4
        wbar = 0.0
    elif kind == 'sech':
        Nn = 2.0; K2 = 0.5*(2/3); U4 = 4/3; wbar = 0.0
    h = (K2 - 0.5*N*N*U4)/Nn         # <w^3> = 0 for these symmetric spectra
    a = N*N*Nn/(2*np.sqrt(3))
    return dict(Nn=Nn, h=h, a=a, wbar=wbar)

def gn_check():
    """Numerical check of the sharp constant on sech (equality) and random profiles (strict)."""
    t = np.linspace(-40, 40, 2**15); dt = t[1]-t[0]
    w = 2*np.pi*np.fft.fftfreq(len(t), dt)
    def ratio(u):
        uh = np.fft.fft(u)
        d2 = (w**2*np.abs(uh)**2).sum()/ (np.abs(uh)**2).sum() * (np.abs(u)**2).sum()*dt   # int|u_t|^2
        return (np.abs(u)**4).sum()*dt / (((np.abs(u)**2).sum()*dt)**1.5*np.sqrt(d2))
    rng = np.random.default_rng(0)
    out = dict(sech=ratio(1/np.cosh(t)+0j), gauss=ratio(np.exp(-t**2/2)+0j), sech_chirped=ratio((1/np.cosh(t))*np.exp(1j*0.7*t**2)))
    rr = []
    for k in range(200):
        c = rng.standard_normal(6)
        u = np.exp(-t**2/2*(0.5+rng.random()))*(1+c[0]*t+c[1]*t**2/2)*np.exp(1j*(c[2]*t+c[3]*t**2)) + c[4]*np.exp(-(t-3*c[5])**2)
        rr.append(ratio(u))
    out['random_max'] = max(rr); out['C'] = C_GN
    return out

def windowed_value(inv, d3, W, M=1601, nv=80, wz=None):
    wz = 1/(6*d3) if wz is None else wz
    w = np.linspace(-W, W, M)
    w = np.unique(np.concatenate([w, [wz]]))
    K = 0.5*w**2 - d3*w**3
    inB = (w >= wz).astype(float)
    best = (0.0, None, None)
    vmax = (W**2)
    vs = np.geomspace(0.3, vmax, nv)
    res = []
    for v in vs:
        sig = np.sqrt(v)
        A_eq = np.vstack([np.ones_like(w), w, w**2])
        b_eq = np.array([1.0, inv['wbar'], v + inv['wbar']**2])
        A_ub = np.vstack([K, -K]); b_ub = np.array([inv['h'] + inv['a']*sig, -inv['h']])
        r = linprog(-inB, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=(0, None), method='highs')
        val = -r.fun if r.status == 0 else np.nan
        res.append(val)
        if r.status == 0 and val > best[0]:
            best = (val, v, w[r.x > 1e-9].tolist())
    return best, list(zip(vs.tolist(), res))

def three_point(inv, d3, r=0.01, m=1.0, w1=None):
    """Explicit vacuity construction on the whole line: band mass at w1, recoil mass r at -wr, far-blue mass eps at
    winf (also in the band), with <K> = h exactly (bisection on winf). Returns the band fraction 1 - r and checks."""
    wz = 1/(6*d3)
    w1 = 1/(2*d3) if w1 is None else w1
    K = lambda w: 0.5*w**2 - d3*w**3
    def build(winf):
        eps = m/winf
        eta = 1 - r - eps
        wr = (eta*w1 + m)/r          # momentum balance: eta w1 + eps winf - r wr = 0
        pts = np.array([w1, -wr, winf]); ps = np.array([eta, r, eps])
        return pts, ps
    def Kmean(winf):
        pts, ps = build(winf); return (ps*K(pts)).sum()
    lo, hi = max(w1, m/(1-r)*1.0001, wz), 1e12
    if Kmean(lo) < inv['h']:
        return None
    for _ in range(300):
        mid = np.sqrt(lo*hi)
        if Kmean(mid) > inv['h']: lo = mid
        else: hi = mid
    pts, ps = build(lo)
    mean = (ps*pts).sum(); var = (ps*(pts-mean)**2).sum()
    return dict(points=pts.tolist(), masses=ps.tolist(), band_fraction=float(ps[pts >= wz].sum()),
                Kmean=float((ps*K(pts)).sum()), h=inv['h'], upper=inv['h']+inv['a']*np.sqrt(var), mean=float(mean))

def cantelli(h_abs, wB, wbar=0.0):
    s2 = 2*h_abs - wbar**2
    return s2/(s2 + (wB - wbar)**2)

def nd_value(h_abs, wB, W, M=4001):
    """Normal dispersion, pure beta2: K = -w^2/2, constraints <K> >= h (i.e. <w^2> <= 2|h|), <w> = 0, upper GN side irrelevant."""
    w = np.linspace(-W, W, M); w = np.unique(np.concatenate([w, [wB]]))
    K = -0.5*w**2
    r = linprog(-(w >= wB).astype(float), A_ub=np.vstack([-K]), b_ub=np.array([h_abs]),
                A_eq=np.vstack([np.ones_like(w), w]), b_eq=np.array([1.0, 0.0]), bounds=(0, None), method='highs')
    return -r.fun

if __name__ == '__main__':
    out = dict(gn=gn_check())
    print('GN check', out['gn'])
    Ns = [3, 4, 6, 8, 10]; d3s = [0.01, 0.02, 0.03, 0.05]
    out['windowed'] = []; out['three_point'] = []
    for N in Ns:
        for d3 in d3s:
            inv = launch_invariants('gauss', N, d3)
            wdw = 1/(2*d3)
            tp = three_point(inv, d3, r=0.01)
            out['three_point'].append(dict(N=N, d3=d3, **(tp or {})))
            row = dict(N=N, d3=d3, h=inv['h'], a=inv['a'], wz=1/(6*d3), wDW=wdw, leak0=0.5*float(__import__('math').erfc(1/(6*d3))))
            for lab, W in [('1.2wDW', 1.2*wdw), ('1.5wDW', 1.5*wdw), ('2wDW', 2*wdw), ('3wDW', 3*wdw)]:
                (val, v, supp), _ = windowed_value(inv, d3, W)
                row[lab] = val; row[lab+'_support'] = supp
            out['windowed'].append(row)
            print(N, d3, 'h', round(inv['h'], 3), 'three-point band frac', tp and round(tp['band_fraction'], 4),
                  'windowed', {k: round(row[k], 4) for k in ['1.2wDW', '1.5wDW', '2wDW', '3wDW']}, flush=True)
    # normal dispersion reduction: Gaussian, K=-w^2/2, invariant h = -(1/4) - N^2/(2 sqrt 2) per photon
    out['normal'] = []
    for N in [2, 5, 10]:
        habs = 0.25 + N*N/(2*np.sqrt(2))
        for wB in [3.0, 5.0, 10.0]:
            lp = nd_value(habs, wB, W=60.0)
            out['normal'].append(dict(N=N, wB=wB, h_abs=habs, lp=lp, cantelli=cantelli(habs, wB), markov=2*habs/wB**2))
            print('normal', N, wB, 'LP', round(lp, 5), 'Cantelli', round(cantelli(habs, wB), 5), 'Markov', round(2*habs/wB**2, 5))
    json.dump(out, open('summary_program.json', 'w'), indent=1, default=float)
