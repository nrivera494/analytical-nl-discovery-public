# Driver for run 2026-10-10-claude-b.6-solver-nd-check.
#
# Usage (repository root):
#   JULIA_NUM_THREADS=2 julia --project=solver --startup-file=no \
#       runs/2026-10-10-claude-b.6-solver-nd-check/run_nd.jl <stage> [<stage> ...]
#
# Every computed (point, filter) is appended as one JSON object per line to
#   ~/analytical-nl-discovery-data/2026-10-10-claude-b.6-solver-nd-check/results.jsonl
# summarize.py turns results.jsonl into summary.json.
#
# Cases (see meta.yaml):
#   A  Kerr only, soliton units realized with T0 = 1 ps, beta2 = +1 ps^2/m,
#      gamma = 1 /W/m, omega0 T0 = 1e6 (self-steepening suppressed), NoRaman().
#   B  physical fibre: beta2 = 0.020 ps^2/m, gamma = 0.010 /W/m, T0 = 0.1 ps,
#      N = 10 (P0 = 20 kW), z = 0.7 xi_wb(10) L_D; self-steepening on (1550 nm),
#      and suppressed (omega0 T0 = 1e6), NoRaman().
#   C  as B with AgarwalRaman() (fR = 0.18, tau1 = 12.2 fs, tau2 = 32 fs),
#      self-steepening on, Nt = 2048 over 4 ps (dt = 1.95 fs); Raman Langevin
#      variance by adjoint contraction with the coth (symmetrized) spectrum.

include(joinpath(@__DIR__, "nd_lib.jl"))
using Random

FFTW.set_num_threads(1)
BLAS.set_num_threads(1)

const RUN_ID = "2026-10-10-claude-b.6-solver-nd-check"
const RAW = joinpath(homedir(), "analytical-nl-discovery-data", RUN_ID)
mkpath(RAW)
# Post-freeze stages (names starting with "post_") write to results_postfreeze.jsonl so the
# results.jsonl hashed in meta.yaml stays unchanged.
const RESULTS = Ref(joinpath(RAW, "results.jsonl"))
const FILTERS = load_filters()
const FNAMES = ("best_binary_bins", "best_interval_bins")

jsonval(x::AbstractString) = "\"" * escape_string(x) * "\""
jsonval(x::Bool) = x ? "true" : "false"
jsonval(x::Integer) = string(x)
jsonval(x::AbstractFloat) = isfinite(x) ? repr(Float64(x)) : "null"
jsonval(x::Nothing) = "null"
jsonval(x::Symbol) = jsonval(string(x))
jsonval(x::AbstractVector) = "[" * join(jsonval.(x), ",") * "]"
jsonval(x::AbstractDict) =
    "{" * join(["\"$(k)\":" * jsonval(v) for (k, v) in x], ",") * "}"
jsonval(x::NamedTuple) =
    "{" * join(["\"$(k)\":" * jsonval(v) for (k, v) in pairs(x)], ",") * "}"

function record(d)
    open(RESULTS[], "a") do io
        println(io, jsonval(d))
    end
end

function base_record(c::NDCase, setup; stage, tag, key, fname, mirror, weights_label)
    return Dict{String,Any}(
        "stage" => stage, "tag" => tag, "label" => c.label, "key" => key,
        "filter" => fname, "mirror" => mirror, "weights" => weights_label,
        "N_soliton" => c.N, "zr" => c.zr, "xi_L" => c.zr * xi_wb(c.N),
        "T0_ps" => c.T0, "beta2_ps2_per_m" => c.beta2, "gamma_per_W_m" => c.gamma,
        "P0_W" => P0(c), "L_D_m" => L_D(c), "length_m" => zlen(c),
        "omega0_rad_per_ps" => c.omega0, "omega0T0" => c.omega0 * c.T0,
        "s_selfsteep" => 1 / (c.omega0 * c.T0),
        "Nt" => c.Nt, "window_T0" => c.window_T0, "dt_fs" => window(c) / c.Nt * 1e3,
        "nsteps" => c.nsteps, "dz_LD" => dzstep(c) / L_D(c),
        "raman" => c.raman ? "AgarwalRaman(fraction=0.18,tau1=0.0122ps,tau2=0.0320ps)" : "NoRaman",
        "n_bins" => length(FILTERS[key][fname]))
end

