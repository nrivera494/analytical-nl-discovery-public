# Independent weak-dispersion derivation

`weak_dispersion_derivation.md` contains the full local optical-generator calculation, its effective oscillator reduction, the peak-order generalization, the second-order coefficient, and the limits of the continuum proof. The calculations here import no repository code or data.

Install the dependencies from `../requirements.txt`. From the extracted `verification` directory:

```bash
python weak_theory/effective_oscillator.py
python weak_theory/second_order_symbolic.py
```

The first command uses NumPy and SciPy to solve three scalar oscillator problems with mesh refinement and Richardson extrapolation. It regenerates `oscillator_constants.json` in this directory. The harmonic ground energy should approach 1; the quartic and sextic energies should approach 1.06036209028 and 1.14480245368.

The second command uses SymPy to evaluate the time-ordered optical perturbation terms and opposite-branch mixing. It regenerates `second_order_symbolic.json`. Its relative second-order coefficient `c2(Phi)` is approximately 0.98946456305 at Phi=3 and 0.98034160063 at Phi=10, with large-Phi limit `2*sqrt(6)/5`.

Both programs locate their output beside the script and can be launched from any working directory. Reruns replace these named result files; copy the archive first if exact supplied hashes must be retained. No vendored dependency directory is required.

The oscillator ground-state minimization is rigorous. Extending the local optical expansion to an equality for the global continuum covariance minimum still requires a matching localization lower bound. The second-order optical remainder has not been proved uniformly over all modes.
