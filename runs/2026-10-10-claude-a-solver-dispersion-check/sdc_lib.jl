# sdc_lib.jl -- solver dispersion check (claude-a.1, task T-20261010-claude-interactive-04)
#
# Linearized output quadrature covariance of a coherent Gaussian pulse after scalar
# Kerr propagation with weak GVD, computed with the solver's discrete RK4IP adjoint
# (PulsePropagation.solve_adjoint(...; adjoint_mode=:discrete_rk4ip)).
#
# Conventions (all from the solver):
#   * temporal field A_t on time_axis(grid) (centered grid, T=0 at index nt/2+1);
#   * centered spectrum A_w = fftshift(ifft(A_t));
#   * the discrete adjoint pulls a centered spectral cotangent lambda at z=L back to
#     a centered spectral cotangent c at z=0 with the real pairing
#     Re<lambda, dA_w(L)> = Re<c, dA_w(0)>  (checked here against finite differences).
# Quadratures: X_j = 2 Re(dA_t[j]) / sqrt(norm), Y_j = 2 Im(dA_t[j]) / sqrt(norm) with a
# constant norm = hbar*omega0/dt for every bin, so the coherent input has V_in = I.
# S maps [X(0); Y(0)] -> [X(L); Y(L)] (2N x 2N, real). V = S S^T.
using PulsePropagation, FFTW, LinearAlgebra, Printf, Random
const PP = PulsePropagation
const C_PS = 2.99792458e-4   # speed of light in m/ps

"""Build solver parameters. gamma = n2*omega0*S/c (checked numerically by the driver)."""
function make_case(; nt=512, window=16.0, beta2=0.0, L=1.0, gamma=0.01,
                   omega0=2π * 193.4 * 1000, overlap=1.0e10, Phi=5.0, T0=1.0)
    grid = TimeGrid(nt, window)
    dom = MMGNLSEDomain(degrees_of_freedom(:time), grid)
    n2 = gamma * C_PS / (omega0 * overlap)
    pars = MMGNLSEParameters(dom; length=L,
        beta=TaylorBeta(reshape([0.0, 0.0, beta2], 3, 1)),
        S=reshape([overlap], 1, 1, 1, 1), n2=n2, omega0=omega0, raman=NoRaman())
    P0 = Phi / (gamma * L)
    t = time_axis(grid)
    A0 = reshape(ComplexF64.(sqrt(P0) .* exp.(-t .^ 2 ./ (2T0^2))), nt, 1, 1)
    return (; grid, pars, A0, t, nt, window, beta2, L, gamma, omega0, overlap, n2, P0, Phi, T0)
end

forward(case, dz) = solve_mmgnlse(case.A0, case.pars, dz)   # RK4IP, Float64, fixed step

"""One row of S from one discrete-adjoint solve.
quad = :X or :Y selects the output quadrature of time bin j."""
function adjoint_row(case, sol, dz, j::Int, quad::Symbol)
    N = case.nt
    mu = quad === :X ? 1.0 + 0im : 0.0 + 1.0im
    ej = zeros(ComplexF64, N); ej[j] = 1
    lam_raw = mu .* conj.(fft(ej))               # Re(conj(lam).dA_w) = Re(conj(mu) dA_t[j])
    lam = reshape(fftshift(lam_raw), N, 1, 1)
    adj = solve_adjoint(lam, case.pars, dz; forward_solution=sol,
                        adjoint_mode=:discrete_rk4ip)
    c = vec(get_spectral_field(adj; z=:initial))  # centered cotangent at z=0
    d = fft(ifftshift(c)) ./ N                   # Re(conj(d).dA_t(0)) = same functional
    return vcat(real.(d), imag.(d))
end

function build_S(case, sol, dz; rows=nothing, verbose=true)
    N = case.nt
    S = zeros(2N, 2N)
    idx = rows === nothing ? collect(1:2N) : rows
    t0 = time()
    for (count, r) in enumerate(idx)
        j = r <= N ? r : r - N
        S[r, :] .= adjoint_row(case, sol, dz, j, r <= N ? :X : :Y)
        if verbose && (count % 128 == 0)
            @printf("    rows %d/%d  %.1f s\n", count, length(idx), time() - t0)
            flush(stdout)
        end
    end
    return S
end

"""Central finite-difference directional derivative of the noise-free solver output,
returned in the same real coordinates [Re dA_t; Im dA_t] as S acts on."""
function fd_direction(case, dz, dvec::Vector{Float64}; eps_rel=1e-6)
    N = case.nt
    delta = reshape(ComplexF64.(dvec[1:N] .+ im .* dvec[N+1:2N]), N, 1, 1)
    h = eps_rel * sqrt(case.P0)
    plus = solve_mmgnlse(case.A0 .+ h .* delta, case.pars, dz)
    minus = solve_mmgnlse(case.A0 .- h .* delta, case.pars, dz)
    dout = vec(get_temporal_field(plus; z=:final) .- get_temporal_field(minus; z=:final)) ./ (2h)
    return vcat(real.(dout), imag.(dout))
end

"""Symplectic defect max|S J S^T - J| with J = [0 I; -I 0] in (X, Y) ordering."""
function symplectic_defect(S)
    n = size(S, 1) ÷ 2
    J = [zeros(n, n) Matrix(1.0I, n, n); -Matrix(1.0I, n, n) zeros(n, n)]
    return maximum(abs.(S * J * S' .- J))
end

"""Spectral amplitude-quadrature covariance with 4x zero padding (padded bins vacuum).
Abar_t: mean output temporal field (length N). Returns (V_amp, kept indices, G1)."""
function amplitude_covariance(V, Abar_t::Vector{ComplexF64}; pad=4, thresh=1e-6)
    N = length(Abar_t)
    Np = pad * N
    offset = (Np - N) ÷ 2                      # window centered in the padded array
    win = offset .+ (1:N)
    Ap = zeros(ComplexF64, Np); Ap[win] .= Abar_t
    Ak = fft(Ap) ./ sqrt(Np)                   # unitary DFT of the padded mean field
    p = abs2.(Ak)
    kept = findall(p .>= thresh * maximum(p))
    psi = angle.(Ak[kept])
    k = kept .- 1
    m = collect(win) .- 1
    U = exp.(-2π * im .* (k * m') ./ Np) ./ sqrt(Np)   # rows: kept bins, cols: window samples
    C = exp.(-im .* psi) .* U
    G1 = hcat(real.(C), -imag.(C))            # x_k = sum_m Re(C) X_m - Im(C) Y_m
    nk = length(kept)
    Vamp = G1 * V * G1' .+ (Matrix(1.0I, nk, nk) .- G1 * G1')
    return Symmetric((Vamp .+ Vamp') ./ 2), kept, G1
end

function covariance_numbers(S, Abar_t)
    V = S * S'
    V = (V .+ V') ./ 2
    ev = eigvals(Symmetric(V))
    lam_min = ev[1]
    sv = svdvals(S)
    lam_min_svd = sv[end]^2
    Vamp, kept, G1 = amplitude_covariance(V, Abar_t)
    eva = eigvals(Vamp)
    return (; lam_min, lam_min_svd, lam_max=ev[end], lam_gen=eva[1],
            lam_gen_max=eva[end], nkept=length(kept), V, Vamp, ev, eva)
end

ideal_dispersionless_lambda_min(Phi) = (sqrt(1 + Phi^2) - Phi)^2
