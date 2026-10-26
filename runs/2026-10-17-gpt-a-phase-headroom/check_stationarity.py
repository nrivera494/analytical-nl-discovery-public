#!/usr/bin/env python3
# agent: gpt-a; model: gpt-6-astra; family: gpt
"""Remeasure the gradient of the actual frozen coefficients at two resolutions."""
from adjoint import *

if __name__=='__main__':
    selection=json.loads((HERE/'selected_masks.json').read_text());rows=[]
    for key,item in selection['masks'].items():
        c=coefficients(str(HERE/item['coefficient_file']))
        np.savetxt(RAW/f'selected_N{key}_julia_coef.csv',c,delimiter=',')
        version=item['coefficient_sha256'][:12]
        np.savetxt(RAW/f'selected_N{key}_{version}_coef.csv',c,delimiter=',')
        for nt,width,hfac,zr in [(8192,80.,1.,4),(32768,160.,.5,4)]:
            pressure=subprocess.check_output(['memory_pressure'],text=True)
            if int(pressure.split('free percentage:')[1].split('%')[0])<35:raise RuntimeError('Memory launch deferred')
            engine=DiscreteAdjoint(item['N'],item['T0_fs'],nt=nt,width=width,hfac=hfac,zs_refine=zr)
            f,g,d,u=engine.evaluate(c)
            np.savez_compressed(RAW/f'stationarity_N{key}_nt{nt}_field.npz',t=engine.t,u=u,c=c)
            np.savez_compressed(RAW/f'stationarity_N{key}_{version}_nt{nt}_field.npz',t=engine.t,u=u,c=c)
            record=dict(agent='gpt-a',model='gpt-6-astra',family='gpt',N=item['N'],T0_fs=item['T0_fs'],
                        coefficient_file=item['coefficient_file'],coefficient_sha256=item['coefficient_sha256'],nt=nt,width=engine.width,h=engine.h,zs_refine=zr,
                        f_zs=f,gradient_norm=float(np.linalg.norm(g)),gradient_max=float(np.max(abs(g))),
                        gradient=g.tolist(),diagnostics=d,stationary_at_1e_5=bool(np.linalg.norm(g)<=1e-5))
            if nt==32768:
                v=np.random.default_rng(2026101705).normal(size=len(c));v/=np.linalg.norm(v);eps=1e-5
                fd=(engine.evaluate(c+eps*v,False)[0]-engine.evaluate(c-eps*v,False)[0])/(2*eps)
                pred=float(g@v);error=abs(fd-pred);tolerance=1e-9+1e-4*max(abs(fd),abs(pred))
                record['directional_check']=dict(seed=2026101705,epsilon=eps,finite_difference=fd,adjoint=pred,
                                                  absolute_error=error,tolerance=tolerance,passed=bool(error<=tolerance))
            (RAW/f'stationarity_N{key}_{version}_nt{nt}.json').write_text(json.dumps(record,indent=2)+'\n')
            rows.append(record)
            (HERE/'stationarity.json').write_text(json.dumps(dict(agent='gpt-a',model='gpt-6-astra',family='gpt',run_id=HERE.name,checks=rows),indent=2)+'\n')
            print('STATIONARITY',item['N'],nt,f,record['gradient_norm'],flush=True)
