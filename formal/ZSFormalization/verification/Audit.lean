module

public import ZSFormalization

@[expose] public section

-- Definitions and theorem signatures are part of the audit, not only axiom lists.
#print ZS.SolvesZS
#print ZS.IsEigenvalue
#print ZS.IsSechSource
#print ZS.IsGaussianSource
#print ZS.sechSource
#print ZS.gaussianSource
#print ZS.attainableHeights
#print ZS.sourceEnergy
#print ZS.attainableFractions
#check ZS.passive_source_eigenvalue_bound
#check ZS.integer_sech_fraction_optimality
#check ZS.gaussian_source_polynomial_ceiling
#check ZS.canonical_integer_sech_optimality
#check ZS.canonical_integer_sech_fraction_optimality
#check ZS.canonical_order_four_fraction_optimum
#check ZS.canonical_sech_polynomial_ceiling
#check ZS.canonical_sech_five_halves_enclosure
#check ZS.canonical_sech_seven_halves_enclosure
#check ZS.canonical_sech_eleven_halves_enclosure
#check ZS.canonical_sech_nineteen_halves_enclosure
#check ZS.gaussianSource_apply
#check ZS.canonical_gaussian_ceiling

#print axioms ZS.sharp_scalar
#print axioms ZS.passive_mask_even_moment
#print axioms ZS.spinorMass_pos
#print axioms ZS.polarization_differential_inequality
#print axioms ZS.polarization_tendsto_atBot
#print axioms ZS.polarization_tendsto_atTop
#print axioms ZS.eigenvalue_even_moment_bound
#print axioms ZS.passive_source_eigenvalue_bound
#print axioms ZS.sech_even_moment
#print axioms ZS.sech_source_polynomial_ceiling
#print axioms ZS.sech_has_top_eigenvalue
#print axioms ZS.integer_sech_optimality
#print axioms ZS.integer_sech_fraction_optimality
#print axioms ZS.order_four_fraction_optimum
#print axioms ZS.sech_five_halves_certificate
#print axioms ZS.sech_seven_halves_certificate
#print axioms ZS.sech_eleven_halves_certificate
#print axioms ZS.sech_nineteen_halves_certificate
#print axioms ZS.gaussian_source_polynomial_ceiling
#print axioms ZS.sechSource_spec
#print axioms ZS.canonical_integer_sech_optimality
#print axioms ZS.canonical_integer_sech_fraction_optimality
#print axioms ZS.canonical_order_four_fraction_optimum
#print axioms ZS.canonical_sech_polynomial_ceiling
#print axioms ZS.real_sech_has_eigenvalue
#print axioms ZS.canonical_sech_five_halves_enclosure
#print axioms ZS.canonical_sech_seven_halves_enclosure
#print axioms ZS.canonical_sech_eleven_halves_enclosure
#print axioms ZS.canonical_sech_nineteen_halves_enclosure
#print axioms ZS.gaussianSource_spec
#print axioms ZS.gaussianSource_apply
#print axioms ZS.canonical_gaussian_ceiling
