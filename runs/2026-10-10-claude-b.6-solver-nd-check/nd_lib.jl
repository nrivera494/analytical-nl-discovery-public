# Shared setup for run 2026-10-10-claude-b.6-solver-nd-check.
#
# Scalar single-mode NLSE in normal dispersion, soliton units tau = T/T0, xi = z/L_D:
#   i u_xi - (1/2) u_tautau + N^2 |u|^2 u = 0,  u(tau, 0) = exp(-tau^2/2),
# realized physically in FastDifferentiableMMNLO (package PulsePropagation, solver/).
# The solver propagates dA/dz = i beta(Omega) A + i n2 (omega0 + Omega)/c * S * F[...],
# so gamma = n2 omega0 S / c and self-steepening has s = 1/(omega0 T0). Photon
# weights are 1/(hbar (omega0 + Omega)) per bin. Kerr-only "soliton-unit" cases
# use omega0 T0 = 1e6 (self-steepening and photon-weight slope suppressed).
#
# Readout: photon number N_T in the bins k of a binary filter, Omega_k T0 = k 2pi/40.
# F = Var(N_T)/<N_T> for linearized vacuum noise of the coherent input,
# Var = sum |dN/dconj(B(0))|^2 (B in photon units) from the discrete RK4IP adjoint,
# as in solver/example_notebooks/squeezing_spectral_filter.ipynb.

using PulsePropagation
using FFTW
using LinearAlgebra
using Printf
using TOML

const C_LIGHT = 2.99792458e-4                    # m/ps (solver unit system)
const HBAR = 1.054571817e-34
const OMEGA0_1550 = 2pi * C_LIGHT / 1550e-9      # rad/ps

include(joinpath(@__DIR__, "raman_bath_spectrum.jl"))   # raman_langevin_spectrum_coth

Base.@kwdef struct NDCase
    label::String = ""
    N::Float64 = 10.0
    zr::Float64 = 0.7            # z / xi_wb(N) / L_D
    T0::Float64 = 1.0            # ps
    beta2::Float64 = 1.0         # ps^2/m (> 0, normal dispersion)
    gamma::Float64 = 1.0         # 1/(W m)
    omega0::Float64 = 1.0e6      # rad/ps
    window_T0::Float64 = 40.0
    Nt::Int = 512
    nsteps::Int = 4000
    raman::Bool = false          # AgarwalRaman() (fraction 0.18, 12.2 fs, 32 fs)
    Sinv::Float64 = 1.0e10       # 1/Aeff in m^-2; n2 is derived from gamma
end

xi_wb(N) = 1 / sqrt(4N^2 * exp(-1.5) - 1)
L_D(c::NDCase) = c.T0^2 / c.beta2
P0(c::NDCase) = c.N^2 * c.beta2 / (c.gamma * c.T0^2)
zlen(c::NDCase) = c.zr * xi_wb(c.N) * L_D(c)
dzstep(c::NDCase) = zlen(c) / c.nsteps
window(c::NDCase) = c.window_T0 * c.T0

"Bin index k with Omega_k = k * 2pi/window; asserts the axis is on the grid."
function bin_index(Omega, win)
    dOmega = 2pi / win
    k = round.(Int, Omega ./ dOmega)
    maximum(abs.(Omega .- k .* dOmega)) < 1e-9 * dOmega ||
        error("frequency axis is not on the k*2pi/window grid")
    count(==(0), k) == 1 || error("no unique Omega=0 bin")
    return k
end

function build(c::NDCase)
    grid = TimeGrid(c.Nt, window(c))
    domain = MMGNLSEDomain(degrees_of_freedom(:time), grid)
    n2 = c.gamma * C_LIGHT / (c.omega0 * c.Sinv)
    betas = reshape([0.0, 0.0, c.beta2], :, 1)
    params = MMGNLSEParameters(domain;
        length=zlen(c),
        beta=TaylorBeta(betas),
        S=c.Sinv,
        n2=n2,
        omega0=c.omega0,
        raman=c.raman ? AgarwalRaman() : NoRaman())
    t = time_axis(grid)
    Omega = frequency_axis(grid)               # centered, rad/ps
    k = bin_index(Omega, window(c))
    initial = zeros(ComplexF64, c.Nt, 1, 1)
    initial[:, 1, 1] .= sqrt(P0(c)) .* exp.(-(t ./ c.T0) .^ 2 ./ 2)
    dt = t[2] - t[1]
    return (; params, t, Omega, k, initial, dt, n2)
