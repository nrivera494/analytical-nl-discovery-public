# Driver for run 2026-10-08-claude-b.5-solver-twomode-check.
#
# Usage (from the repository root):
#   JULIA_NUM_THREADS=2 julia --project=solver --startup-file=no \
#       runs/2026-10-08-claude-b.5-solver-twomode-check/run_twomode.jl <stage> [<stage> ...]
#
# Every computed point is appended as one JSON object per line to
#   ~/analytical-nl-discovery-data/2026-10-08-claude-b.5-solver-twomode-check/results.jsonl
# and the frequency axis, bin indices and final photon-unit spectra are written to
#   .../npz/<tag>.npz
# summarize.py turns results.jsonl into summary.json.
#
# Stages:
#   exact_*  : coherent elements S1221 = S2112 = 0 (symmetric = false), kappa = 0.
#              This is the incoherent model itself (no averaging error).
#   sym_*    : the specified tensor (all two-1/two-2 elements = S0/2) with a
#              propagation-constant offset kappa = Delta beta0 * L_D on mode 2,
#              dz chosen so that 2 kappa dz <= 0.2.

include(joinpath(@__DIR__, "twomode_lib.jl"))
using NPZ

FFTW.set_num_threads(1)
BLAS.set_num_threads(1)

const RUN_ID = "2026-10-08-claude-b.5-solver-twomode-check"
const RAW = joinpath(homedir(), "analytical-nl-discovery-data", RUN_ID)
mkpath(joinpath(RAW, "npz"))
const RESULTS = joinpath(RAW, "results.jsonl")

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
    open(RESULTS, "a") do io
        println(io, jsonval(d))
    end
end

"""Run one parameter point: forward, diagnostics, F for every kmax."""
function run_point(case::Case; stage::String, tag::String)
    setup = build(case)
    sol, t_fwd = forward(case, setup)
    diag = diagnostics(setup, sol)
    res = fano_all(case, setup, sol)
    nsteps = length(sol.cache.integration_z) - 1
    k = bin_index(setup.Omega, case.window * T0)
    spectrum = get_spectral_field(sol; z=:final, units=:photon)[:, :, 1]
    npzdata = Dict{String,Any}(
        "Omega_T0" => collect(setup.Omega .* T0),
        "k" => collect(k),
        "final_spectrum_photon_re" => real.(spectrum),
        "final_spectrum_photon_im" => imag.(spectrum))
    for kmax in case.kmax_list
        r = res[kmax]
        Fano = r.F
        rec = Dict{String,Any}(
            "stage" => stage, "tag" => tag, "label" => case.label,
            "p2" => case.p2, "C22" => case.C22, "delta" => case.delta,
            "zeta" => case.zeta, "kappa" => case.kappa,
            "symmetric_S" => case.symmetric, "Nt" => case.Nt,
            "window_T0" => case.window, "dz_LD" => case.dz,
            "nsteps" => nsteps, "omega0T0" => case.omega0T0,
            "Sigma" => setup.Sigma, "kmax" => kmax,
            "edge_OmegaT0" => (kmax + 0.5) * 2pi / case.window,
            "N" => r.N, "F" => Fano,
            "var_frac_mode2" => r.var_mode2 / (r.var_mode1 + r.var_mode2),
            "E0" => diag.E0, "EL" => diag.EL, "peak0" => diag.pk0,
            "peakL" => diag.pkL, "t_forward_s" => t_fwd,
            "t_adjoint_s" => r.adj_time)
        record(rec)
        @printf("%-10s %-34s p2=%.3f C22=%.2f d=%.2f z=%.1f kap=%.0e sym=%d Nt=%d dz=%.2e w0T0=%.1e kmax=%d  F=%.12f  (fwd %.1fs adj %.1fs)\n",
                stage, tag, case.p2, case.C22, case.delta, case.zeta, case.kappa,
                case.symmetric, case.Nt, case.dz, case.omega0T0, kmax, Fano,
                t_fwd, r.adj_time)
        flush(stdout)
    end
    npzwrite(joinpath(RAW, "npz", tag * ".npz"), npzdata)
    return res
end

