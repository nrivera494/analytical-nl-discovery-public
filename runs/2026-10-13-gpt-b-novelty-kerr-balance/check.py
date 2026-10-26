"""Algebra audit; agent gpt-b, model gpt-6-astra, family gpt.
Square-completion under an assumed stationary or averaged power balance.
These checks do not construct stationary solutions or establish attainability.
"""
import json, pathlib, time
import sympy as s
base=pathlib.Path(__file__).resolve().parent
t0=time.perf_counter()
f,x,y,c=s.symbols('f x y c',real=True,nonzero=True)
eta=4*c*c*(f*x-x*x-y*y)/(f*f)
t=1-2*c*(x+s.I*y)/f
cw=s.simplify(eta-(c*c-4*c*c*((x-f/2)**2+y*y)/(f*f)))
transmission=s.simplify(eta-(c*c-s.expand_complex(t-(1-c))*s.conjugate(s.expand_complex(t-(1-c)))))
# General complex pump: real/imaginary coordinates; explicit finite-dimensional sum.
fx=s.symbols('f0:3',real=True);fy=s.symbols('g0:3',real=True)
ax=s.symbols('x0:3',real=True);ay=s.symbols('y0:3',real=True)
Fp=sum(a*a+b*b for a,b in zip(fx,fy))
outside=sum(a*x+b*y-x*x-y*y for a,b,x,y in zip(fx,fy,ax,ay))
completed=Fp/4-sum((x-a/2)**2+(y-b/2)**2 for a,b,x,y in zip(fx,fy,ax,ay))
multi=s.simplify(outside-completed)
# Mean-square identity relevant to breathers: variance cannot improve ceiling.
xm,ym,vx,vy=s.symbols('xm ym vx vy',real=True)
averaged=s.expand((xm-f/2)**2+ym**2+vx+vy)
# The dual-pump metric in Gasmi arXiv:2210.09760 includes pump-line weights.
# At weak equal pumping on resonance a_j=f_j, no generated outside line exists.
metric_limit=s.simplify((s.Rational(1,2)*(f*f/2)+s.Rational(1,2)*(f*f/2))/(f*f))
result=dict(agent='gpt-b',model='gpt-6-astra',family='gpt',run_id=base.name,cw_square_completion_residual=str(cw),transmission_residual=str(transmission),three_complex_pumps_residual=str(multi),breather_mean_square=str(averaged),gasmi_linear_equal_pump_metric=str(metric_limit),strict_outside_pump_linear_efficiency=0,wall_seconds=time.perf_counter()-t0,interpretation='Identities conditional on uniform-loss norm balance, not LLE existence or stability tests. The general M proof is the sum of the same scalar identity.')
assert cw==0 and transmission==0 and multi==0
(base/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