end

function load_filters(path=joinpath(@__DIR__, "filters.toml"))
    d = TOML.parsefile(path)
    out = Dict{String,Dict{String,Vector{Int}}}()
    for (key, v) in d
        out[key] = Dict(name => Int.(v[name])
                        for name in ("best_binary_bins", "best_interval_bins"))
    end
    return out
end

"Binary mask on the centered frequency axis; mirror=true uses bins -k."
function filter_mask(k, bins; mirror::Bool=false)
    s = Set(mirror ? -bins : bins)
    f = Float64[(ki in s) ? 1.0 : 0.0 for ki in k]
    Int(sum(f)) == length(bins) || error("some filter bins are not on the grid")
    return f
end

"Physical photon weights (s/J per bin, centered) for carrier omega0 (rad/ps)."
photon_w(c::NDCase, omega0) =
    Float64.(PulsePropagation.photon_bin_weights(c.Nt, window(c) / c.Nt,
                                                  omega0 / (2pi); shifted=true))

function forward(c::NDCase, setup; saveat=nothing)
    t0 = time()
    sol = solve_mmgnlse(setup.initial, setup.params, dzstep(c); saveat=saveat)
    return sol, time() - t0
end

"""
F for one binary filter from the discrete RK4IP adjoint.

weights = nothing: observable and input vacuum in the solver's own photon units
(1/(hbar(omega0_run + Omega))).
weights = w (centered vector): observable = sum filt * w * |A|^2 and input vacuum
in the photon units defined by w (used to count photons at the physical carrier
in a run whose omega0 is a numerical device).
"""
function fano(c::NDCase, setup, sol, filt; weights=nothing, saveat=nothing)
    wrun = photon_w(c, c.omega0)
    eff = weights === nothing ? filt :
          [wrun[i] > 0 ? filt[i] * weights[i] / wrun[i] : 0.0 for i in eachindex(filt)]
    obs = SpectralPhotonNumber(filter=eff, modes=:all)
    Nmean = value(obs, sol)
    lam = terminal_condition(obs, sol)
    t0 = time()
    adj = solve_adjoint(lam, setup.params, dzstep(c); forward_solution=sol,
                        adjoint_mode=:discrete_rk4ip, saveat=saveat)
    tadj = time() - t0
    lam0 = get_spectral_field(adj; z=:initial, units=:power)[:, 1, 1]
    w = weights === nothing ? wrun : weights
    sens = [w[i] > 0 ? lam0[i] / sqrt(w[i]) : zero(ComplexF64) for i in eachindex(w)]
    var = sum(abs2, sens)
    if weights === nothing
        # cross-check against the solver's own photon-unit conversion
        sens_solver = get_spectral_field(adj; z=:initial, units=:photon)[:, 1, 1]
        var2 = sum(abs2, sens_solver)
        abs(var2 - var) <= 1e-12 * var || error("photon-unit conversion mismatch")
    end
    return (; N=Nmean, var, F=var / Nmean, adj, tadj)
end

