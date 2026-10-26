# H5 (exploration): quantum-limited timing jitter of the leading Raman soliton after fission.
# FastDifferentiableMMNLO (agents' copy, pinned b9fa957), discrete RK4IP adjoint, single mode, Agarwal (Blow-Wood) Raman,
# self-steepening built in, beta2 only. Observable: temporal centroid of the leading soliton, i.e. the first temporal
# moment weighted by a window w(t) around the tallest output peak (half-width max(6/amp, 1) T0 in soliton units, as in
# h3_scan.measure). Variance contributions, following example_notebooks/soliton_jitter.ipynb:
#   vacuum (coherent input):  sum |dJ/dB*(0)|^2  (photon units)
#   Raman (phonon bath):      gamma^2 sum_z sum_w |B(z,w)|^2 C(w) df dz,  B = -2 Im(A lambda*)
# with the symmetrized coth bath spectrum C(w) of raman_bath_spectrum.jl (solver branch task/T-20261004-gpt-b-02, copied
# below unchanged). Baseline: an isolated fundamental soliton with the leading soliton's duration T1 = T0/(2 eta1) and the
# same physical length, whose full-pulse centroid jitter is computed the same way, and the SPT formulas of the notebook
# for N = 1 (validation). Usage (repo root): JULIA_NUM_THREADS=2 julia --project=solver runs/<run-id>/h5_jitter.jl
using PulsePropagation, FFTW, LinearAlgebra, Printf
const PP = PulsePropagation
FFTW.set_num_threads(1)

function raman_langevin_spectrum_coth(nt::Integer, dt::Real, f0::Real, gamma_eff::Real;
                                      raman_fraction::Real=0.18, tau1::Real=0.0122, tau2::Real=0.0320,
                                      temperature_K::Real=300.0)
    T = Float64
    hRω = PP.agarwal_raman_response(nt, T(dt), T(raman_fraction), T(tau1 * 1e3), T(tau2 * 1e3))
    omega = PP.ifft_frequency_grid(nt, T(dt))
    hbar = 1.054571817e-34; kb = 1.380649e-23
    prefactor = (hbar / gamma_eff) * (2π * f0 * 1e12)
    cω = zeros(T, nt); w1 = 0.0; imh1 = 0.0
    for k in 1:nt
        w = abs(omega[k]) * 1e12
        w == 0 && continue
        imh = abs(imag(hRω[k]))
        if w1 == 0.0 || w < w1
            w1, imh1 = w, imh
        end
        thermal = temperature_K == 0 ? 1.0 : (x = hbar * w / (2kb * temperature_K); x > 350 ? 1.0 : coth(x))
        cω[k] = prefactor * imh * thermal
    end
    for k in 1:nt
        if abs(omega[k]) * 1e12 == 0
            cω[k] = temperature_K == 0 ? 0.0 : prefactor * (imh1 / w1) * (2kb * temperature_K / hbar)
        end
    end
    return cω
end

c_light = 2.99792458e-4; lambda0 = 1550e-9; omega0 = 2pi * c_light / lambda0; f0 = omega0 / 2pi
material = Silica(raman=AgarwalRaman())
mfd = 9.2e-6; Aeff = pi * (mfd / 2)^2
gamma = material.n2 * (2pi / lambda0) / Aeff
beta2 = -0.0206
hbar = 1.054571817e-34; kb = 1.380649e-23

"""Propagate amplitude-A sech of width Tp (ps) over L (m) with nsteps; return variances (s^2) of the windowed centroid
(window around the tallest peak, half-width hw ps; hw = Inf gives the full-pulse centroid) and diagnostics."""
function jitter(Apk, Tp, L, nsteps, Nt, width, hw_rule; save_every=1)
    grid = TimeGrid(Nt, width); domain = MMGNLSEDomain(degrees_of_freedom(:time), grid)
    t = time_axis(grid); dt = t[2] - t[1]
    pars = MMGNLSEParameters(domain; length=L, beta=TaylorBeta(reshape([0.0, 0.0, beta2], :, 1)), S=1 / Aeff,
                             n2=material.n2, omega0=omega0, raman=AgarwalRaman())
    A0 = zeros(ComplexF64, Nt, 1, 1); A0[:, 1, 1] = Apk .* sech.(t ./ Tp)
    dz = L / nsteps
    sol = solve_mmgnlse(A0, pars, dz; saveat=save_every * dz)
    A = get_temporal_field(sol)[:, 1, 1]
    k = argmax(abs.(A)); hw = hw_rule(abs(A[k]))
    w = Float64.(abs.(t .- t[k]) .<= hw)
    Ew = sum(w .* abs2.(A)); J = sum(w .* t .* abs2.(A)) / Ew
    grad = reshape(w .* (t .- J) .* A ./ Ew, :, 1, 1)
    λL = PP._mmgnlse_time_gradient_to_centered_spectral(grad)
    adj = solve_adjoint(λL, pars, dz; forward_solution=sol, saveat=save_every * dz, adjoint_mode=:discrete_rk4ip)
    var_vac = sum(abs2.(get_spectral_field(adj; units=:photon)[:, :, 1])) * 1e-24
    Cω = fftshift(raman_langevin_spectrum_coth(Nt, dt, f0, gamma))
    Azt = get_temporal_field(sol; z=:all, units=:power)
    λzt = conj(get_temporal_field(adj; z=:all, units=:power))
    # align the saved z-samples of the forward and adjoint trajectories (they can differ by one end point)
    kf = Dict(round(Int, z / dz) => i for (i, z) in enumerate(sol.z))
    pairs = [(kf[round(Int, z / dz)], i) for (i, z) in enumerate(adj.z) if haskey(kf, round(Int, z / dz))]
    nd = ndims(Azt)
    Azt = selectdim(Azt, nd, first.(pairs)); λzt = selectdim(λzt, nd, last.(pairs))
    Bzt = -2 .* imag.(Azt .* λzt)
    Bzω = fftshift(ifft(Bzt, 1), 1)
    df = 1 / (Nt * dt)          # THz
    var_ram = gamma^2 * sum(abs2.(Bzω) .* Cω) * (df * 1e12) * (save_every * dz) * 1e-24   # Riemann sum over saved z
    n_photons = sum(abs2.(A0)) * dt * 1e-12 / (hbar * omega0 * 1e12)
    n_window = Ew * dt * 1e-12 / (hbar * omega0 * 1e12)
    return (var_vac=var_vac, var_ram=var_ram, t_peak=t[k], J=J, amp=abs(A[k]), n_in=n_photons, n_window=n_window,
            E_window_frac=Ew / sum(abs2.(A)))
