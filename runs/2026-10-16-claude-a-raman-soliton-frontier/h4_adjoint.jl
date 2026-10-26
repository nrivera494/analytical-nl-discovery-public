# H4 with an adjoint gradient (FastDifferentiableMMNLO agents' copy b9fa957, adjoint_mode = :discrete_rk4ip).
# Objective: windowed energy fraction of the leading soliton at L = 4 L_D/N, J = sum_w |A(L)|^2 / E0, window of half-width
# max(6/amp, 1) T0 around the tallest output peak (as in h3_scan.measure; the window follows the peak, its motion is not
# differentiated). Control: spectral phase phi = sum_{m=2}^{M} c_m P_m(Omega/Omega_c) on the laser support, applied in the
# solver's spectral convention A_w = fftshift(ifft(A_t)); dJ/dphi = -2 Im(conj(lambda_0) A_w0). L-BFGS (Optim.jl).
# Self-steepening is suppressed to match the s = 0 model of C-20261016-claude-a-02/03: omega0 is scaled by 1000 and n2 by
# 1/1000, which leaves gamma unchanged and makes the Kerr prefactor (omega0 + Omega)/omega0 = 1 + O(1e-3 Omega/omega0).
# The gradient is checked against central finite differences before optimizing. Optimized launch fields are written to
# ~/analytical-nl-discovery-data/<run-id>/h4_adjoint/ for the ZS re-measurement in Python (h4_adjoint_measure.py).
# Usage (repo root): JULIA_NUM_THREADS=2 julia --project=solver runs/<run-id>/h4_adjoint.jl N T0_fs M nrandomstarts [warm_coef.csv]
using PulsePropagation, FFTW, LinearAlgebra, Optim, Printf, Random, DelimitedFiles
const PP = PulsePropagation
FFTW.set_num_threads(1)
N = parse(Float64, ARGS[1]); T0 = parse(Float64, ARGS[2]) / 1000; M = parse(Int, ARGS[3]); nrand = parse(Int, ARGS[4])
outdir = expanduser("~/analytical-nl-discovery-data/2026-10-16-claude-a-raman-soliton-frontier/h4_adjoint"); mkpath(outdir)
tag = @sprintf("N%g_T0%d_M%d", N, round(Int, T0 * 1000), M) * (length(ARGS) >= 5 ? "_warm" : "")
logio = open(joinpath(@__DIR__, "h4_adjoint_" * tag * ".log"), "w")
say(s) = (println(s); println(logio, s); flush(stdout); flush(logio))

c_light = 2.99792458e-4; lambda0 = 1550e-9; omega0 = 2pi * c_light / lambda0
material = Silica(raman=AgarwalRaman())
mfd = 9.2e-6; Aeff = pi * (mfd / 2)^2
gamma = material.n2 * (2pi / lambda0) / Aeff
beta2 = -0.0206; SSF = 1000.0
Nt = N <= 4 ? 8192 : 16384; width = 160 * T0
grid = TimeGrid(Nt, width); domain = MMGNLSEDomain(degrees_of_freedom(:time), grid)
t = time_axis(grid); Om = frequency_axis(grid)
LD = T0^2 / abs(beta2); P0 = N^2 * abs(beta2) / (gamma * T0^2); L = 4.0 / N * LD
h = 0.4 / (N * (2N - 1))^2; nsteps = round(Int, (4.0 / N) / h); dz = L / nsteps
pars = MMGNLSEParameters(domain; length=L, beta=TaylorBeta(reshape([0.0, 0.0, beta2], :, 1)), S=1 / Aeff,
                         n2=material.n2 / SSF, omega0=omega0 * SSF, raman=AgarwalRaman())
A_TL = sqrt(P0) .* sech.(t ./ T0) .+ 0im
Aw_TL = fftshift(ifft(A_TL))
absQ = abs.(Aw_TL); Wc = maximum(abs.(Om[absQ .> 1e-4 * maximum(absQ)]))
x = clamp.(Om ./ Wc, -1, 1)
function legendre_all(x, M)
    P = [ones(length(x)), copy(x)]
    for m in 1:M-1
        push!(P, ((2m + 1) .* x .* P[end] .- m .* P[end-1]) ./ (m + 1))
    end
    return P            # P[m+1] = P_m
