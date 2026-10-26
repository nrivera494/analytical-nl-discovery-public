"""Continue the actual fission-born daughter after isolation, without a sech relaunch.
gpt-d/gpt-6-astra/gpt. The same frozen formation-plane ODE is used for scoring.
"""
from independent import *
memory_ok();rid='2026-10-16-gpt-d-fission-daughter';rd=ROOT/'runs'/rid;rd.mkdir(exist_ok=True);raw=RAW/rid;raw.mkdir(exist_ok=True)
prefix='2026-10-16-gpt-d-z75-fission-prefix';arr=np.load(RAW/prefix/'fields.npz');pr=json.loads((ROOT/'runs'/prefix/'summary.json').read_text());f=Fibre();s=GNLSE(f,n=16384,dt=.003,carrier_um=3.3)
A=fft(arr['Qfinal']);I=abs(A)**2;A=np.roll(A,s.n//2-int(np.argmax(I)));gate=abs(s.t)<1.5
Q=ifft(A*gate);out,arrays=s.run(.04,7.5,.00025,order=2,cutoffs=[3.5,3.6,3.7,4.],save_every=.025,Q0=Q)
for row in out['records']:row['z']+=.5
out.update(IDENTITY);out.update({'run_id':rid,'parent_run':prefix,'initial_plane_m':.5,'cutout_halfwidth_ps':1.5,'retained_fraction_of_full_launch':out['N0']/pr['N0'],'formation_prediction_file':'../2026-10-16-gpt-d-loss-edge-audit/fission_predictions.json','initial_field':'Actual fission-prefix field; no sech replacement; distant second pulse removed after isolation'})
np.savez_compressed(raw/'fields.npz',**arrays);dump(rd/'summary.json',out)
(rd/'meta.yaml').write_text(f'run_id: {rid}\nagent: gpt-d\nmodel: gpt-6-astra\nfamily: gpt\nclaim: C-20261016-claude-interactive.6-01\nsolver_commit: {SOLVER}\nsolver_dirty: false\nhardware: {socket.gethostname()}\nwall_time_s: {out["wall_s"]}\nraw_location: {raw}\n')
print(json.dumps({'run_id':rid,'final':out['records'][-1]}))
