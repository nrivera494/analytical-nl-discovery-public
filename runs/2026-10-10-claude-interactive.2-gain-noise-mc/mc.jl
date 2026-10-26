# Route (i): Monte Carlo with the solver's legacy stochastic backend (ShotNoise + GainLangevin, fixed-step RK4IP).
# Usage: julia --project=solver mc.jl <case> <ntraj> <seed> <outfile>
#   case = kerr_ns0.5 | kerr_ns1.0 | kerr_vac | kerr_ase | lin_ns0.5 | lin_ns1.0
# Writes one CSV line per trajectory: q, N (photons), Tc (ps), Wc (rad/ps).
include(joinpath(@__DIR__, "..", "2026-10-10-claude-interactive.2-simval-lib", "simlib.jl"))

case = ARGS[1]; ntraj = parse(Int, ARGS[2]); seed = parse(Int, ARGS[3]); outfile = ARGS[4]
kerr = startswith(case, "kerr")
svac, ns = if endswith(case, "ns0.5"); (0.5, 0.5)
elseif endswith(case, "ns1.0"); (0.5, 1.0)
elseif endswith(case, "vac"); (0.5, 0.0)
elseif endswith(case, "ase"); (0.0, 0.5)
else error("case") end

const EPS0 = 0.1; const GAM = sqrt(18); const GL = 4.0; const NT = 1024; const WIN = 16.0; const NSTEPS = 2000
S = mkparams(eps0=EPS0, Gamma=GAM, gL=GL, Nt=NT, window=WIN)
A0 = vec(seed_parabola(S; delta=0.5 * S.eps0^(2/3)))
dz = S.L / NSTEPS
lambda0 = 2π * CLIGHT / S.omega0
n2 = kerr ? S.gam * CLIGHT / S.omega0 : 0.0
system = PulsePropagation.PassiveFiber(; length=S.L, lambda0=lambda0, material=PulsePropagation.LegacySilica(),
                      betas=reshape([0.0, 0.0, S.b2], :, 1), sr=reshape([1.0], 1, 1, 1, 1), n2=n2,
                      raman_fraction=0.0)
zs = collect(range(0, S.L; length=NSTEPS + 1))
solver = PulsePropagation.RK4IPSolver(; stepping=PulsePropagation.FixedStep(; dz=dz), saveat=PulsePropagation.SaveAt(zs), linear_gain=PulsePropagation.LinearGain(S.g))
problem = PulsePropagation.PulsePropagationProblem(; grid=S.grid, system=system, solver=solver, fields=reshape(A0, :, 1))

rng = MersenneTwister(seed)
open(outfile, "a") do io
    for q in 1:ntraj
        ens = PulsePropagation.stochastic_ensemble(problem; noise=PulsePropagation.ShotNoise(; noise_scale=svac), ntraj=1, rng=rng)
        st = PulsePropagation.stochastic_solve(problem, ens; drives=[PulsePropagation.GainLangevin(; noise_scale=ns)], rng=rng)
        A = st.fields[:, 1, end, 1]
        m = moments(A, S)
        @printf(io, "%d,%.17e,%.17e,%.17e\n", q, photons(S, A), m.Tc, m.Wc)
        q % 50 == 0 && flush(io)
    end
end
