"""Serial, resumable runner. gpt-c / gpt-6-astra / gpt."""
import json,sys,time,subprocess,resource,traceback,hashlib,os
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
from independent import RAW,propagate,census,write_json,IMPLEMENTATION_SHA256
HERE=Path(__file__).resolve().parent
class EdgeStop(Exception):pass

def guard():
    while True:
        r=subprocess.run("memory_pressure | grep 'free percentage'",shell=True,capture_output=True,text=True)
        free=int(r.stdout.split(':')[-1].strip().rstrip('%'))
        print(r.stdout.strip(),flush=True)
        if free>=35:return free
        print('Memory below 35%; waiting 30 seconds.',flush=True);time.sleep(30)

def main():
    print('Serial runner PID:',os.getpid(),flush=True)
    cases=json.loads(Path(sys.argv[1]).read_text());RAW.mkdir(parents=True,exist_ok=True)
    freeze=json.loads((HERE/'freeze.json').read_text())
    for case in cases:
        progress=json.loads((HERE/'session_progress.json').read_text())
        deadline=datetime.fromisoformat(progress['production_stop_utc'].replace('Z','+00:00'))
        if datetime.now(timezone.utc)>=deadline:
            print('Production deadline reached; remaining cases retained as unrun.',flush=True)
            return
        out=HERE/(case['id']+'.json')
        if out.exists():
            x=json.loads(out.read_text())
            if x.get('complete') or x.get('terminated_for_edge') or x.get('error'):continue
        free=guard();start=time.monotonic()
        report={'agent':'gpt-c','model':'gpt-6-astra','family':'gpt','case':case,'checkpoints':[],
                'implementation_sha256':IMPLEMENTATION_SHA256,'predictions_commit':freeze['predictions_commit'],
                'design_commits':{k:v for k,v in freeze.items() if k.endswith('commit')},
                'material_sha256':hashlib.sha256((HERE/'material.py').read_bytes()).hexdigest(),
                'holdout_fit_commit':freeze.get('holdout_fit_commit'),
                'physical_resolution_prediction_commit':freeze.get('physical_resolution_prediction_commit'),
                'free_percentage_at_start':free,'complete':False}
        def callback(t,q,stats):
            stats['process_peak_rss_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            np.savez(RAW/(case['id']+'_zN'+str(stats['zN'])+'.npz'),t=t,q=q)
            stats.update(census(t,q,case))
            report['checkpoints'].append(stats);write_json(out,report)
            lead=stats['leading']
            print(case['id'],'zN',stats['zN'],'f',round(lead['f_zs'],7) if lead else None,
                  'time_edge',f"{stats['max_time_edge_fraction']:.1e}",'freq_edge',f"{stats['max_spectral_edge_fraction']:.1e}",
                  's',round(time.monotonic()-start,1),flush=True)
            if max(stats[k] for k in ['max_time_edge_fraction','max_spectral_edge_fraction',
                                     'time_edge_fraction','spectral_edge_fraction'])>1e-6 and case.get('stop_on_edge',True):
                raise EdgeStop('Edge threshold exceeded; this checkpoint and later outputs excluded.')
            if stats['process_peak_rss_bytes']>3e9:raise RuntimeError('RSS exceeds 3 GB budget')
        try:
            propagate(case,callback);report['complete']=True
        except EdgeStop as e:report.update(terminated_for_edge=True,stop_reason=str(e))
        except Exception as e:
            report.update(error=str(e),traceback=traceback.format_exc());write_json(out,report);raise
        report.update(wall_seconds=time.monotonic()-start,process_peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        write_json(out,report)
if __name__=='__main__':main()
