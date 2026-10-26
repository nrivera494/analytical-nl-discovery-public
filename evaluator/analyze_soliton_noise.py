#!/usr/bin/env python3
"""agent: gpt-b; model: gpt-6-astra; family: gpt.

Independent covariance contractions and checks for the scalar solver baseline.
Python 3.9+, numpy/scipy/matplotlib/tomli. No parameters are fitted to set noise.
"""
import json
import os
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MPLCONFIGDIR", "/private/tmp/gpt-b-matplotlib")
from pathlib import Path
import sys
import tomli
import numpy as np
from scipy.integrate import cumulative_simpson
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import expm_multiply
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HBAR, KB = 1.054571817e-34, 1.380649e-23
COORDS = ["energy", "phase", "timing", "frequency"]
C0 = np.array([2., (np.pi**2+12)/72, np.pi**2/24, 1/6])
TR_PS = .18*2/.032 / ((1/.032)**2+(1/.0122)**2)


def psd(k, t0, temp):
    """Corney--Drummond Wigner FDT, including finite thermal DC limit."""
    a, b = 1/.032, 1/.0122
    omega = np.abs(k)/t0
    response = .18*(a*a+b*b)/((a-1j*omega)**2+b*b)
    out = np.zeros_like(k)
    nonzero = omega > 0
    if temp:
        occupation = 1/np.expm1(HBAR*omega[nonzero]*1e12/(KB*temp))
        out[nonzero] = np.abs(response[nonzero].imag)*(2*occupation+1)
        out[~nonzero] = 2*KB*temp/HBAR*TR_PS*1e-12
    else:
        out = np.abs(response.imag)
    return out


def power(z, y, lower=1.0):
    mask = (z >= lower) & (y > 0)
    slope, intercept = np.polyfit(np.log(z[mask]), np.log(y[mask]), 1)
    return {"exponent": float(slope), "coefficient": float(np.exp(intercept)),
            "z_min": float(z[mask][0]), "z_max": float(z[mask][-1])}


def theory(z):
    out = np.zeros((len(z), 4, 4))
    for j in range(4):
        out[:, j, j] = C0[j]
    out[:, 1, 1] += z*z/2
    out[:, 2, 2] += z*z/6
    out[:, 0, 1] = out[:, 1, 0] = z
    out[:, 2, 3] = out[:, 3, 2] = z/6
    return out


def trace_analysis(data, t0=.5, temp=300, alpha=.1):
    r = data["response"]
    z, x, k = data["z"], data["x"], data["k"]
    dt, n = x[1]-x[0], len(x)
    cov = np.einsum("zij,zkj->zik", r, r)/4
    gain = 2*alpha*cumulative_simpson(cov, x=z, axis=0, initial=0)
    # R_ij = sqrt(dt)*g_eff,ij. Multiplicative real phase noise uses only
    # the imaginary-field columns, multiplied by the unperturbed sech.
    weighted = np.fft.fft(r[:, :, n:]/np.cosh(x), axis=-1)
    s = psd(k, t0, temp)
    rkernel = np.einsum("zij,zkj,j->zik", weighted.conj(), weighted, s).real/n
    raman = cumulative_simpson(rkernel, x=z, axis=0, initial=0)
    expected = theory(z)
    diag = np.diagonal(cov, axis1=1, axis2=2)
    expected_diag = np.diagonal(expected, axis1=1, axis2=2)
    transport = np.repeat(r[:1], len(z), axis=0)
    transport[:, 1, :] += z[:, None]*r[0, 0, :]/2
    transport[:, 2, :] += z[:, None]*r[0, 3, :]
    mean = data["mean_fields"]
    exact = 1/np.cosh(x[:, None])*np.exp(.5j*z[None, :])
    mean_error = np.linalg.norm(mean-exact, axis=0)/np.linalg.norm(exact, axis=0)
    mean_energy = dt*np.sum(abs(mean)**2, axis=0)
    stats = {
        "variance_over_q_at_zmax": dict(zip(COORDS, diag[-1].tolist())),
        "predicted_variance_over_q_at_zmax": dict(zip(COORDS, expected_diag[-1].tolist())),
        "maximum_relative_diagonal_covariance_error": float(np.max(abs(diag/expected_diag-1))),
        "maximum_relative_transport_error": float(np.max(
            np.linalg.norm(r-transport, axis=(1, 2))/np.linalg.norm(transport, axis=(1, 2)))),
        "maximum_mean_field_relative_l2_error": float(max(mean_error)),
        "maximum_relative_energy_error": float(max(abs(mean_energy/2-1))),
        "biorthogonality_max_error": float(np.max(abs(data["biorthogonality"]-np.eye(4)))),
        "input_energy": power(z, diag[:, 0]),
        "input_frequency": power(z, diag[:, 3]),
        "input_phase_excess": power(z, diag[:, 1]-C0[1]),
        "input_timing_excess": power(z, diag[:, 2]-C0[2]),
        "gain_timing_cubic_excess": power(z, gain[:, 2, 2]-alpha*np.pi**2*z/12),
        "raman_timing": power(z, raman[:, 2, 2]),
        "raman_frequency": power(z, raman[:, 3, 3]),
        "raman_frequency_diffusion_over_q": float(rkernel[0, 3, 3]),
        "raman_timing_cubic_coefficient_over_q": float(rkernel[0, 3, 3]/3),
        "wall_seconds": float(data["wall_seconds"]),
    }
    # Source coefficient evaluated independently at launch by a Fourier quadrature.
    b = np.tanh(x)/np.cosh(x)**2
    d = dt/n*np.sum(s*abs(np.fft.fft(b))**2)
    stats["independent_raman_frequency_diffusion_over_q"] = float(d)
    return stats, {"z": z, "vacuum": cov, "gain": gain, "raman": raman,
                   "raman_kernel": rkernel}


