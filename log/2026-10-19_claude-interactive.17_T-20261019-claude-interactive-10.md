---
date: 2026-10-19
agent: claude-interactive.17
model: claude-opus-5-5
family: claude
task: T-20261019-claude-interactive-10
duration_min: 35
---

## Did

Wrote the promising results for the dispersion and similariton cluster, on the PI's decision of 2026-10-19. The branch is stacked on PR #70.

| Result | Claim | Problem | Gates met | Gates open |
|---|---|---|---|---|
| [R-0011](../results/promising/R-0011-similariton-shape-noise-exponents/RESULT.md) | C-20261008-claude-a-02, as narrowed | P-001 | G1–G4 | G5, G6, G7, G8 |
| [R-0012](../results/promising/R-0012-weak-normal-dispersion-lambda-min/RESULT.md) | C-20261010-claude-a-01, as narrowed | P-20261010-claude-interactive-01 | G1–G4, G6 | G5, G7, G8 |
| [R-0013](../results/promising/R-0013-strong-normal-dispersion-lambda-over-n2/RESULT.md) | C-20261010-claude-b-01, as narrowed | P-20261010-claude-interactive-01 | G1, G3, G4, G6 | G2, G5, G7, G8 |

Each folder has:
- `RESULT.md`;
- one figure: page 1 of GPT 6 Pro's committed verification PDF, rendered with Ghostscript at 110 dpi (27–40 KB);
- `verification-*.md` pointers for GPT 6 Pro (2026-10-18) and gpt-a (2026-10-11);
- `repro/README.md`.

R-0012 and R-0013 also link the proposers' own run figures, with captions saying which panels belong to the result.

Decisions, recorded here because nobody was available to ask:
- **gpt-a's 2026-10-11 checks are filed as verifications, not audits.** Its task was titled a clean-context audit, and it did not read the derivation notes. But its input manifest (run `2026-10-11-gpt-a-highlights-audit-c1`) includes the proposers' run scripts and a same-family validation note, which `docs/AUDIT_PROTOCOL.md` does not allow. The C-20261010-claude-a-01 card already classifies it as a verification, and I followed that.
- **R-0012's scope.** Items 1, 2, 3(b) and 4 (two models) and item 5. Excluded:
  - item 3(a), and item 4's intermediate beat length and vector Raman: no other family tested them;
  - the refuted finite-band regime of 3(b);
  - the false "any even, smooth pulse" prediction;
  - the anomalous-dispersion remark;
  - $c_2(\Phi)$, which is C-20261019-pi-chatgpt-01.
- **R-0011's scope** excludes everything in C-20261019-pi-chatgpt-02: the $C_{PP}$ power, short-gain squeezing, and the large-gain $\Theta(G^{1/3})$ matched-mode minimum.
- **G2.**
  - Met for R-0011 and R-0012: each stated part has a formal derivation that another family rederived. The caveats are stated: for R-0012 the matching global lower bound is unproved; for R-0011 there are finite-mode proofs only.
  - Open for R-0013: the post-breaking law and $\lambda_{\rm pass}=\lambda_2$ have no derivation.
- **G6.**
  - Open for R-0011: the two closest leads, Wang et al. 2016 and the Wabnitz 2007 journal text, are unread.
  - Met for R-0012 and R-0013: two families searched, and the closest prior work and the difference are stated.
- **G7 open for all three.** See Found.
- **Card edits.** Claim and problem cards were edited byte-exactly (Python replacement with checks), so that the existing control characters stay for the repair task instead of being silently changed.

## Found

**Record inconsistencies.** All are in task T-20261019-claude-interactive.17-02; none was silently fixed.
1. **gpt-a's verdicts are missing from two cards.** C-20261008-claude-a-02 and C-20261010-claude-b-01 do not record gpt-a's 2026-10-11 verdicts (`docs/review-2026-10-11-gpt-a-highlights-audit.md`, candidates 2 and 1); C-20261010-claude-a-01 does.
2. **A held-out failure is missing from the similariton card.** For C-20261008-claude-a-02:
   - The full-field held-out spectral ratio at $\Gamma=1$, $gL=2$ does not converge to the frozen 0.4257. It is 0.3854–0.3901 over $\varepsilon_0=0.1$–0.0125 (run `2026-10-10-claude-interactive.2-moment-noise`), and 0.385841 and 0.385432 in gpt-a's independent code (run `2026-10-11-gpt-a-highlights-audit-c2`).
   - The $s_1$ ASE entry is 14–19% high.
   - By the card's own P6 criterion these refute those table entries. `docs/HIGHLIGHTS.md` and the simulation ledger record this; the card does not.
   - R-0011 reports it and keeps the finite-gain tables out of the result.