end
PL = legendre_all(x, M)[3:M+1]          # orders 2..M
E0 = sum(abs2, A_TL)
nev = Ref(0)

function launch(c)
    phi = zeros(Nt); for i in eachindex(c); phi .+= c[i] .* PL[i]; end
    Aw0 = cis.(phi) .* Aw_TL
    return Aw0, fft(ifftshift(Aw0))
end

function JG(c; grad=true)
    nev[] += 1
    Aw0, A0 = launch(c)
    sol = solve_mmgnlse(reshape(A0, :, 1, 1), pars, dz; saveat=L)
    A = get_temporal_field(sol)[:, 1, 1]
    k = argmax(abs.(A)); amp_n = N * abs(A[k]) / sqrt(P0); hw = max(6 / amp_n, 1.0) * T0
    w = Float64.(abs.(t .- t[k]) .<= hw)
    J = sum(w .* abs2.(A)) / E0
    grad || return J, nothing
    lamL = PP._mmgnlse_time_gradient_to_centered_spectral(reshape(w .* A ./ E0, :, 1, 1))
    adj = solve_adjoint(lamL, pars, dz; forward_solution=sol, adjoint_mode=:discrete_rk4ip)
    lam0 = get_spectral_field(adj; z=:initial)[:, 1, 1]
    dJdphi = -2 .* imag.(conj.(lam0) .* Aw0)
    return J, [sum(dJdphi .* PL[i]) for i in eachindex(c)]
end

# gradient check (central differences, two coefficients, at a random point)
rng = MersenneTwister(5)
c_chk = 0.3 .* randn(rng, M - 1)
J0, G0 = JG(c_chk)
for i in (1, 2)
    e = zeros(M - 1); e[i] = 1e-4
    Jp, _ = JG(c_chk .+ e; grad=false); Jm, _ = JG(c_chk .- e; grad=false)
    say(@sprintf("gradcheck %s coef %d: adjoint %.6e  finite-diff %.6e  rel.err %.2e", tag, i + 1, G0[i], (Jp - Jm) / 2e-4,
                 abs(G0[i] - (Jp - Jm) / 2e-4) / max(abs(G0[i]), 1e-12)))
end
J_TL, _ = JG(zeros(M - 1); grad=false)
say(@sprintf("%s TL windowed fraction J_TL = %.6f", tag, J_TL))

function fg!(F, G, c)
    J, g = JG(c; grad=(G !== nothing))
    if G !== nothing
        G .= -g
    end
    return -J
end

starts = [("TL", zeros(M - 1))]
for s in 1:nrand
    push!(starts, (@sprintf("rand%d", s), (0.5 * s) .* randn(rng, M - 1) ./ (1:M-1)))
end
if length(ARGS) >= 5          # warm start from a saved coefficient file (continuation of a previous run)
    starts = [("warm", vec(readdlm(ARGS[5], ',')))]
end
best = (J_TL, zeros(M - 1))
for (name, c0) in starts
    nev[] = 0; t1 = time()
    res = optimize(Optim.NLSolversBase.only_fg!(fg!), c0, LBFGS(), Optim.Options(iterations=30, g_tol=1e-7))
    Jopt = -Optim.minimum(res); copt = Optim.minimizer(res)
    say(@sprintf("%s start %s: J_opt = %.6f  ratio %.5f  iters %d  evals %d  |g| %.2e  wall %.0f s", tag, name, Jopt, Jopt / J_TL,
                 Optim.iterations(res), nev[], Optim.g_residual(res), time() - t1))
    if Jopt > best[1]
        global best = (Jopt, copt)
    end
    _, A0 = launch(copt)
    writedlm(joinpath(outdir, tag * "_" * name * ".csv"), hcat(t ./ T0, real.(A0) ./ sqrt(P0), imag.(A0) ./ sqrt(P0)), ',')
    writedlm(joinpath(outdir, tag * "_" * name * "_coef.csv"), copt, ',')
end
say(@sprintf("%s BEST J = %.6f  headroom (windowed energy) %.5f", tag, best[1], best[1] / J_TL))
close(logio)
