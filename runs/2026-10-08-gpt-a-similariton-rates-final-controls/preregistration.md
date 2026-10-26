# Final controls for the Nstar=20 rate measurement

- agent: gpt-a
- model: gpt-6-astra
- family: gpt
- task: T-20261008-gpt-a-01

After the additional Nstar=20 spatial doubling in rates-fine has been analyzed, freeze independent step/cap halving and window doubling at the preceding 16384-point spatial resolution. These checks address time and boundary errors separately from the already measured spatial error. Restart each archived Nstar=20 checkpoint at gain length 6, preserve the paired launch separation, and fit only the previously frozen interval 6–12 against the same hydrodynamic targets. Source hashes are recorded. Prefix accuracy is assessed by the existing 8192/16384 comparisons through gain length 6. Do not choose a new fitting interval to improve agreement. These are adaptive convergence controls, not held-out prediction tests.
