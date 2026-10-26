# Independent normal-dispersion audit

Agent `gpt-e`, model `gpt-6-astra`, family `gpt`, 2026-10-19.

`run.py` uses only the new solver written in the sibling auditor run
`2026-10-19-gpt-e-weak-dispersion/tangent.py`. No cited prior numerical run,
Hermite basis, or proposer code is imported.

Run `run.py --suite pilot`, `--suite main`, `--suite edges`, `--suite checks`,
and `--suite theorem` serially with the Python executable specified by the PI
and `-W ignore`. Check system memory before each heavy launch. The tests use
one numerical thread. Arrays are saved outside git under the run's raw-data
directory.

The full covariance is applied matrix-free. Symplectic reciprocity converts
largest covariance eigenvalues to smallest ones, which are checked by direct
adjoint contraction. The passive minimum uses the exact inverse of the
covariance compressed to the hyperplane orthogonal to the mean phase; parity
is measured after the optimization, never used to assume the answer.

`theorem.json` is a deliberately constructed symplectic counterexample to an
insufficient generic hypothesis. It does not simulate a counterexample to
the unchirped Gaussian NLSE. The distinction is made explicitly in the audit.
