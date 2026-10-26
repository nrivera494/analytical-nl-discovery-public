#!/usr/bin/env python3
"""agent: gpt-b; model: gpt-6-astra; family: gpt. Reconstruct frozen shell choice.

This checks the committed prediction file rather than overwriting a freeze.
"""
import json
from pathlib import Path
RUN=Path(__file__).resolve().parent
key=lambda r:(r['E'],r['seed'],r['include_L'])
initial=json.loads((RUN/'conditioned_predictions.json').read_text())['rows']
refined={key(r):r for r in json.loads((RUN/'conditioned_refined_predictions.json').read_text())['rows']}
frozen=json.loads((RUN/'final_predictions.json').read_text())['rows']
combined=[refined.get(key(r),r) for r in initial]
assert len(combined)==len(frozen)==24
for current,saved in zip(combined,frozen):
    assert key(current)==key(saved)
    for a,b in zip(current['widths'],saved['widths']):
        assert abs(a['mean']-b['mean'])<1e-12
        assert abs(a['se']-b['se'])<1e-12
    assert current['widths'][-1]['resolved'] and current['bandwidth_shift']<.01
print('All 24 frozen predictions match the documented initial/refined selection.')