end

outlines = String[]
function report(s)
    println(s); flush(stdout); push!(outlines, s)
end

# 1. Validation: N = 1, full-pulse centroid against SPT (notebook formulas, symmetrized Raman bath); skipped when N list given
isempty(ARGS) && let T0 = 0.1, Nt = 8192, width = 160 * 0.1
    LD = T0^2 / abs(beta2); P0 = abs(beta2) / (gamma * T0^2)
    F0 = 2 * kb * 300 / hbar * (32e-15) / (1 + 32^2 / 12.2^2) * 0.18
    for zfac in (1.0, 2.0, 4.0)
        r = jitter(sqrt(P0), T0, zfac * LD, round(Int, 100 * zfac), Nt, width, a -> Inf)
        spt_vac = (T0 * 1e-12)^2 * (pi^2 / 12 + zfac^2 / 3) / r.n_in
        spt_ram = (16 / 45) * (T0 * 1e-12)^2 * F0 * zfac^3 / r.n_in
        report(@sprintf("VALID N=1 T0=%.0f fs z/LD=%.1f: var_vac=%.4e (SPT %.4e, ratio %.4f)  var_ram=%.4e (SPT %.4e, ratio %.4f)",
                        T0 * 1e3, zfac, r.var_vac, spt_vac, r.var_vac / spt_vac, r.var_ram, spt_ram, r.var_ram / spt_ram))
    end
end

# 2. Leading soliton after fission, N = 2, 3, 4 at T0 = 100 fs, L = 4 L_D / N; baseline isolated soliton of width
#    T1 = T0/(2 eta1) (eta1 from the h3 runs) over the same physical length.
for N in (isempty(ARGS) ? (2, 3, 4) : Tuple(parse.(Int, ARGS)))
    T0 = 0.1; Nt = 8192; width = 160 * T0
    LD = T0^2 / abs(beta2); P0 = N^2 * abs(beta2) / (gamma * T0^2); L = 4.0 / N * LD
    nsteps = round(Int, (4.0 / N) / (0.4 / (N * (2N - 1))^2))
    r = jitter(sqrt(P0), T0, L, nsteps, Nt, width, a -> max(6.0 / (N * a / sqrt(P0)), 1.0) * T0; save_every=4)
    # leading-soliton amplitude in soliton units ~ 2 eta1: use the measured peak amplitude
    amp_n = N * r.amp / sqrt(P0)
    P1 = r.amp^2; T1 = sqrt(abs(beta2) / (gamma * P1))    # fundamental soliton with the leading soliton's peak power
    nst1 = 40 * max(round(Int, L / (T1^2 / abs(beta2)) / 0.02 / 40), 5)
    rb = jitter(sqrt(P1), T1, L, nst1, Nt, width, a -> Inf; save_every=8)
    report(@sprintf("N=%d T0=100 fs L=%.3f m: lead var_vac=%.4e var_ram=%.4e (t_pk=%.3f ps, amp_n=%.3f, window photons %.3e of %.3e) | isolated T1=%.2f fs: var_vac=%.4e var_ram=%.4e (photons %.3e) | ratios vac %.3f ram %.3f total %.3f",
                    N, L, r.var_vac, r.var_ram, r.t_peak, amp_n, r.n_window, r.n_in, T1 * 1e3, rb.var_vac, rb.var_ram, rb.n_in,
                    r.var_vac / rb.var_vac, r.var_ram / rb.var_ram, (r.var_vac + r.var_ram) / (rb.var_vac + rb.var_ram)))
end
open(joinpath(@__DIR__, isempty(ARGS) ? "h5_jitter.out" : "h5_jitter_N" * join(ARGS, "_") * ".out"), "w") do io
    foreach(l -> println(io, l), outlines)
end
