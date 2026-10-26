# Driver for run 2026-10-10-claude-b.6-solver-weighted-raman.
#
# Weighted spectral readouts N_w = sum_k w_k n_k with claude-b's weights
# (weights_for_solver.json; bins k in claude-b's numpy convention, solver bin = -k,
# called "mirror" here; "given" puts w_k on solver bin +k).
# F_w = Var(N_w) / sum_k w_k^2 nbar_k, Var from the discrete RK4IP adjoint
# (input vacuum) plus, with Raman, the Langevin contraction (coth 300 K).
#
# Usage (repository root):
#   JULIA_NUM_THREADS=2 julia --project=solver --startup-file=no \
#       runs/2026-10-10-claude-b.6-solver-weighted-raman/run_wr.jl <stage> ...
#
# nd_lib.jl and raman_bath_spectrum.jl are unchanged copies from run
# 2026-10-10-claude-b.6-solver-nd-check.

include(joinpath(@__DIR__, "nd_lib.jl"))
using Statistics

FFTW.set_num_threads(1)
BLAS.set_num_threads(1)

const RUN_ID = "2026-10-10-claude-b.6-solver-weighted-raman"
const RAW = joinpath(homedir(), "analytical-nl-discovery-data", RUN_ID)
mkpath(RAW)
const RESULTS = joinpath(RAW, "results.jsonl")
const WNAMES = ("w_centroid", "w_lambda_gen_eigvec", "w_best_binary")

jsonval(x::AbstractString) = "\"" * escape_string(x) * "\""
jsonval(x::Bool) = x ? "true" : "false"
jsonval(x::Integer) = string(x)
jsonval(x::AbstractFloat) = isfinite(x) ? repr(Float64(x)) : "null"
jsonval(x::Nothing) = "null"
jsonval(x::Symbol) = jsonval(string(x))
jsonval(x::AbstractVector) = "[" * join(jsonval.(x), ",") * "]"
jsonval(x::AbstractDict) =
    "{" * join(["\"$(k)\":" * jsonval(v) for (k, v) in x], ",") * "}"
record(d) = open(io -> println(io, jsonval(d)), RESULTS, "a")

"Read weights_for_solver.json with a minimal parser (the solver env has no JSON package)."
function load_weights(path=joinpath(@__DIR__, "weights.toml"))
    d = TOML.parsefile(path)
    out = Dict{String,Any}()
    for (key, v) in d
        out[key] = Dict("bins_k" => Int.(v["bins_k"]),
                        [n => Float64.(v[n]) for n in WNAMES]...)
    end
    return out
end
const WEIGHTS = load_weights()

"Weight vector on the solver's centered axis; mirror=true puts w_k on solver bin -k."
function weight_vector(setup, key, wname; mirror::Bool)
    p = WEIGHTS[key]
    pos = Dict(ki => i for (i, ki) in enumerate(setup.k))
    w = zeros(length(setup.k))
    for (kk, wk) in zip(p["bins_k"], p[wname])
        kk2 = mirror ? -kk : kk
        haskey(pos, kk2) || error("bin $kk2 not on the grid")
        w[pos[kk2]] = wk
    end
    return w
end

"Photon-number spectrum moments (Omega T0 units) with counting weights wcount."
function bandwidth(c::NDCase, setup, sol, wcount)
    out = Dict{String,Float64}()
    for (lab, z) in (("in", :initial), ("out", :final))
        n = wcount .* abs2.(get_spectral_field(sol; z=z)[:, 1, 1])
        x = setup.Omega .* c.T0
        m = sum(x .* n) / sum(n)
        v = sum((x .- m) .^ 2 .* n) / sum(n)
        out["mean_" * lab] = m
        out["var_" * lab] = v
    end
    out["ratio_var_in_over_out"] = out["var_in"] / out["var_out"]
    return out
end

coth300(c::NDCase, f0_THz) = ifftshift(raman_langevin_spectrum_coth(c.Nt, window(c) / c.Nt,
    f0_THz, c.gamma; raman_fraction=0.18, tau1=0.0122, tau2=0.0320, temperature_K=300.0))