const KALL = [3, 4, 5, 6, 7]
const DZ_EXACT = 5.0e-4         # production step for the exact (no-FWM) tensor
const W0 = 1.0e6                # production omega0*T0 (self-steepening s = 1e-6)

dz_sym(kappa) = 0.1 / kappa     # 2*kappa*dz = 0.2

function stage_exact_main()
    pts = Case[]
    # case 1: Manakov check (C22 = 1)
    for p2 in (0.0, 0.3)
        push!(pts, Case(label="case1", p2=p2, C22=1.0, zeta=2.0))
    end
    # case 2
    for p2 in (0.0, 0.1, 0.2, 0.3)
        push!(pts, Case(label="case2", p2=p2, C22=0.5, zeta=2.0))
    end
    # case 4
    for p2 in (0.0, 0.15, 0.3)
        push!(pts, Case(label="case4", p2=p2, C22=0.5, zeta=5.0))
    end
    # case 5 (reference p2 = 0 at zeta = 2 is the case-2 p2 = 0 point)
    for d in (0.1, 0.2)
        push!(pts, Case(label="case5", p2=0.5, C22=1.0, delta=d, zeta=2.0))
    end
    # case 6
    for p2 in (0.1, 0.3)
        push!(pts, Case(label="case6", p2=p2, C22=0.75, zeta=2.0))
    end
    for c0 in pts
        c = Case(; label=c0.label, p2=c0.p2, C22=c0.C22, delta=c0.delta,
                 zeta=c0.zeta, kappa=0.0, symmetric=false, dz=DZ_EXACT,
                 omega0T0=W0, kmax_list=KALL)
        tag = @sprintf("exact_%s_p%.2f_C%.2f_d%.2f_z%.0f", c.label, c.p2, c.C22,
                       c.delta, c.zeta)
        run_point(c; stage="exact_main", tag=tag)
    end
end

function stage_exact_conv()
    # step, grid and self-steepening checks on the exact tensor
    base = [Case(label="case2", p2=0.0, C22=0.5, zeta=2.0),
            Case(label="case2", p2=0.3, C22=0.5, zeta=2.0),
            Case(label="case4", p2=0.3, C22=0.5, zeta=5.0),
            Case(label="case5", p2=0.5, C22=1.0, delta=0.2, zeta=2.0)]
    for c0 in base
        for (vname, dz, Nt, w0) in (("dz_x2", 2DZ_EXACT, 256, W0),
                                    ("dz_half", DZ_EXACT / 2, 256, W0),
                                    ("Nt_x2", DZ_EXACT, 512, W0),
                                    ("w0T0_1e7", DZ_EXACT, 256, 1.0e7))
            c = Case(; label=c0.label, p2=c0.p2, C22=c0.C22, delta=c0.delta,
                     zeta=c0.zeta, kappa=0.0, symmetric=false, dz=dz, Nt=Nt,
                     omega0T0=w0, kmax_list=KALL)
            tag = @sprintf("exact_conv_%s_%s_p%.2f_d%.2f_z%.0f", vname, c.label,
                           c.p2, c.delta, c.zeta)
            run_point(c; stage="exact_conv_" * vname, tag=tag)
        end
    end
end

function stage_exact_selfsteep()
    # F versus s = 1/(omega0 T0); 1215.4 = 2 pi c / 1550 nm at T0 = 1 ps
    for w0 in (2pi * C_LIGHT / 1550e-9, 1.0e4, 1.0e5, 1.0e6, 1.0e7)
        for c0 in (Case(label="case2", p2=0.3, C22=0.5, zeta=2.0),
                   Case(label="case5", p2=0.5, C22=1.0, delta=0.2, zeta=2.0))
            c = Case(; label=c0.label, p2=c0.p2, C22=c0.C22, delta=c0.delta,
                     zeta=c0.zeta, kappa=0.0, symmetric=false, dz=DZ_EXACT,
                     omega0T0=w0, kmax_list=[5])
            tag = @sprintf("exact_ss_%s_p%.2f_d%.2f_w0T0_%.4g", c.label, c.p2,
                           c.delta, w0)
            run_point(c; stage="exact_selfsteep", tag=tag)
        end
    end
end