def bogoliubov_check(data):
    """A second solver: matrix exponential of an independent Fourier linearization."""
    x, k, g = data["x"], data["k"], data["dual"]
    n, dt = len(x), x[1]-x[0]
    s = 1/np.cosh(x)
    d2 = np.fft.ifft(-k[:, None]**2*np.fft.fft(np.eye(n), axis=0), axis=0).real
    lm = d2/2+np.diag(s*s-.5)
    lp = d2/2+np.diag(3*s*s-.5)
    generator = np.block([[np.zeros((n, n)), -lm], [lp, np.zeros((n, n))]])
    gradients = dt*np.vstack([g.real, g.imag])
    target = np.zeros_like(gradients)
    target[:, 1] = gradients[:, 0]/2
    target[:, 2] = gradients[:, 3]
    residual = np.einsum("ji,jk->ik", generator, gradients, optimize=False)-target
    evolved = expm_multiply(csr_matrix(generator.T), gradients,
                            start=0, stop=12, num=7, traceA=0)
    cov = np.einsum("zij,zik->zjk", evolved, evolved)/(4*dt)
    z = np.linspace(0, 12, 7)
    target_cov = theory(z)
    err = np.max(abs(np.diagonal(cov, axis1=1, axis2=2)/
                     np.diagonal(target_cov, axis1=1, axis2=2)-1))
    return {"adjoint_identity_relative_residual": float(np.linalg.norm(residual)/np.linalg.norm(gradients)),
            "matrix_exponential_max_relative_variance_error": float(err),
            "variance_over_q_at_z12": np.diag(cov[-1]).tolist()}


