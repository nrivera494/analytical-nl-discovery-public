# Reproduction sources

Copy registration: agent gpt-a; model gpt-6-astra; family gpt; 2026-10-11.

The Julia files in the three dated subdirectories are unchanged permitted validation scripts by claude-interactive.2, copied from commit `00b3420eae8d47091ea792d2669b331960c09f5e`, branch `task/T-20261010-claude-interactive.2-01`. Their authorship remains Claude-family. The cross-family audit reran them and compared them with independently written Python propagation/analysis; it does not claim independent authorship of the measurement scripts.

`numeric.json` is the audit's reproduction of the proposer's reduced-model numeric script, source commit `1f766ac814b39705697cfd108e5d6d3f32bb0667`, `runs/2026-10-08-claude-a-amp-sim-checks/numeric.py`. It is supplementary; the report uses the independently implemented `gain.py` calculations.
