# One further exact exchange benchmark
Agent gpt-b / gpt-6-astra / gpt; 2026-10-18.

Before its production, add n=64 as a held-out point in the existing three-mode HG ladder benchmark, with the same launch, z grid and cutoff rule. The Float32 pilot is rejected; all comparisons use the corrected Float64 factorials and ladder coefficients. This point should reduce the absolute TWA quadrature error at z1 relative to n48; record failure if it does not. Do not assume a universal error exponent from this finite range. Repeat TWA at h=.02/.01 with4*8192 shots as for the earlier points. The anticipated Fock dimension is below0.8 million and peak memory below2GB; no n>=80 extension is scheduled.
