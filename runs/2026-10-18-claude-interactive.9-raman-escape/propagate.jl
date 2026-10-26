# Raman escape check for C-20261018-pi-chatgpt-01 (claude-interactive.9): the bound concerns input scattering data
# of the integrable NLSE. Propagate a TL N = 2 sech (T0 = 100 fs, 1550 nm, beta2 only) in the agents' solver at b9fa957
# with the Agarwal Raman response and, as a control, with NoRaman(); save 17 planes (z = 0, L/16, ..., L). The Python analysis
# measures the ZS eigenvalue of the separated leading soliton with the verifier's own ZS solver.
using PulsePropagation
using FFTW

c_light = 2.99792458e-4            # m/ps
Nt = 2^14
time_window = 16.384               # ps (dt = 1 fs)
lam0 = 1550e-9
w0 = 2pi * c_light / lam0
grid = TimeGrid(Nt, time_window)
domain = MMGNLSEDomain(degrees_of_freedom(:time), grid)
t = time_axis(grid)
n2 = 2.6e-20
Aeff = 80e-12
beta2 = -21.7e-27 * 1e24           # ps^2/m
betas = reshape([0.0, 0.0, beta2], :, 1)
gamma = n2 * w0 / c_light / Aeff
N = parse(Float64, get(ENV, "NSOL", "2"))
T0 = parse(Float64, get(ENV, "T0PS", "0.100"))
LD = T0^2 / abs(beta2)
L = parse(Float64, get(ENV, "LOVERLD", "6")) * LD
P0 = N^2 * abs(beta2) / (gamma * T0^2)
nsteps = parse(Int, get(ENV, "NSTEPS", "6000"))
dz = L / nsteps
outdir = joinpath(homedir(), "analytical-nl-discovery-data", "2026-10-18-claude-interactive.9-raman-escape")
mkpath(outdir)
for (label, raman) in (("raman", AgarwalRaman(fraction=0.18, tau1=0.0122, tau2=0.0320)), ("noraman", NoRaman()))
    field = zeros(ComplexF64, Nt, 1, 1)
    field[:, 1, 1] = sqrt(P0) .* sech.(t ./ T0)
    params = MMGNLSEParameters(domain; length=L, beta=TaylorBeta(betas), S=1 / Aeff, n2=n2, omega0=w0, raman=raman)
    t_start = time()
    sol = solve_mmgnlse(field, params, dz; saveat=L / 16)
    wall = time() - t_start
    A = get_temporal_field(sol; z=:all, units=:power)
    Aall = reshape(A, Nt, :)
    tag = "N$(N)_T0$(T0)_L$(round(L/LD, digits=2))LD_n$(nsteps)_$(label)"
    open(io -> write(io, ComplexF64.(Aall)), joinpath(outdir, "fields_" * tag * ".bin"), "w")
    println(label, " planes=", size(Aall, 2), " gamma=", gamma, " P0=", P0, " LD=", LD, " L=", L, " dz=", dz, " wall_s=", wall, " tag=", tag)
end
open(io -> write(io, collect(Float64, t)), joinpath(outdir, "t_f64.bin"), "w")
