"""Independent moment-overlap quadrature. gpt-c / gpt-6-astra / gpt."""
import json
from pathlib import Path
import numpy as np
from scipy.integrate import simpson,quad
from scipy.optimize import minimize_scalar
from independent import response,write_json
HERE=Path(__file__).resolve().parent
# R(T)=(pi/2) integral_0^infty x^3 [-Im H(x/T)] / sinh(pi x/2)^2 dx.
# d<Omega>/dz=-|beta2| fR R(T)/T^3 for total-gamma area relation.
# Multiplying R by fR/(1-fR) for electronic-gamma convention does not move its peak.
def overlap(T,model,scale=1.,n=8193):
    x=np.linspace(1e-7,18,n)
    H,_=response(x,T,model,scale)
    return float(np.pi/2*simpson(x**3*(-H.imag)/np.sinh(np.pi*x/2)**2,x=x))
def first_moment(model,scale=1.):
    # Independent time-domain quadrature avoids subtractive cancellation in
    # -Im H(omega)/omega at extremely small frequencies, especially for HC.
    from kernel_validation import sampled
    norm,en=quad(lambda t:float(sampled(np.asarray(t),model)),0,10000,epsabs=1e-9,epsrel=1e-11,limit=1000)
    moment,em=quad(lambda t:t*float(sampled(np.asarray(t),model)),0,10000,epsabs=1e-8,epsrel=1e-11,limit=1000)
    fr=response(np.array([0.]),1,model)[1]
    return scale*fr*moment/norm,scale*fr*(em/abs(norm)+abs(moment)*en/norm**2)

def main():
    rows=[]
    for model,scale in [('bw',1),('hc',1),('as2s3',1),('bw_damped',1),('bw',2)]:
        scan_T=np.geomspace(2*scale,500*scale,201)
        scan_R=np.array([overlap(t,model,scale,4097) for t in scan_T]);j=int(np.argmax(scan_R))
        if j in [0,len(scan_T)-1]:raise RuntimeError('Unbracketed overlap maximum for '+model)
        fit=minimize_scalar(lambda logT:-overlap(np.exp(logT),model,scale),bounds=(np.log(scan_T[j-1]),np.log(scan_T[j+1])),method='bounded',options={'xatol':1e-11})
        T=float(np.exp(fit.x));fine=minimize_scalar(lambda x:-overlap(np.exp(x),model,scale,16385),bounds=(np.log(.9*T),np.log(1.1*T)),method='bounded',options={'xatol':1e-11})
        om=np.linspace(0,.6,60001);H,fR=response(om,1,model,scale)
        tiny_frequency_estimate=-float(response(np.array([1e-7]),1,model,scale)[0].imag[0])/1e-7*fR
        tauR,moment_error=first_moment(model,scale)
        tail_T=np.array([400.,800.,1600.,3200.])*scale
        tail_err=np.array([abs(overlap(t,model,scale)-8*tauR/(15*fR*t)) for t in tail_T])
        rows.append({'long_pulse_widths_fs':tail_T.tolist(),'long_pulse_absolute_remainder':tail_err.tolist(),'long_pulse_remainder_orders':(-np.diff(np.log(tail_err))/np.diff(np.log(tail_T))).tolist(),'overlap_search_interval_fs':[float(scan_T[0]),float(scan_T[-1])],'overlap_max_bracket_fs':[float(scan_T[j-1]),float(scan_T[j+1])],'search_edge_to_peak_ratios':[float(scan_R[0]/max(scan_R)),float(scan_R[-1]/max(scan_R))],'response':model,'time_scale':scale,'overlap_max_width_fs':T,'quadrature_doubled_width_fs':float(np.exp(fine.x)),
                     'quadrature_width_difference_fs':float(np.exp(fine.x)-T),'Rmax':-float(fit.fun),'fR':fR,'first_moment_fs':tauR,'first_moment_quadrature_error_estimate_fs':moment_error,'tiny_frequency_derivative_estimate_fs':tiny_frequency_estimate,
                     'gain_peak_rad_per_fs':float(om[np.argmax(-H.imag)]),'long_pulse_R_times_T_at_1e5_fs':overlap(1e5,model,scale)*1e5,
                     'expected_long_pulse_R_times_T':8*tauR/(15*fR)})
    grid=np.geomspace(2,150,151)
    write_json(HERE/'overlap.json',{'agent':'gpt-c','model':'gpt-6-astra','family':'gpt','rows':rows,
      'curves':[{'response':m,'width_fs':grid.tolist(),'R':[overlap(T,m,n=4097) for T in grid]} for m in ['bw','hc','as2s3','bw_damped']]})
    print(json.dumps(rows,indent=2))
if __name__=='__main__':main()
