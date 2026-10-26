# Shared setup for run 2026-10-08-claude-b.5-solver-twomode-check.
#
# Two-mode incoherent cross-phase model (normalized soliton units)
#   i a_z + a_tt/2 + (|a|^2 + |b|^2) a = 0
#   i b_z + i delta b_t + b_tt/2 + (|a|^2 + C22 |b|^2) b = 0
# emulated with FastDifferentiableMMNLO (package PulsePropagation, solver/).
#
# Physical scaling: T0 = 1 ps, beta2 = -1 ps^2/m (L_D = 1 m), gamma = n2*omega0*S0/c
# = 1 W^-1 m^-1 (P0 = |beta2|/(gamma T0^2) = 1 W). omega0 is a free numerical
# parameter; the solver's nonlinear prefactor n2*(omega0+Omega)/c contains
# self-steepening with s = 1/(omega0 T0), and the photon weights are
# 1/(hbar (omega0+Omega)). The normalized model is the limit omega0*T0 -> Inf.
#
# Overlap tensor: S1111 = S0, S2222 = C22*S0, all elements with two 1s and two
# 2s = S0/2 (symmetric = true). With symmetric = false the two coherent
# elements S[1,2,2,1] and S[2,1,1,2] (the A2^2 A1^* and A1^2 A2^* terms in the
# solver's N_p = sum S[p,l,m,n] A_l A_m conj(A_n)) are set to zero, which
# removes coherent four-wave mixing exactly (used only as a cross-check).
# Coherent terms in the symmetric tensor are suppressed by a propagation-constant
# offset Delta beta0 = kappa / L_D on mode 2 (row 1 of TaylorBeta).

using PulsePropagation
using FFTW
using LinearAlgebra
using Printf

const C_LIGHT = 2.99792458e-4  # m/ps, solver unit system

Base.@kwdef struct Case
    label::String = ""
    p2::Float64 = 0.0
    C22::Float64 = 0.5
    delta::Float64 = 0.0
    zeta::Float64 = 2.0
    kappa::Float64 = 1.0e4          # Delta beta0 * L_D
    symmetric::Bool = true          # keep coherent elements S1221, S2112
    Nt::Int = 256
    window::Float64 = 40.0          # in units of T0
    dz::Float64 = 1.0e-5            # in units of L_D
    omega0T0::Float64 = 1.0e6       # self-steepening parameter s = 1/omega0T0
    kmax_list::Vector{Int} = [3, 4, 5, 6, 7]
end

const T0 = 1.0       # ps
const BETA2 = -1.0   # ps^2/m
const GAMMA = 1.0    # W^-1 m^-1
const S0 = 1.0e10    # m^-2 (arbitrary; n2 is set to give GAMMA)

L_D() = T0^2 / abs(BETA2)
P0() = abs(BETA2) / (GAMMA * T0^2)

function overlap_tensor(C22::Real; symmetric::Bool=true)
    S = zeros(Float64, 2, 2, 2, 2)
    S[1, 1, 1, 1] = S0
    S[2, 2, 2, 2] = C22 * S0
    for idx in ((1, 1, 2, 2), (1, 2, 1, 2), (1, 2, 2, 1),
                (2, 2, 1, 1), (2, 1, 2, 1), (2, 1, 1, 2))
        S[idx...] = S0 / 2
    end
    if !symmetric
        S[1, 2, 2, 1] = 0.0
        S[2, 1, 1, 2] = 0.0
    end
    return S
end

function build(case::Case)
    LD = L_D()
    time_grid = TimeGrid(case.Nt, case.window * T0)
    domain = MMGNLSEDomain(degrees_of_freedom(:time, :space), time_grid)
    omega0 = case.omega0T0 / T0
    n2 = GAMMA * C_LIGHT / (omega0 * S0)
    betas = zeros(Float64, 3, 2)                 # rows: beta0, beta1, beta2
    betas[3, :] .= BETA2
    betas[1, 2] = case.kappa / LD                # Delta beta0 on mode 2 (1/m)
    betas[2, 2] = case.delta * abs(BETA2) / T0   # Delta beta1 on mode 2 (ps/m)
    parameters = MMGNLSEParameters(domain;
        length=case.zeta * LD,
        beta=TaylorBeta(betas),
        S=overlap_tensor(case.C22; symmetric=case.symmetric),
        n2=n2,
        omega0=omega0,
        raman=NoRaman())
    t = time_axis(time_grid)
    Omega = frequency_axis(time_grid)           # centered, rad/ps
    p1 = 1.0 - case.p2
    Sigma = p1^2 + 2p1 * case.p2 + case.C22 * case.p2^2
    initial = zeros(ComplexF64, case.Nt, 2, 1)
    initial[:, 1, 1] .= sqrt(P0() * p1 / Sigma) .* sech.(t ./ T0)
    initial[:, 2, 1] .= sqrt(P0() * case.p2 / Sigma) .* sech.(t ./ T0)
    return (; parameters, t, Omega, initial, Sigma, LD)
end

"Bin index k with Omega_k = k * 2pi/window; asserts the axis is on the grid."
function bin_index(Omega, window)
    dOmega = 2pi / window
    k = round.(Int, Omega ./ dOmega)
    maximum(abs.(Omega .- k .* dOmega)) < 1e-9 * dOmega ||
        error("frequency axis is not on the k*2pi/window grid")
    count(==(0), k) == 1 || error("no unique Omega=0 bin")
    return k
end

bandpass(k, kmax) = Float64.(abs.(k) .<= kmax)

"Forward solve; returns solution and wall time."
function forward(case::Case, setup)
    t0 = time()
    sol = solve_mmgnlse(setup.initial, setup.parameters, case.dz * setup.LD)
    return sol, time() - t0
end

"""
Fano factor of the all-mode bandpassed photon number for each kmax, from the
discrete RK4IP adjoint (exact derivative of the fixed-step forward map).
Var(N) = sum |dN/dconj(B(0))|^2 for coherent (vacuum-noise) inputs, B in photon
units, as in solver/example_notebooks/squeezing_spectral_filter.ipynb.
"""
function fano_all(case::Case, setup, sol)
    k = bin_index(setup.Omega, case.window * T0)
    out = Dict{Int,NamedTuple}()
    for kmax in case.kmax_list
        filt = bandpass(k, kmax)
        obs = SpectralPhotonNumber(filter=filt, modes=:all)
        N = value(obs, sol)
        lambda_L = terminal_condition(obs, sol)
        t0 = time()
        adj = solve_adjoint(lambda_L, setup.parameters, case.dz * setup.LD;
                            forward_solution=sol, adjoint_mode=:discrete_rk4ip)
        sens = get_spectral_field(adj; units=:photon)
        var_mode = [sum(abs2, @view sens[:, m, :]) for m in 1:size(sens, 2)]
        F = sum(var_mode) / N
        out[kmax] = (; N, F, var_mode1=var_mode[1], var_mode2=var_mode[2],
                     adj_time=time() - t0)
    end
    return out
end

"Diagnostics of the forward solution: energies, peak powers, widths."
function diagnostics(setup, sol)
    A0 = get_temporal_field(sol; z=:initial)
    AL = get_temporal_field(sol; z=:final)
    dt = setup.t[2] - setup.t[1]
    E0 = [sum(abs2, A0[:, m, 1]) * dt for m in 1:2]
    EL = [sum(abs2, AL[:, m, 1]) * dt for m in 1:2]
    pk0 = [maximum(abs2, A0[:, m, 1]) for m in 1:2]
    pkL = [maximum(abs2, AL[:, m, 1]) for m in 1:2]
    return (; E0, EL, pk0, pkL)
end
