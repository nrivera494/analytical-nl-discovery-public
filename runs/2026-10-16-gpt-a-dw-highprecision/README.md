<!-- agent: gpt-a; model: gpt-6-astra; family: gpt -->

# Direct higher-precision gate test

This is a separate implementation of the same scalar RK4IP scheme, using
Double64 arithmetic and GenericFFT. Package versions are pinned in the local
Manifest.toml. The FFT round trip and the exact TOD-free gated breather are
checked before full propagation. The latter checks the radiation-free tail
at a level below the ordinary Float64 floor. A propagated TOD-free control,
step refinement, and doubled window accompany the full-TOD cases.

The definitions and tolerances were committed before propagation. The pilot
only measured cost and an exact null; it did not supply a new full-TOD
outcome. The raw serialized Double64 fields and already-gated spectra remain
outside git. Recomputing a very small gated spectrum after converting the
ungated field to Float64 would lose the precision being tested.

The library documentation was checked at the primary repositories:
[GenericFFT](https://github.com/JuliaApproximation/GenericFFT.jl) and
[DoubleFloats](https://github.com/JuliaMath/DoubleFloats.jl). This was a
software-capability check, not a further literature novelty search.

The first serial launcher completed its six numerical cases, then exited on
a trailing shell fragment after the launcher file had been revised while
it was running. The original `queue.log` is retained. The endpoint queue
was started only after that process exited, and skips completed TOML-marked
cases. No numerical result was overwritten by the restart. The resumed
launcher remains unchanged during execution.

The final spatial-resolution check is a matched pair at h=2.25/4096:
`precompression_grid_reference` uses 16384 points and `precompression_grid`
uses 32768, both in window 256. This revision was frozen before either
paired outcome to fit the numerical cutoff. The named grid dispatch prints
its actual design, superseding the older step argument in the already
running queue. Do not compare the fine-grid case directly against the
9216-step baseline as a grid error: that would also change the step. The
baseline's temporal error is checked independently at 9216 and 18432 steps.
