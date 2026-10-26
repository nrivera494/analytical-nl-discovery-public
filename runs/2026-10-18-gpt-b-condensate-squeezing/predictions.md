# Frozen condensate covariance and ensemble tests, 2026-10-18
Agent gpt-b; model gpt-6-astra; family gpt. Task T-20261018-claude-interactive.7-03.
Same independent model/numerical definitions as companion grin-squeezing predictions. No production yet.

## Exact algebra being narrowed
For any positive two-dimensional covariance (Gaussian or not), lambda_-=det(V)/lambda_+, and det(V)/V_P overestimates lambda_- by lambda_+/V_P-1. The proposed approximation requires V_X/V_P<<1 (and lambda_-/V_P<<1), not Gaussianity. Test the original <=.3 dB error over z>=5, all runs. Fit the small V_X/V_P error dependence and report exact residual rather than calling a matrix identity a dynamical law. Do not equate conditional residual V_P-C^2/V_X with cloud noise without a controlled comparison: it includes intrinsic phase vacuum, exchange and other unobserved fluctuations.

## Ensemble predictions (new independent seeds)
K5; checkpoints1,2,5,10,20,50,100. Core E'=.3, sigma=.3; fixed launch4201, disorder7601..7612 (12); fixed disorder7601, launch4201..4212 (12). Strong sigma1,3: disorder7601..7606. Held out E'=.45,sigma.3,12disorder cases; E'=.3,sigma2,6disorder cases. Record f0 rather than substituting a nominal equilibrium value.
Score original mean/spread predictions: E'.45 mean[-11,-6]dB at z10,20 and SD>=1.5dB; sigma2 mean[-11,-6]dB at z20,50 and SD<=1.5dB. Core mean -8..-10dB is tested with 95% uncertainty of finite ensemble, not enforced as a tolerance. All errors distinguish realization SD from mean SE.
TWA: E'.3, sigma.3, launch4201/dis7601, n1e6,1e8,1e10, checkpoints10,20,50. Additional held-out launch4202/dis7602 at sigma3,n1e10. Expect <=1dB vs tangent where V_P^2/(8 n0 lambda_-)<.1; test >1dB departures at n1e6,z20,50. Fit 1/n excess only when resolved. Shot convergence4*512 to4*1024, step .02/.01 (Brownian bridge); refine failed checks. All simultaneous GRIN data are shared with companion run by explicit provenance.

## Relax ideal loss and detection
Use eta_det=.9, uniform output transmission eta_out=.9: exact lambda_detected=1-eta_det*eta_out+eta_det*eta_out*lambda_in. Also simulate distributed quantum-limited loss alpha=-ln(.9)/50 per LNL (10% intensity lost at z50), sigma3,E'.3,n1e10, four disorder seeds. Add vacuum Langevin increments and compare .02/.01. Detection maps remaining covariance exactly. These are specified 10%-loss/90%-detection stress tests, not a calibrated prediction for a particular fibre; identify physical calibration as unresolved. Test absence of technical phase stabilization separately via covariance phase averaging.
No Raman claim is present: scalar instantaneous electronic Kerr is assumed by all three cards. A multi-peak silica Raman calculation requires a temporal mode/coherence bandwidth, temperature and wavelength; none are specified. Do not invent a Raman noise number or label CW quadrature predictions a complete silica-fibre result. Record this boundary and a follow-up if needed.
