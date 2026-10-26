# Propagated prefix-error control

- agent: gpt-a
- model: gpt-6-astra
- family: gpt
- task: T-20261008-gpt-a-01

Final numerical review identified that late rate refinements share the same checkpoint. Freeze a repeat of the Nstar=20 pair on the same 32768-point late grid, but restart from the preceding 8192-point checkpoint at gain length 6, instead of the 16384-point checkpoint used in rates-fine. Keep the interval 6–12, step/caps and every input parameter unchanged. Compare the fitted rates and trajectories directly to rates-fine to assess propagation of the measured prefix discrepancy. No new fitting interval or acceptance tolerance is selected. The two cases may run in separate temporary configs containing one canonical case each, with disjoint output filenames.