def source_analysis(data, cfg):
    x, k, q = data["x"], data["k"], float(data["q"])
    dt, n = x[1]-x[0], len(x)
    s = 1/np.cosh(x)
    b = np.column_stack([np.tanh(x)*s*s, (1-x*np.tanh(x))*s*s])
    bf = np.fft.fft(b, axis=0)
    result = {"q": q, "mean_photons": 2/q, "LD_m": float(data["LD_m"]),
              "P0_W": float(data["P0_W"]), "samples": cfg["n_samples"],
              "expected_relative_variance_standard_error": (2/(cfg["n_samples"]-1))**.5}
    for temp in cfg["temperatures_K"]:
        expected = dt/n*np.sum(psd(k, cfg["t0_ps"], temp)[:, None]*abs(bf)**2, axis=0)
        result[str(temp)] = {"expected_diffusion_over_q": expected.tolist()}
        for name in ["legacy", "wigner"]:
            measured = np.var(data[f"{name}_{temp}_samples"], axis=0, ddof=1)/q
            c = data[f"{name}_{temp}_C"]
            gamma = cfg["gamma_W_m"]
            ld = cfg["t0_ps"]**2/abs(cfg["beta2_ps2_m"])
            df_hz = 1/(n*dt*cfg["t0_ps"])*1e12
            exact_sampler = gamma**2*ld*df_hz*dt**2*np.sum(c[:, None]*abs(bf)**2, axis=0)/q
            result[str(temp)][name] = {
                "measured_over_Wigner_prediction": (measured/expected).tolist(),
                "exact_sampler_over_Wigner_prediction": (exact_sampler/expected).tolist(),
                "measured_over_sampler_prediction": (measured/exact_sampler).tolist()}
    for name in ["wigner", "legacy"]:
        measured = np.var(data[f"vacuum_{name}_samples"], axis=0, ddof=1)/q
        result[f"input_{name}_variance_ratio"] = (measured/C0).tolist()
    return result


def drift_analysis(data, cfg):
    result = []
    for t0 in cfg["t0_ps"]:
        row = {"T0_ps": t0, "long_pulse_normalized_rate": 8*TR_PS/(15*t0)}
        for method in ["rk4ip", "splitstep"]:
            key = str(t0).replace(".", "p")+"_"+method
            z, v = data[key+"_z"], data[key+"_frequency"]
            rate = np.polyfit(z, v, 1)[0]
            initial_exact = float(data[key+"_initial_exact_rate"])
            row[method] = {
                "measured_normalized_rate": float(rate),
                "launch_exact_convolution_rate": initial_exact,
                "relative_error_vs_long_pulse": float(rate/row["long_pulse_normalized_rate"]-1),
                "relative_error_vs_launch_exact": float(rate/initial_exact-1),
                "max_relative_energy_error": float(max(abs(data[key+"_energy"]/2-1))),
                "z_growth": power(z, v, lower=.5)}
        row["integrator_relative_rate_difference"] = abs(
            row["rk4ip"]["measured_normalized_rate"]/row["splitstep"]["measured_normalized_rate"]-1)
        result.append(row)
    t0 = np.array(cfg["t0_ps"])
    rates = np.array([r["rk4ip"]["measured_normalized_rate"] for r in result])
    # beta2 is held fixed; d(physical detuning)/dz = -V' |beta2| / T0^3.
    physical = rates*.021/t0**3
    relerr = abs(rates/(8*TR_PS/(15*t0))-1)
    return {"TR_ps": TR_PS, "rows": result,
            "physical_redshift_exponent_longest_three": float(np.polyfit(np.log(t0[-3:]),np.log(physical[-3:]),1)[0]),
            "long_pulse_relative_error_exponent_longest_three": float(np.polyfit(np.log(t0[-3:]),np.log(relerr[-3:]),1)[0]),
            "physical_redshift_magnitude_rad_per_ps_per_m": physical.tolist()}


