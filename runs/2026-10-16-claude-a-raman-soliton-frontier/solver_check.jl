# Second implementation for H3: the same launch propagated with FastDifferentiableMMNLO (agents' copy, PulsePropagation),
# single mode, Agarwal (= Blow-Wood) Raman (fR = 0.18, tau1 = 12.2 fs, tau2 = 32 fs), beta2 only, fixed-step RK4IP.
# The solver's Kerr prefactor n2 (omega0 + Omega)/c includes self-steepening, so the numpy comparison uses s = 1/(omega0 T0).
# Output fields (raw) go to ~/analytical-nl-discovery-data/<run-id>/solver_check/; the ZS measurement is done in Python
# (solver_check_measure.py) with the same `measure` as h3_scan.py.
# Usage (from the repository root): JULIA_NUM_THREADS=2 julia --project=solver runs/<run-id>/solver_check.jl
using PulsePropagation, FFTW, DelimitedFiles
FFTW.set_num_threads(1)
outdir = expanduser("~/analytical-nl-discovery-data/2026-10-16-claude-a-raman-soliton-frontier/solver_check")
mkpath(outdir)
c_light = 2.99792458e-4            # m/ps
lambda0 = 1550e-9
omega0 = 2pi * c_light / lambda0   # rad/ps
material = Silica(raman=AgarwalRaman())
mfd = 9.2e-6; Aeff = pi * (mfd / 2)^2
gamma = material.n2 * (2pi / lambda0) / Aeff
beta2 = -0.0206                    # ps^2/m
cases = [(3, 0.1, true), (4, 0.2, true), (3, 0.1, false)]
for (N, T0, raman) in cases
    width = 160.0 * T0; Nt = 8192
    grid = TimeGrid(Nt, width)
    domain = MMGNLSEDomain(degrees_of_freedom(:time), grid)
    t = time_axis(grid)
    LD = T0^2 / abs(beta2)
    P0 = N^2 * abs(beta2) / (gamma * T0^2)
    L = 4.0 / N * LD
    h = 0.4 / (N * (2N - 1))^2
    nsteps = round(Int, (4.0 / N) / h)
    dz = L / nsteps
    pars = MMGNLSEParameters(domain; length=L, beta=TaylorBeta(reshape([0.0, 0.0, beta2], :, 1)), S=1 / Aeff,
                             n2=material.n2, omega0=omega0, raman=(raman ? AgarwalRaman() : NoRaman()))
    A0 = zeros(ComplexF64, Nt, 1, 1); A0[:, 1, 1] = sqrt(P0) .* sech.(t ./ T0)
    t1 = time()
    sol = solve_mmgnlse(A0, pars, dz)
    At = get_temporal_field(sol)[:, 1, 1]
    tag = "N$(N)_T0$(round(Int, T0*1000))fs_raman$(Int(raman))"
    writedlm(joinpath(outdir, tag * ".csv"), hcat(t ./ T0, real.(At) ./ sqrt(P0), imag.(At) ./ sqrt(P0)), ',')
    println("done $tag steps=$nsteps dz=$dz L=$L P0=$P0 gamma=$gamma wall=$(round(time()-t1, digits=1)) E_ratio=$(sum(abs2, At)/sum(abs2, A0))")
    flush(stdout)
end
