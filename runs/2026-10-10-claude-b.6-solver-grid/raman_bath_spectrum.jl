# Raman Langevin spectrum with the symmetrized thermal factor.
#
# Shared by soliton_jitter.ipynb, squeezing_spectral_filter.ipynb and
# raman_stochastic_check.jl. Same grid, ordering and prefactor as
# PulsePropagation.raman_langevin_spectrum; only the thermal factor differs.
#
# For a Hermitian observable that is linear in the phonon noise m(z,t),
# Var = γ² ∫dz ∫dω/2π |B̂(ω)|² C(ω) with real B. Only C(ω) + C(-ω) enters, so
# the thermal phonon expectation values give
#     C(ω) = (ħ ω0 / γ) |Im h_R(|ω|)| coth(ħ|ω| / 2 k_B T)
#          = (ħ ω0 / γ) |Im h_R(|ω|)| (2 n_th(|ω|) + 1).
# The legacy factor (2 n_th + Θ(ω)) sums to 4 n_th + 1 per ± pair instead of
# 4 n_th + 2, which halves the zero-point part. The legacy function also sets
# the ω = 0 bin to zero. Its correct value is the finite thermal limit
# (ħ ω0 / γ) |Im h_R'(0)| (2 k_B T / ħ), evaluated here from the first nonzero bin.

using PulsePropagation

function raman_langevin_spectrum_coth(nt::Integer, dt::Real, f0::Real, gamma_eff::Real;
                                      raman_fraction::Real=0.18,
                                      tau1::Real=0.0122,     # ps, as in AgarwalRaman
                                      tau2::Real=0.0320,     # ps
                                      temperature_K::Real=300.0)
    T = Float64
    hRω = PulsePropagation.agarwal_raman_response(nt, T(dt), T(raman_fraction),
                                                   T(tau1 * 1e3), T(tau2 * 1e3))   # fs
    omega = PulsePropagation.ifft_frequency_grid(nt, T(dt))   # rad/ps, unshifted order
    hbar = 1.054571817e-34
    kb = 1.380649e-23
    prefactor = (hbar / gamma_eff) * (2π * f0 * 1e12)          # ħ ω0 / γ
    cω = zeros(T, nt)
    w1 = 0.0          # first nonzero |ω| (rad/s), for the DC limit
    imh1 = 0.0
    for k in 1:nt
        w = abs(omega[k]) * 1e12
        w == 0 && continue
        imh = abs(imag(hRω[k]))
        if w1 == 0.0 || w < w1
            w1, imh1 = w, imh
        end
        thermal = if temperature_K == 0
            1.0
        else
            x = hbar * w / (2kb * temperature_K)
            x > 350 ? 1.0 : coth(x)
        end
        cω[k] = prefactor * imh * thermal
    end
    for k in 1:nt
        if abs(omega[k]) * 1e12 == 0
            cω[k] = temperature_K == 0 ? 0.0 :
                    prefactor * (imh1 / w1) * (2kb * temperature_K / hbar)
        end
    end
    return cω
end
