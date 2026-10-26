# Run 2026-10-16-claude-b.7-solver-masks (agent claude-b.7, task T-20261016-claude-interactive-03).
# Evaluates claude-b's optimized input masks in FastDifferentiableMMNLO, model M0:
#   i u_xi + (1/2) u_tautau + N^2|u|^2 u = i delta3 u_tautautau, N = 3, delta3 = 0.05, xi_f = 2,
#   laser u = exp(-tau^2/2); input uhat_in(w) = a(w) exp(i phi(w)) uhat_laser(w) on the listed
#   bins (w = k 2pi/70, |w| <= 4.757), uhat_laser elsewhere. Solver convention
#   A(t) = sum_k A_k exp(-i w_k tau), A_k = fftshift(ifft(A(t))) (checked in run
#   2026-10-16-claude-b.7-solver-dwyield, stage lin), so A_k(0) is multiplied by a exp(i phi).
# Observables at xi = 2, normalized by the LASER energy sum_k |A_laser,k|^2 (before the mask):
#   eta_B  = sum_{w >= 1/(6 delta3)} |A_k|^2 / E_laser
#   eta_G  = same after multiplying A(t) by g = 1 - 0.5 [tanh(tau + 15) - tanh(tau - 15)]
# Masks were converted from claude-b's JSON (mask arrays only) to mask_<name>.npz in the raw folder.
#
# Usage: JULIA_NUM_THREADS=2 julia --project=solver --startup-file=no \
#            runs/2026-10-16-claude-b.7-solver-masks/masks.jl

include(joinpath(@__DIR__, "dw_lib.jl"))   # copy of runs/2026-10-16-claude-b.7-solver-dwyield/dw_lib.jl

FFTW.set_num_threads(1)
BLAS.set_num_threads(1)

const RUN_ID = "2026-10-16-claude-b.7-solver-masks"
const RAW = joinpath(homedir(), "analytical-nl-discovery-data", RUN_ID)
# omega0 T0 (self-steepening residual s = 1/(omega0 T0)); default 1e6. MASKS_W0T0=1e8 runs only the
# primary-grid cases and writes results_ss.jsonl (self-steepening residual check).
const W0T0 = parse(Float64, get(ENV, "MASKS_W0T0", "1e6"))
const RESULTS = W0T0 == 1.0e6 ? joinpath(RAW, "results_v2.jsonl") :   # v1 (results.jsonl) lacked the fractional-edge sums
                                joinpath(RAW, "results_ss.jsonl")

function load_mask(name)
    d = npzread(joinpath(RAW, "mask_$(name).npz"))
    return (; name, w=Float64.(d["w"]), k=Int.(d["k"]), phi=Float64.(d["phi"]), a=Float64.(d["a"]))
end

gate15(tau) = 1 .- 0.5 .* (tanh.(tau .+ 15) .- tanh.(tau .- 15))

case(Nt, TW, nsteps) = DWCase(; label="N3_d0.05", pulse=:gauss, N=3.0, delta3=0.05, xi=2.0,
                               window_T0=TW, Nt=Nt, nsteps=nsteps, omega0T0=W0T0)

"Masked input on a grid whose bin spacing is 2pi/70 (exact bin match by integer k)."
function masked_exact(c, s, mask)
    At = s.initial[:, 1, 1]
    mask === nothing && return At
    Ak = spec(At)
    dw = 2pi / c.window_T0
    kg = round.(Int, s.w ./ dw)
    pos = Dict(k => i for (i, k) in enumerate(kg))
    for j in eachindex(mask.k)
        Ak[pos[mask.k[j]]] *= mask.a[j] * cis(mask.phi[j])
    end
    return fft(ifftshift(Ak))
end

"Masked input with phi and a interpolated linearly in w (a = 1, phi = 0 outside the listed range)."
function masked_interp(c, s, mask)
    At = s.initial[:, 1, 1]
    Ak = spec(At)
    p = sortperm(mask.w)
    wm, phm, am = mask.w[p], mask.phi[p], mask.a[p]
    for (i, w) in enumerate(s.w)
        (w < wm[1] || w > wm[end]) && continue
        r = searchsortedfirst(wm, w)
        if wm[r] == w
            ph, a = phm[r], am[r]
        else
            l = r - 1
            t = (w - wm[l]) / (wm[r] - wm[l])
            ph = phm[l] + t * (phm[r] - phm[l])
            a = am[l] + t * (am[r] - am[l])
        end
        Ak[i] *= a * cis(ph)
    end
    return fft(ifftshift(Ak))
end

"Zero-pad a centered time-domain field (even Nt) into a centered grid with Nt_big points."
function embed(At::AbstractVector, Ntbig::Int)
    n = length(At)
    out = zeros(ComplexF64, Ntbig)
    out[(Ntbig ÷ 2 - n ÷ 2 + 1):(Ntbig ÷ 2 + n ÷ 2)] .= At
    return out
end

