# H4: adjoint-optimized input masks maximizing the photon fraction beyond lambda_c (frozen in commit 4f0f1ff).
# Usage: julia --project=solver h4_opt.jl <case_dir> <out_dir> <lambda_c_um> <phase|passive> <tl|rand1|rand2> <maxiter> <wall_s> <dz_m> [fdcheck]
# <case_dir> holds params.txt, omega.txt, beta.txt, At.txt (TL laser on the centred time grid), as written by
# ../2026-10-16-claude-interactive.6-h1-conservation/h1_julia_crosscheck.py.
using PulsePropagation, DelimitedFiles, FFTW, LinearAlgebra, Random, Printf
dir, outdir = ARGS[1], ARGS[2]
lamc = parse(Float64, ARGS[3]); masktype = ARGS[4]; start = ARGS[5]
maxiter = parse(Int, ARGS[6]); wall_budget = parse(Float64, ARGS[7]); dz = parse(Float64, ARGS[8])
fdcheck = length(ARGS) >= 9 && ARGS[9] == "fdcheck"
mkpath(outdir)
p = Dict{String,Float64}()
for line in eachline(joinpath(dir, "params.txt"))
    k, v = split(strip(line)); p[k] = parse(Float64, v)
end
nt = Int(p["nt"]); dt = p["dt"]; omega0 = p["omega0"]
omega = vec(readdlm(joinpath(dir, "omega.txt"))); beta = vec(readdlm(joinpath(dir, "beta.txt")))
Atx = readdlm(joinpath(dir, "At.txt")); At0 = ComplexF64.(Atx[:, 1] .+ 1im .* Atx[:, 2])
grid = TimeGrid{Float64}(nt, dt)
domain = MMGNLSEDomain(:time; time_grid=grid)
params = MMGNLSEParameters(domain; length=p["L"], alpha=0.0, beta=SampledBeta(omega, beta), S=p["S"], n2=p["n2"],
                           omega0=omega0, raman=AgarwalRaman(; fraction=p["fR"], tau1=p["tau1"], tau2=p["tau2"]))
Q = fftshift(ifft(At0))
wabs = omega0 .+ omega
weights = photon_weights(grid, omega0)
cJ = weights .* (wabs .< 2pi * 299.792458 / lamc)
Nlaser = sum(weights .* abs2.(Q))
band = findall(abs.(Q) .> 1e-3 * maximum(abs.(Q)))
nb = length(band)
function field_from(phi, s)
    Aw = copy(Q)
    m = masktype == "passive" ? clamp.(s, 0.0, 1.0) : ones(nb)
    Aw[band] .= Q[band] .* m .* cis.(phi)
    return Aw
end
function J_only(phi, s)
    Aw = field_from(phi, s); At = fft(ifftshift(Aw))
    sol = solve_mmgnlse(reshape(At, nt, 1, 1), params, dz)
    AL = get_spectral_field(sol; z=:final)[:, 1, 1]
    return sum(cJ .* abs2.(AL)) / Nlaser
end
function J_and_grad(phi, s)
    Aw = field_from(phi, s); At = reshape(fft(ifftshift(Aw)), nt, 1, 1)
    sol = solve_mmgnlse(At, params, dz)
    AL = get_spectral_field(sol; z=:final)[:, 1, 1]
    J = sum(cJ .* abs2.(AL)) / Nlaser
    lamT = reshape(cJ .* AL ./ Nlaser, nt, 1, 1)
    adj = solve_adjoint(lamT, params, dz; initial_field=At, dz_forward=dz, adjoint_mode=:discrete_rk4ip)
    lam0 = get_spectral_field(adj; z=:initial)[:, 1, 1]
    gphi = -2 .* imag.(conj.(lam0[band]) .* Aw[band])
    gs = masktype == "passive" ? 2 .* real.(conj.(lam0[band]) .* Q[band] .* cis.(phi)) : zeros(nb)
    return J, gphi, gs
end
rng = MersenneTwister(start == "rand1" ? 11 : 23)
xb = (omega[band] .- omega[band[1]]) ./ (omega[band[end]] - omega[band[1]]) .* 2 .- 1   # in [-1, 1]
phi = if start == "tl"
    zeros(nb)
