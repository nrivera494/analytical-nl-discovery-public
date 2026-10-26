# Deterministic background moments W(z) for a realistic Yb similariton amplifier (Kerr + beta2 + flat gain),
# and the same seed with gamma = 0 (linear amplifier). Used to evaluate the exact moment formula (a) of
# C-20261008-claude-a-01 outside the semiclassical regime. No noise is simulated here.
# Run from the repository root:
#   JULIA_NUM_THREADS=2 julia --project=solver runs/2026-10-08-claude-a-realistic-W/w_of_z.jl
# Optional environment overrides for convergence checks: NT, WINDOW (ps), DZ (m), TAG.
using PulsePropagation, FFTW, Printf, NPZ
const PP = PulsePropagation
const RUN_ID = "2026-10-08-claude-a-realistic-W"
const RAW = joinpath(homedir(), "analytical-nl-discovery-data", RUN_ID)
mkpath(RAW)
const OUT = @__DIR__

const LAMBDA0 = 1030e-9
const BETA2 = 0.025          # ps^2/m
const GAMMA = 0.005          # 1/(W m)
const G_PER_M = 1.9          # power gain, 1/m
const L = 3.2                # m  (gL = 6.08)
const FWHM_PS = 0.25         # Gaussian intensity FWHM of the seed
const E0_PJ = 10.0
const NT = parse(Int, get(ENV, "NT", "8192"))
const WINDOW = parse(Float64, get(ENV, "WINDOW", "40.0"))
const DZ = parse(Float64, get(ENV, "DZ", "0.0005"))
const TAG = get(ENV, "TAG", "base")
const NSAVE = 321

function run_case(gamma)
    grid = TimeGrid(NT, WINDOW)
    t = PP.time_axis(grid)
    f0 = 2.99792458e-4 / LAMBDA0
    w0 = 2pi * f0                                   # rad/ps
    c = 2.99792458e-4                               # m/ps
    n2 = 2.3e-20
    sr = gamma == 0 ? 1.0e10 : gamma / (n2 * w0 / c)  # 1/A_eff so that gamma = n2 w0 sr / c
    tau = FWHM_PS / (2 * sqrt(log(2)))
    A = exp.(-t .^ 2 ./ (2 * tau^2))
    A .*= sqrt(E0_PJ / (sum(abs2, A) * grid.dt))
    system = PP.PassiveFiber(; length=L, lambda0=LAMBDA0, betas=reshape([0.0, 0.0, BETA2], :, 1),
                             sr=reshape([sr], 1, 1, 1, 1), n2=(gamma == 0 ? 0.0 : n2), raman_fraction=0.0)
    zs = collect(range(0.0, L; length=NSAVE))
    solver = PP.RK4IPSolver(; stepping=PP.FixedStep(; dz=DZ), saveat=PP.SaveAt(zs),
                            linear_gain=PP.LinearGain(G_PER_M))
    prob = PP.PulsePropagationProblem(; grid=grid, system=system,
                                      fields=reshape(ComplexF64.(A), NT, 1), solver=solver)
    sol = PP.solve(prob)
    F = sol.output.fields[:, 1, :]                   # NT x NSAVE, time domain, sqrt(W)
    dt = grid.dt
    om = 2pi .* fftfreq(NT, 1 / dt)                  # rad/ps
    E = vec(sum(abs2, F; dims=1)) .* dt
    Tc = [sum(t .* abs2.(F[:, k])) * dt / E[k] for k in 1:NSAVE]
    sT2 = [sum((t .- Tc[k]) .^ 2 .* abs2.(F[:, k])) * dt / E[k] for k in 1:NSAVE]
    Cov = zeros(NSAVE); sW2 = zeros(NSAVE); Om = zeros(NSAVE)
    edge = zeros(NSAVE)
    for k in 1:NSAVE
        a = F[:, k]
        da = ifft(1im .* om .* fft(a))              # d a/dt (FFTW: a = ifft(fft(a)) with exp(+i om t) synthesis);
        # convention verified by the Ehrenfest check below (d sigma_T^2/dz must equal 2 beta2 Cov)
        j = -imag.(conj.(a) .* da)                  # rho * instantaneous frequency (Agrawal sign if check passes)
        Om[k] = sum(j) * dt / E[k]
        Cov[k] = sum((t .- Tc[k]) .* (j .- Om[k] .* abs2.(a))) * dt / E[k]
        sW2[k] = sum(abs2.(da)) * dt / E[k] - Om[k]^2
        edge[k] = (abs2(a[1]) + abs2(a[end])) / maximum(abs2.(a))   # window-edge leakage diagnostic
    end
    return (; zs, E, Tc, sT2, Cov, sW2, Om, edge)