function evaluate(maskname, mask; Nt70=1024, nsteps=2000, wfac=1, mode="exact", tag="")
    c70 = case(Nt70, 70.0, nsteps)
    s70 = build(c70)
    if wfac == 1 || mode == "interp"
        c = wfac == 1 ? c70 : case(Nt70 * wfac, 70.0 * wfac, nsteps)
        s = wfac == 1 ? s70 : build(c)
        Alas = s.initial[:, 1, 1]
        Ain = mask === nothing ? Alas :
              (mode == "exact" ? masked_exact(c, s, mask) : masked_interp(c, s, mask))
    else
        c = case(Nt70 * wfac, 70.0 * wfac, nsteps)
        s = build(c)
        Alas = s.initial[:, 1, 1]
        Ain = embed(masked_exact(c70, s70, mask === nothing ? nothing : mask), c.Nt)
        Ain = mask === nothing ? Alas : Ain
    end
    t0 = time()
    sol = solve_mmgnlse(reshape(ComplexF64.(Ain), :, 1, 1), s.params, dz(c))
    tw = time() - t0
    AtL = sol.fields[:, 1, 1, end]
    Elas = sum(abs2, spec(Alas))
    band = s.w .>= 1 / (6 * 0.05)
    S = abs2.(spec(AtL))
    Sg = abs2.(spec(AtL .* gate15(s.tau)))
    Pin = abs2.(Ain)
    inv0 = invariants(c, Ain)
    inv1 = invariants(c, AtL)
    edge = abs.(s.tau) .> 0.85 * maximum(abs.(s.tau))
    PL = abs2.(AtL)
    dwg = s.w[2] - s.w[1]
    frac = clamp.((s.w .+ dwg / 2 .- 1 / (6 * 0.05)) ./ dwg, 0.0, 1.0)
    rec = Dict{String,Any}(
        "eta_B_fracedge" => sum(frac .* S) / Elas, "eta_G_fracedge" => sum(frac .* Sg) / Elas,
        "mask" => maskname, "mode" => mode, "tag" => tag, "omega0T0" => c.omega0T0, "Nt" => c.Nt, "TW" => c.window_T0,
        "dtau" => c.window_T0 / c.Nt, "w_max" => pi * c.Nt / c.window_T0, "nsteps" => nsteps,
        "dxi" => dz(c), "eta_B" => sum(S[band]) / Elas, "eta_G" => sum(Sg[band]) / Elas,
        "E_in_over_E_laser" => sum(abs2, spec(Ain)) / Elas,
        "E_out_over_E_in" => sum(S) / sum(abs2, spec(Ain)),
        "input_peak_power_ratio" => maximum(Pin) / maximum(abs2.(Alas)),
        "input_edge_power_ratio" => maximum(Pin[edge]) / maximum(Pin),
        "output_edge_power_ratio" => maximum(PL[edge]) / maximum(PL),
        "E_rel_drift" => inv1.E / inv0.E - 1, "P_abs_drift" => inv1.P - inv0.P,
        "H_rel_drift" => inv1.H / inv0.H - 1, "t_wall_s" => tw)
    open(RESULTS, "a") do io
        println(io, jsonval(rec))
    end
    @printf("%-8s %-6s %-10s Nt=%5d TW=%5.0f n=%5d  eta_B=%.8e  eta_G=%.8e  fracB=%.8e fracG=%.8e Ein/El=%.6f  inpk=%.3f inedge=%.1e outedge=%.1e dE=%.1e  (%.1fs)\n",
            maskname, mode, tag, c.Nt, c.window_T0, nsteps, rec["eta_B"], rec["eta_G"],
            rec["eta_B_fracedge"], rec["eta_G_fracedge"],
            rec["E_in_over_E_laser"], rec["input_peak_power_ratio"], rec["input_edge_power_ratio"],
            rec["output_edge_power_ratio"], rec["E_rel_drift"], tw)
    flush(stdout)
    return rec
end

masks = [("TL", nothing), ("phase", load_mask("phase")), ("passive", load_mask("passive"))]
if W0T0 != 1.0e6
    for (name, m) in masks, n in (2000, 8000)
        evaluate(name, m; Nt70=1024, nsteps=n, tag="R_w0T0_$(W0T0)")
    end
    exit()
end
for (name, m) in masks
    # claude-b's grid (TW 70, Nt 1024) and step (h = 0.001), then step halving twice
    for n in (2000, 4000, 8000)
        evaluate(name, m; Nt70=1024, nsteps=n, tag="R")
    end
    # finer tau grid (same bins), wider windows (input zero-padded in time: identical field)
    evaluate(name, m; Nt70=2048, nsteps=8000, tag="Ftau")
    evaluate(name, m; Nt70=1024, nsteps=8000, wfac=2, tag="W140")
    evaluate(name, m; Nt70=1024, nsteps=8000, wfac=4, tag="W280")
    # mask interpolated linearly in w onto the 2pi/140 bins (different input field; sensitivity)
    m === nothing || evaluate(name, m; Nt70=1024, nsteps=8000, wfac=2, mode="interp", tag="W140interp")
end
