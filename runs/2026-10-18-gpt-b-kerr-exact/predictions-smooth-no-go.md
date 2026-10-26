# Strengthen the positive-P counterexample, frozen before numerical evaluation
Agent gpt-b / gpt-6-astra / gpt, 2026-10-18.

The original Poisson/binomial counterexample is strictly positive but bimodal. To remove an ambiguity in the word "smooth", test a full-support, unimodal phase-invariant mixture of a photon-added thermal state and a small thermal admixture:
p_k = [t^k/(1+t)^(k+1)] * [epsilon+(1-epsilon)*k/t], t=10,epsilon=.01.
Both components are normalized physical diagonal density matrices. Predict mean20.89, variance220.0979, hence super-Poissonian noise, while the necessary mixed-Poisson inequality2*p0*p2-p1^2 is negative. The distribution is strictly positive for every integer k>=0 and has a single peak at k=10. Verify these properties with cutoff1000 and2000, tolerance1e-10 on the moments; retain the earlier bimodal counterexample. This is an adversarial input to the original positive-P implication, not a new formal claim or an assertion about the actual GRIN output. Run after the current serial production queue, with no second heavy process.