3. **Corrupted LaTeX escapes in the "As verified" blocks.**
   - C-20261008-claude-a-02: `\v` became a vertical tab in four places ("arepsilon", lines 30 and 35). `\r` became a line break in `{\rm Var}` and `\lambda_{\rm LO}`: a CR on main, which PR #70 turned into an LF, splitting the math across lines 25–26 and 31–32.
   - C-20261010-claude-a-01: `N_{\rm ph}` has a CR (lines 35–36).
4. **Overstated verifier coverage.** C-20261010-claude-a-01's `verified_by` says gpt-a verified "items 1-5", but gpt-a lists item 3(a) as not independently tested.
5. **Inconsistent regime on the similariton card.** C-20261008-claude-a-02's Regime says $gL\le12$, while its exponents are fitted at $gL=12$–18 (verified over 12–26).

**Figures cannot be rebuilt from committed files.** The build scripts in the GPT 6 Pro archive need raw files kept at the run's `raw_location`.
- In a scratch copy, `weak/build_summary.py` and `strong/build_summary.py` stop with FileNotFoundError on `mode_phi3_y0.0001.npz` and `N20_Z075_n256_s300.npz`. Only the redraw scripts were run, with no propagation.
- `similariton/build_figures.py` reads `results_fv.json` and `results_nlse_extended.json`, which are also raw.
- Hence G7 is open for all three (task .17-01).

**Stale tasks.** Three other-family verify tasks remain open although their claims are now cross-family verified: T-20261008-claude-a-03, T-20261010-claude-a-01 and T-20261010-claude-b-01. The orchestrator may close or rescope them. T-20261010-claude-a-01 still covers item 3(a), and R-0012 cites it for that.

## Changed

- **New result folders:** `results/promising/R-0011-similariton-shape-noise-exponents/`, `R-0012-weak-normal-dispersion-lambda-min/`, `R-0013-strong-normal-dispersion-lambda-over-n2/`.
- **Claims** C-20261008-claude-a-02, C-20261010-claude-a-01 and C-20261010-claude-b-01: `status: sim-verified` → `promoted`; `result` set to R-0011, R-0012 and R-0013; an Outcome paragraph and an audit-trail row each. Statements unchanged.
- **Problems.** P-001: `results: [R-0011]`, with an audit-trail row. P-20261010-claude-interactive-01: `results: [R-0012, R-0013]`, with an audit-trail row. Statuses unchanged.
- **Tasks.** New T-20261019-claude-interactive.17-01 to -05. T-20261019-claude-interactive-10 set to done.

## Not verified

- **No numbers were recomputed.** No simulation was run. Every number in the three results is copied from committed runs and reports, and I checked each against the run's `summary.json` or the report text.
- **R-0012's "close to $\sqrt{10}$ per decade"** is a reading of five committed ratios, not a fit.
- **R-0013's experimental routes.** Cooling the fibre, or a Raman-free medium, suppresses the reservoir. This is inferred from the claim's formula $\hat c(0)\propto k_BT$ and is untested; the text says so.
- **The full regeneration commands** listed in the three `repro/README.md` files are copied from the archive READMEs. They have not been run (task .17-01).

## Loose ends

- T-20261019-claude-interactive.17-01: G7, regenerate the three figures from committed code.
- T-20261019-claude-interactive.17-02: record gpt-a's verdicts and the held-out failure on the cards; repair the corrupted escapes.
- T-20261019-claude-interactive.17-03: continuum spectral estimates (R-0012's lower bound, R-0013's $L^2$ lemma).
- T-20261019-claude-interactive.17-04: complete-grid $\Lambda(Z)$, $\Pi(Z)$ table for R-0013.
- T-20261019-claude-interactive.17-05: G8, Lean formalization of the finite-dimensional cores of R-0012 and R-0013.
- G5 for all three waits on T-20261019-claude-interactive-04 (agent gpt-e, running; not contacted).
