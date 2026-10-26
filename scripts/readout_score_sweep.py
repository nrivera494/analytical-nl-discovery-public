#!/usr/bin/env python3
# agent: gpt-a; model: gpt-6-astra; family: gpt
"""Score each frozen case after Julia has atomically completed its TOML summary."""
import argparse
import json
import re
import time
from pathlib import Path
from readout_bounds import score_file

ap = argparse.ArgumentParser()
ap.add_argument('config')
ap.add_argument('--wait', action='store_true')
ap.add_argument('--no-smooth', action='store_true')
ap.add_argument('--rerun', action='store_true')
args = ap.parse_args()
text = Path(args.config).read_text()
raw = Path(re.search(r'^raw_location = "([^"]+)"', text, re.M)[1])
labels = re.findall(r'^label = "([^"]+)"', text, re.M)
for label in labels:
    path = raw/(label+'.npz')
    while not (raw/(label+'.toml')).exists():
        if not args.wait:
            break
        time.sleep(3)
    else:
        if args.rerun or not path.with_suffix('.bounds.json').exists():
            try:
                score_file(path, use_smooth=not args.no_smooth)
            except Exception as error:
                (raw/(label+'.score-failed.json')).write_text(json.dumps({
                    'agent': 'gpt-a', 'model': 'gpt-6-astra', 'family': 'gpt',
                    'error': repr(error)}, indent=2)+'\n')
                raise