function stage_exact_smallzeta()
    for z in (0.001, 0.01, 0.1)
        for p2 in (0.0, 0.3)
            c = Case(label="case1_smallzeta", p2=p2, C22=1.0, zeta=z, kappa=0.0,
                     symmetric=false, dz=min(DZ_EXACT, z / 20), omega0T0=W0,
                     kmax_list=KALL)
            tag = @sprintf("exact_smallzeta_p%.2f_z%.3g", p2, z)
            run_point(c; stage="exact_smallzeta", tag=tag)
        end
    end
end

# ---- specified tensor with Delta beta0 ------------------------------------

function sym_case(c0::Case, kappa; dzfac=1.0, Nt=256, kmax_list=KALL)
    return Case(; label=c0.label, p2=c0.p2, C22=c0.C22, delta=c0.delta,
                zeta=c0.zeta, kappa=kappa, symmetric=true,
                dz=dz_sym(kappa) * dzfac, Nt=Nt, omega0T0=W0,
                kmax_list=kmax_list)
end

symtag(c, extra="") = @sprintf("sym_%s_p%.2f_C%.2f_d%.2f_z%.0f_kap%.0f_dz%.3g_Nt%d%s",
                               c.label, c.p2, c.C22, c.delta, c.zeta, c.kappa,
                               c.dz, c.Nt, extra)

function stage_sym_case1()
    for kappa in (1.0e3, 2.0e3)
        c = sym_case(Case(label="case1", p2=0.3, C22=1.0, zeta=2.0), kappa)
        run_point(c; stage="sym_case1", tag=symtag(c))
    end
end

function stage_sym_case2()
    for kappa in (1.0e3, 2.0e3)
        for p2 in (0.1, 0.2, 0.3)
            c = sym_case(Case(label="case2", p2=p2, C22=0.5, zeta=2.0), kappa)
            run_point(c; stage="sym_case2", tag=symtag(c))
        end
    end
end

function stage_sym_conv()
    c0 = Case(label="case2", p2=0.3, C22=0.5, zeta=2.0)
    # halve dz at kappa = 1e3 and at kappa = 2e3
    for kappa in (1.0e3, 2.0e3)
        c = sym_case(c0, kappa; dzfac=0.5, kmax_list=[5])
        run_point(c; stage="sym_conv_dz_half", tag=symtag(c))
    end
    # double Nt at fixed window
    c = sym_case(c0, 1.0e3; Nt=512, kmax_list=[5])
    run_point(c; stage="sym_conv_Nt_x2", tag=symtag(c))
    # larger kappa: 1/kappa scaling of the averaging error
    for kappa in (4.0e3, 8.0e3)
        c = sym_case(c0, kappa; kmax_list=[5])
        run_point(c; stage="sym_conv_kappa", tag=symtag(c))
    end
end

function stage_sym_case4()
    for kappa in (1.0e3, 2.0e3)
        for p2 in (0.15, 0.3)
            c = sym_case(Case(label="case4", p2=p2, C22=0.5, zeta=5.0), kappa)
            run_point(c; stage="sym_case4", tag=symtag(c))
        end
    end
end

function stage_sym_case5()
    for kappa in (1.0e3, 2.0e3)
        for d in (0.1, 0.2)
            c = sym_case(Case(label="case5", p2=0.5, C22=1.0, delta=d, zeta=2.0), kappa)
            run_point(c; stage="sym_case5", tag=symtag(c))
        end
    end
end

function stage_sym_case6()
    for kappa in (1.0e3, 2.0e3)
        for p2 in (0.1, 0.3)
            c = sym_case(Case(label="case6", p2=p2, C22=0.75, zeta=2.0), kappa)
            run_point(c; stage="sym_case6", tag=symtag(c))
        end
    end
end

# ---- independent checks ----------------------------------------------------

