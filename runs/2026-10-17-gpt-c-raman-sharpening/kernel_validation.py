"""Time-domain kernel cross-check; gpt-c / gpt-6-astra / gpt."""
from pathlib import Path
import numpy as np
from scipy.fft import fft,fftfreq
from independent import response,write_json
HERE=Path(__file__).resolve().parent

def sampled(t,model):
    if model in ['bw','as2s3','bw_damped']:
        t1,t2=(15.5,230.5) if model=='as2s3' else (12.2,16 if model=='bw_damped' else 32)
        a,b=1/t2,1/t1
        return (a*a+b*b)/b*np.exp(-a*t)*np.sin(b*t)
    pos=np.array([56.25,100,231.25,362.5,463,497,611.5,691.67,793.67,835.5,930,1080,1215])
    amp=np.array([1,11.4,36.67,67.67,74,4.5,6.8,4.6,4.2,4.5,2.7,3.1,3])
    ga=np.array([52.1,110.42,175,162.5,135.33,24.5,41.5,155,59.5,64.3,150,91,160])
    lo=np.array([17.37,38.81,58.33,54.17,45.11,8.17,13.83,51.67,19.83,21.43,50,30.33,53.33])
    conv=np.pi*2.99792458e-5
    h=np.zeros_like(t,dtype=float)
    for p,A,g,l in zip(pos,amp,ga,lo):
        h+=A*np.exp(-conv*l*t-(conv*g*t)**2/4)*np.sin(2*conv*p*t)
    return h

def main():
    out=[]
    for model in ['bw','hc','as2s3','bw_damped']:
        for dt in [3,1.5,.75,.375]:
            t=np.arange(32768,dtype=float)*dt;w=2*np.pi*fftfreq(len(t),dt);h=sampled(t,model);H=fft(h)*dt;norm=H[0].real;H/=norm
            exact,fR=response(w,1,model);band=(abs(w)<=.3)
            moment=float(fR*np.sum(t*h)*dt/norm)
            out.append({'response':model,'dt_fs':dt,'n':len(t),'raw_integral':float(norm),'normalized_integral':float(H[0].real),
                        'max_response_difference_below_0p3_rad_fs':float(max(abs(H[band]-exact[band]))),'first_moment_fs':moment})
    write_json(HERE/'kernel_validation.json',{'agent':'gpt-c','model':'gpt-6-astra','family':'gpt','rows':out})
    for r in out:print(r)
if __name__=='__main__':main()
