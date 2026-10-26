# Forward run with the agents' solver that writes the photon-unit spectral field at every saved plane.
# Usage: julia --project=solver jl_forward_planes.jl <dir>   (same input files as jl_forward.jl, plus nsave)
# Output: <dir>/jl_planes_z.txt, <dir>/jl_planes_B.bin (Float64, column-major [re; im] for nt x nplanes), <dir>/jl_meta.txt
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
B = get_spectral_field(sol; z=:all, units=:photon)[:, 1, 1, :]
writedlm(joinpath(dir, "jl_planes_z.txt"), sol.z)
open(joinpath(dir, "jl_planes_B.bin"), "w") do io
    write(io, real.(B)); write(io, imag.(B))
end
open(joinpath(dir, "jl_meta.txt"), "w") do io
    println(io, "wall_s ", wall); println(io, "nplanes ", length(sol.z)); println(io, "nt ", nt)
end
println("wall ", wall)
