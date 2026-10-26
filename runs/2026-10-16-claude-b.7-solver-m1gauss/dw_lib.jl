# Shared setup for run 2026-10-16-claude-b.7-solver-dwyield (agent claude-b.7).
#
# Normalized model (Roy, Bhadra & Agrawal, PRA 79, 023824 (2009) convention):
#   i u_xi + (1/2) u_tautau + N^2 |u|^2 u = i delta3 u_tautautau,
#   delta3 = beta3 / (6 |beta2| T0), xi = z / L_D, tau = t / T0, beta2 < 0, beta3 > 0.
# Physics Fourier convention u = (1/2pi) int uhat(w) exp(-i w tau) dw, w = Omega T0 > 0 blue;
# linear phase uhat ~ exp(i D(w) xi), D(w) = delta3 w^3 - w^2/2, w_z = 1/(6 delta3).
#
# Realized in FastDifferentiableMMNLO (PulsePropagation, submodule solver/, read-only) with
#   L_D = 1 m:  beta2 = -T0^2 ps^2/m, beta3 = 6 delta3 T0^3 ps^3/m, gamma = 1 /W/m,
#   P0 = N^2 W, length = xi m, n2 = gamma c / (omega0 S), S = 1e10 m^-2,
#   omega0 T0 = 1e6 (self-steepening and (omega0+Omega)/omega0 slope suppressed).
# Solver convention (checked in stage "lin"): A(t) = sum_k A_k exp(-i Omega_k t),
#   A_k = ifft(A(t)), linear step exp(i (beta2/2 Omega^2 + beta3/6 Omega^3) dz).
# Model M1 adds AgarwalRaman (Blow-Wood single damped oscillator,
#   h(t) = (tau1^2+tau2^2)/(tau1 tau2^2) exp(-t/tau2) sin(t/tau1), f_R = 0.18,
#   tau1 = 12.2 fs, tau2 = 32 fs); nonlinearity (1-f_R)|A|^2 A + f_R A (h * |A|^2).

using PulsePropagation
using FFTW
using LinearAlgebra
using Printf
using NPZ

const C_LIGHT = 2.99792458e-4    # m/ps (solver unit system)

Base.@kwdef struct DWCase
    label::String = ""
    pulse::Symbol = :sech        # :sech -> u0 = sech(tau); :gauss -> exp(-tau^2/2)
    N::Float64 = 2.0
    delta3::Float64 = 0.02
    xi::Float64 = 4.0
    T0::Float64 = 1.0            # ps
    window_T0::Float64 = 160.0
    Nt::Int = 4096
    nsteps::Int = 4000
    raman::Bool = false
    omega0T0::Float64 = 1.0e6
    gamma::Float64 = 1.0         # 1/(W m)
    Sinv::Float64 = 1.0e10       # 1/Aeff, m^-2
    save_xi::Vector{Float64} = Float64[]
    gate_T0::Float64 = 8.0
    band_delta3::Float64 = NaN   # if set, band edge w_z uses this delta3 (reference runs)
end

beta2(c::DWCase) = -c.T0^2                       # L_D = T0^2/|beta2| = 1 m
beta3(c::DWCase) = 6 * c.delta3 * abs(beta2(c)) * c.T0
P0(c::DWCase) = c.N^2 * abs(beta2(c)) / (c.gamma * c.T0^2)
band_d3(c::DWCase) = isnan(c.band_delta3) ? c.delta3 : c.band_delta3
wz(c::DWCase) = 1 / (6 * band_d3(c))
dz(c::DWCase) = c.xi / c.nsteps                  # m (L_D = 1 m)

function build(c::DWCase; linear::Bool=false)
    grid = TimeGrid(c.Nt, c.window_T0 * c.T0)
    domain = MMGNLSEDomain(degrees_of_freedom(:time), grid)
    omega0 = c.omega0T0 / c.T0
    n2 = linear ? 0.0 : c.gamma * C_LIGHT / (omega0 * c.Sinv)
    betas = reshape([0.0, 0.0, beta2(c), beta3(c)], :, 1)
    params = MMGNLSEParameters(domain;
        length=c.xi,
        beta=TaylorBeta(betas),
        S=c.Sinv,
        n2=n2,
        omega0=omega0,
        raman=c.raman ? AgarwalRaman(fraction=0.18, tau1=0.0122, tau2=0.0320) : NoRaman())
    t = time_axis(grid)
    Omega = frequency_axis(grid)
    tau = t ./ c.T0
    w = Omega .* c.T0
    u0 = c.pulse === :sech ? sech.(tau) :
         c.pulse === :gauss ? exp.(-tau .^ 2 ./ 2) : error("unknown pulse")
    initial = zeros(ComplexF64, c.Nt, 1, 1)
    initial[:, 1, 1] .= sqrt(P0(c)) .* u0
    return (; params, t, tau, Omega, w, initial)