"""
One forward solve, then F_w for every weight and side.
counting = :solver -> photon weights 1/(hbar(omega0_run + Omega)) (physical when omega0 is);
counting = :uniform_1550 -> photons counted uniformly at hbar*omega0(1550 nm) (used when
omega0 T0 is a numerical device); the reservoir prefactor hbar*omega0/gamma then uses the
1550 nm carrier, i.e. the reservoir is normalized to physical photons at 1550 nm.
"""
function run_weighted(c::NDCase; stage, key, counting::Symbol, raman_contraction::Bool,
                      sides=(true, false), wnames=WNAMES)
    setup = build(c)
    saveat = raman_contraction ? :steps : nothing
    sol, tfwd = forward(c, setup; saveat=saveat)
    wrun = photon_w(c, c.omega0)
    wcount, f0res = if counting === :solver
        wrun, c.omega0 / (2pi)
    elseif counting === :uniform_1550
        wp = photon_w(c, OMEGA0_1550)
        i0 = findfirst(==(0), setup.k)
        fill(wp[i0], length(wp)), OMEGA0_1550 / (2pi)
    else
        error("counting")
    end
    bw = bandwidth(c, setup, sol, wcount)
    Cw = raman_contraction ? coth300(c, f0res) : nothing
    diag = diagnostics(c, setup, sol)
    specL = abs2.(get_spectral_field(sol; z=:final)[:, 1, 1])
    nbar = wcount .* specL
    nbar_in = wcount .* abs2.(get_spectral_field(sol; z=:initial)[:, 1, 1])
    for mirror in sides, wname in wnames
        wvec = weight_vector(setup, key, wname; mirror=mirror)
        eff = [wrun[i] > 0 ? wvec[i] * wcount[i] / wrun[i] : 0.0 for i in eachindex(wvec)]
        obs = SpectralPhotonNumber(filter=eff, modes=:all)
        Nw = value(obs, sol)
        D = sum(wvec .^ 2 .* nbar)
        lam = terminal_condition(obs, sol)
        t0 = time()
        adj = solve_adjoint(lam, setup.params, dzstep(c); forward_solution=sol,
                            adjoint_mode=:discrete_rk4ip, saveat=saveat)
        tadj = time() - t0
        lam0 = get_spectral_field(adj; z=:initial, units=:power)[:, 1, 1]
        var = sum(wcount[i] > 0 ? abs2(lam0[i]) / wcount[i] : 0.0 for i in eachindex(wcount))
        rec = Dict{String,Any}(
            "stage" => stage, "label" => c.label, "key" => key, "weight" => wname,
            "side" => mirror ? "mirror(claude-b convention, solver bin -k)" : "given(solver bin +k)",
            "mirror" => mirror, "counting" => string(counting),
            "N_soliton" => c.N, "zr" => c.zr, "xi_L" => c.zr * xi_wb(c.N), "T0_ps" => c.T0,
            "beta2" => c.beta2, "gamma" => c.gamma, "P0_W" => P0(c), "length_m" => zlen(c),
            "omega0T0" => c.omega0 * c.T0, "raman" => c.raman, "Nt" => c.Nt,
            "dt_fs" => window(c) / c.Nt * 1e3, "nsteps" => c.nsteps,
            "Nw_mean" => Nw, "denominator_sum_w2_nbar" => D, "var_input_vacuum" => var,
            "F_det" => var / D, "t_forward_s" => tfwd, "t_adjoint_s" => tadj)
        for (k, v) in bw
            rec["bw_" * k] = v
        end
        # if N_w were exactly conserved: F_w = sum w^2 nbar_in / sum w^2 nbar_out (same bins)
        rec["conserved_prediction_sum_w2_nin_over_sum_w2_nout"] = sum(wvec .^ 2 .* nbar_in) / D
        # share of sum (Omega - mean)^2 n_out lying outside the weight bins
        let x = setup.Omega .* c.T0, m = bw["mean_out"], inb = wvec .!= 0
            tot = sum((x .- m) .^ 2 .* nbar)
            rec["out_var_share_outside_weight_bins"] = 1 - sum(((x .- m) .^ 2 .* nbar)[inb]) / tot
        end
        for (k, v) in pairs(diag)
            rec["diag_" * string(k)] = v
        end
        line = @sprintf("%-10s %-14s %-9s %-20s %-6s Nt=%d n=%d w0T0=%.4g  F_det=%.10f  bwratio=%.10f",
                        stage, c.label, key, wname, mirror ? "mirror" : "given", c.Nt, c.nsteps,
                        c.omega0 * c.T0, var / D, bw["ratio_var_in_over_out"])
        if raman_contraction
            for ss in (false, true)
                rv = raman_variance(c, setup, sol, adj; Cw=Cw, ssweight=ss)
                lab = ss ? "ssweight" : "notebook"
                rec["varR_coth300_" * lab * "_trap"] = rv.trap
                rec["varR_coth300_" * lab * "_rect"] = rv.rect
                rec["F_R_" * lab] = rv.trap / D
                rec["F_total_" * lab] = (var + rv.trap) / D
            end
            line *= @sprintf("  F_R(nb)=%.8f  F_R(ss)=%.8f", rec["F_R_notebook"], rec["F_R_ssweight"])
        end
        record(rec)
        println(line, @sprintf("  (fwd %.1fs adj %.1fs)", tfwd, tadj))
        flush(stdout)
    end
