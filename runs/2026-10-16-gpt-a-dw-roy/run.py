#!/usr/bin/env python3
"""agent: gpt-a; model: gpt-6-astra; family: gpt.
Run this configuration through the shared independent implementation.
Run serially, after memory_pressure reports at least 35 percent free.
Completed cases are retained and skipped on restart.
"""
from pathlib import Path
import runpy
import sys

folder = Path(__file__).resolve().parent
shared = folder.parent / "2026-10-16-gpt-a-dw-core" / "simulate.py"
sys.argv = [str(shared), str(folder / "config.yaml"), *sys.argv[1:]]
runpy.run_path(str(shared), run_name="__main__")
