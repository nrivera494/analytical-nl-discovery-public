# Final strong-disorder resolution check, frozen 2026-10-18
Agent gpt-b / gpt-6-astra / gpt.

The original h=.005/.0025 comparison failed its individual-path gate at sigma=2,3. No result at h=.00125 or .000625 has been generated. Keep the same gates, rather than relaxing them: paired ensemble-mean change <.3 dB and every individual-path change <1 dB, at z=10,20. Test E'=.3, launch4201, disorder7601..7612, sigma2 and3, with the same nested Brownian tree. Record both finest-grid changes, even if they fail. This is a refinement of known cases, not a fresh held-out ensemble.

For sigma3, first path7601, also propagate the n=1e10 nonlinear vacuum ensemble at h=.00125 and .000625, four scrambles of256 shots. The same-path nonlinear-minus-tangent deviation should remain within1dB. These calculations test high-occupation curvature and stochastic resolution separately; agreement of nonlinear and tangent at the same step is not itself convergence to the continuum. No new claim or physical disorder calibration follows from this check.

Stop at z=20: the finest grid has32000 integration steps, below2^15, and stores only seven snapshots. No parallel numerical process. This extension and the originally frozen missing QMC occupations64,1024 run after final_checks.sh has finished. If time or memory prevents completion, leave the corresponding checks explicitly unresolved.