end

"Centered spectrum in the package convention Aw = fftshift(ifft(At))."
spec(At::AbstractVector) = fftshift(ifft(At))

"""Global band maximum and largest interior local maximum of S over the band."""
function band_peak(w, S, band)
    idx = findall(band)
    i0, i1 = first(idx), last(idx)
    j = idx[argmax(S[idx])]
    at_edge = (j == i0) || (j == i1)
    jl = 0
    best = -Inf
    for i in (i0 + 1):(i1 - 1)
        if S[i] >= S[i - 1] && S[i] >= S[i + 1] && S[i] > best
            jl = i
            best = S[i]
        end
    end
    return (; j, at_edge, jl)
end

db(x) = x > 0 ? 10 * log10(x) : -Inf

"Invariants in the normalized continuous units (E = int|u|^2 dtau, P = <w>, H)."
function invariants(c::DWCase, At::AbstractVector)
    Twin = c.window_T0
    u = At ./ sqrt(P0(c))
    cw = ifft(u)                          # u_j = sum_k cw_k exp(-i w_k tau_j)
    wraw = ifftshift(c.T0 .* frequency_axis(TimeGrid(c.Nt, c.window_T0 * c.T0)))
    S = abs2.(cw)
    E = Twin * sum(S)
    P = sum(wraw .* S) / sum(S)
    K = wraw .^ 2 ./ 2 .- c.delta3 .* wraw .^ 3   # K = -D
    dtau = Twin / c.Nt
    H = Twin * sum(K .* S) - (c.N^2 / 2) * sum(abs2.(u) .^ 2) * dtau
    return (; E, P, H)
end

"""
All observables of one saved field At (time domain, power units) relative to the
input field At0. Hard gate: field set to zero for |tau| < gate_T0 (definition).
Smooth-gate variant (diagnostic only): multiply by (1 + tanh((|tau| - gate_T0)/1))/2.
"""
function observables(c::DWCase, s, At0::AbstractVector, At::AbstractVector)
    w = s.w
    band = w .>= wz(c)
    S0 = abs2.(spec(At0))
    Ein = sum(S0)
    S = abs2.(spec(At))
    etaB = sum(S[band]) / Ein
    hard = Float64.(abs.(s.tau) .>= c.gate_T0)
    Sg = abs2.(spec(At .* hard))
    etaDW = sum(Sg[band]) / Ein
    smooth = 0.5 .* (1 .+ tanh.((abs.(s.tau) .- c.gate_T0) ./ 1.0))
    Sgs = abs2.(spec(At .* smooth))
    etaDW_smooth = sum(Sgs[band]) / Ein
    pk = band_peak(w, S, band)
    pkg = band_peak(w, Sg, band)
    maxin = maximum(S0)
    maxout = maximum(S)
    jl = pk.jl
    # numerical-health diagnostics
    nyq = maximum(abs.(w))
    hi = abs.(w) .> 0.8 * nyq
    nedge = max(1, c.Nt ÷ 50)
    P = abs2.(At)
    edge_t = maximum(P[[1:nedge; end-nedge+1:end]]) / maximum(P)
    return Dict{String,Any}(
        "w_z" => wz(c),
        "eta_B" => etaB,
        "eta_DW" => etaDW,
        "eta_DW_smoothgate" => etaDW_smooth,
        "E_ratio_spectral" => sum(S) / Ein,
        "peak_band_max_w" => w[pk.j],
        "peak_band_max_at_band_edge" => pk.at_edge,
        "peak_band_max_dB_rel_input_max" => db(S[pk.j] / maxin),
        "peak_band_max_dB_rel_output_max" => db(S[pk.j] / maxout),
        "peak_band_max_dnuT0" => w[pk.j] / (2pi),
        "peak_local_w" => jl > 0 ? w[jl] : NaN,
        "peak_local_dB_rel_input_max" => jl > 0 ? db(S[jl] / maxin) : NaN,
        "peak_local_dB_rel_output_max" => jl > 0 ? db(S[jl] / maxout) : NaN,
        "peak_local_dnuT0" => jl > 0 ? w[jl] / (2pi) : NaN,
        "gated_peak_w" => w[pkg.j],
        "gated_peak_dB_rel_input_max" => db(Sg[pkg.j] / maxin),
        "output_max_w" => w[argmax(S)],
        "spec_frac_above_0.8nyq" => sum(S[hi]) / sum(S),
        "spec_max_dB_above_0.8nyq_rel_max" => db(maximum(S[hi]) / maxout),
        "time_edge_power_ratio" => edge_t,
        "peak_power_ratio" => maximum(P) / P0(c),
        "t_peak_T0" => s.tau[argmax(P)],
    )
