# Driver for run 2026-10-10-claude-b.6-solver-grid.
#
# Kerr-only weighted Fano factors F_w = Var(N_w) / sum_k w_k^2 nbar_k on claude-b's 12-point
# grid (weights_grid_for_solver.json), soliton units realized with T0 = 1 ps,
# beta2 = +1 ps^2/m, gamma = 1 /W/m (L_D = 1 m, P0 = N^2 W), omega0 T0 = 1e9 (s = 1e-9),
# NoRaman(), length = xi L_D with xi taken from the file. Weights on solver bin -k
# ("mirror", claude-b's convention). Var(N_w) from solve_adjoint(...; adjoint_mode=:discrete_rk4ip).
# Also: var_in/var_out of the photon-number spectrum (whole grid) and F_centroid with the
# centroid weight extended to every grid bin (exact identity check).
#
# Usage (repository root):
#   JULIA_NUM_THREADS=2 julia --project=solver --startup-file=no \
#       runs/2026-10-10-claude-b.6-solver-grid/run_grid.jl <stage> ...

include(joinpath(@__DIR__, "nd_lib.jl"))     # unchanged copy (bin_index, photon_w, C_LIGHT)
using Statistics

FFTW.set_num_threads(1)
BLAS.set_num_threads(1)

const RUN_ID = "2026-10-10-claude-b.6-solver-grid"
const RAW = joinpath(homedir(), "analytical-nl-discovery-data", RUN_ID)
mkpath(RAW)
const RESULTS = joinpath(RAW, "results.jsonl")
const WNAMES = ("w_centroid", "w_lambda_gen_eigvec", "w_best_binary")
const GRID = TOML.parsefile(joinpath(@__DIR__, "grid.toml"))
const ORDER = ["N5_zr0.3", "N5_zr0.7", "N5_zr1", "N5_zr1.5",
               "N10_zr0.3", "N10_zr0.7", "N10_zr1", "N10_zr1.5",
               "N20_zr0.3", "N20_zr0.7", "N20_zr1", "N20_zr1.5"]
const OMEGA0T0 = 1.0e9
const SINV = 1.0e10

jsonval(x::AbstractString) = "\"" * escape_string(x) * "\""
jsonval(x::Bool) = x ? "true" : "false"
jsonval(x::Integer) = string(x)
jsonval(x::AbstractFloat) = isfinite(x) ? repr(Float64(x)) : "null"
jsonval(x::Nothing) = "null"
jsonval(x::AbstractVector) = "[" * join(jsonval.(x), ",") * "]"
jsonval(x::AbstractDict) =
    "{" * join(["\"$(k)\":" * jsonval(v) for (k, v) in x], ",") * "}"
record(d) = open(io -> println(io, jsonval(d)), RESULTS, "a")

"Default steps: N^2 dz <= 0.002 (nonlinear phase per step), at least 4000, rounded up to 1000."
default_nsteps(N, xi) = max(4000, 1000 * ceil(Int, N^2 * xi / 0.002 / 1000))

function setup_point(key; Nt=nothing, nsteps=nothing)
    p = GRID[key]
    N, xi = Float64(p["N"]), Float64(p["xi"])
    Ntu = Nt === nothing ? Int(p["Nt"]) : Nt
    ns = nsteps === nothing ? default_nsteps(N, xi) : nsteps
    win = Float64(p["TW"])                  # T0 = 1 ps
    grid = TimeGrid(Ntu, win)
    domain = MMGNLSEDomain(degrees_of_freedom(:time), grid)
    omega0 = OMEGA0T0                       # rad/ps with T0 = 1 ps
    n2 = 1.0 * C_LIGHT / (omega0 * SINV)    # gamma = 1 /W/m
    params = MMGNLSEParameters(domain; length=xi, beta=TaylorBeta(reshape([0.0, 0.0, 1.0], :, 1)),
                               S=SINV, n2=n2, omega0=omega0, raman=NoRaman())
    t = time_axis(grid)
    Omega = frequency_axis(grid)
    k = bin_index(Omega, win)
    initial = zeros(ComplexF64, Ntu, 1, 1)
    initial[:, 1, 1] .= N .* exp.(-t .^ 2 ./ 2)     # sqrt(P0) = N
    w = Float64.(PulsePropagation.photon_bin_weights(Ntu, win / Ntu, omega0 / (2pi); shifted=true))
    return (; key, N, xi, Nt=Ntu, nsteps=ns, dz=xi / ns, win, params, Omega, k, initial, wph=w)
end

function weight_vector(s, wname)
    p = GRID[s.key]
    pos = Dict(ki => i for (i, ki) in enumerate(s.k))
    w = zeros(length(s.k))
    for (kk, wk) in zip(p["bins_k"], p[wname])
        haskey(pos, -kk) || error("bin $(-kk) not on the grid")
        w[pos[-kk]] = wk                    # claude-b bin k -> solver bin -k
    end
    return w
end