def stochastic_analysis(data, source, reference, cfg):
    from scipy.stats import chi2
    coords, z, q = data["coordinates"], data["z"], float(data["q"])
    n = coords.shape[2]
    centered = coords-coords.mean(axis=2, keepdims=True)
    covariance = np.einsum("zin,zjn->zij", centered, centered)/((n-1)*q)
    key = "raman" if source.startswith("raman") else source
    pred = np.stack([np.interp(z, reference["z"], reference[key][:, j, j]) for j in range(4)], axis=1)
    diag = np.diagonal(covariance, axis1=1, axis2=2)
    sel = [1, 2] if source == "vacuum" else [2]
    result = {"trajectories": n, "q": q,
        "variance_over_q_at_zmax": dict(zip(COORDS,diag[-1].tolist())),
        "reference_variance_over_q_at_zmax": dict(zip(COORDS,pred[-1].tolist())),
        "relative_variance_standard_error": (2/(n-1))**.5,
        "variance_95_percent_interval_over_q_at_zmax": {
            name: [float((n-1)*diag[-1,j]/chi2.ppf(.975,n-1)),
                   float((n-1)*diag[-1,j]/chi2.ppf(.025,n-1))]
            for j,name in enumerate(COORDS)}}
    rng = np.random.default_rng(cfg["seed"]+len(source))
    mask = z >= 2
    for j in sel:
        offset = C0[j] if source == "vacuum" else (.1*np.pi**2*z/12 if source == "gain" else 0.)
        result[COORDS[j]+"_growth"] = power(z, diag[:,j]-offset, lower=2)
        powers = []
        for _ in range(200):
            indices = rng.integers(0,n,n)
            v = np.var(coords[:,j,indices],axis=-1,ddof=1)/q-offset
            if np.all(v[mask] > 0):
                powers.append(np.polyfit(np.log(z[mask]),np.log(v[mask]),1)[0])
        result[COORDS[j]+"_growth"]["bootstrap_95_percent_exponent_interval"] = np.quantile(powers,[.025,.975]).tolist()
    result["timing_at_zmax_ratio_to_continuum_reference"] = float(diag[-1,2]/pred[-1,2])
    if key != "vacuum":
        result["frequency_at_zmax_ratio_to_continuum_reference"] = float(diag[-1,3]/pred[-1,3])
    return result, covariance


def crosscheck_analysis(data):
    z, r, ss, initial = data["z"], data["rk4ip"], data["splitstep"], data["initial"]
    exact = np.repeat(initial[None],len(z),axis=0)
    exact[:,1,:] += z[:,None]*initial[0,:]/2
    exact[:,2,:] += z[:,None]*initial[3,:]
    scale = np.linalg.norm(exact,axis=(1,2))
    return {"full_field_probes": int(initial.shape[1]),
            "RK4IP_max_relative_transport_error": float(np.max(np.linalg.norm(r-exact,axis=(1,2))/scale)),
            "splitstep_max_relative_transport_error": float(np.max(np.linalg.norm(ss-exact,axis=(1,2))/scale)),
            "integrator_max_relative_difference": float(np.max(np.linalg.norm(ss-r,axis=(1,2))/scale))}


def figures(path, traces, stochastic, sources, drift):
    plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False})
    fig, ax = plt.subplots(2,2,figsize=(10.4,7.4),layout="constrained")
    z = traces["z"]
    good = z > 0
    for j,name,color in [(1,"Phase","#a33a35"),(2,"Timing","#226c9e")]:
        y = traces["vacuum"][:,j,j]-C0[j]
        ax[0,0].loglog(z[good],y[good],color=color,label=name+"; solver covariance")
        ax[0,0].loglog(z[good],z[good]**2/(2 if j==1 else 6),"--",color=".3",lw=1)
    ax[0,0].set(title="Input vacuum: excess variance",xlabel=r"$\zeta=z/L_D$",ylabel=r"$[\mathrm{Var}(X)-\mathrm{Var}(X_0)]/q$")
    ax[0,0].legend(fontsize=8)
    for name,color in [("gain","#825099"),("raman","#28865e")]:
        y=traces[name][:,2,2].copy()
        if name=="gain": y-=.1*np.pi**2*z/12
        ax[0,1].loglog(z[good],y[good],label=name.capitalize()+"; impulse covariance",color=color)
        sd,sc=stochastic[name]
        zz=sd["z"]
        yy=sc[:,2,2].copy()
        if name=="gain": yy-=.1*np.pi**2*zz/12
        pick=(zz>=2)&(np.arange(len(zz))%3==0)
        ax[0,1].loglog(zz[pick],yy[pick],"o",ms=3,color=color,label=name.capitalize()+"; 2048 trajectories")
    ax[0,1].set(title="Distributed sources: cubic timing term",xlabel=r"$\zeta$",ylabel=r"$\mathrm{Var}(T)_{\rm cubic}/q$")
    ax[0,1].legend(fontsize=8)
    temperatures=[0,77,300]
    x=np.arange(3)
    for shift,name,color in [(-.17,"legacy","#a33a35"),(.17,"wigner","#28865e")]:
        heights=[sources[str(t)][name]["exact_sampler_over_Wigner_prediction"][0] for t in temperatures]
        ax[1,0].bar(x+shift,heights,width=.3,color=color,label="Default" if name=="legacy" else "Explicit Wigner spectrum")
    ax[1,0].axhline(1,color=".3",ls="--",lw=1)
    ax[1,0].set(xticks=x,xticklabels=temperatures,xlabel="Temperature (K)",ylabel="Frequency-diffusion coefficient / theory",title="Default Raman zero-point test fails",ylim=(0,1.16))
    ax[1,0].legend(fontsize=8)
    t0=np.array([r["T0_ps"] for r in drift["rows"]])
    rates=np.array(drift["physical_redshift_magnitude_rad_per_ps_per_m"])
    ax[1,1].loglog(t0,rates,"o-",color="#226c9e",label="Delayed-response RK4IP")
    ax[1,1].loglog(t0,8/15*TR_PS*.021/t0**4,"--",color=".3",label=r"Gordon long-pulse $T_0^{-4}$")
    ax[1,1].set(xlabel=r"$T_0$ (ps)",ylabel=r"$|d\Omega/dz|$ (rad ps$^{-1}$ m$^{-1}$)",title="Mean Raman redshift")
    ax[1,1].legend(fontsize=8)
    fig.savefig(path/"baselines.png",dpi=160)
    plt.close(fig)


