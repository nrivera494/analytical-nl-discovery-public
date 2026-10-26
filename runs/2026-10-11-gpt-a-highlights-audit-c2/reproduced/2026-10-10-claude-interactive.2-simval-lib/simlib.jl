# Shared helpers for the amplifier-similariton validation runs (claude-interactive.2, 2026-10-10).
# Model: dA/dz = -(i/2) b2 A_TT + i gam |A|^2 A + (g/2) A  (+ noise), solved with PulsePropagation
# (FastDifferentiableMMNLO agents' copy). Self-steepening is made negligible by a large carrier
# omega0 (ratio omega/omega0 <= 1e-5); no Raman; the solver's spectral damping window acts only
# near the grid edge and is checked through the edge-energy diagnostics.
using PulsePropagation, FFTW, LinearAlgebra, Statistics, Printf, Random

const CLIGHT = 2.99792458e-4      # m/ps
const HBAR = 1.054571817e-34
const OMEGA0_BIG = 1.0e8          # rad/ps

softplus(x, d) = x > 30d ? x : d * log1p(exp(x / d))

"""Normalized units: T0 = 1 ps (seed half-width scale), beta2 = 1 ps^2/m, so L_D = 1 m."""
function mkparams(; eps0, Gamma, gL, Nt, window, gam=1e-5, b2=1.0, T0=1.0, omega0=OMEGA0_BIG)
    P0 = b2 / (gam * eps0^2 * T0^2)
    sq = eps0 * T0^2 / b2               # sqrt(L_D L_NL) in m
    g = Gamma / sq
    L = gL / g
    grid = TimeGrid(Nt, window)
    domain = MMGNLSEDomain(degrees_of_freedom(:time), grid)
    n2 = gam * CLIGHT / omega0          # S = 1 m^-2
    params = MMGNLSEParameters(domain; length=L, gain=g, beta=TaylorBeta([0.0, 0.0, b2]),
                               S=1.0, n2=n2, omega0=omega0)
    t = collect(time_axis(grid))
    dt = grid.dt
    w = PulsePropagation.ifft_frequency_grid(Nt, dt)   # raw (unshifted) omega matching ifft(A_t)
    return (; params, grid, domain, t, dt, w, Nt, window, eps0, Gamma, gL, gam, b2, T0, P0, g, L, sq, omega0)
end

"""Same physical setup with a different length (gain gL)."""
function withlength(S, gL)
    L = gL / S.g
    n2 = S.gam * CLIGHT / S.omega0
    params = MMGNLSEParameters(S.domain; length=L, gain=S.g, beta=TaylorBeta([0.0, 0.0, S.b2]),
                               S=1.0, n2=n2, omega0=S.omega0)
    return merge(S, (; params, L, gL))
end

"""Parabolic seed with softplus edges: rho = P0*softplus(1-(t/b0)^2, delta); chirp v = q*g*T
(omega_inst = q*g*T/b2, convention A ~ exp(-i omega t))."""
function seed_parabola(S; b0=S.T0, P0=S.P0, q=0.0, delta=0.0)
    rho = [delta > 0 ? P0 * softplus(1 - (x / b0)^2, delta) : P0 * max(1 - (x / b0)^2, 0.0) for x in S.t]
    phi = @. -q * S.g * S.t^2 / (2 * S.b2)
    A = @. sqrt(rho) * cis(phi)
    return reshape(ComplexF64.(A), :, 1, 1)
end

"""i d/dT in the solver's convention (A_t = fft(ifft(A_t)), A ~ exp(-i omega t))."""
iddt(A, w) = fft(w .* ifft(A))

"""Moments of a time-domain field vector: E, Tc, varT, Wc, varW, cov (symmetrized T-omega covariance)."""
function moments(A::AbstractVector, S)
    rho = abs2.(A)
    E = sum(rho) * S.dt
    Tc = sum(S.t .* rho) * S.dt / E
    varT = sum((S.t .- Tc) .^ 2 .* rho) * S.dt / E
    B = iddt(A, S.w)
    cur = real.(conj.(A) .* B)                 # rho * omega_inst
    Wc = sum(cur) * S.dt / E
    cov = sum((S.t .- Tc) .* (cur .- Wc .* rho)) * S.dt / E
    varW = sum(abs2.(B .- Wc .* A)) * S.dt / E
    return (; E, Tc, varT, Wc, varW, cov)
end

"""Energy fraction in the outer 20% of the time window and in the outer 25% of the frequency window."""
function edge_fractions(A::AbstractVector, S)
    rho = abs2.(A)
    Tw = S.window / 2
    et = sum(rho[abs.(S.t) .> 0.8Tw]) / sum(rho)
    Aw = abs2.(ifft(A))
    wn = maximum(abs.(S.w))
    ew = sum(Aw[abs.(S.w) .> 0.75wn]) / sum(Aw)
    return (; et, ew)
end

photons(S, A) = sum(abs2.(A)) * S.dt * 1e-12 / (HBAR * S.omega0 * 1e12)

"""dJ/dconj(A_omega) in the solver's centered spectral convention, from g_t = dJ/dconj(A_t[n])."""
lam_from_time_grad(gt) = reshape(fftshift(length(gt) .* ifft(vec(gt))), :, 1, 1)

"""Time-domain Wirtinger gradients dJ/dconj(A_t) of the centroids and photon number at field A."""
function grad_Tc(A, S)
    m = moments(A, S)
    return (S.t .- m.Tc) .* A .* (S.dt / m.E)
end
function grad_Wc(A, S)
    m = moments(A, S)
    return (iddt(A, S.w) .- m.Wc .* A) .* (S.dt / m.E)
end
grad_N(A, S) = A .* (S.dt * 1e-12 / (HBAR * S.omega0 * 1e12))

"""Hydrodynamic width ODE in zeta units (zeta = z/sqrt(L_D L_NL)): a'' = 2 e^{Gamma zeta}/a^2 (RK4)."""
function hydro_width(a0, ap0, Gamma, zetaL; n=200000)
    h = zetaL / n
    f(z, y) = (y[2], 2 * exp(Gamma * z) / y[1]^2)
    y = (a0, ap0)
    zs = zeros(n + 1); as = zeros(n + 1); aps = zeros(n + 1)
    as[1] = a0; aps[1] = ap0
    for i in 1:n
        z = (i - 1) * h
        k1 = f(z, y)
        k2 = f(z + h / 2, y .+ (h / 2) .* k1)
        k3 = f(z + h / 2, y .+ (h / 2) .* k2)
        k4 = f(z + h, y .+ h .* k3)
        y = y .+ (h / 6) .* (k1 .+ 2 .* k2 .+ 2 .* k3 .+ k4)
        zs[i+1] = i * h; as[i+1] = y[1]; aps[i+1] = y[2]
    end
    return zs, as, aps
end
