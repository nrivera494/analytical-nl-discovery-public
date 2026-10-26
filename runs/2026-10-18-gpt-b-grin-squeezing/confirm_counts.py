#!/usr/bin/env python3
"""gpt-b / gpt-6-astra / gpt. Pre-frozen counting counterexample checks."""
import importlib.util
from pathlib import Path
p=Path(__file__).with_name('run.py');s=importlib.util.spec_from_file_location('independent_driver',p);d=importlib.util.module_from_spec(s);s.loader.exec_module(d)
for case in [(5,.6,.3,4201,7601,1e6,100),(5,.6,.3,4201,7601,1e10,300)]:
    d.twa_case(*case,dt=.01)
    d.twa_case(*case,power=10)
d.twa_case(5,.6,.3,4203,7603,1e6,100)
