#!/usr/bin/env python3
"""gpt-b / gpt-6-astra / gpt. Frozen resolution and deterministic counting attacks."""
import importlib.util
import sys
from pathlib import Path
p=Path(__file__).with_name('run.py');s=importlib.util.spec_from_file_location('independent_driver',p);d=importlib.util.module_from_spec(s);s.loader.exec_module(d)
if len(sys.argv)>1 and sys.argv[1]=='last':
    d.twa_case(5,.6,.3,4203,7603,1e6,100,dt=.0025)
    sys.exit(0)
for h in [.005,.0025]:d.twa_case(5,.6,.3,4201,7601,1e6,100,dt=h)
for h in [.01,.005]:d.twa_case(5,.6,.3,4203,7603,1e6,100,dt=h)
for launch in [4201,4203,4213]:
    for h in [.02,.01]:d.twa_case(5,.6,0,launch,7601,1e6,100,dt=h)
d.twa_case(5,.6,0,4201,7601,1e6,100,power=10)