"""
Raman Langevin variance of N_T from the forward and adjoint trajectories saved
at every step, contracted as in the squeezing notebook (gpt-b branch version):
  B(t,z) = -2 Im(A(t,z) conj(lambda(t,z)))   (power units, time domain)
  Var_R = gamma^2 * sum_z w_z * sum_omega |ifft(B)|^2 C(omega) * df_Hz
`ssweight = true` multiplies the spectral adjoint by the solver's nonlinear
prefactor ratio (1 + Omega/omega0) * damped_freq_window before forming B, i.e.
injects the noise through the same self-steepening operator as the delayed
Kerr term; `false` is the notebook formula. z weights: "rect" = nominal dz at
every saved plane (notebook); "trap" = trapezoid on the saved z grid.
"""
function raman_variance(c::NDCase, setup, sol, adj; Cw, ssweight::Bool)
    A = sol.fields
    Lam = adj.fields
    size(A) == size(Lam) || error("forward/adjoint saved shapes differ")
    zf = Float64.(sol.z)
    za = Float64.(adj.z)
    maximum(abs.(zf .- za)) <= 1e-12 * zlen(c) || error("z grids differ")
    nz = length(zf)
    Omega_raw = ifftshift(setup.Omega)
    damp = Float64.(PulsePropagation.damped_freq_window(c.Nt))
    fac = ssweight ? (1 .+ Omega_raw ./ c.omega0) .* damp : ones(c.Nt)
    s = zeros(nz)
    for j in 1:nz
        a = @view A[:, 1, 1, j]
        l = Vector{ComplexF64}(Lam[:, 1, 1, j])
        if ssweight
            l = fft(ifft(l) .* fac)
        end
        B = -2 .* imag.(a .* conj.(l))
        Bw = ifftshift(ifft(B))
        s[j] = sum(abs2.(Bw) .* Cw)
    end
    df_Hz = 1e12 / window(c)
    wtrap = zeros(nz)
    for j in 1:nz-1
        h = zf[j+1] - zf[j]
        wtrap[j] += h / 2
        wtrap[j+1] += h / 2
    end
    rect = c.gamma^2 * df_Hz * dzstep(c) * sum(s)
    trap = c.gamma^2 * df_Hz * sum(wtrap .* s)
    return (; rect, trap, nz)
end

"Centered Raman noise spectra for the case's grid."
function raman_spectra(c::NDCase)
    dt = window(c) / c.Nt
    f0 = c.omega0 / (2pi)
    coth300 = ifftshift(raman_langevin_spectrum_coth(c.Nt, dt, f0, c.gamma;
        raman_fraction=0.18, tau1=0.0122, tau2=0.0320, temperature_K=300.0))
    coth0 = ifftshift(raman_langevin_spectrum_coth(c.Nt, dt, f0, c.gamma;
        raman_fraction=0.18, tau1=0.0122, tau2=0.0320, temperature_K=0.0))
    legacy300 = ifftshift(PulsePropagation.raman_langevin_spectrum(c.Nt, dt, f0, c.gamma;
        raman_fraction=0.18, temperature_K=300.0))
    return (; coth300, coth0, legacy300)
end

"Diagnostics of the forward solution."
function diagnostics(c::NDCase, setup, sol)
    A0 = get_temporal_field(sol; z=:initial)[:, 1, 1]
    AL = get_temporal_field(sol; z=:final)[:, 1, 1]
    E0 = sum(abs2, A0)
    EL = sum(abs2, AL)
    wrun = photon_w(c, c.omega0)
    S0 = abs2.(get_spectral_field(sol; z=:initial)[:, 1, 1])
    SL = abs2.(get_spectral_field(sol; z=:final)[:, 1, 1])
    n0 = sum(wrun .* S0)
    nL = sum(wrun .* SL)
    nyq = maximum(abs.(setup.Omega))
    hi = abs.(setup.Omega) .> 0.5 * nyq
    k = setup.k
    edge = maximum(abs2, AL[[1:8; end-7:end]]) / maximum(abs2, AL)
    # spectral centroid and rms width in Omega T0
    cen = sum(setup.Omega .* SL) / sum(SL) * c.T0
    rms = sqrt(sum((setup.Omega .* c.T0 .- cen) .^ 2 .* SL) / sum(SL))
    return (; energy_rel_change=EL / E0 - 1, photon_rel_change=nL / n0 - 1,
            spec_frac_above_half_nyquist=sum(SL[hi]) / sum(SL),
            time_edge_power_ratio=edge, centroid_OmegaT0=cen, rms_OmegaT0=rms,
            peak_power_ratio_L=maximum(abs2, AL) / P0(c))
end