"""Forward once, then F for both filters of `key`, as given and mirrored."""
function run_point(c::NDCase; stage, key, weights=nothing, weights_label="solver",
                   raman_contraction::Bool=false, mirrors=(false, true))
    setup = build(c)
    saveat = raman_contraction ? :steps : nothing
    sol, tfwd = forward(c, setup; saveat=saveat)
    diag = diagnostics(c, setup, sol)
    nsteps_actual = length(sol.cache.integration_z) - 1
    spectra = raman_contraction ? raman_spectra(c) : nothing
    out = Dict{Tuple{String,Bool},Any}()
    for fname in FNAMES, mirror in mirrors
        filt = filter_mask(setup.k, FILTERS[key][fname]; mirror=mirror)
        r = fano(c, setup, sol, filt; weights=weights, saveat=saveat)
        tag = @sprintf("%s_%s_%s_%s%s_Nt%d_n%d", stage, c.label, key, fname,
                       mirror ? "_mirror" : "", c.Nt, c.nsteps)
        rec = base_record(c, setup; stage, tag, key, fname, mirror, weights_label)
        rec["nsteps_actual"] = nsteps_actual
        rec["Nmean"] = r.N
        rec["var_input_vacuum"] = r.var
        rec["F"] = r.F
        rec["t_forward_s"] = tfwd
        rec["t_adjoint_s"] = r.tadj
        for (kk, vv) in pairs(diag)
            rec["diag_" * string(kk)] = vv
        end
        line = @sprintf("%-8s %-10s %-10s %-19s mir=%d Nt=%d n=%d w0T0=%.4g  N=%.10e  F=%.12f",
                        stage, c.label, key, fname, mirror, c.Nt, c.nsteps,
                        c.omega0 * c.T0, r.N, r.F)
        if raman_contraction
            for (sname, Cw) in pairs(spectra), ss in (false, true)
                rv = raman_variance(c, setup, sol, r.adj; Cw=Cw, ssweight=ss)
                lab = string(sname) * (ss ? "_ssweight" : "_notebook")
                rec["varR_" * lab * "_rect"] = rv.rect
                rec["varR_" * lab * "_trap"] = rv.trap
                rec["F_total_" * lab * "_trap"] = (r.var + rv.trap) / r.N
                rec["F_total_" * lab * "_rect"] = (r.var + rv.rect) / r.N
                rec["nz_saved"] = rv.nz
            end
            line *= @sprintf("  varR(coth300,nb,trap)/N=%.6e  varR(coth300,ss,trap)/N=%.6e",
                             rec["varR_coth300_notebook_trap"] / r.N,
                             rec["varR_coth300_ssweight_trap"] / r.N)
        end
        record(rec)
        println(line, @sprintf("  (fwd %.1fs adj %.1fs)", tfwd, r.tadj))
        flush(stdout)
        out[(fname, mirror)] = r.F
    end
    return out
end

# ---------------- case A: Kerr only, soliton units ----------------

const A_POINTS = (("N10_zr0.7", 10.0, 0.7), ("N20_zr0.3", 20.0, 0.3))

caseA(key, N, zr; Nt=512, nsteps=4000, omega0T0=1.0e6) =
    NDCase(label="A", N=N, zr=zr, T0=1.0, beta2=1.0, gamma=1.0,
           omega0=omega0T0 / 1.0, Nt=Nt, nsteps=nsteps, raman=false, Sinv=1.0e10)

function stage_A()
    for (key, N, zr) in A_POINTS
        run_point(caseA(key, N, zr); stage="A", key=key)
    end
end

function stage_A_conv()
    for (key, N, zr) in A_POINTS
        for (v, kw) in (("n2000", (; nsteps=2000)), ("n8000", (; nsteps=8000)),
                        ("Nt1024", (; Nt=1024)), ("w0T0_1e7", (; omega0T0=1.0e7)))
            run_point(caseA(key, N, zr; kw...); stage="A_conv_" * v, key=key,
                      mirrors=(false,))
        end
    end
end

"""
Self-steepening/photon-weight residual: at omega0 T0 = 1e6 the mirrored filters
differ at O(s) = O(1e-6). Parity maps (filter T, s) to (-T, -s), so the
mirror average is F(s=0) + O(s^2); larger omega0 T0 checks this directly.
"""
function stage_A_w0()
    for (key, N, zr) in A_POINTS
        for w0 in (1.0e7, 1.0e8, 1.0e9)
            run_point(caseA(key, N, zr; omega0T0=w0); stage="A_w0", key=key)
        end
    end
end

