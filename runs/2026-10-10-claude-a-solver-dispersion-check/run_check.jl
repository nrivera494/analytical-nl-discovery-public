# run_check.jl -- main driver. Usage:
#   JULIA_NUM_THREADS=2 julia --project=solver --startup-file=no \
#       runs/2026-10-10-claude-a-solver-dispersion-check/run_check.jl <case> [<case> ...]
# Cases are defined in CASES below (and in config.yaml). Each case writes
#   <raw>/<case>.npz  (S, mean output field, eigenvalues of V and V_amp, kept bins)
#   <raw>/<case>.json (scalar results)
# and the summary.json in the run folder is rebuilt from all <raw>/*.json after every case.
include(joinpath(@__DIR__, "sdc_lib.jl"))
using NPZ
BLAS.set_num_threads(2); FFTW.set_num_threads(1)

const RUN_ID = "2026-10-10-claude-a-solver-dispersion-check"
const RAW = joinpath(homedir(), "analytical-nl-discovery-data", RUN_ID)
const RUNDIR = @__DIR__
const PHI = 5.0
const L = 1.0
const T0 = 1.0
b2(x) = x * T0^2 / (PHI^2 * L)            # |beta2| in ps^2/m for x = Phi^2 L / L_D

const CASES = Dict(
    "b0"        => (beta2=0.0,       x=0.0, nt=512, dz=0.002, omega0=2π*193.4*1000, role="main"),
    "p0.1"      => (beta2=+b2(0.1),  x=0.1, nt=512, dz=0.002, omega0=2π*193.4*1000, role="main"),
    "m0.1"      => (beta2=-b2(0.1),  x=0.1, nt=512, dz=0.002, omega0=2π*193.4*1000, role="main"),
    "p1"        => (beta2=+b2(1.0),  x=1.0, nt=512, dz=0.002, omega0=2π*193.4*1000, role="main"),
    "m1"        => (beta2=-b2(1.0),  x=1.0, nt=512, dz=0.002, omega0=2π*193.4*1000, role="main"),
    "m1_dzhalf" => (beta2=-b2(1.0),  x=1.0, nt=512, dz=0.001, omega0=2π*193.4*1000, role="dz-convergence check of m1"),
    "b0_dzhalf" => (beta2=0.0,       x=0.0, nt=512, dz=0.001, omega0=2π*193.4*1000, role="dz-convergence check of b0"),
    "m0.1_dzhalf" => (beta2=-b2(0.1), x=0.1, nt=512, dz=0.001, omega0=2π*193.4*1000, role="dz-convergence check of m0.1 (MI-dominated lambda_min)"),
    "m0.1_nt400"=> (beta2=-b2(0.1),  x=0.1, nt=400, dz=0.002, omega0=2π*193.4*1000, role="diagnostic: time-grid sensitivity (dt=0.04 ps)"),
    "b0_nt400"  => (beta2=0.0,       x=0.0, nt=400, dz=0.002, omega0=2π*193.4*1000, role="diagnostic: time-grid sensitivity (dt=0.04 ps)"),
    "b0_selfsteep" => (beta2=0.0,    x=0.0, nt=512, dz=0.002, omega0=2π*193.4,      role="diagnostic: physical omega0 (1550 nm), solver's built-in self-steepening active"),
)

jsonify(x::AbstractString) = "\"" * replace(x, "\\" => "\\\\", "\"" => "\\\"") * "\""
jsonify(x::Bool) = x ? "true" : "false"
jsonify(x::Integer) = string(x)
jsonify(x::Real) = isfinite(x) ? repr(Float64(x)) : "null"
jsonify(x::Nothing) = "null"
jsonify(x::AbstractVector) = "[" * join(jsonify.(x), ", ") * "]"
jsonify(x::Symbol) = jsonify(String(x))
function jsonify(d::AbstractDict; indent=0)
    pad = " "^(indent + 2)
    items = [pad * jsonify(string(k)) * ": " *
             (v isa AbstractDict ? jsonify(v; indent=indent + 2) : jsonify(v))
             for (k, v) in sort(collect(d); by=first)]
    return "{\n" * join(items, ",\n") * "\n" * " "^indent * "}"
end

