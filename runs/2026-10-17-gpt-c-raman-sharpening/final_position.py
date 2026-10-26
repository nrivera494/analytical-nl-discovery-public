"""Descriptive final peak-position analysis; never refits frozen predictions.
Agent gpt-c / model gpt-6-astra / family gpt.
"""
import json
from pathlib import Path
import numpy as np
from fit_models import fit_power,student
from independent import write_json
HERE=Path(__file__).resolve().parent

def describe(peaks,tau=12.2):
    ps=sorted(peaks,key=lambda p:p['N']);N=np.array([p['N'] for p in ps]);T=np.array([p['T0_fs'] for p in ps])
    out=fit_power(N,T*12.2/tau);x=np.log(N);xc=x-x.mean();den=np.sum(xc*xc)
    out['reference_time_fs']=tau
    X=np.column_stack([np.ones(len(N)),x]);b=np.linalg.lstsq(X,np.log(T/tau),rcond=None)[0]
    residual=np.log(T/tau)-X@b;df=len(N)-2
    cov=np.linalg.inv(X.T@X)*(residual@residual/max(1,df));ci=student.ppf(.975,max(1,df))*np.sqrt(cov[0,0])
    out['prefactor_OLS_95_interval']=[float(np.exp(b[0]-ci)),float(np.exp(b[0]+ci))]
    out['covariance_logprefactor_exponent']=cov.tolist()
    out['peak_bracket_full_corner_sensitivity']=[float(sum(xc[i]*np.log(p['T_bracket_fs'][0 if xc[i]>=0 else 1]) for i,p in enumerate(ps))/den),float(sum(xc[i]*np.log(p['T_bracket_fs'][1 if xc[i]>=0 else 0]) for i,p in enumerate(ps))/den)]
    rng=np.random.default_rng(20261017);draw=np.array([rng.uniform(*p['T_bracket_fs'],size=10000) for p in ps])
    slope=np.sum(xc[:,None]*np.log(draw),axis=0)/den
    out['uniform_bracket_sensitivity_95']=np.quantile(slope,[.025,.975]).tolist()
    intercept=np.mean(np.log(draw/tau),axis=0)-x.mean()*slope
    out['prefactor_uniform_bracket_sensitivity_95']=np.quantile(np.exp(intercept),[.025,.975]).tolist()
    weights=1/len(N)-x.mean()*xc/den
    out['prefactor_full_corner_sensitivity']=[float(np.exp(sum(weights[i]*np.log(p['T_bracket_fs'][0 if weights[i]>=0 else 1]/tau) for i,p in enumerate(ps)))),
        float(np.exp(sum(weights[i]*np.log(p['T_bracket_fs'][1 if weights[i]>=0 else 0]/tau) for i,p in enumerate(ps))))]
    out['T0_fs']=T.tolist();out['T_brackets_fs']=[p['T_bracket_fs'] for p in ps]
    out['original_position_law_max_relative_error']=float(max(abs(T/(21*tau/12.2*N**1.62)-1)))
    out['y_star']=(N*N*tau/T).tolist()
    out['y_prefactor']=1/out['prefactor_tau1'];out['y_exponent']=2-out['exponent']
    out['y_exponent_OLS_95_interval']=[2-out['exponent_OLS_95_interval'][1],2-out['exponent_OLS_95_interval'][0]]
    ylo=max(p['N']**2*tau/p['T_bracket_fs'][1] for p in ps)
    yhi=min(p['N']**2*tau/p['T_bracket_fs'][0] for p in ps)
    out['common_constant_y_allowed_by_all_brackets']=ylo<=yhi
    out['intersection_y_bracket_endpoints']=[float(ylo),float(yhi)]
    out['coordinate_note']='y is an empirical scaled inverse duration, not a measured compressed bandwidth.'
    return out

def main():
    s=json.loads((HERE/'summary.json').read_text());bw=[p for p in s['preferred_peaks'] if p['response']=='bw' and p['shape']=='sech' and p['dispersion']=='constant']
    out=dict(agent='gpt-c',model='gpt-6-astra',family='gpt',run_id=HERE.name,
             note='Post-test descriptive fits. training_fit.json alone supplies the frozen heldout predictions.',
             calibration=describe([p for p in bw if p['split']=='calibration']),all_N=describe(bw),subranges=[])
    for lo,hi in [(3,8),(6,16),(8,16)]:
        ps=[p for p in bw if lo<=p['N']<=hi]
        if len(ps)>=3:out['subranges'].append(dict(interval=[lo,hi],**describe(ps)))
    out['response_shape_descriptive_fits']=[]
    for response,shape in [('bw','sech'),('hc','sech'),('as2s3','sech'),('bw','gaussian')]:
        ps=[p for p in s['preferred_peaks'] if p['response']==response and p['shape']==shape and p['dispersion']=='constant' and p['split']!='matched_shape']
        if len(ps)>=3:
            out['response_shape_descriptive_fits'].append(dict(response=response,shape=shape,**describe(ps,15.5 if response=='as2s3' else 12.2)))
    out['output_checkpoint_sensitivity']=[]
    for mode in ['earliest','latest']:
        selected=[]
        for peak in bw:
            options=[q for q in s['peak_fits'] if q.get('bracketed') and q['response']=='bw' and q['shape']=='sech'
                     and q['N']==peak['N'] and q['dispersion']=='constant' and q.get('plateau_complete')
                     and q['max_plateau_relative_change']<=.005]
            selected.append((min if mode=='earliest' else max)(options,key=lambda q:q['zN']))
        out['output_checkpoint_sensitivity'].append(dict(checkpoint_choice=mode,**describe(selected)))
    write_json(HERE/'final_position.json',out)
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
