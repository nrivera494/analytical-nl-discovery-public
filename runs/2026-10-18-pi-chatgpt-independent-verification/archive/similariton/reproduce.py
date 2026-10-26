#!/usr/bin/env python3
"""Reproduce every independent similariton calculation with explicit settings.

Requires Python, NumPy and SciPy. No network access or repository checkout
is needed. The 'all' suite takes several minutes on a modern CPU.
"""
import argparse
import json
import platform
import sys
from pathlib import Path

import numpy as np
import scipy
import fv_covariance
import lens_nlse


CONFIGS = {
    "base": [
        dict(end=.02, eps=.05, ngrid=512, dt=.0002),
        dict(end=.02, eps=.05, ngrid=1024, dt=.0001),
        dict(end=4., eps=.1, ngrid=1024, dt=.002),
        dict(end=4., eps=.1, ngrid=2048, dt=.001),
        dict(end=4., eps=.05, ngrid=2048, dt=.002),
        dict(end=4., eps=.05, ngrid=4096, dt=.001),
    ],
    "extended": [
        dict(eps=.025, end=4., ngrid=4096, dt=.001),
        dict(eps=.025, end=4., ngrid=8192, dt=.0005),
        dict(eps=.05, end=6., ngrid=2048, dt=.002, do_cov=False),
        dict(eps=.05, end=6., ngrid=4096, dt=.001, do_cov=False),
    ],
    "window": [
        dict(eps=.05, end=4., ngrid=4096, dt=.001, box=4.),
        dict(eps=.05, end=4., ngrid=8192, dt=.001, box=4.),
        dict(eps=.05, end=4., ngrid=8192, dt=.001, box=8.),
    ],
    "certification": [
        dict(eps=.05, end=.02, ngrid=1024, dt=.0001),
        dict(eps=.05, end=4., ngrid=8192, dt=.0005, box=4.),
        dict(eps=.025, end=4., ngrid=8192, dt=.00025, box=2.),
    ],
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite",
                        choices=["all", "fv", "quick", *CONFIGS], default="all")
    parser.add_argument("--output-dir", type=Path,
                        default=Path(__file__).parent / "reproduced")
    args = parser.parse_args()
    dest = args.output_dir.resolve()
    dest.mkdir(parents=True, exist_ok=True)
    provenance = dict(python=sys.version, platform=platform.platform(),
                      numpy=np.__version__, scipy=scipy.__version__,
                      suite=args.suite,
                      definitions=dict(G="exp(tau)", tau="g*z",
                                       nsp=1, Gamma=float(np.sqrt(18)),
                                       default_launch="asymptotic",
                                       default_smoothing=".25*eps**(2/3)"))
    (dest / "environment.json").write_text(
        json.dumps(provenance, indent=2) + "\n")
    if args.suite in ("all", "fv"):
        fv_covariance.run(dest / "results_fv.json")
    selected = list(CONFIGS) if args.suite == "all" else [args.suite]
    for suite in selected:
        if suite == "fv":
            continue
        configs = CONFIGS["base"][:2] if suite == "quick" else CONFIGS[suite]
        suffix = "" if suite == "base" else "_" + suite
        path = dest / ("results_nlse" + suffix + ".json")
        rows = []
        for config in configs:
            result = lens_nlse.simulate(**config)
            rows.append(result)
            path.write_text(json.dumps(dict(cases=rows), indent=2) + "\n")
            print(suite, {key: result.get(key) for key in
                         ["eps", "tau", "ngrid", "dt", "box",
                          "matched_LO_min", "spectral_ratio",
                          "phase_energy_deficit",
                          "commutator_relative_error"]}, flush=True)
    print("Outputs:", dest)


if __name__ == "__main__":
    main()