function run_case(name)
    spec = CASES[name]
    @printf("=== case %s: beta2=%+.6g ps^2/m, x=%.3g, nt=%d, dz=%.4g m, omega0=%.6g rad/ps ===\n",
            name, spec.beta2, spec.x, spec.nt, spec.dz, spec.omega0)
    flush(stdout)
    wall0 = time()
    case = make_case(; nt=spec.nt, window=16.0, beta2=spec.beta2, L=L, gamma=0.01,
                     omega0=spec.omega0, Phi=PHI, T0=T0)
    sol = forward(case, spec.dz)
    Abar = ComplexF64.(vec(get_temporal_field(sol; z=:final)))
    i0 = case.nt ÷ 2 + 1
    S = build_S(case, sol, spec.dz)
    # finite-difference spot check of the whole S on two random directions
    rng = MersenneTwister(20261010)
    fd_err = Float64[]
    for _ in 1:2
        d = randn(rng, 2case.nt)
        fdv = fd_direction(case, spec.dz, d; eps_rel=1e-6)
        push!(fd_err, maximum(abs.(S * d .- fdv)) / maximum(abs.(fdv)))
    end
    nums = covariance_numbers(S, Abar)
    sdef = symplectic_defect(S)
    # locality of S (only meaningful for beta2 = 0): norm outside the per-bin 2x2 blocks
    N = case.nt
    mask = falses(2N, 2N)
    for j in 1:N, a in (j, j + N), b in (j, j + N)
        mask[a, b] = true
    end
    nonlocal = norm(S[.!mask]) / norm(S)
    energy_drift = sum(abs2, Abar) / sum(abs2, case.A0) - 1
    edge = round(Int, 0.05N)
    edge_frac = (sum(abs2, Abar[1:edge]) + sum(abs2, Abar[end-edge+1:end])) / sum(abs2, Abar)
    wall = time() - wall0
    res = Dict{String,Any}(
        "case" => name, "role" => spec.role,
        "beta2_ps2_per_m" => spec.beta2, "x" => spec.x,
        "Phi" => PHI, "L_m" => L, "T0_ps" => T0, "gamma_per_W_m" => case.gamma,
        "P0_W" => case.P0, "omega0_rad_per_ps" => spec.omega0, "n2_m2_per_W" => case.n2,
        "nt" => N, "window_ps" => 16.0, "dt_ps" => case.grid.dt,
        "dz_m" => spec.dz, "nsteps" => round(Int, L / spec.dz),
        "lambda_min" => nums.lam_min, "lambda_min_from_svd_of_S" => nums.lam_min_svd,
        "lambda_max" => nums.lam_max,
        "lambda_gen" => nums.lam_gen, "lambda_gen_max" => nums.lam_gen_max,
        "n_bins_kept" => nums.nkept, "pad_factor" => 4, "keep_threshold" => 1e-6,
        "path" => "discrete adjoint: one solve_adjoint(...; adjoint_mode=:discrete_rk4ip) per row of S (2N rows); both lambda_min and lambda_gen from this S",
        "fd_check_max_rel_err" => fd_err,
        "symplectic_defect_max_abs" => sdef,
        "nonlocal_fraction_of_S" => nonlocal,
        "energy_drift" => energy_drift, "edge_energy_fraction_5pct" => edge_frac,
        "peak_phase_check_rad" => angle(Abar[i0] / case.A0[i0]),
        "ideal_dispersionless_lambda_min" => ideal_dispersionless_lambda_min(PHI),
        "wall_s" => wall,
    )
    npzwrite(joinpath(RAW, name * ".npz"), Dict(
        "S" => S, "Abar_re" => real.(Abar), "Abar_im" => imag.(Abar),
        "A0_re" => real.(vec(case.A0)), "t_ps" => case.t,
        "eig_V" => nums.ev, "eig_Vamp" => nums.eva))
    open(joinpath(RAW, name * ".json"), "w") do io
        println(io, jsonify(res))
    end
    @printf("  lambda_min=%.8g (svd %.8g)  lambda_gen=%.8g  nkept=%d  FDerr=%s  sympl=%.2e  nonlocal=%.2e  wall=%.0f s\n",
            nums.lam_min, nums.lam_min_svd, nums.lam_gen, nums.nkept, string(round.(fd_err; sigdigits=3)),
            sdef, nonlocal, wall)
    flush(stdout)
    return res
end

function rebuild_summary()
    files = filter(f -> endswith(f, ".json"), readdir(RAW))
    cases = Dict{String,Any}()
    for f in files
        txt = read(joinpath(RAW, f), String)
        cases[replace(f, ".json" => "")] = txt
    end
    # assemble by text to avoid a JSON parser dependency
    body = join([pad_json(k, cases[k]) for k in sort(collect(keys(cases)))], ",\n")
    open(joinpath(RUNDIR, "summary_cases.json"), "w") do io
        println(io, "{\n", body, "\n}")
    end
end
pad_json(k, txt) = "  " * jsonify(k) * ": " * replace(strip(txt), "\n" => "\n  ")

for name in ARGS
    run_case(name)
    rebuild_summary()
end
