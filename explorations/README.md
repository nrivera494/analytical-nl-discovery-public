# Explorations

Free exploration of the simulator. One note per observed phenomenon, named `<date>-<agent>-<short-name>.md`:

- what was seen, with run ids and one figure;
- which simplicity signal it shows (few slow directions in the propagator Jacobian, data collapse under rescaling, a nearly conserved quantity, insensitivity to input, anomalous noise transfer);
- artefact checks done;
- whether it is worth a problem file, and if so the target quantity.

Useful search moves: continuation from a solvable limit (NLSE, Manakov, constant-gain similariton, cubic–quintic Ginzburg–Landau) toward the full model; Newton–Krylov for states that reproduce themselves up to a symmetry operation; optimization of inputs for a simplicity score with a robustness penalty.
