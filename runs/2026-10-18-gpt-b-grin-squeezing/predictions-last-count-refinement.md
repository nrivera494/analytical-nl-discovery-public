# Last counting refinement, frozen 2026-10-18
Agent gpt-b / gpt-6-astra / gpt.

The independent launch4203/disorder7603, E'=.6,sigma.3,n1e6,z100 case now has fixed-weight discrepancies10.979 and13.668dB at h=.01 and.005, and reoptimized discrepancies3.267 and2.590dB. These are not converged. The minimum mean occupation exceeds1000 on the .005 grid and the condensate coherence is0.9937. Before running h=.0025, freeze one final refinement at2048 shots, using the existing four vacuum scrambles and nested Brownian tree.

Score fixed physical weights, reoptimized count covariance, and cross-fitted weights separately. Apply the same .3dB or three-SE convergence gate to each discrepancy and require it to exceed the original .5dB tolerance by three SE before accepting a discrepancy for that observable. Because the vacuum samples are shared, use paired SE for the difference between grids. Do not use the larger quadrature sum of marginal SEs. The earlier core4201 refinement misses the paired gate (change .307dB versus tolerance .3dB); preserve it as marginal/unresolved.

The40000 integration steps are the already justified counting-convergence exception to2^15; store only eight snapshots. Run serially after final_checks.sh, before the final strong-disorder refinement. Stop further production by09:56 EDT to preserve the required final15minutes. If resources/time prevent this refinement, report the attack unresolved; do not substitute its coarse value.
