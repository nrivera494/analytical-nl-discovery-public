---
agent: claude-interactive
model: claude-opus-5-5
family: claude
task: T-20261018-claude-interactive-04
date: 2026-10-18
---

# Provenance of the ZSFormalization library

- **Formalizer.** The PI's Codex session, recorded as `pi-codex`. The family is gpt; the model is GPT 6 Astra Max (gpt-6-astra at maximum reasoning effort), as the PI recorded on 2026-10-19 (task T-20261018-claude-interactive-08). It formalizes the even-exponent parts (A)–(D) of claim C-20261018-pi-chatgpt-01, which GPT 6 Pro proposed in the PI's ChatGPT session.
- **Origin.** `~/Documents/Codex/2026-10-18/loo/outputs/ZSFormalization` on the PI's laptop, received 2026-10-18.
- **Copied verbatim.** These were copied: the 13 modules, the root `ZSFormalization.lean`, the formalizer's [`README.md`](README.md), and the formalizer's [`verification/`](verification/) folder (build log, axiom log, environment, hashes, `Audit.lean`). Every SHA-256 in `verification/source-sha256.txt` matches.
- **Superseded.** The formalizer's `lakefile.toml`, `lake-manifest.json` and `lean-toolchain` are superseded by `formal/`'s. All nine dependency pins are identical (Lean `v4.35.0-rc4`, Mathlib `1f414401f69059aa7eead47b53ee40bd38455eeb`).
- **The one build-setting change.** In `formal/lakefile.toml` the library turns off Mathlib's line-length linter. That linter produced the only warnings (32), and turning it off keeps the sources byte-identical.
- **Build.**

  ```sh
  export PATH=$HOME/.elan/bin:$PATH
  cd formal && lake exe cache get && lake build ZSFormalization
  lake env lean ZSFormalization/verification/Audit.lean   # the formalizer's axiom audit
  ```

- **Cross-family audit.** [`results/formalized/R-0001-zs-even-moment-passive-mask-ceiling/audit/formal-audit-2026-10-18-claude-interactive.md`](../../results/formalized/R-0001-zs-even-moment-passive-mask-ceiling/audit/formal-audit-2026-10-18-claude-interactive.md), reproduced by `runs/2026-10-18-claude-interactive-zs-lean-audit/run.sh`. The result built on this library is [R-0001](../../results/formalized/R-0001-zs-even-moment-passive-mask-ceiling/RESULT.md).
- **Changes.** Do not edit these files: they are hash-pinned. Extensions go in new modules (task T-20261018-claude-interactive-06).
