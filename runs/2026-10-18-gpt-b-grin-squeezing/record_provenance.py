#!/usr/bin/env python3
"""gpt-b / gpt-6-astra / gpt. Record completed audit provenance; no propagation."""
import datetime
import hashlib
import json
import subprocess
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
RAW = Path('~/analytical-nl-discovery-data')
IDENTITY = dict(agent='gpt-b', model='gpt-6-astra', family='gpt')
stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
base = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
shared = [ROOT/'evaluator'/name for name in [
    'thermalized_light.py', 'thermalized_light_core.c', 'squeezing.py',
    'squeezing_core.c', 'kerr_squeezing.py', 'serial_numerical.py']]
shared = [p for p in shared if p.exists()]
grin = ROOT/'runs/2026-10-18-gpt-b-grin-squeezing'
resources, free = [], []
for folder in sorted(RAW.glob('2026-10-18-gpt-b-*')):
    for path in sorted(folder.glob('*.log')):
        for line in path.read_text(errors='replace').splitlines():
            if line.startswith('{'):
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                if 'child_peak_rss_bytes' in row:
                    resources.append(dict(log=str(path), **row))
            if 'System-wide memory free percentage:' in line:
                try:
                    free.append(int(line.split(':')[-1].strip().rstrip('%')))
                except ValueError:
                    pass
resource_summary = dict(**IDENTITY, recorded_at=stamp, children=resources,
    recorded_child_peak_bytes=max((r['child_peak_rss_bytes'] for r in resources), default=None),
    minimum_logged_free_percent=min(free) if free else None,
    scope='Resource-wrapper children only; every production launcher separately gates free memory. Logs and raw trajectories remain outside git.')
(grin/'resource_summary.json').write_text(json.dumps(resource_summary, indent=2)+'\n')
for run in sorted((ROOT/'runs').glob('2026-10-18-gpt-b-*')):
    sources = set(shared+[p for p in run.iterdir() if p.suffix in {'.py', '.c', '.jl', '.sh'}])
    if run.name.endswith('condensate-squeezing'):
        sources.add(grin/'run.py')
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted(sources)}
    (run/'source_hashes.json').write_text(json.dumps(dict(**IDENTITY,
        recorded_at=stamp, base_commit=base,
        note='Hashes identify the exact source bytes, including changes committed after base_commit.',
        sha256=hashes), indent=2)+'\n')
    summary = json.loads((run/'summary.json').read_text())
    meta_path = run/'meta.yaml'
    meta = yaml.safe_load(meta_path.read_text())
    meta.update(status='complete; failed and unresolved gates retained' if summary['complete']
                else 'partial; missing frozen confirmations are explicitly recorded',
                finished_at=stamp, source_hashes='source_hashes.json',
                resource_summary='../2026-10-18-gpt-b-grin-squeezing/resource_summary.json',
                production_complete=summary['complete'])
    meta_path.write_text(yaml.safe_dump(meta, sort_keys=False))
    config_path = run/'config.yaml'
    config = yaml.safe_load(config_path.read_text())
    config['production_finished'] = summary['complete']
    config['production_stopped_at'] = stamp
    config_path.write_text(yaml.safe_dump(config, sort_keys=False))
print('Recorded source hashes, resource observations and run completion flags')
