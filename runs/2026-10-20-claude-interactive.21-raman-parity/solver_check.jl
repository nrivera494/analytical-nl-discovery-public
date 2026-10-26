# Second-solver check of the first-order Raman modal-transfer closed form (claim C-20261020-claude-interactive.21-01 (C))
# with the repository solver (agents' copy, PulsePropagation), which has multimode Raman and the (omega+omega0) shock.
# usage: JULIA_NUM_THREADS=2 julia --project=solver runs/.../solver_check.jl predict|run
# Variance reduction: each launch A0 is paired with its time mirror R A0. By the selection rule the Kerr first-order
# fluctuations cancel in [dN(A0) - dN(R A0)]/2, while the Raman transfer (odd in the centroid offsets) adds.
using PulsePropagation, FFTW, Random, Statistics, Printf, LinearAlgebra

const mode = length(ARGS) > 0 ? ARGS[1] : "predict"
# "noraman" (post hoc, added after the P4 outcome): same realizations with raman=NoRaman(), to measure the
# lambda-independent, shock-odd Kerr contribution that the mirror estimator cannot cancel.
# "rerun_b" (post hoc): case b only, 2048 fresh pairs (new seed), after case b missed P4 narrowly.
const here = @__DIR__
const c = 2.99792458e-4
const nt = 4096
const window = 16.384
const omega0 = 1770.4
const n2 = 2.6e-20
const gamma = 1e-3
const fR = 0.18
const S0 = gamma * c / (n2 * omega0)          # S_0000 in m^-2 giving gamma = 1e-3 /W/m

function hg_overlaps()
    S = zeros(3, 3, 3, 3)
    function put(idx, v)
        for p in unique(collect(Iterators.product(ntuple(_ -> 1:4, 4)...)))
            perm = (p...,)
            length(unique(perm)) == 4 || continue
            S[idx[perm[1]], idx[perm[2]], idx[perm[3]], idx[perm[4]]] = v
        end
    end
    put((1, 1, 1, 1), 1.0); put((1, 1, 2, 2), 0.5); put((1, 1, 3, 3), 0.5)
    put((2, 2, 2, 2), 0.75); put((3, 3, 3, 3), 0.75); put((2, 2, 3, 3), 0.25)
    return S
end

tg = TimeGrid(Nt=nt, window=window)
dt = tg.dt
domain = MMGNLSEDomain(degrees_of_freedom(:time, :space), tg)
Sn = hg_overlaps()
beta = TaylorBeta(reshape([0.0, 0.0, 0.1, -500.0, 0.0, 0.1, -500.0, 0.0, 0.1], 3, 3))
raman = AgarwalRaman(fraction=fR, tau1=0.0122, tau2=0.032)
params(L; r=raman) = MMGNLSEParameters(domain; length=L, beta=beta, S=SpatialOverlap(Sn .* S0), n2=n2, omega0=omega0, raman=r)

W = 2pi .* fftfreq(nt, 1 / dt)
w = 1 .+ W ./ omega0
nyq = nt ÷ 2 + 1
cases = Dict(
    "c_centroid_offset" => (powers=[4000.0, 3000.0, 3000.0], sig=[20.0, 20.0, 20.0], cen=[-5.0, 5.0, 5.0], photon_sym=false),
    "d_heldout_offset_widths" => (powers=[5000.0, 2500.0, 2500.0], sig=[12.0, 25.0, 18.0], cen=[3.0, -2.0, 0.0], photon_sym=false),
    "b_symmetric_photon_shock" => (powers=[4000.0, 3000.0, 3000.0], sig=[40.0, 15.0, 15.0], cen=[0.0, 0.0, 0.0], photon_sym=true),
)

function densities(cs)
    b = zeros(nt, 3)
    for p in 1:3
        g = exp.(-(W .- cs.cen[p]) .^ 2 ./ (2 * cs.sig[p]^2))
        cs.photon_sym && (g .*= w)
        g[nyq] = 0.0
        b[:, p] = cs.powers[p] .* g ./ sum(g)
    end
    return b
end

function closed_form(b, H)
    ImH = imag.(H)
    out = zeros(3)
    for p in 1:3, q in 1:3
        Spq = Sn[p, q, p, q]
        Spq == 0 && continue
        conv = real.(ifft(fft(ImH) .* fft(b[:, q])))
        out[p] += -2 * gamma * fR * Spq * sum(b[:, p] .* conv)
    end
    return out
end

H = PulsePropagation._mmgnlse_raman_kernels(params(1e-3)).ha
pred = Dict(k => closed_form(densities(v), H) for (k, v) in cases)
if mode == "predict"
    open(joinpath(here, "predictions_solver.txt"), "w") do io
        println(io, "# closed-form first-order slopes dN_p/dz (W/m) with the solver's own sampled Raman kernel, written before any solver propagation")
        println(io, "# sum(h)*dt of the solver kernel = ", real(H[1]))
        for k in sort(collect(keys(pred)))
            @printf(io, "%s %.4f %.4f %.4f\n", k, pred[k]...)
        end
    end
    println(read(joinpath(here, "predictions_solver.txt"), String))
    exit()
end

mirror(B) = vcat(B[1:1, :], reverse(B[2:end, :], dims=1))
photon(B) = vec(sum(abs2.(B) ./ w, dims=1))
z1 = 1e-3; dz = 2e-4
P = mode == "noraman" ? params(z1; r=NoRaman()) : params(z1)
res = Dict{String,Any}()
for name in (mode == "rerun_b" ? ["b_symmetric_photon_shock"] : sort(collect(keys(cases))))
    cs = cases[name]
    b = densities(cs)
    rng = MersenneTwister(mode == "rerun_b" ? 20261020 : hash(name) % 10^6)
    npair = mode == "rerun_b" ? 2048 : 512
    est = zeros(npair, 3)
    t0 = time()
    for r in 1:npair
        B0 = sqrt.(b ./ 2) .* (randn(rng, nt, 3) .+ 1im .* randn(rng, nt, 3))
        B0[nyq, :] .= 0
        dN = zeros(3, 2)
        for (j, Bstart) in enumerate((B0, mirror(B0)))
            A0 = reshape(fft(Bstart, 1), nt, 3, 1)
            sol = solve_mmgnlse(A0, P, dz; saveat=[z1])
            Az = get_temporal_field(sol)
            Bz = ifft(Az[:, :, 1, end], 1)
            dN[:, j] = (photon(Bz) .- photon(Bstart)) ./ z1
        end
        est[r, :] = (dN[:, 1] .- dN[:, 2]) ./ 2
    end
    m = vec(mean(est, dims=1)); se = vec(std(est, dims=1)) ./ sqrt(npair)
    res[name] = (mean=m, se=se, pred=pred[name], wall=time() - t0)
    @printf("%s: solver %s +- %s ; closed form %s ; %.0f s\n", name, string(round.(m, digits=2)), string(round.(se, digits=2)), string(round.(pred[name], digits=2)), time() - t0)
end
open(joinpath(here, "results", mode == "noraman" ? "solver_check_noraman.txt" : mode == "rerun_b" ? "solver_check_rerun_b.txt" : "solver_check.txt"), "w") do io
    println(io, "# solver commit ", strip(read(`git -C $(joinpath(here, "..", "..", "solver")) rev-parse HEAD`, String)))
    for (k, v) in res
        @printf(io, "%s mean %s se %s pred %s wall_s %.0f\n", k, string(v.mean), string(v.se), string(v.pred), v.wall)
    end
end