def main(config_path):
    config_path=Path(config_path)
    with config_path.open("rb") as f: cfg=tomli.load(f)
    raw=Path(cfg["raw_location"])
    summary={"agent":"gpt-b","model":"gpt-6-astra","family":"gpt",
             "run_id":config_path.parent.name,
             "coordinate_order":COORDS,"covariance_units":"dimensionless variance divided by q",
             "traces":{},"stochastic":{},"acceptance":{
                 "deterministic_relative_covariance_tolerance":1e-4,
                 "deterministic_growth_exponent_absolute_tolerance":1e-3,
                 "sampler_variance_standard_errors":4,
                 "conventions":"Wigner input half photon, balanced gain/loss alpha_G=0.1, explicitly symmetrized Raman spectrum"}}
    trace_arrays={}
    for variant in cfg["trace"]:
        data=np.load(raw/("trace_"+variant["name"]+".npz"))
        stats,arrays=trace_analysis(data)
        summary["traces"][variant["name"]]=stats
        trace_arrays[variant["name"]]=arrays
    base=trace_arrays["base"]
    summary["convergence"]={}
    for name,a in trace_arrays.items():
        if name=="base": continue
        summary["convergence"][name]={key:float(np.max(abs(
            np.diagonal(a[key],axis1=1,axis2=2)[1:,:]/
            np.diagonal(base[key],axis1=1,axis2=2)[1:,:]-1)))
            for key in ["vacuum","gain"]}
        summary["convergence"][name]["raman_timing"]=float(np.max(abs(a["raman"][1:,2,2]/base["raman"][1:,2,2]-1)))
    summary["independent_linearized_solver"]=bogoliubov_check(np.load(raw/"trace_base.npz"))
    summary["source_checks"]=source_analysis(np.load(raw/"source_checks.npz"),cfg["source_checks"])
    summary["raman_drift"]=drift_analysis(np.load(raw/"drift.npz"),cfg["drift"])
    summary["integrator_crosscheck"]=crosscheck_analysis(np.load(raw/"crosscheck.npz"))
    stochastic={}
    for source in cfg["stochastic"]["sources"]:
        data=np.load(raw/("stochastic_"+source+".npz"))
        stats,cov=stochastic_analysis(data,source,base,cfg["stochastic"])
        summary["stochastic"][source]=stats
        stochastic[source]=(data,cov)
    summary["checks"]={
        "NLSE_covariance":max(s["maximum_relative_diagonal_covariance_error"] for s in summary["traces"].values())<1e-4,
        "independent_Bogoliubov_covariance":summary["independent_linearized_solver"]["matrix_exponential_max_relative_variance_error"]<1e-4,
        "default_Raman_Wigner_zero_point_normalization":abs(summary["source_checks"]["0"]["legacy"]["exact_sampler_over_Wigner_prediction"][0]-1)<1e-4,
        "explicit_Wigner_Raman_spectrum":max(abs(r-1) for t in ["0","77","300"] for r in summary["source_checks"][t]["wigner"]["measured_over_Wigner_prediction"])<4*(2/(cfg["source_checks"]["n_samples"]-1))**.5,
    }
    figures(config_path.parent,base,stochastic,summary["source_checks"],summary["raman_drift"])
    (config_path.parent/"summary.json").write_text(json.dumps(summary,indent=2,allow_nan=False)+"\n")
    contracted=raw/"contracted_covariances.npz"
    if contracted.exists():
        with np.load(contracted) as old:
            if any(not np.array_equal(old[k],v) for k,v in base.items()):
                raise RuntimeError("Changed contraction would overwrite an existing run; use a fresh raw directory")
    else:
        np.savez(contracted,**base)
    print(json.dumps({"checks":summary["checks"],"base":summary["traces"]["base"],
                      "source_checks":summary["source_checks"],"stochastic":summary["stochastic"]},indent=2))