"""
Finite-difference check of the adjoint sensitivity: for random complex
directions v in photon units, compare [N(B0 + eps v) - N(B0 - eps v)]/(2 eps)
with 2 Re sum conj(lambda) v, where lambda = dN/dconj(B(0)) from the discrete
RK4IP adjoint.
"""
function fd_check_point(case::Case; tag::String, ndir::Int=3, eps::Float64=1e-2)
    setup = build(case)
    sol, _ = forward(case, setup)
    k = bin_index(setup.Omega, case.window * T0)
    kmax = case.kmax_list[1]
    obs = SpectralPhotonNumber(filter=bandpass(k, kmax), modes=:all)
    lambda_L = terminal_condition(obs, sol)
    adj = solve_adjoint(lambda_L, setup.parameters, case.dz * setup.LD;
                        forward_solution=sol, adjoint_mode=:discrete_rk4ip)
    lam = get_spectral_field(adj; units=:photon)            # centered, photon units
    w = photon_weights(setup.parameters.domain.time_grid, setup.parameters.omega0)
    A0w = fftshift(ifft(setup.initial, 1), 1)
    B0 = A0w .* sqrt.(w)
    rng_state = 1234
    for d in 1:ndir
        # deterministic pseudo-random direction (LCG) so the check is reproducible
        v = zeros(ComplexF64, size(B0))
        for i in eachindex(v)
            rng_state = mod(1103515245 * rng_state + 12345, 2^31)
            re = rng_state / 2^31 - 0.5
            rng_state = mod(1103515245 * rng_state + 12345, 2^31)
            im_ = rng_state / 2^31 - 0.5
            v[i] = complex(re, im_)
        end
        v ./= norm(v)
        Nval = Float64[]
        for sgn in (1.0, -1.0)
            Bw = B0 .+ sgn * eps .* v
            Aw = Bw ./ sqrt.(w)
            At = fft(ifftshift(Aw, 1), 1)
            s2 = solve_mmgnlse(At, setup.parameters, case.dz * setup.LD)
            push!(Nval, value(obs, s2))
        end
        fd = (Nval[1] - Nval[2]) / (2eps)
        an = 2real(sum(conj.(lam) .* v))
        rec = Dict{String,Any}("stage" => "fd_check", "tag" => tag,
            "label" => case.label, "p2" => case.p2, "C22" => case.C22,
            "delta" => case.delta, "zeta" => case.zeta, "kappa" => case.kappa,
            "symmetric_S" => case.symmetric, "Nt" => case.Nt,
            "dz_LD" => case.dz, "omega0T0" => case.omega0T0, "kmax" => kmax,
            "direction" => d, "eps_photon" => eps, "dN_fd" => fd,
            "dN_adjoint" => an, "rel_diff" => (fd - an) / abs(an))
        record(rec)
        @printf("fd_check %-30s dir %d  fd %.12e  adjoint %.12e  rel %.2e\n",
                tag, d, fd, an, (fd - an) / abs(an))
        flush(stdout)
    end
end

function stage_fd_check()
    c = Case(label="case2", p2=0.3, C22=0.5, zeta=2.0, kappa=0.0,
             symmetric=false, dz=DZ_EXACT, omega0T0=W0, kmax_list=[5])
    fd_check_point(c; tag="fd_exact_case2_p0.30_k5")
    c = Case(label="case5", p2=0.5, C22=1.0, delta=0.2, zeta=2.0, kappa=0.0,
             symmetric=false, dz=DZ_EXACT, omega0T0=W0, kmax_list=[3])
    fd_check_point(c; tag="fd_exact_case5_d0.20_k3")
    c = sym_case(Case(label="case2", p2=0.3, C22=0.5, zeta=2.0), 1.0e3;
                 kmax_list=[5])
    fd_check_point(c; tag="fd_sym_case2_p0.30_kap1000_k5")
end