function stage_A_conv2()
    for (key, N, zr) in A_POINTS
        for (v, kw) in (("n1000", (; nsteps=1000)), ("n16000", (; nsteps=16000)),
                        ("Nt2048", (; Nt=2048)))
            run_point(caseA(key, N, zr; kw...); stage="A_conv_" * v, key=key,
                      mirrors=(false,))
        end
    end
end

# ---------------- case B: physical fibre, self-steepening ----------------

caseB(; omega0=OMEGA0_1550, Nt=512, nsteps=4000, raman=false, label="B") =
    NDCase(label=label, N=10.0, zr=0.7, T0=0.1, beta2=0.020, gamma=0.010,
           omega0=omega0, Nt=Nt, nsteps=nsteps, raman=raman, Sinv=1.0e11)

function stage_B()
    key = "N10_zr0.7"
    # self-steepening on, physical carrier (1550 nm)
    run_point(caseB(label="B_ss"); stage="B", key=key)
    # self-steepening suppressed (omega0 T0 = 1e6), solver photon weights (uniform)
    c = caseB(omega0=1.0e6 / 0.1, label="B_noss")
    run_point(c; stage="B", key=key)
    # same dynamics, photons counted at the physical carrier (observable and input vacuum)
    run_point(c; stage="B", key=key, weights=photon_w(c, OMEGA0_1550),
              weights_label="physical_1550nm")
end

function stage_B_conv()
    key = "N10_zr0.7"
    run_point(caseB(nsteps=8000, label="B_ss"); stage="B_conv_n8000", key=key)
    run_point(caseB(Nt=1024, label="B_ss"); stage="B_conv_Nt1024", key=key)
    run_point(caseB(Nt=2048, label="B_ss"); stage="B_conv_Nt2048", key=key)
end

# ---------------- case C: Raman ----------------

function stage_C()
    key = "N10_zr0.7"
    run_point(caseB(Nt=2048, raman=true, label="C_ss_raman"); stage="C", key=key,
              raman_contraction=true)
end

function stage_C_conv()
    key = "N10_zr0.7"
    run_point(caseB(Nt=2048, nsteps=8000, raman=true, label="C_ss_raman");
              stage="C_conv_n8000", key=key, raman_contraction=true)
    run_point(caseB(Nt=4096, raman=true, label="C_ss_raman");
              stage="C_conv_Nt4096", key=key, raman_contraction=true)
end

function stage_C_conv2()
    key = "N10_zr0.7"
    run_point(caseB(Nt=2048, nsteps=2000, raman=true, label="C_ss_raman");
              stage="C_conv_n2000", key=key, raman_contraction=true, mirrors=(false,))
    run_point(caseB(Nt=1024, raman=true, label="C_ss_raman");
              stage="C_conv_Nt1024", key=key, raman_contraction=true, mirrors=(false,))
end

"""
The Raman kernel is sampled at t_n = n dt (h(0) = 0, kink at t = 0), so the
delayed response converges as O(dt^2): Nt = 1024 -> 2048 -> 4096 changes F by
1.3e-3 and 3.3e-4 (binary filter). Nt = 8192 (dt = 0.49 fs) checks the dt^2
extrapolation; nsteps = 2000 (dz is converged to 1e-11 at Nt = 2048).
"""
function stage_C_conv3()
    key = "N10_zr0.7"
    run_point(caseB(Nt=8192, nsteps=2000, raman=true, label="C_ss_raman");
              stage="C_conv_Nt8192", key=key, raman_contraction=true)
end

# ---------------- adjoint vs finite differences ----------------

