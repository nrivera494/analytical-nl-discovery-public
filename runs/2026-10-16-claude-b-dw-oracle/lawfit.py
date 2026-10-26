"""Fit ln eta_DW = c + p ln d3 - d/d3 (3 parameters) to the k smallest-d3 points; local slopes; error exponent."""
import numpy as np, json, sys

def load(files, key='h2'):
    pts = {}
    for f in files:
        for r in json.load(open(f)):
            pts[r['d3']] = (r[key]['eta_DW'], r['conv_eta_DW'], r[key].get('eta_DW_tg_plus5'))
    d3 = np.array(sorted(pts)); eta = np.array([pts[x][0] for x in d3])
    conv = np.array([pts[x][1] for x in d3]); g5 = np.array([pts[x][2] for x in d3])
    return d3, eta, conv, g5

def fit3(d3, eta, k=4):
    x = d3[:k]; y = np.log(eta[:k])
    X = np.vstack([np.ones_like(x), np.log(x), -1/x]).T
    c, *_ = np.linalg.lstsq(X, y, rcond=None)
    return dict(c=c[0], p=c[1], d=c[2])

def local_slopes(d3, eta):
    s = -np.diff(np.log(eta))/np.diff(1/d3)
    mid = 0.5*(d3[1:] + d3[:-1])
    return mid, s

if __name__ == '__main__':
    files = sys.argv[2:]; dstar = float(sys.argv[1])
    d3, eta, conv, g5 = load(files)
    mid, s = local_slopes(d3, eta)
    out = dict(d3=d3.tolist(), eta_DW=eta.tolist(), conv=conv.tolist(), gate_ratio=(g5/eta).tolist(),
               slope_mid=mid.tolist(), slope=s.tolist(), dstar=dstar)
    for k in (3, 4, 5, 6):
        out[f'fit{k}'] = fit3(d3, eta, k)
    err = np.abs(s - dstar)
    m = mid < 0.016
    if m.sum() >= 2:
        q = np.polyfit(np.log(mid[m]), np.log(err[m]), 1)
        out['slope_error_exponent'] = q[0]
    print(json.dumps({k: v for k, v in out.items() if k.startswith('fit') or k == 'slope_error_exponent'}, default=float))
    for a, b in zip(mid, s): print(f'  mid {a:.4f} slope {b:.4f} rel.dev {(b-dstar)/dstar:+.3f}')
    print('gate ratio (tg+5)/tg:', np.round(g5/eta, 4))
    json.dump(out, open(sys.argv[2].replace('.json', '_lawfit.json'), 'w'), indent=1, default=float)
