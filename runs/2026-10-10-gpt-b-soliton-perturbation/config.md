# Configuration

agent: gpt-b; model: gpt-6-astra; family: gpt.

Run `soliton_odd_perturbations.py --output <raw>/summary.json` with the Python
environment and thread limits in the Kerr run. Fundamental coherent sech,
no Raman, normalized distance 3, window 40, 256 temporal samples, 600 fixed
RK4IP steps, and output spectral halfwidth 6. The generator/pullback is the
one independently compared with the public solver in the physical run.

The baseline is s=delta3=0. For each perturbation separately use both signs
of .001, .002, .004 and .008. Here s=1/(omega0*T0) and
delta3=beta3/(6*abs(beta2)*T0). Negative s is a formal parity check, not a
negative-carrier physical experiment. The full numerical grid has positive
photon metric in every case. The fixed centered mask is abs(k)<.7368.

All readout quartets and best masks are recorded. The measured order uses
differences from the unperturbed case under parameter halving. A change in
the best binary branch is reported separately from fixed-mask or isolated
eigenvalue perturbation theory.
