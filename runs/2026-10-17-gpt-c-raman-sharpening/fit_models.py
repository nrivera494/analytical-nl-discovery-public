"""Finite-range regression, no asymptotic inference. gpt-c / gpt-6-astra / gpt."""
import json
from pathlib import Path
import numpy as np
from scipy.stats import t as student
from independent import write_json
HERE=Path(__file__).resolve().parent
IDENT={'agent':'gpt-c','model':'gpt-6-astra','family':'gpt'}

def fit_power(N,T):
    x=np.log(N);v=np.log(T/12.2);X=np.column_stack([np.ones(len(N)),x]);b=np.linalg.lstsq(X,v,rcond=None)[0];r=v-X@b
    df=len(N)-2;cov=np.linalg.inv(X.T@X)*(r@r/max(1,df));se=np.sqrt(np.diag(cov));ci=student.ppf(.975,max(1,df))*se
    return {'prefactor_tau1':float(np.exp(b[0])),'exponent':float(b[1]),'exponent_OLS_SE':float(se[1]),
            'exponent_OLS_95_interval':[float(b[1]-ci[1]),float(b[1]+ci[1])],
            'max_relative_residual':float(np.max(abs(np.exp(r)-1))),'N':list(map(float,N)),
            'uncertainty_note':'Descriptive regression residual interval, not experimental confidence or asymptotic error.'}

def main():
    freeze=json.loads((HERE/'freeze.json').read_text())
    if freeze.get('holdout_fit_commit') and (HERE/'training_fit.json').exists():
        raise RuntimeError('Training coefficients are frozen. Do not refit after holdout production.')
    s=json.loads((HERE/'summary.json').read_text());peaks=s['preferred_peaks']
    bw=sorted([p for p in peaks if p['response']=='bw' and p['shape']=='sech' and p['split']=='calibration' and p['dispersion']=='constant'],key=lambda p:p['N'])
    N=np.array([p['N'] for p in bw]);T=np.array([p['T0_fs'] for p in bw]);a=np.array([p['scaled_share'] for p in bw])
    if len(N)<4:raise RuntimeError('Need at least four complete calibration peaks')
    result=dict(IDENT,run_id=HERE.name,training_cases=[p['cases'] for p in bw],power_position=fit_power(N,T))
    rng=np.random.default_rng(20261017)
    draws=np.array([rng.uniform(*p['T_bracket_fs'],size=10000) for p in bw]);x=np.log(N); xc=x-x.mean()
    pp=np.sum(xc[:,None]*np.log(draws),axis=0)/np.sum(xc*xc)
    if not np.all(np.isfinite(pp)):raise RuntimeError("Nonfinite bracket sensitivity draw")
    result['power_position']['peak_bracket_sensitivity_95']=np.quantile(pp,[.025,.975]).tolist()
    result['power_position']['peak_bracket_full_corner_sensitivity']=[float(sum(xc[i]*np.log(p['T_bracket_fs'][0 if xc[i]>=0 else 1]) for i,p in enumerate(bw))/(xc@xc)),float(sum(xc[i]*np.log(p['T_bracket_fs'][1 if xc[i]>=0 else 0]) for i,p in enumerate(bw))/(xc@xc))]
    result['power_position']['y_exponent']=2-result['power_position']['exponent']
    y=N*N*12.2/T
    result['constant_y_test']={'best_geometric_constant':float(np.exp(np.mean(np.log(y)))),
        'range': [float(min(y)),float(max(y))],
        'max_relative_residual':float(max(abs(y/np.exp(np.mean(np.log(y)))-1))),
        'interpretation':'Finite-range constant test only; cannot determine N to infinity.'}
    # Refit each acceptable output checkpoint without changing the calibration split.
    alternatives=[]
    for mode in ['earliest','latest']:
        chosen=[]
        for pp in bw:
            options=[q for q in s['peak_fits'] if q.get('bracketed') and q['response']=='bw' and q['shape']=='sech'
                     and q['N']==pp['N'] and q['split']=='calibration' and q['dispersion']=='constant'
                     and q.get('plateau_complete',False) and q['max_plateau_relative_change']<=.005]
            chosen.append((min if mode=='earliest' else max)(options,key=lambda q:q['zN']))
        alternatives.append(dict(checkpoint_choice=mode,**fit_power(N,np.array([q['T0_fs'] for q in chosen]))))
    result['output_checkpoint_position_sensitivity']=alternatives
    result['subrange_position_fits']=[dict(interval=[lo,hi],**fit_power(N[(N>=lo)&(N<=hi)],T[(N>=lo)&(N<=hi)])) for lo,hi in [(3,8),(6,16),(8,16)] if np.sum((N>=lo)&(N<=hi))>=3]
    # Frozen functional form: a(N)=a0+a1 log(N/6)+a2 log(N/6)^2.
    # Three coefficients provide a descriptive finite-range curve, not an asymptotic law.
    x=np.log(N/6);coef=np.polynomial.polynomial.polyfit(x,a,2);pred=np.polynomial.polynomial.polyval(x,coef)
    result['scaled_share_log_quadratic']={'coefficients':coef.tolist(),'variable':'log(N/6)','domain_N':[3,16],
        'max_abs_training_residual':float(max(abs(a-pred))),'heldout_absolute_tolerance':.006,
        'constant_best':float(a.mean()),'constant_max_residual':float(max(abs(a-a.mean()))),'not_asymptotic':True}
    X=np.column_stack([np.ones(len(N)),1/N,np.log(N)])
    c=np.linalg.lstsq(X,a,rcond=None)[0];ap=X@c
    result['scaled_share_inverse_log']={'coefficients':c.tolist(),'basis':['1','1/N','log(N)'],'domain_N':[3,16],
        'max_abs_training_residual':float(max(abs(a-ap))),'heldout_absolute_tolerance':.006,'not_asymptotic':True}
    # Both forms are calibration models. Choose the smaller training max error
    # before the holdout run; holdouts never participate in model selection.
    result['selected_share_model']='scaled_share_inverse_log' if max(abs(a-ap))<max(abs(a-pred)) else 'scaled_share_log_quadratic'
    result['existing_laws']={'share_1p29_relative_errors':(a/1.29-1).tolist(),'T_21N162_relative_errors':(T/(21*N**1.62)-1).tolist(),
        'N':N.tolist(),'scaled_share':a.tolist(),'T0_fs':T.tolist()}
    result['holdout_predictions']=[]
    A=result['power_position']['prefactor_tau1'];p=result['power_position']['exponent']
    for n in [9,11,13,15]:
        result['holdout_predictions'].append({'N':n,'scaled_share':float(np.array([1,1/n,np.log(n)])@c) if result['selected_share_model']=='scaled_share_inverse_log' else float(np.polynomial.polynomial.polyval(np.log(n/6),coef)),
            'scaled_share_absolute_tolerance':.006,'T0_fs':float(12.2*A*n**p),'T0_relative_tolerance':.05})
    write_json(HERE/'training_fit.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ['training_cases']},indent=2))
if __name__=='__main__':main()