elseif startswith(start, "file:")   # continue from a saved best_phase.txt (columns: detuning, phase, amplitude)
    vec(readdlm(start[6:end])[:, 2])
elseif start == "tod"      # best point of the numpy TOD scan: TOD = -60000 fs^3 about the laser centre
    xc = omega[band] .- omega[argmax(abs.(Q))]
    -6e-5 .* xc .^ 3 ./ 6
else   # smooth random phase: random Legendre-like polynomial of degree 2..6, amplitude ~ 3 rad
    c = randn(rng, 5) .* 3.0
    c[1] .* xb .^ 2 .+ c[2] .* xb .^ 3 .+ c[3] .* xb .^ 4 .+ c[4] .* xb .^ 5 .+ c[5] .* xb .^ 6
end
s = ones(nb)
logf = open(joinpath(outdir, "log.txt"), "w")
t0 = time()
J0, g0, gs0 = J_and_grad(phi, s)
@printf(logf, "init J=%.6f  (t=%.1f s, nb=%d, Nlaser=%.4e)\n", J0, time() - t0, nb, Nlaser); flush(logf)
if fdcheck
    for trial in 1:2
        d = randn(MersenneTwister(100 + trial), nb) .* 0.05
        eps = 1.0
        Jp = J_only(phi .+ eps .* d, s); Jm = J_only(phi .- eps .* d, s)
        @printf(logf, "fdcheck phase dir %d: FD %.6e  adjoint %.6e\n", trial, (Jp - Jm) / (2eps), dot(g0, d)); flush(logf)
        if masktype == "passive"
            ds = randn(MersenneTwister(200 + trial), nb) .* 0.05
            s0 = fill(0.9, nb)
            Jb, gb, gsb = J_and_grad(phi, s0)
            Jp = J_only(phi, s0 .+ eps .* ds); Jm = J_only(phi, s0 .- eps .* ds)
            @printf(logf, "fdcheck amp dir %d: FD %.6e  adjoint %.6e\n", trial, (Jp - Jm) / (2eps), dot(gsb, ds)); flush(logf)
        end
    end
end
# Adam ascent
lr = 0.08; b1 = 0.9; b2 = 0.999; m1 = zeros(nb); v1 = zeros(nb); m2 = zeros(nb); v2 = zeros(nb)
J, g, gs = J0, g0, gs0
best = (J, copy(phi), copy(s)); hist = [J]
for it in 1:maxiter
    global J, g, gs, phi, s, m1, v1, m2, v2, best
    m1 .= b1 .* m1 .+ (1 - b1) .* g; v1 .= b2 .* v1 .+ (1 - b2) .* g .^ 2
    phi .+= lr .* (m1 ./ (1 - b1^it)) ./ (sqrt.(v1 ./ (1 - b2^it)) .+ 1e-12)
    if masktype == "passive"
        m2 .= b1 .* m2 .+ (1 - b1) .* gs; v2 .= b2 .* v2 .+ (1 - b2) .* gs .^ 2
        s .+= 0.05 .* (m2 ./ (1 - b1^it)) ./ (sqrt.(v2 ./ (1 - b2^it)) .+ 1e-12)
        s .= clamp.(s, 0.0, 1.0)
    end
    J, g, gs = J_and_grad(phi, s)
    push!(hist, J)
    J > best[1] && (best = (J, copy(phi), copy(s)))
    @printf(logf, "it %d J=%.6f best=%.6f |g|=%.3e t=%.1f\n", it, J, best[1], norm(g), time() - t0); flush(logf)
    time() - t0 > wall_budget && break
end
close(logf)
writedlm(joinpath(outdir, "best_phase.txt"), hcat(omega[band], best[2], clamp.(best[3], 0.0, 1.0)))
writedlm(joinpath(outdir, "history.txt"), hist)
open(joinpath(outdir, "result.txt"), "w") do io
    println(io, "J_init ", J0); println(io, "J_best ", best[1]); println(io, "iterations ", length(hist) - 1)
    println(io, "wall_s ", time() - t0); println(io, "nb ", nb); println(io, "dz ", dz)
end
println("J_init ", J0, " J_best ", best[1])
