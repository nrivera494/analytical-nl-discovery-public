# smoke.jl -- timing, gamma calibration, adjoint-vs-FD and thread-safety checks before the main run.
include(joinpath(@__DIR__, "sdc_lib.jl"))
BLAS.set_num_threads(1); FFTW.set_num_threads(1)
println("threads = ", Threads.nthreads())

# 1. gamma / phase calibration with beta2 = 0
c0 = make_case(beta2=0.0)
dz = 0.002
s0 = forward(c0, dz)
Aout = vec(get_temporal_field(s0; z=:final))
i0 = c0.nt ÷ 2 + 1
@printf("t[i0]=%.3g  |A|^2 in/out at T=0: %.6f %.6f  phase(out)-phase(in) = %.8f (expect %.8f mod 2pi)\n",
        c0.t[i0], abs2(c0.A0[i0]), abs2(Aout[i0]), angle(Aout[i0] / c0.A0[i0]), rem2pi(5.0, RoundNearest))

# 2. timing of one adjoint row, x = 1, beta2 < 0
c1 = make_case(beta2=-0.04)
s1 = forward(c1, dz)
r = adjoint_row(c1, s1, dz, 257, :X)     # compile
t = @elapsed for j in (200, 257, 300)
    adjoint_row(c1, s1, dz, j, :X)
end
@printf("adjoint row time: %.3f s per row (nsteps=%d)\n", t / 3, round(Int, 1 / dz))
tf = @elapsed forward(c1, dz)
@printf("forward time: %.3f s\n", tf)

# 3. adjoint rows vs finite differences on random directions
N = c1.nt
rows = [257, 240, 300, N + 257, N + 270, 10, N + 5]
Srows = zeros(length(rows), 2N)
for (a, rr) in enumerate(rows)
    j = rr <= N ? rr : rr - N
    Srows[a, :] .= adjoint_row(c1, s1, dz, j, rr <= N ? :X : :Y)
end
rng = MersenneTwister(7)
for trial in 1:2
    d = randn(rng, 2N)
    for eps_rel in (1e-5, 1e-6)
        fdv = fd_direction(c1, dz, d; eps_rel)
        pred = Srows * d
        @printf("trial %d eps_rel=%.0e: adjoint %s\n    FD      %s\n    max rel err %.2e\n", trial, eps_rel,
                string(round.(pred; sigdigits=8)), string(round.(fdv[rows]; sigdigits=8)),
                maximum(abs.(pred .- fdv[rows])) / maximum(abs.(fdv[rows])))
    end
end

# 4. thread safety: same rows computed in a threaded loop
Sthr = zeros(length(rows), 2N)
tt = @elapsed Threads.@threads for a in eachindex(rows)
    rr = rows[a]
    j = rr <= N ? rr : rr - N
    Sthr[a, :] .= adjoint_row(c1, s1, dz, j, rr <= N ? :X : :Y)
end
@printf("threaded: max abs diff vs serial = %.3e, time %.3f s for %d rows\n",
        maximum(abs.(Sthr .- Srows)), tt, length(rows))
