<!-- agent: gpt-a; model: gpt-6-astra; family: gpt -->

# Higher-precision evidence

Source run: `2026-10-16-gpt-a-dw-highprecision`. Full-precision arithmetic is used before gating and Fourier measurement.

| Case | xi | TOD | Steps | Gate-15 band | Gate-20 resonant | Ratio | Core peak time |
|---|---:|---:|---:|---:|---:|---:|---:|
| halfstep | 2.3561945 | 0.003 | 16384 | 6.835352160e-44 | 2.325277858e-47 | 2939.59 | 0.0625 |
| lower | 2.3561945 | 0.0028 | 8192 | 3.452338441e-45 | 3.647632577e-51 | 946460 | 0.0625 |
| precompression | 2.25 | 0.003 | 9216 | 2.635600446e-45 | 2.309832369e-47 | 114.104 | 0.0625 |
| precompression_grid | 2.25 | 0.003 | 4096 | 2.633564917e-45 | 2.054611620e-47 | 128.178 | 0.054688 |
| precompression_grid_reference | 2.25 | 0.003 | 4096 | 2.633564920e-45 | 2.054612021e-47 | 128.178 | 0.0625 |
| precompression_halfstep | 2.25 | 0.003 | 18432 | 2.635729544e-45 | 2.324788495e-47 | 113.375 | 0.0625 |
| precompression_window | 2.25 | 0.003 | 9216 | 2.623285923e-45 | 2.309831782e-47 | 113.57 | 0.0625 |
| primary | 2.3561945 | 0.003 | 8192 | 6.835424476e-44 | 2.296422904e-47 | 2976.55 | 0.0625 |
| propagated_null | 2.3561945 | 0 | 8192 | 1.626769491e-44 | 3.460586572e-59 | 4.70085e+14 | 0 |
| upper | 2.3561945 | 0.0032 | 8192 | 9.676079474e-43 | 4.773011477e-44 | 20.2725 | 0.0625 |
| window | 2.3561945 | 0.003 | 8192 | 6.805527872e-44 | 2.296422356e-47 | 2963.53 | 0.0625 |

The `propagated_null` has zero TOD; its measurement band is labeled by 0.003. It is not radiation generation.

| Variant / reference | Gate-15 change | Resonant gate-20 change | Both below 1%? |
|---|---:|---:|---|
| halfstep / primary | -0.00105796% | 1.25652% | no |
| window / primary | -0.437377% | -2.38302e-05% | yes |
| precompression_halfstep / precompression | 0.00489826% | 0.647498% | yes |
| precompression_window / precompression | -0.467238% | -2.539e-05% | yes |
| precompression_grid / precompression_grid_reference | -1.4152e-07% | -1.95205e-05% | yes |

| TOD interval at xi=3*pi/4 | Gate-15 local rate | Resonant gate-20 rate | Claimed d_star |
|---|---:|---:|---:|
| [0.0028, 0.003] | 0.12539738 | 0.36739982 | 0.37473443 |
| [0.003, 0.0032] | 0.12720592 | 0.36669024 | 0.37473443 |

Deferred optional cases: lower_halfstep, quarterstep, middle. Their absence does not count as a passed test.
