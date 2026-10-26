"""Response quadrature, dispersion units and Gordon sign checks. gpt-c/gpt-6-astra/gpt."""
import numpy as np
from pathlib import Path
from scipy.fft import fft,fftfreq
from independent import response,propagate,write_json,K,W0,measured_D,measured_beta2,measured_residual,carrier_beta2,BETA2,BETA3,S0

out={'agent':'gpt-c','model':'gpt-6-astra','family':'gpt','raman_quadrature':[],'gordon':[]}
v=np.array([0.,.001,.02,.05,.08,.15,.23])
t=np.arange(0,5000.0001,.25)
pos=np.array([56.25,100,231.25,362.5,463,497,611.5,691.67,793.67,835.5,930,1080,1215])
amp=np.array([1,11.4,36.67,67.67,74,4.5,6.8,4.6,4.2,4.5,2.7,3.1,3])
ga=np.array([52.1,110.42,175,162.5,135.33,24.5,41.5,155,59.5,64.3,150,91,160])
lo=np.array([17.37,38.81,58.33,54.17,45.11,8.17,13.83,51.67,19.83,21.43,50,30.33,53.33])
conv=np.pi*2.99792458e-5
for model in ['bw','hc','la']:
    ha=(12.2**2+32**2)/(12.2*32**2)*np.exp(-t/32)*np.sin(t/12.2)
    if model=='bw': h=ha
    elif model=='la': h=.79*ha+.21*(192-t)/96**2*np.exp(-t/96)
    else:
        h=sum(a*np.exp(-conv*l*t-(conv*g*t)**2/4)*np.sin(2*conv*p*t) for p,a,g,l in zip(pos,amp,ga,lo))
    h=h/np.trapezoid(h,t)
    numeric=np.array([np.trapezoid(h*np.exp(-1j*w*t),t) for w in v])
    exact,f=response(v,1,model)
    out['raman_quadrature'].append({'model':model,'max_absolute_error':float(max(abs(numeric-exact))),
         'TR_quad_fs':float(f*np.trapezoid(t*h,t)),'dt_fs':.25,'duration_fs':5000})
for T in [400,800,1600]:
    rows=[]
    def cb(t,q,s):
        dt=t[1]-t[0];w=2*np.pi*fftfreq(len(t),dt);spec=abs(fft(q))**2
        rows.append({'z':s['z_LD'],'centroid_red_w':float(sum(w*spec)/sum(spec)),**s})
    propagate({'N':1,'T0_fs':T,'raman':'bw','n':4096,'width':64,'zN':[.5,1,2],'tol':1e-10},cb)
    measured=(rows[-1]['centroid_red_w']-rows[0]['centroid_red_w'])/(rows[-1]['z']-rows[0]['z'])
    TR=.18*2*(1/32)/((1/32)**2+(1/12.2)**2)
    predicted=8/15*TR/T
    out['gordon'].append({'T0_fs':T,'predicted_red_slope':predicted,'measured_red_slope':measured,'relative_error':measured/predicted-1,'checkpoints':rows})
eps=1e-4
out['dispersion']={'card_beta2_ps2_km':-BETA2/1000,'telecom_beta3_ps3_km':BETA3/1e6,'telecom_S0_ps_nm2_km':S0,
 'measured_beta2_ps2_km':float(measured_beta2(W0)/1000),'measured_beta3_ps3_km':float((measured_beta2(W0+eps)-measured_beta2(W0-eps))/(2*eps)/1e6),
 'numerical_integral_second_derivative_relative_error':float((measured_residual(W0+eps)+measured_residual(W0-eps))/eps**2/measured_beta2(W0)-1),
 'comparison':[{'lambda_nm':l,'D_measured_ps_nm_km':float(measured_D(l)),'beta2_measured_ps2_km':float(measured_beta2(K/l)/1000)} for l in [1200,1310,1550,1700,2000,2300]]}
write_json(Path(__file__).with_name('physics_calibration.json'),out)
print(out)
