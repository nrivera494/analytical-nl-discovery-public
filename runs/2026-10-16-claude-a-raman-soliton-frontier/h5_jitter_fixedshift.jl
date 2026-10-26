# H5, fixed-shift variant: as h5_jitter.jl, but the isolated-soliton baseline is propagated until its spectral centroid
# reaches the leading soliton's red shift (the card's 'fixed shift' comparison), not over the same length.
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

"""Spectral centroid (rad/ps, solver convention) of the windowed field around the tallest peak; and the isolated-soliton
centroid trajectory versus z."""
function centroid_shift(A, t, hw)
    k = argmax(abs.(A)); w = Float64.(abs.(t .- t[k]) .<= hw)
    Aw = fftshift(ifft(A .* w)); Om = 2pi .* fftshift(fftfreq(length(t), 1 / (t[2] - t[1])))
    return sum(Om .* abs2.(Aw)) / sum(abs2.(Aw))
end

for N in (isempty(ARGS) ? (2, 3, 4, 5) : Tuple(parse.(Int, ARGS)))
    T0 = parse(Float64, get(ENV, "H5_T0_FS", "100")) / 1000; Nt = T0 <= 0.1 ? 8192 : 16384; width = 160 * T0   # keeps dt <= 2 fs (Raman kernel)
    LD = T0^2 / abs(beta2); P0 = N^2 * abs(beta2) / (gamma * T0^2); L = 4.0 / N * LD
    nsteps = round(Int, (4.0 / N) / (0.4 / (N * (2N - 1))^2))
    grid = TimeGrid(Nt, width); domain = MMGNLSEDomain(degrees_of_freedom(:time), grid); t = time_axis(grid)
    hwr = a -> max(6.0 / (N * a / sqrt(P0)), 1.0) * T0
    # leading soliton: jitter at L and its red shift
    r = jitter(sqrt(P0), T0, L, nsteps, Nt, width, hwr; save_every=4)
    pars = MMGNLSEParameters(domain; length=L, beta=TaylorBeta(reshape([0.0, 0.0, beta2], :, 1)), S=1 / Aeff,
                             n2=material.n2, omega0=omega0, raman=AgarwalRaman())
    A0 = zeros(ComplexF64, Nt, 1, 1); A0[:, 1, 1] = sqrt(P0) .* sech.(t ./ T0)
    A = get_temporal_field(solve_mmgnlse(A0, pars, L / nsteps))[:, 1, 1]
    shiftL = centroid_shift(A, t, hwr(maximum(abs.(A))))
    # isolated soliton with the leading soliton's peak power: find the length at which its centroid reaches shiftL
    P1 = r.amp^2; T1 = sqrt(abs(beta2) / (gamma * P1)); LD1 = T1^2 / abs(beta2)
    Lmax = 4 * L; nst = 40 * max(round(Int, Lmax / LD1 / 0.02 / 40), 5); dz1 = Lmax / nst
    pb = MMGNLSEParameters(domain; length=Lmax, beta=TaylorBeta(reshape([0.0, 0.0, beta2], :, 1)), S=1 / Aeff,
                           n2=material.n2, omega0=omega0, raman=AgarwalRaman())
    B0 = zeros(ComplexF64, Nt, 1, 1); B0[:, 1, 1] = sqrt(P1) .* sech.(t ./ T1)
    sb = solve_mmgnlse(B0, pb, dz1; saveat=8 * dz1)
    zs = sb.z; Bz = get_temporal_field(sb; z=:all)
    shifts = [centroid_shift(vec(selectdim(Bz, ndims(Bz), j)), t, Inf) for j in eachindex(zs)]
    j = findfirst(x -> abs(x) >= abs(shiftL), shifts)
    if j === nothing
        report(@sprintf("N=%d T0=%.0f fs: isolated soliton does not reach the leading soliton's shift %.3f rad/ps within 4L", N, T0 * 1e3, shiftL)); continue
    end
    Lb = zs[j]; nb = max(round(Int, Lb / dz1 / 8) * 8, 8)
    rb = jitter(sqrt(P1), T1, nb * dz1, nb, Nt, width, a -> Inf; save_every=8)
    report(@sprintf("FIXEDSHIFT N=%d T0=%.0f fs: lead L=%.3f m shift=%.3f rad/ps var_vac=%.4e var_ram=%.4e | isolated T1=%.2f fs reaches the shift at L_b=%.3f m: var_vac=%.4e var_ram=%.4e | ratios vac %.3f ram %.3f total %.3f",
                    N, T0 * 1e3, L, shiftL, r.var_vac, r.var_ram, T1 * 1e3, nb * dz1, rb.var_vac, rb.var_ram,
                    r.var_vac / rb.var_vac, r.var_ram / rb.var_ram, (r.var_vac + r.var_ram) / (rb.var_vac + rb.var_ram)))
end
open(joinpath(@__DIR__, "h5_jitter_fixedshift_T" * get(ENV, "H5_T0_FS", "100") * "_N" * join(isempty(ARGS) ? ["2", "3", "4", "5"] : ARGS, "_") * ".out"), "w") do io
    foreach(l -> println(io, l), outlines)
end