"""
Central finite differences of N_T with respect to the input in photon units
along fixed pseudo-random complex directions v: compare
[N(B0 + eps v) - N(B0 - eps v)]/(2 eps) with 2 Re sum conj(lambda) v.
"""
function fd_check(c::NDCase, key, fname; ndir=2, eps=1e-2, tag="")
    setup = build(c)
    sol, _ = forward(c, setup)
    filt = filter_mask(setup.k, FILTERS[key][fname])
    obs = SpectralPhotonNumber(filter=filt, modes=:all)
    lam = terminal_condition(obs, sol)
    adj = solve_adjoint(lam, setup.params, dzstep(c); forward_solution=sol,
                        adjoint_mode=:discrete_rk4ip)
    lamB = get_spectral_field(adj; z=:initial, units=:photon)
    w = photon_w(c, c.omega0)
    A0w = fftshift(ifft(setup.initial, 1), 1)
    B0 = A0w .* sqrt.(w)
    rng = MersenneTwister(20261010)
    for d in 1:ndir
        v = randn(rng, ComplexF64, size(B0))
        v[w .<= 0] .= 0
        v ./= norm(v)
        Nval = Float64[]
        for sgn in (1.0, -1.0)
            Bw = B0 .+ sgn * eps .* v
            Aw = [w[i] > 0 ? Bw[i] / sqrt(w[i]) : zero(ComplexF64) for i in eachindex(w)]
            At = fft(ifftshift(reshape(Aw, size(B0)), 1), 1)
            s2 = solve_mmgnlse(At, setup.params, dzstep(c))
            push!(Nval, value(obs, s2))
        end
        fd = (Nval[1] - Nval[2]) / (2eps)
        an = 2real(sum(conj.(lamB) .* v))
        rec = base_record(c, setup; stage="fd_check", tag=tag * "_dir$d", key=key,
                          fname=fname, mirror=false, weights_label="solver")
        rec["direction"] = d
        rec["eps_photon"] = eps
        rec["dN_fd"] = fd
        rec["dN_adjoint"] = an
        rec["rel_diff"] = (fd - an) / abs(an)
        record(rec)
        @printf("fd_check %-28s dir %d  fd %.12e  adjoint %.12e  rel %.2e\n",
                tag, d, fd, an, (fd - an) / abs(an))
        flush(stdout)
    end
end

function stage_fd()
    fd_check(caseA("N10_zr0.7", 10.0, 0.7), "N10_zr0.7", "best_binary_bins"; tag="fd_A_N10")
    fd_check(caseB(Nt=2048, raman=true, label="C_ss_raman"), "N10_zr0.7",
             "best_binary_bins"; tag="fd_C_N10")
end

"""
Case C has N_T ~ 1e10 photons, so eps = 1e-2 photon units is limited by
rounding of N (about 1e-14 relative after 4000 steps); repeat with larger eps.
"""
function stage_fd2()
    for eps in (1.0, 3.0)
        fd_check(caseB(Nt=2048, raman=true, label="C_ss_raman"), "N10_zr0.7",
                 "best_binary_bins"; eps=eps, tag=@sprintf("fd_C_N10_eps%.0f", eps))
    end
end

"""
POST-FREEZE (added after summary.json was hashed, motivated only by the spectral sign
and photon-weight conventions of claude-b's numpy code, none of whose outputs had been
opened): self-steepening dynamics with photon counting uniform in frequency (observable
and input vacuum both use the Omega = 0 photon weight), as a uniform-weight soliton-unit
code with self-steepening s = 1/(omega0 T0) = 1/121.526 computes it.
"""
function stage_post_B_ss_uniform()
    RESULTS[] = joinpath(RAW, "results_postfreeze.jsonl")
    key = "N10_zr0.7"
    c = caseB(label="B_ss")
    w = photon_w(c, c.omega0)
    i0 = findfirst(==(0), build(c).k)
    run_point(c; stage="post_B", key=key, weights=fill(w[i0], length(w)),
              weights_label="uniform_Omega0")
    c2 = caseB(label="B_ss", nsteps=8000)
    w2 = photon_w(c2, c2.omega0)
    run_point(c2; stage="post_B_conv_n8000", key=key, weights=fill(w2[i0], length(w2)),
              weights_label="uniform_Omega0")
end

"""
POST-FREEZE: same as post_B_ss_uniform with s = 0.0082 exactly (omega0 T0 = 121.951)
instead of s = 1/121.526 = 0.0082287, to show the sensitivity of F to rounding s.
"""
function stage_post_B_ss_uniform_s0082()
    RESULTS[] = joinpath(RAW, "results_postfreeze.jsonl")
    key = "N10_zr0.7"
    c = caseB(label="B_ss_s0.0082", omega0=1 / (0.0082 * 0.1))
    w = photon_w(c, c.omega0)
    i0 = findfirst(==(0), build(c).k)
    run_point(c; stage="post_B_s0082", key=key, weights=fill(w[i0], length(w)),
              weights_label="uniform_Omega0")
end

const STAGES = Dict(
    "post_B_ss_uniform" => stage_post_B_ss_uniform,
    "post_B_ss_uniform_s0082" => stage_post_B_ss_uniform_s0082,
    "fd2" => stage_fd2,
    "C_conv3" => stage_C_conv3,
    "A" => stage_A, "A_conv" => stage_A_conv, "A_conv2" => stage_A_conv2,
    "A_w0" => stage_A_w0,
    "B" => stage_B, "B_conv" => stage_B_conv,
    "C" => stage_C, "C_conv" => stage_C_conv, "C_conv2" => stage_C_conv2,
    "fd" => stage_fd,
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
