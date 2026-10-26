# Second-solver cross-check (claude-interactive.8): case A3 (N=3, 100 fs FWHM, SMF-28 surrogate, 0.25 m)
# in the agents' solver at b9fa957 (forward only, no adjoint). Saves fields at 101 planes as raw data;
# the Python analysis computes E(z), Q(z), rho(z) from them with the verifier's own diagnostics.
using PulsePropagation
using FFTW
using DelimitedFiles

c_light = 2.99792458e-4            # m/ps
Nt = 2^14
time_window = 16.384               # ps  (dt = 1 fs)
lam0 = 1550e-9
w0 = 2pi * c_light / lam0          # rad/ps
grid = TimeGrid(Nt, time_window)
domain = MMGNLSEDomain(degrees_of_freedom(:time), grid)
t = time_axis(grid)

n2 = 2.6e-20
Aeff = 80e-12
beta2 = -21.7e-27 * 1e24           # ps^2/m
beta3 = 0.127e-39 * 1e36           # ps^3/m
betas = reshape([0.0, 0.0, beta2, beta3], :, 1)
gamma = n2 * w0 / c_light / Aeff   # 1/(W m)

N = 3
T0 = 0.100 / (2 * acosh(sqrt(2)))  # ps
P0 = N^2 * abs(beta2) / (gamma * T0^2)
L = 0.25
nsteps = 4000
dz = L / nsteps

field = zeros(ComplexF64, Nt, 1, 1)
field[:, 1, 1] = sqrt(P0) .* sech.(t ./ T0)

params = MMGNLSEParameters(domain; length=L, beta=TaylorBeta(betas), S=1 / Aeff, n2=n2, omega0=w0,
                           raman=AgarwalRaman(fraction=0.18, tau1=0.0122, tau2=0.0320))
t_start = time()
sol = solve_mmgnlse(field, params, dz; saveat=L / 100)
wall = time() - t_start
Azt = get_temporal_field(sol; z=:all, units=:power)
outdir = joinpath(homedir(), "analytical-nl-discovery-data", "2026-10-17-claude-interactive.8-concentration")
mkpath(outdir)
A2 = reshape(Azt, Nt, :)             # (Nt, planes)
open(io -> write(io, ComplexF64.(A2)), joinpath(outdir, "julia_A3_field_c128.bin"), "w")
open(io -> write(io, collect(Float64, t)), joinpath(outdir, "julia_A3_t_f64.bin"), "w")
println("gamma=", gamma, " P0=", P0, " size=", size(Azt), " planes=", size(A2, 2), " wall_s=", wall)
