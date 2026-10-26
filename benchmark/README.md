# Rediscovery benchmark

Used to measure how often the loop finds a known result when that result is masked. Do this before trusting any new result.

- `public.md` — classic results. Models have seen these in training, so use the deformed variants listed there to reduce recall.
- Held-out tier — results published after mid-2025. **Kept outside this repository** by the PI so that agents with read access cannot see the answers. An agent running a held-out item receives only the masked problem statement.
- `results/` — one file per calibration run: item, hit or miss, time, what the agent produced.

Rules for a run: no web search, no reading of the unmasked entry or of problem files that cite it, simulation and CAS only.
