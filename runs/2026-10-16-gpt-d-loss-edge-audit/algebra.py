"""Independent exact-ODE and asymptotic checks, gpt-d/gpt-6-astra/gpt."""
from independent import *
out={**IDENTITY,'constant_ode':[],'finite_launch':[],'long_pulse_rate':{}}
# Dimensionless K=1, alpha=.02. Compare exact trajectories at fixed final frequency.
for N0 in [1.,1.4]:
 delta=.2; N=(N0**4-4*.02*delta)**.25;z=-np.log(N/N0)/.02
 out['constant_ode'].append({'N0':N0,'N':N,'lost_N':N0-N,'lost_N4':N0**4-N**4,'z':z,'delta_omega':delta})
# Exact exponential edge with constant K, arbitrary finite initial detuning D.
# N^4/N0^4 = [1-exp(-delta/weff)]/[1-exp(-D/weff)].
for D in [.25,.5,1.,2.,4.,8.]:
 out['finite_launch'].append({'initial_detuning_over_weff':D,'claimed_launch_N_ratio':(1-np.exp(-D))**.25,'correct_launch_N_ratio':1.,'terminal_condition_factor':1/(1-np.exp(-D))})
# Fixed terminal omega: delta~exp(-4 alpha_inf z), N~delta^(1/4).
x=np.geomspace(1e-5,.1,80);N=(1-np.exp(-x))**.25
out['quarter_power_exact_ODE_fit']=float(np.polyfit(np.log(x),np.log(N),1)[0])
for mat in ['S28','Z75']:
 f=Fibre(mat);arr=[]
 for T in np.array([30,50,80,100,120,200,300,500,800,1200])*1e-3:
  _,N0=f.launch(T);rate=-overlap_rate(f,f.w0,N0);g=f.K(f.w0)*N0**4
  arr.append({'T_fs':T*1000,'exact_rate':rate,'gordon_rate':g,'relative_error':float((g-rate)/rate)})
 out['long_pulse_rate'][mat]={'cases':arr,'exponent_50_200':float(-np.polyfit(np.log([q['T_fs'] for q in arr if 50<=q['T_fs']<=200]),np.log([abs(q['relative_error']) for q in arr if 50<=q['T_fs']<=200]),1)[0]),'exponent_300_1200':float(-np.polyfit(np.log([q['T_fs'] for q in arr if q['T_fs']>=300]),np.log([abs(q['relative_error']) for q in arr if q['T_fs']>=300]),1)[0])}
# Absorption edge slope independently inferred from primary-source measured points.
ls=np.array([4.3,4.5,4.8]);db=np.array([1.,2.25,8.]);co=np.polyfit(1/ls,np.log(db),1)
out['xia2006_loss_fit']={'DOI':'10.1364/OL.31.002553','access':'full text','lambda_um':ls,'alpha_db_m':db,'B_um':-co[0],'A_db_m':np.exp(co[1]),'predicted_db_m':np.exp(np.polyval(co,1/ls)),'at_4p2_db_m':np.exp(np.polyval(co,1/4.2)),'pairwise_B_um':[np.log(db[i+1]/db[i])/(1/ls[i]-1/ls[i+1]) for i in range(2)]}
dump(Path(__file__).parent/'algebra_summary.json',out)
print(json.dumps(out,default=lambda x:x.tolist() if hasattr(x,'tolist') else str(x)),flush=True)