def pathwise_main(config_path):
    config_path=Path(config_path)
    with config_path.open("rb") as f: cfg=tomli.load(f)
    raw=Path(cfg["raw_location"])
    c=cfg["stochastic"]
    result={"agent":"gpt-b","model":"gpt-6-astra","family":"gpt",
            "run_id":config_path.parent.name,"sources":{},
            "purpose":"Independent-parameter full-field versus same-noise coordinate transport; no fit of source coefficients"}
    for source in c["sources"]:
        data=np.load(raw/("stochastic_"+source+".npz"))
        assert data["shadow_enabled"]
        u,v,z,q=data["coordinates"],data["shadow_coordinates"],data["z"],float(data["q"])
        vv=np.var(v,axis=2,ddof=1)/q
        uv=np.var(u,axis=2,ddof=1)/q
        selected=[0,1,2,3] if source=="gain" else [1,2,3]
        row={"trajectories":u.shape[2],"q":q,
            "relative_rms_pathwise_errors":{},"variance_relative_errors":{}}
        for j in selected:
            rms=np.linalg.norm(u[1:,j]-v[1:,j],axis=1)/np.linalg.norm(v[1:,j],axis=1)
            row["relative_rms_pathwise_errors"][COORDS[j]]=float(max(rms))
            row["variance_relative_errors"][COORDS[j]]=float(max(abs(uv[1:,j]/vv[1:,j]-1)))
        offset=2*c["alpha_G"]*C0[2]*z if source=="gain" else 0.
        row["field_timing_exponent"]=power(z,uv[:,2]-offset,lower=2)
        row["same_noise_reduced_timing_exponent"]=power(z,vv[:,2]-offset,lower=2)
        n=np.rint(z/c["h"]).astype(int)
        discrete_integral=c["h"]**3*n*(n-1)*(2*n-1)/6
        if source=="gain":
            d=c["alpha_G"]/3
        else:
            nn=c["n"]
            dt=c["window"]/nn
            x=(np.arange(nn)-nn//2)*dt
            k=2*np.pi*np.fft.fftfreq(nn,dt)
            b=np.tanh(x)/np.cosh(x)**2
            d=dt/nn*np.sum(psd(k,c["t0_ps"],c["temperature_K"])*abs(np.fft.fft(b))**2)
        predicted=offset+d*discrete_integral
        row["discrete_expected_timing_exponent"]=power(z,predicted-offset,lower=2)
        row["timing_variance_final_over_discrete_expectation"]=float(uv[-1,2]/predicted[-1])
        row["same_noise_reduced_variance_final_over_discrete_expectation"]=float(vv[-1,2]/predicted[-1])
        row["maximum_pathwise_timing_error_below_0p2_percent"]=row["relative_rms_pathwise_errors"]["timing"]<.002
        result["sources"][source]=row
    (config_path.parent/"summary.json").write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    if "--pathwise" in sys.argv:
        pathwise_main(sys.argv[1])
    else:
        main(sys.argv[1])