function Fw(s, sol, wvec, nb_out)
    obs = SpectralPhotonNumber(filter=wvec, modes=:all)
    D = sum(wvec .^ 2 .* nb_out)
    adj = solve_adjoint(terminal_condition(obs, sol), s.params, s.dz; forward_solution=sol,
                        adjoint_mode=:discrete_rk4ip)
    var = sum(abs2, get_spectral_field(adj; z=:initial, units=:photon)[:, 1, 1])
    return var / D, var, D, value(obs, sol)
end

function run_point(key; stage, Nt=nothing, nsteps=nothing)
    s = setup_point(key; Nt, nsteps)
    t0 = time()
    sol = solve_mmgnlse(s.initial, s.params, s.dz)
    tf = time() - t0
    nsteps_actual = length(sol.cache.integration_z) - 1
    nb_in = s.wph .* abs2.(get_spectral_field(sol; z=:initial)[:, 1, 1])
    nb_out = s.wph .* abs2.(get_spectral_field(sol; z=:final)[:, 1, 1])
    x = s.Omega                              # Omega T0 with T0 = 1
    m_in, m_out = sum(x .* nb_in) / sum(nb_in), sum(x .* nb_out) / sum(nb_out)
    v_in = sum((x .- m_in) .^ 2 .* nb_in) / sum(nb_in)
    v_out = sum((x .- m_out) .^ 2 .* nb_out) / sum(nb_out)
    nyq = maximum(abs.(x))
    rec = Dict{String,Any}("stage" => stage, "key" => key, "N" => s.N, "zr" => Float64(GRID[key]["zr"]),
        "xi" => s.xi, "length_used" => Float64(s.params.length), "Nt" => s.Nt, "grid_Nt_given" => Int(GRID[key]["Nt"]),
        "window_T0" => s.win, "nsteps" => s.nsteps, "nsteps_actual" => nsteps_actual, "dz_LD" => s.dz,
        "omega0T0" => OMEGA0T0, "side" => "mirror (solver bin -k)",
        "var_in" => v_in, "var_out" => v_out, "mean_in" => m_in, "mean_out" => m_out,
        "bandwidth_ratio_var_in_over_out" => v_in / v_out,
        "photon_rel_change" => sum(nb_out) / sum(nb_in) - 1,
        "out_frac_above_0.8_nyquist" => sum(nb_out[abs.(x) .> 0.8nyq]) / sum(nb_out),
        "out_frac_above_0.5_nyquist" => sum(nb_out[abs.(x) .> 0.5nyq]) / sum(nb_out),
        "t_forward_s" => tf)
    line = @sprintf("%-14s %-10s Nt=%d n=%d  ratio=%.10f", stage, key, s.Nt, s.nsteps, v_in / v_out)
    for wname in WNAMES
        wvec = weight_vector(s, wname)
        F, var, D, Nw = Fw(s, sol, wvec, nb_out)
        rec["F_" * wname] = F
        rec["var_" * wname] = var
        rec["D_" * wname] = D
        rec["Nw_" * wname] = Nw
        line *= @sprintf("  %s=%.10f", wname[3:8], F)
    end
    # centroid weight extended to every grid bin: w = -(Omega T0) + off (mirror mapping)
    p = GRID[key]
    off = mean(Float64.(p["w_centroid"]) .- Float64.(p["bins_k"]) .* (2pi / s.win))
    wfull = -x .+ off
    F, var, D, Nw = Fw(s, sol, wfull, nb_out)
    pred = sum(wfull .^ 2 .* nb_in) / D
    rec["centroid_offset"] = off
    rec["F_centroid_full_grid"] = F
    rec["F_centroid_full_grid_prediction_same_center"] = pred
    rec["F_full_over_ratio_minus_1"] = F / (v_in / v_out) - 1
    rec["F_full_over_prediction_minus_1"] = F / pred - 1
    rec["t_total_s"] = time() - t0
    record(rec)
    println(line, @sprintf("  full=%.10f  full/ratio-1=%.2e  (%.0fs)", F, F / (v_in / v_out) - 1, time() - t0))
    flush(stdout)
end

const STAGES = Dict(
    "base" => () -> foreach(k -> run_point(k; stage="base"), ORDER),
    "conv" => () -> begin
        key = "N20_zr1.5"
        ns = default_nsteps(GRID[key]["N"], GRID[key]["xi"])
        run_point(key; stage="conv_steps_half", nsteps=ns ÷ 2)
        run_point(key; stage="conv_steps_double", nsteps=2ns)
        run_point(key; stage="conv_Nt_double", Nt=2 * Int(GRID[key]["Nt"]))
    end,
    "ntdouble" => () -> foreach(k -> run_point(k; stage="Nt_double", Nt=2 * Int(GRID[k]["Nt"])),
                               filter(!=("N20_zr1.5"), ORDER)),
)

println("run ", RUN_ID, "  julia ", VERSION, "  threads ", Threads.nthreads(),
        "  solver ", strip(read(`git -C $(joinpath(@__DIR__, "..", "..", "solver")) rev-parse HEAD`, String)))
for name in ARGS
    haskey(STAGES, name) || error("unknown stage $name")
    t0 = time()
    println("=== stage ", name, " start ", Libc.strftime("%H:%M:%S", time()))
    flush(stdout)
    STAGES[name]()
    @printf("=== stage %s done in %.1f s\n", name, time() - t0)
    flush(stdout)
end