"Scalar soliton check: peak power and rms width along z for p2 = 0."
function stage_soliton_check()
    for (dz, Nt) in ((DZ_EXACT, 256), (DZ_EXACT, 512))
        c = Case(label="soliton", p2=0.0, C22=0.5, zeta=5.0, kappa=0.0,
                 symmetric=false, dz=dz, Nt=Nt, omega0T0=W0)
        setup = build(c)
        sol = solve_mmgnlse(setup.initial, setup.parameters, dz * setup.LD;
                            saveat=0.5 * setup.LD)
        At = get_temporal_field(sol; z=:all)
        t = setup.t
        pk = [maximum(abs2, At[:, 1, 1, j]) for j in axes(At, 4)]
        E = [sum(abs2, At[:, 1, 1, j]) for j in axes(At, 4)]
        tc = [sum(t .* abs2.(At[:, 1, 1, j])) / E[j] for j in axes(At, 4)]
        rmsw = [sqrt(sum((t .- tc[j]) .^ 2 .* abs2.(At[:, 1, 1, j])) / E[j])
                for j in axes(At, 4)]
        rec = Dict{String,Any}("stage" => "soliton_check",
            "tag" => @sprintf("soliton_Nt%d_dz%.3g", Nt, dz), "Nt" => Nt,
            "dz_LD" => dz, "omega0T0" => W0, "z_LD" => collect(sol.z ./ setup.LD),
            "peak_power_over_P0" => pk ./ P0(),
            "rms_width_over_T0" => rmsw ./ T0,
            "rms_width_sech_exact" => pi / sqrt(12),
            "max_abs_peak_dev" => maximum(abs.(pk ./ P0() .- 1)),
            "max_abs_width_dev" => maximum(abs.(rmsw ./ rmsw[1] .- 1)))
        record(rec)
        @printf("soliton_check Nt=%d dz=%.2e  max|P/P0-1| = %.3e  max|w/w0-1| = %.3e  w0=%.12f (pi/sqrt12=%.12f)\n",
                Nt, dz, rec["max_abs_peak_dev"], rec["max_abs_width_dev"],
                rmsw[1], pi / sqrt(12))
        flush(stdout)
    end
end

"""
Residual coherent-FWM end effect: the O(1/kappa) correction to the output
field oscillates as exp(+-2i kappa zeta_L). At zeta = 2, kappa -> kappa + j pi/8
shifts that end phase by j pi/2 while leaving the secular part unchanged.
"""
function stage_sym_osc()
    c0 = Case(label="case2", p2=0.3, C22=0.5, zeta=2.0)
    for j in 1:3
        c = sym_case(c0, 1.0e3 + j * pi / 8; kmax_list=[5])
        run_point(c; stage="sym_osc", tag=symtag(c, @sprintf("_j%d", j)))
    end
end

"""
kappa scan with the end phase 2 kappa zeta locked to 0 mod 2pi (zeta = 2:
kappa = m pi/2), so that F(kappa) - F(exact) has a single 1/kappa coefficient.
"""
function stage_sym_kscan_locked()
    c0 = Case(label="case2", p2=0.3, C22=0.5, zeta=2.0)
    for m in (637, 1273, 2546, 5093)
        c = sym_case(c0, m * pi / 2; kmax_list=[5])
        run_point(c; stage="sym_kscan_locked", tag=symtag(c, @sprintf("_m%d", m)))
    end
end

function stage_sym_kscan_locked_long()
    c0 = Case(label="case2", p2=0.3, C22=0.5, zeta=2.0)
    for m in (10186,)
        c = sym_case(c0, m * pi / 2; kmax_list=[5])
        run_point(c; stage="sym_kscan_locked", tag=symtag(c, @sprintf("_m%d", m)))
    end
end

"With the coherent elements removed, Delta beta0 must have no effect at all."
function stage_exact_kappa()
    for kappa in (1.0e3, 2.0e3)
        c = Case(label="case2", p2=0.3, C22=0.5, zeta=2.0, kappa=kappa,
                 symmetric=false, dz=DZ_EXACT, omega0T0=W0, kmax_list=KALL)
        tag = @sprintf("exact_kappa_case2_p0.30_kap%.0f", kappa)
        run_point(c; stage="exact_kappa", tag=tag)
    end
end

const STAGES = Dict(
    "exact_kappa" => stage_exact_kappa,
    "sym_osc" => stage_sym_osc,
    "sym_kscan_locked" => stage_sym_kscan_locked,
    "sym_kscan_locked_long" => stage_sym_kscan_locked_long,
    "fd_check" => stage_fd_check,
    "soliton_check" => stage_soliton_check,
    "exact_main" => stage_exact_main,
    "exact_conv" => stage_exact_conv,
    "exact_selfsteep" => stage_exact_selfsteep,
    "exact_smallzeta" => stage_exact_smallzeta,
    "sym_case1" => stage_sym_case1,
    "sym_case2" => stage_sym_case2,
    "sym_conv" => stage_sym_conv,
    "sym_case4" => stage_sym_case4,
    "sym_case5" => stage_sym_case5,
    "sym_case6" => stage_sym_case6,
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
