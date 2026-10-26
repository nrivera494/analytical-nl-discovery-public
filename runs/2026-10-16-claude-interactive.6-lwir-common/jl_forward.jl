# Forward GNLSE run with the agents' solver (PulsePropagation), driven by files written by numpy.
# Usage: julia --project=solver jl_forward.jl <dir>
# <dir>/params.txt : nt dt omega0 L dz n2 S fR tau1 tau2 nsave   (one per line, "key value")
# <dir>/omega.txt  : centred detuning grid (rad/ps), <dir>/beta.txt : beta(omega0+W) (1/m)
# <dir>/alpha.txt  : power loss (1/m) on the centred grid (optional)
# <dir>/At.txt     : two columns, real and imaginary part of the launch field on the centred time grid (sqrt W)
# Writes <dir>/jl_out_Aw_photon.txt (final spectral field, photon units, centred), <dir>/jl_out_N.txt (photons at saved z)
using PulsePropagation, DelimitedFiles, FFTW
dir = ARGS[1]
p = Dict{String,Float64}()
for line in eachline(joinpath(dir, "params.txt"))
    k, v = split(strip(line)); p[k] = parse(Float64, v)
end
nt = Int(p["nt"]); dt = p["dt"]
omega = vec(readdlm(joinpath(dir, "omega.txt")))
beta = vec(readdlm(joinpath(dir, "beta.txt")))
At = readdlm(joinpath(dir, "At.txt"))
field = reshape(ComplexF64.(At[:, 1] .+ 1im .* At[:, 2]), nt, 1, 1)
grid = TimeGrid{Float64}(nt, dt)
domain = MMGNLSEDomain(:time; time_grid=grid)
alpha = isfile(joinpath(dir, "alpha.txt")) ? vec(readdlm(joinpath(dir, "alpha.txt"))) : 0.0
raman = p["fR"] > 0 ? AgarwalRaman(; fraction=p["fR"], tau1=p["tau1"], tau2=p["tau2"]) : NoRaman()
params = MMGNLSEParameters(domain; length=p["L"], alpha=alpha, beta=SampledBeta(omega, beta),
                           S=p["S"], n2=p["n2"], omega0=p["omega0"], raman=raman)
nsave = Int(p["nsave"])
saveat = collect(range(0.0, p["L"], length=nsave + 1))
t0 = time()
sol = solve_mmgnlse(field, params, p["dz"]; saveat=saveat)
wall = time() - t0
Nz = [photon_number(sol; z=i) for i in 1:length(sol.z)]
B = get_spectral_field(sol; z=:final, units=:photon)
writedlm(joinpath(dir, "jl_out_Aw_photon.txt"), hcat(real.(B[:, 1, 1]), imag.(B[:, 1, 1])))
writedlm(joinpath(dir, "jl_out_N.txt"), hcat(sol.z, Nz))
open(joinpath(dir, "jl_out_meta.txt"), "w") do io
    println(io, "wall_s ", wall)
    println(io, "rel_photon_drift ", (Nz[end] - Nz[1]) / Nz[1])
end
println("wall ", wall, " s; rel photon drift ", (Nz[end] - Nz[1]) / Nz[1])
