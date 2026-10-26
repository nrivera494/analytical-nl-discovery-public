"""d_*(C) = min over xi <= xi_f of the strip width of the delta3 = 0 evolution of the chirped Gaussian launch
fft(u0) = exp(i C w^2/2) fft(exp(-tau^2/2)) (same mask convention as the GDD scan of optimize.py)."""
import numpy as np, json, sys
from dw_lib import *
from singularity import strip_width
N, xif = float(sys.argv[1]), float(sys.argv[2])
Cs = [float(c) for c in sys.argv[3].split(',')]
Nt, TW = 16384, 64.0
h = min(2.5e-4, 0.0025/N**2)
out = []
for C in Cs:
    p = Prop(Nt, TW, N, 0.0, xif, h, 4)
    ul = np.exp(-p.tau**2/2) + 0j
    u0 = ifft(np.exp(1j*C*p.w**2/2)*fft(ul))
    xs = list(np.round(np.arange(0.02, xif + 1e-9, 0.005), 6))
    xs = [round(round(x/p.h)*p.h, 10) for x in xs]
    _, _, sn = p.run(u0, record=xs)
    d = [(x, strip_width(sn[x], p.w)[0]) for x in xs]
    good = [(x, v) for x, v in d if np.isfinite(v)]
    i = int(np.argmin([v for _, v in good]))
    if 0 < i < len(good) - 1:
        (x1, y1), (x2, y2), (x3, y3) = good[i-1], good[i], good[i+1]
        M = np.array([[x1**2, x1, 1], [x2**2, x2, 1], [x3**2, x3, 1]]); a, b, c = np.linalg.solve(M, [y1, y2, y3])
        xv, dv = -b/(2*a), c - b*b/(4*a)
    else:
        xv, dv = good[i]
    print(N, C, 'xi*', round(xv, 4), 'd*', round(dv, 5), flush=True)
    out.append(dict(C=C, xi_star=xv, d_star=dv))
    json.dump(dict(N=N, xif=xif, Nt=Nt, TW=TW, h=h, res=out), open(f'dstar_chirp_N{int(N)}_{sys.argv[4]}.json', 'w'), indent=1, default=float)