end

# ---------------- cases ----------------

kerr(key; N, zr, Nt=512, nsteps=4000, omega0T0=1.0e9) =
    NDCase(label="kerr_s0", N=N, zr=zr, T0=1.0, beta2=1.0, gamma=1.0, omega0=omega0T0,
           Nt=Nt, nsteps=nsteps, raman=false, Sinv=1.0e10)

fibre(; N=10.0, zr=0.7, omega0=OMEGA0_1550, Nt=2048, nsteps=4000, raman=true, label="") =
    NDCase(label=label, N=N, zr=zr, T0=0.1, beta2=0.020, gamma=0.010, omega0=omega0,
           Nt=Nt, nsteps=nsteps, raman=raman, Sinv=1.0e11)

const PTS = (("N10_zr0.7", 10.0, 0.7), ("N20_zr0.3", 20.0, 0.3))

stage_1() = for (key, N, zr) in PTS
    run_weighted(kerr(key; N, zr); stage="1_kerr", key=key, counting=:solver,
                 raman_contraction=false)
end

stage_1conv() = for (key, N, zr) in PTS
    run_weighted(kerr(key; N, zr, nsteps=2000); stage="1_conv_n2000", key=key,
                 counting=:solver, raman_contraction=false, sides=(true,))
    run_weighted(kerr(key; N, zr, Nt=1024); stage="1_conv_Nt1024", key=key,
                 counting=:solver, raman_contraction=false, sides=(true,))
end

# (2a) self-steepening suppressed (omega0 T0 = 1e6, as B_noss), no Raman, Nt = 512
stage_2a() = run_weighted(fibre(omega0=1.0e6 / 0.1, Nt=512, raman=false, label="2a_noss"),
                          stage="2a", key="N10_zr0.7", counting=:uniform_1550,
                          raman_contraction=false)

# (2b) self-steepening suppressed (omega0 T0 = 1e9), Raman on
stage_2b(; Nt=2048, nsteps=4000, sides=(true, false), tag="2b") =
    run_weighted(fibre(omega0=1.0e9 / 0.1, Nt=Nt, nsteps=nsteps, raman=true, label="2b_noss_raman"),
                 stage=tag, key="N10_zr0.7", counting=:uniform_1550, raman_contraction=true,
                 sides=sides)

# (2c) self-steepening on (1550 nm) + Raman; physical photon counting
stage_2c(; Nt=2048, nsteps=4000, sides=(true, false), tag="2c") =
    run_weighted(fibre(Nt=Nt, nsteps=nsteps, raman=true, label="2c_ss_raman"),
                 stage=tag, key="N10_zr0.7", counting=:solver, raman_contraction=true,
                 sides=sides)

# (3) N = 20, z = 0.3 z_wb, self-steepening + Raman
stage_3(; Nt=2048, nsteps=4000, sides=(true, false), tag="3") =
    run_weighted(fibre(N=20.0, zr=0.3, Nt=Nt, nsteps=nsteps, raman=true, label="3_ss_raman"),
                 stage=tag, key="N20_zr0.3", counting=:solver, raman_contraction=true,
                 sides=sides)

