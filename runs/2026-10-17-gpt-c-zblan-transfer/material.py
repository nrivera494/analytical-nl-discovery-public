"""Published measured ZBLAN response. gpt-c / gpt-6-astra / gpt.

Yan et al. DOI 10.1364/JOSAB.29.000238, Table 1, intermediate
broadening convention of Hollenbeck-Cantrell DOI 10.1364/JOSAB.19.002886.
No single-oscillator stand-in. Units: fs and radians/fs.
"""
import numpy as np
from scipy.special import erfcx

TABLE=np.array([
 [54.43,8.48,58.67,23.46], [102.91,17.12,82.40,32.96],
 [169.95,51.78,115.27,46.11], [275.91,155.69,160.76,64.30],
 [377.35,62.12,137.90,55.16], [504.77,107.05,184.62,73.85],
 [576.43,27.69,38.50,15.40], [648.44,17.83,135.84,54.34]])
C=np.pi*2.99792458e-5

def unnormalized(v):
    v=np.asarray(v); ans=np.zeros_like(v,dtype=complex)
    for p,A,g,l in TABLE:
        om,G,gam=2*C*p,C*g,C*l
        def integral(f):return np.sqrt(np.pi)/G*erfcx((gam+1j*f)/G)
        ans+=A*(integral(v-om)-integral(v+om))/(2j)
    return ans

NORM=float(unnormalized(np.asarray(0.)).real)

def response(v):return unnormalized(v)/NORM

def time_response(t):
    t=np.asarray(t); y=np.zeros_like(t,dtype=float)
    for p,A,g,l in TABLE:
        y+=A*np.exp(-C*l*t-(C*g*t)**2/4)*np.sin(2*C*p*t)
    return np.where(t>=0,y/NORM,0.)
