"""Sequential runner. gpt-c / gpt-6-astra / gpt."""
import json, sys, time, subprocess, resource
from pathlib import Path
import numpy as np
from independent import RAW, propagate, census, write_json, D0,S0,BETA3,IMPLEMENTATION_SHA256

HERE=Path(__file__).resolve().parent
class EdgeStop(Exception):
    pass
def guard():
    while True:
        text=subprocess.check_output(['memory_pressure'],text=True)
        free=int(text.split('System-wide memory free percentage:')[1].split('%')[0])
        print('memory free',free,flush=True)
        if free>=35: return
        print('Waiting 30 seconds for memory recovery.',flush=True);time.sleep(30)

def main():
    cases=json.loads(Path(sys.argv[1]).read_text()); RAW.mkdir(parents=True,exist_ok=True)
    for case in cases:
        out=HERE/(case['id']+'.json')
        if out.exists():
            previous=json.loads(out.read_text())
            if previous.get('complete') or previous.get('terminated_for_edge') or previous.get('intentionally_interrupted') or previous.get('measurement_failed'):continue
        guard(); start=time.monotonic()
        report={'agent':'gpt-c','model':'gpt-6-astra','family':'gpt','case':case,'checkpoints':[],
                'implementation_sha256':IMPLEMENTATION_SHA256,
                'physical_dispersion':{'D1550_ps_nm_km':D0,'S0_ps_nm2_km':S0,'beta3_ps3_km':BETA3/1e6},'complete':False}
        def callback(t,q,stats):
            stats['process_peak_rss_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            np.savez(RAW/(case['id']+'_zN'+str(stats['zN'])+'.npz'),t=t,q=q)
            measured=census(t,q,case)
            report['checkpoints'].append(dict(stats,**measured)); write_json(out,report)
            lead=measured['leading']
            print(case['id'],stats['zN'],'f',None if lead is None else round(lead['f_zs'],8),
                  'nm',None if lead is None or lead['lambda_nm'] is None else round(lead['lambda_nm'],2),
                  'drift',stats['mass_drift'],'steps',stats['steps'],'sec',round(time.monotonic()-start,1),flush=True)
            if case.get('stop_on_edge',case['N']>=10) and max(stats['max_spectral_edge_fraction'],stats['max_time_edge_fraction'])>1e-6:
                raise EdgeStop('Recorded checkpoint exceeds the preregistered edge-occupancy acceptance threshold; later propagation is not used.')
        try:
            propagate(case,callback)
            report['complete']=True
        except EdgeStop as e:
            report['terminated_for_edge']=True;report['stop_reason']=str(e)
        report['wall_seconds']=time.monotonic()-start
        report['process_peak_rss_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        write_json(out,report)

if __name__=='__main__': main()
