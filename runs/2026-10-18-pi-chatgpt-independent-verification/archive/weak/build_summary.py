#!/usr/bin/env python3
"""Aggregate existing independent weak-GVD calculations; never propagate.

Writes summary.json, numerical_results.csv, weak_verification.pdf/.png.
Requires NumPy and Matplotlib.  Run from any working directory.
"""
import csv
import hashlib
import json
import os
from pathlib import Path

os.environ.setdefault('MPLCONFIGDIR', '/tmp/fiber-audit-mpl')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, NullFormatter

HERE = Path(__file__).resolve().parent
THEORY = HERE.parent/'weak_theory'


def c2(phi):
    s = np.sqrt(1+phi*phi)
    return np.sqrt(6)*(45+81*phi**2+56*phi**4+40*phi**3*s)/(240*phi**2*s*s)


def load_records(path):
    obj = json.loads(path.read_text())
    return obj if isinstance(obj, list) else [obj]


def main():
    source_files = [HERE/'weak_results.json', HERE/'second_order_results.json',
                    HERE/'second_order_phi10.json', THEORY/'oscillator_constants.json',
                    THEORY/'second_order_symbolic.json']
    missing = [str(p) for p in source_files if not p.exists()]
    if missing:
        raise FileNotFoundError('Required recorded inputs missing: '+', '.join(missing))
    oscillator = json.loads(source_files[3].read_text())
    base = load_records(source_files[0])
    all_records = []
    for path in source_files[:3]:
        for index, item in enumerate(load_records(path)):
            r = dict(item)
            r['source_file'] = path.name
            r['label'] = r.get('label', f'{path.stem}_{index+1}')
            m, phi, y = int(r['m']), float(r['phi']), float(r['y'])
            factor = oscillator[str(m)]['relative_excess_prefactor_before_Phi_over_sqrt']
            if m == 1:
                factor = np.sqrt(2/3)
            r['theory_exponent'] = m/(m+1)
            r['theory_prediction'] = factor*phi/np.sqrt(1+phi*phi)*y**(m/(m+1))
            r['theory_ratio'] = r['excess']/r['theory_prediction'] if y else None
            r['rms_theory'] = oscillator[str(m)]['rms_prefactor_before_y_power']*y**(1/(2*m+2))
            r['rms_ratio'] = r['xrms']/r['rms_theory'] if y else None
            r['c2_theory'] = float(c2(phi)) if m == 1 else None
            r['c2_effective'] = (r['theory_ratio']-1)/np.sqrt(y) if m == 1 and y else None
            all_records.append(r)
    primary = [r for r in all_records if r['source_file']=='weak_results.json'
               and (r['label'].startswith('gaussian_') or r['label'].startswith('flat'))]
    primary.sort(key=lambda r: (r['m'],r['phi'],r['y']))
    by_label = {r['label']:r for r in all_records}
    series = []
    for m, phi in [(1,3.),(1,10.),(2,3.),(3,3.)]:
        rr = [r for r in primary if r['m']==m and r['phi']==phi]
        fit = [r for r in rr if 1e-6 <= r['y'] <= 1e-4]
        x = np.log([r['y'] for r in fit])
        slope, intercept = np.polyfit(x,np.log([r['excess'] for r in fit]),1)
        width_slope = np.polyfit(x,np.log([r['xrms'] for r in fit]),1)[0]
        series.append(dict(m=m,phi=phi,profile=f'exp(-x^{2*m})',
            number_of_points=len(rr),fit_y_range=[1e-6,1e-4],fit_points=len(fit),
            excess_exponent_expected=m/(m+1),excess_exponent_fitted=float(slope),
            rms_exponent_expected=1/(2*m+2),rms_exponent_fitted=float(width_slope),
            leading_ratio_low_y=float(rr[0]['theory_ratio']),
            leading_ratio_y_1e_2=float(rr[-1]['theory_ratio']),
            maximum_rms_relative_error_y_le_1e_4=float(max(abs(r['rms_ratio']-1) for r in fit))))

    def comparison(name, first, second):
        a,b = by_label[first],by_label[second]
        return dict(name=name,first=first,second=second,
            lambda_relative_difference=float(a['lambda_min_upper']/b['lambda_min_upper']-1),
            excess_absolute_difference=float(a['excess']-b['excess']),
            rms_relative_difference=float(a['xrms']/b['xrms']-1))

    comparisons = [
        comparison('grid_2048_vs_3072', 'gaussian_phi3_y1e-06', 'grid_gaussian_fine'),
        comparison('tolerance_and_support_refinement','gaussian_phi10_y0.0001','tolerance_gaussian'),
        comparison('input_support_0.6_vs_1.2','support_standard','support_wide'),
        comparison('restricted_vs_full_same_grid','support_standard','full_tangent'),
        comparison('time_window_8_vs_12_same_dx','gaussian_phi3_y0.001','window_wide')]
    second = [dict(phi=r['phi'],y=r['y'],n=r['n'],rtol=r['rtol'],
                   c2_effective=r['c2_effective'],c2_theory=r['c2_theory'],
                   difference=r['c2_effective']-r['c2_theory'],source_file=r['source_file'])
              for r in all_records if r['source_file']!='weak_results.json']
    summary = dict(
        title='Independent weak normal-dispersion covariance verification',
        repository_commit='970bfe756b131094872de351ff91ab46a537d9b2',
        method='Eighth-order periodic finite differences; adaptive DOP853 for mean and real tangent map',
        observable='Inverse squared largest singular value; upper estimate of full minimum covariance eigenvalue when input columns are restricted',
        shot_noise=1,
        inputs={str(p.relative_to(HERE.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in source_files},
        base_record_count=len(base),all_record_count=len(all_records),primary_series=series,
        convergence=dict(comparisons=comparisons,
            max_symplectic_embedding_absolute_defect=max(r['symplectic_max_abs'] for r in all_records),
            max_mean_energy_relative_error=max(abs(r['mean_energy_relative_error']) for r in all_records),
            full_map_reciprocity_relative_error=by_label['full_tangent']['reciprocity_relative_error'],
            zero_dispersion_relative_error=by_label['zero_dispersion']['excess']),
        second_order=dict(
            formula='c2=sqrt(6)*(45+81*Phi^2+56*Phi^4+40*Phi^3*sqrt(1+Phi^2))/(240*Phi^2*(1+Phi^2))',
            status='Independently derived formal local expansion; full-NLSE numerical check, not a certified global remainder',
            cases=second,
            extraction_caveat='The y coefficient is obtained by subtracting a much larger anchor and square-root term; finite integration/grid errors are amplified as y decreases.'),
        caveats=[
            'Fits use three points y=1e-6,1e-5,1e-4; these are deterministic regression slopes, not statistical confidence intervals.',
            'Input-column truncation gives a variational upper estimate of lambda_min in the full finite-grid symplectic model; support and full-map checks quantify representative truncation error.',
            'Reciprocity and symplectic checks validate normalization but do not certify spatial truncation or all continuum frequencies.',
            'An ordinary covariance eigenvalue optimizes arbitrary homodyne mode; it is not the optimized binary-filter photon-counting Fano factor.',
            'The all-mode small-dispersion limit assumes increasing resolved optical bandwidth and appropriate quantum linearization validity.'])
    (HERE/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    columns=['source_file','label','phi','m','y','delta','n','dx','half_window','support',
             'full','input_columns','rtol','lambda_min_upper','vmin','excess',
             'prediction','theory_prediction','theory_ratio','xrms','rms_theory','rms_ratio',
             'c2_effective','c2_theory','symplectic_max_abs','mean_energy_relative_error',
             'direct_lambda_min','reciprocity_relative_error','runtime_seconds']
    with (HERE/'numerical_results.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=columns,extrasaction='ignore')
        writer.writeheader()
        writer.writerows(all_records)

    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,
        'axes.labelsize':10.5,'axes.titlesize':11.5,'axes.titleweight':'bold',
        'axes.linewidth':.8,'xtick.labelsize':9,'ytick.labelsize':9,
        'legend.fontsize':8.7,'pdf.fonttype':42,'ps.fonttype':42,
        'savefig.facecolor':'white','figure.facecolor':'white'})
    fig,axs=plt.subplots(2,2,figsize=(11.4,8.35))
    fig.subplots_adjust(left=.085,right=.975,bottom=.145,top=.90,wspace=.32,hspace=.40)
    fig.suptitle('Weak normal dispersion: independent covariance and mode verification',
                 x=.53,y=.965,fontsize=14,fontweight='bold')
    configs=[(1,3.,'#2367a3','o',r'Gaussian, $\Phi=3$'),
             (1,10.,'#6494bd','D',r'Gaussian, $\Phi=10$'),
             (2,3.,'#c4711d','s',r'$p=e^{-x^4}$, $\Phi=3$'),
             (3,3.,'#32816f','^',r'$p=e^{-x^6}$, $\Phi=3$')]
    dense=np.geomspace(8e-7,1.3e-2,300)
    for m,phi,color,marker,label in configs:
        rr=[r for r in primary if r['m']==m and r['phi']==phi]
        yy=np.array([r['y'] for r in rr]);ex=np.array([r['excess'] for r in rr])
        factor=oscillator[str(m)]['relative_excess_prefactor_before_Phi_over_sqrt']
        leading=factor*phi/np.sqrt(1+phi*phi)*dense**(m/(m+1))
        face='white' if phi==10 else color
        axs[0,0].loglog(dense,leading,'--',color=color,lw=1.15,alpha=.8)
        axs[0,0].loglog(yy,ex,marker=marker,ls='none',color=color,mfc=face,
                        ms=5.2,mew=1.1,label=label)
        axs[0,1].semilogx(yy,[r['theory_ratio'] for r in rr],marker=marker,
                         color=color,mfc=face,ms=5,lw=1.35,label=label)
        if m==1:
            axs[0,1].semilogx(dense,1+c2(phi)*np.sqrt(dense),'--',color=color,lw=1.15)
        width=oscillator[str(m)]['rms_prefactor_before_y_power']*dense**(1/(2*m+2))
        if phi==3:
            axs[1,0].loglog(dense,width,'--',color=color,lw=1.2)
        axs[1,0].loglog(yy,[r['xrms'] for r in rr],marker=marker,ls='none',
                        color=color,mfc=face,ms=5.2,mew=1.1,label=label)
    axs[0,0].set(title='(a) Covariance excess',xlabel=r'$y=\Phi L/L_D$',
        ylabel=r'$\lambda/\lambda_0-1$',xlim=(8e-7,1.3e-2))
    axs[0,0].legend(loc='upper left',frameon=False)
    axs[0,0].text(.97,.07,r'Predicted powers: $1/2,\ 2/3,\ 3/4$',
                  transform=axs[0,0].transAxes,ha='right',fontsize=9)
    axs[0,1].set(title='(b) Ratio to the leading prediction',xlabel=r'$y=\Phi L/L_D$',
        ylabel='Measured excess / leading asymptotic',xlim=(8e-7,1.3e-2),ylim=(.996,1.115))
    axs[0,1].axhline(1,color='#777777',lw=.7)
    axs[0,1].text(.04,.94,'Dashed: Gaussian prediction including\nthe independently derived '+r'$c_2\sqrt{y}$'+' term',
        transform=axs[0,1].transAxes,va='top',fontsize=9,linespacing=1.5)
    axs[1,0].set(title='(c) Temporal localization',xlabel=r'$y=\Phi L/L_D$',
        ylabel=r'Mode rms width $\sigma_t/T_0$',xlim=(8e-7,1.3e-2))
    axs[1,0].text(.03,.94,r'Predicted powers: $1/4,\ 1/6,\ 1/8$',
                  transform=axs[1,0].transAxes,va='top',fontsize=9)
    ax=axs[1,1]
    for filename,phi,y,color,label in [
        ('mode_phi3_y0.0001.npz',3,1e-4,'#2367a3',r'$\Phi=3,\ y=10^{-4}$'),
        ('mode_phi10_y1e-06.npz',10,1e-6,'#c4711d',r'$\Phi=10,\ y=10^{-6}$')]:
        data=np.load(HERE/filename)
        sigma=(y/24)**.25;xx=data['x'];dx=float(xx[1]-xx[0])
        density=data['density']/np.sum(data['density'])*sigma/dx
        visible=abs(xx/sigma)<4
        ax.plot(xx[visible]/sigma,density[visible],color=color,lw=1.65,label=label)
    xx=np.linspace(-4,4,300)
    ax.plot(xx,np.exp(-xx**2/2)/np.sqrt(2*np.pi),'--',color='#252525',lw=1.15,
            label='Oscillator ground state')
    ax.set(title='(d) Shape of the localized Gaussian mode',xlabel=r'$t/\sigma_{t,\mathrm{pred}}$',
           ylabel='Normalized mode intensity',xlim=(-3.6,3.6),ylim=(0,.44))
    ax.legend(loc='upper right',fontsize=8.3,frameon=False)
    for ax in axs.flat:
        ax.grid(True,which='major',color='#dfe4e8',lw=.6)
        ax.set_axisbelow(True)
        ax.spines[['top','right']].set_visible(False)
    for ax in [axs[0,0],axs[1,0]]:
        ax.xaxis.set_major_locator(LogLocator(base=10,numticks=6))
        ax.yaxis.set_minor_formatter(NullFormatter())
    fig.text(.085,.032,'Symbols: independent finite-difference NLSE + DOP853 tangent propagation.  '
             'Dashed: analytical asymptotics.\n'
             'Vacuum variance = 1; input-support convergence and full-map reciprocity are recorded in summary.json.',
             fontsize=8.5,color='#4d5660',linespacing=1.5)
    fig.savefig(HERE/'weak_verification.pdf')
    fig.savefig(HERE/'weak_verification.png',dpi=240)
    plt.close(fig)
    print(json.dumps({'records':len(all_records),'series':series,'outputs':[
        str(HERE/p) for p in ['summary.json','numerical_results.csv','weak_verification.pdf','weak_verification.png']]},indent=2))


if __name__=='__main__':
    main()