end

function exact_formula(r)
    # N0 Var = I_in + (2 n_sp - 1) I_ase ; units ps^2, (rad/ps)^2, ps*(rad/ps)
    zs = r.zs
    zL = zs[end]
    n = length(zs)
    W(k) = [r.sT2[k] r.Cov[k]; r.Cov[k] r.sW2[k]]
    Phi(z) = [1.0 BETA2*(zL-z); 0.0 1.0]
    Sin = Phi(zs[1]) * W(1) * Phi(zs[1])'
    integrand = [G_PER_M * exp(-G_PER_M * zs[k]) .* (Phi(zs[k]) * W(k) * Phi(zs[k])') for k in 1:n]
    Sase = zeros(2, 2)
    for k in 1:n-1
        Sase .+= 0.5 .* (zs[k+1] - zs[k]) .* (integrand[k] .+ integrand[k+1])
    end
    Dc = -r.Cov[end] / r.sW2[end]
    v = [1.0, Dc]
    return (; Sin, Sase, Dc, comp_in=v' * Sin * v, comp_ase=v' * Sase * v)
end

jsonval(x::AbstractDict) = "{" * join(["\"$(k)\": " * jsonval(v) for (k, v) in x], ", ") * "}"
jsonval(x::AbstractString) = "\"$(x)\""
jsonval(x) = string(x)

res = Dict{String,Any}("tag" => TAG, "NT" => NT, "window_ps" => WINDOW, "dz_m" => DZ)
for (name, gam) in (("similariton", GAMMA), ("linear", 0.0))
    t0 = time()
    r = run_case(gam)
    f = exact_formula(r)
    dsdz = [(r.sT2[k+1] - r.sT2[k-1]) / (r.zs[k+1] - r.zs[k-1]) for k in 2:length(r.zs)-1]
    rel = maximum(abs.(dsdz .- 2BETA2 .* r.Cov[2:end-1])) / maximum(abs.(dsdz))
    npzwrite(joinpath(RAW, "$(TAG)_$(name)_moments.npz"),
             Dict("z" => r.zs, "E_pJ" => r.E, "Tc" => r.Tc, "sT2" => r.sT2, "Cov" => r.Cov, "sW2" => r.sW2, "Om" => r.Om))
    res[name] = Dict(
        "E_out_over_E0" => r.E[end] / r.E[1],
        "rms_width_in_ps" => sqrt(r.sT2[1]), "rms_width_out_ps" => sqrt(r.sT2[end]),
        "rms_bw_in_radps" => sqrt(r.sW2[1]), "rms_bw_out_radps" => sqrt(r.sW2[end]),
        "Cov_out_ps_radps" => r.Cov[end],
        "ehrenfest_dsT2dz_vs_2beta2Cov_maxrel" => rel,
        "max_window_edge_leakage" => maximum(r.edge),
        "N0Var_Tc_ps2" => Dict("in" => f.Sin[1, 1], "ase" => f.Sase[1, 1]),
        "N0Var_Om_radps2" => Dict("in" => f.Sin[2, 2], "ase" => f.Sase[2, 2]),
        "N0Cov_ps_radps" => Dict("in" => f.Sin[1, 2], "ase" => f.Sase[1, 2]),
        "compressor_GDD_ps2" => f.Dc,
        "N0Var_Tcomp_ps2" => Dict("in" => f.comp_in, "ase" => f.comp_ase),
        "wall_s" => time() - t0)
    @printf("%s [%s]: E gain %.3f, rms width %.4f->%.4f ps, rms bw %.3f->%.3f rad/ps, Ehrenfest %.2e, edge %.1e, N0Var(Tcomp) = %.5g + (2nsp-1) %.5g ps^2, N0Var(Om) = %.5g + (2nsp-1) %.5g\n",
            name, TAG, r.E[end] / r.E[1], sqrt(r.sT2[1]), sqrt(r.sT2[end]), sqrt(r.sW2[1]), sqrt(r.sW2[end]), rel,
            maximum(r.edge), f.comp_in, f.comp_ase, f.Sin[2, 2], f.Sase[2, 2])
end
open(joinpath(OUT, "summary_$(TAG).json"), "w") do io
    print(io, jsonval(res))
end
println("done")