end

function case_record(c::DWCase)
    return Dict{String,Any}(
        "label" => c.label, "pulse" => string(c.pulse), "N" => c.N,
        "delta3" => c.delta3, "band_delta3" => band_d3(c), "xi_end" => c.xi,
        "T0_ps" => c.T0, "window_T0" => c.window_T0, "Nt" => c.Nt,
        "dtau" => c.window_T0 / c.Nt, "w_max" => pi * c.Nt / c.window_T0,
        "nsteps" => c.nsteps, "dxi" => c.xi / c.nsteps, "raman" => c.raman,
        "raman_model" => c.raman ? "AgarwalRaman(fraction=0.18,tau1=0.0122ps,tau2=0.0320ps)" : "NoRaman",
        "dt_fs" => c.window_T0 * c.T0 / c.Nt * 1e3,
        "omega0T0" => c.omega0T0, "beta2_ps2_per_m" => beta2(c),
        "beta3_ps3_per_m" => beta3(c), "gamma_per_W_m" => c.gamma, "P0_W" => P0(c),
        "gate_T0" => c.gate_T0)
end

# ---------------- JSON lines ----------------
jsonval(x::AbstractString) = "\"" * escape_string(x) * "\""
jsonval(x::Bool) = x ? "true" : "false"
jsonval(x::Integer) = string(x)
jsonval(x::AbstractFloat) = isfinite(x) ? repr(Float64(x)) : "null"
jsonval(x::Nothing) = "null"
jsonval(x::Symbol) = jsonval(string(x))
jsonval(x::AbstractVector) = "[" * join(jsonval.(x), ",") * "]"
jsonval(x::AbstractDict) =
    "{" * join(["\"$(k)\":" * jsonval(v) for (k, v) in sort(collect(x); by=first)], ",") * "}"
jsonval(x::NamedTuple) =
    "{" * join(["\"$(k)\":" * jsonval(v) for (k, v) in pairs(x)], ",") * "}"

"""
Run one case: forward RK4IP (Float64, fixed step), observables at every saved
plane, invariants at start and end. Appends JSON lines to `results` and saves
the input/output spectra (and gated output spectrum) to `rawdir` as npz.
"""
function run_case(c::DWCase; stage::String, results::String, rawdir::String,
                  save_raw::Bool=true)
    s = build(c)
    saveat = isempty(c.save_xi) ? nothing : c.save_xi
    t0 = time()
    sol = solve_mmgnlse(s.initial, s.params, dz(c); saveat=saveat)
    twall = time() - t0
    At0 = sol.fields[:, 1, 1, 1]
    inv0 = invariants(c, At0)
    nsteps_actual = length(sol.cache.integration_z) - 1
    recs = Dict{String,Any}[]
    for (jz, z) in enumerate(sol.z)
        At = sol.fields[:, 1, 1, jz]
        rec = case_record(c)
        rec["stage"] = stage
        rec["xi"] = z
        rec["nsteps_actual"] = nsteps_actual
        rec["t_wall_s"] = twall
        merge!(rec, observables(c, s, At0, At))
        inv = invariants(c, At)
        rec["E"] = inv.E
        rec["P_mean_w"] = inv.P
        rec["H"] = inv.H
        rec["E0"] = inv0.E
        rec["P0_mean_w"] = inv0.P
        rec["H0"] = inv0.H
        rec["E_rel_drift"] = inv.E / inv0.E - 1
        rec["P_abs_drift"] = inv.P - inv0.P
        rec["H_rel_drift"] = inv.H / inv0.H - 1
        push!(recs, rec)
        open(results, "a") do io
            println(io, jsonval(rec))
        end
    end
    if save_raw
        fn = joinpath(rawdir, @sprintf("%s_%s.npz", stage, c.label))
        Sin = abs2.(spec(At0))
        AtL = sol.fields[:, 1, 1, end]
        hard = Float64.(abs.(s.tau) .>= c.gate_T0)
        npzwrite(fn, Dict("w" => collect(s.w), "tau" => collect(s.tau),
                          "S_in" => Sin, "S_out" => abs2.(spec(AtL)),
                          "S_out_gated" => abs2.(spec(AtL .* hard)),
                          "P_out" => abs2.(AtL),
                          "z_saved" => collect(Float64.(sol.z))))
    end
    return recs, sol, s
end
