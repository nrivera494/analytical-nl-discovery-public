# Sagnac pump-integral and photon-convention check
Agent gpt-b / gpt-6-astra / gpt; 2026-10-18. Frozen after the first Sagnac checks.

The original exact pump integral used1024 Dirichlet power samples, while the full Wigner check used65536. Their Phi30 variances differ by about.9%, so the claimed1% accuracy needs a pump-integral convergence test. Freeze two fresh scrambled Dirichlet integrations at2^14 and2^16 pump powers, seeds8881,8882, Phi30. Record sampling error separately from the exact conditional Kerr moments. Expect tracking variance minus coherent baseline to agree with the actual sampled relative power variance within5% (the original card's stricter1% is also scored, not silently replaced).

The first run defined n=1e10 per arm, hence2e10 input pump photons. Also test n=5e9 per arm (1e10 total input photons), same Phi30 and power distribution. No change of convention is allowed when quoting a number. The zero-jitter reference is exact Kerr evolution, not the tangent ellipse. No new physical claim is being proposed by this resolution extension.