"""
Diagnostic for the centroid identity: claude-b's w_centroid lives on 282 (N10) / 237 (N20)
bins. Extend it to every grid bin, w(Omega) = -(Omega T0) - c (mirror mapping, c the
constant offset of the given weights), and compare F with var_in/var_out.
"""
function stage_1full()
    for (key, N, zr) in PTS
        for (Nt, ns) in ((512, 4000), (1024, 4000), (512, 2000))
            c = kerr(key; N, zr, Nt=Nt, nsteps=ns)
            setup = build(c)
            sol, _ = forward(c, setup)
            wrun = photon_w(c, c.omega0)
            p = WEIGHTS[key]
            dk = 2pi / 40
            off = mean(p["w_centroid"] .- p["bins_k"] .* dk)      # w = k dk + off
            x = setup.Omega .* c.T0
            for (lab, wvec) in (("full_grid", -x .+ off),
                                ("given_bins", weight_vector(setup, key, "w_centroid"; mirror=true)))
                obs = SpectralPhotonNumber(filter=wvec, modes=:all)
                nb_out = wrun .* abs2.(get_spectral_field(sol; z=:final)[:, 1, 1])
                nb_in = wrun .* abs2.(get_spectral_field(sol; z=:initial)[:, 1, 1])
                D = sum(wvec .^ 2 .* nb_out)
                adj = solve_adjoint(terminal_condition(obs, sol), setup.params, dzstep(c);
                                    forward_solution=sol, adjoint_mode=:discrete_rk4ip)
                var = sum(abs2, get_spectral_field(adj; z=:initial, units=:photon)[:, 1, 1])
                bw = bandwidth(c, setup, sol, wrun)
                pred = sum(wvec .^ 2 .* nb_in) / D
                rec = Dict{String,Any}("stage" => "1_identity_" * lab, "label" => c.label,
                    "key" => key, "weight" => "w_centroid_" * lab, "mirror" => true,
                    "Nt" => Nt, "nsteps" => ns, "omega0T0" => c.omega0 * c.T0,
                    "F_det" => var / D, "conserved_prediction" => pred,
                    "bw_ratio_var_in_over_out" => bw["ratio_var_in_over_out"],
                    "F_over_ratio_minus_1" => (var / D) / bw["ratio_var_in_over_out"] - 1,
                    "F_over_prediction_minus_1" => (var / D) / pred - 1, "offset" => off)
                record(rec)
                @printf("identity %-10s %-10s Nt=%d n=%d  F=%.12f  pred=%.12f  ratio=%.12f  F/ratio-1=%.3e  F/pred-1=%.3e\n",
                        key, lab, Nt, ns, var / D, pred, bw["ratio_var_in_over_out"],
                        rec["F_over_ratio_minus_1"], rec["F_over_prediction_minus_1"])
                flush(stdout)
            end
        end
    end
end

const STAGES = Dict(
    "1full" => stage_1full,
    "1" => stage_1, "1conv" => stage_1conv, "2a" => stage_2a,
    "2b" => () -> stage_2b(), "2c" => () -> stage_2c(), "3" => () -> stage_3(),
    "2b_n2000" => () -> stage_2b(nsteps=2000, sides=(true,), tag="2b_conv_n2000"),
    "2c_n2000" => () -> stage_2c(nsteps=2000, sides=(true,), tag="2c_conv_n2000"),
    "3_n2000" => () -> stage_3(nsteps=2000, sides=(true,), tag="3_conv_n2000"),
    "2b_Nt4096" => () -> stage_2b(Nt=4096, sides=(true,), tag="2b_conv_Nt4096"),
    "2c_Nt4096" => () -> stage_2c(Nt=4096, sides=(true,), tag="2c_conv_Nt4096"),
    "3_Nt4096" => () -> stage_3(Nt=4096, sides=(true,), tag="3_conv_Nt4096"),
    "2b_Nt8192" => () -> stage_2b(Nt=8192, nsteps=2000, sides=(true,), tag="2b_conv_Nt8192"),
    "2c_Nt8192" => () -> stage_2c(Nt=8192, nsteps=2000, sides=(true,), tag="2c_conv_Nt8192"),
    "3_Nt8192" => () -> stage_3(Nt=8192, nsteps=2000, sides=(true,), tag="3_conv_Nt8192"),
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
