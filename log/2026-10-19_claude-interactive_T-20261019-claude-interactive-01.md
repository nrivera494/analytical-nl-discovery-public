---
date: 2026-10-19
agent: claude-interactive
model: claude-opus-5-5
family: claude
task: T-20261019-claude-interactive-01
duration_min: 75
---

## Did

- Read GPT 6 Pro's report in full: the 26-page technical report, and the 17-page chat reply that summarizes it. Compared it with the three target claims and with gpt-a's 2026-10-11 audit.
- Verified the reproducibility archive (sha256 `1fca535b…`):
  - all 82 internal checksums pass;
  - all 44 inventoried repository files match snapshot `970bfe7` once one trailing newline (added by the fetch) is accounted for;
  - every script was read and grepped before running; none uses the network, subprocesses, or writes outside its folder.
- Reran the four quick checks unmodified on a second platform (run `2026-10-19-claude-interactive-gpt6pro-quick-repro`). All agree:
  - weak cross-check $\lambda_{\min}$ to $7\times10^{-13}$;
  - the short-gain counterexample 0.8964864655 to the same digits;
  - the oscillator constants to $4\times10^{-12}$;
  - the symbolic $c_2(\Phi)$ identically.
- Committed the archive's 55 non-raw files as run `2026-10-18-pi-chatgpt-independent-verification`. Raw JSON, `.npz` arrays and PNG duplicates stay at `~/analytical-nl-discovery-data/gpt6pro-reports/`.
- Wrote the review summary `docs/review-2026-10-18-pi-chatgpt-similariton-normal-dispersion-verification.md`.
- Updated the three cards (narrowed statements, superseded wording marked inline, Checks rows, Outcome, Audit trail), filed two new GPT-family claims, completed two stale problem claim lists, and created tasks -02 to -06.

## Found

- **The report's corrections hold up against the repository's own records:**
  - C-20261008-claude-a-02's table P4 ($\varepsilon_0^2C_{PP}/G=3.81, 61.8, 701$) and its own $l=0$ phase formula both imply $C_{PP}\propto G^{7/3}/\varepsilon_0^2$, contradicting the card's $G/\varepsilon_0^2$;
  - C-20261010-claude-a-01's "exponent 0.50 for any even, smooth pulse" contradicts its own flat-top statement.
- **The weak-dispersion numbers match the card closely.** The report's ratios at $\Phi=3$ (1.00099 to 1.094) match the card's to about 3 digits.
- **C-20261010-claude-a-01 was cross-family checked on 2026-10-11, but the card was never updated.** gpt-a audited items 1–5 then, refuting 3(b)'s finite 1% regime, and the card stayed `proposed` with empty Checks.
- **What C-20261010-claude-b-01's numbers actually compute after breaking.** The card's reduced computation uses full-NLSE propagations at $N=200$, so it computes what the report calls the full tangent-block limit. The card's wording (shallow-water map) is what fails after breaking, not its numbers.

## Changed

- **C-20261008-claude-a-02:** cheap-checks-passed → sim-verified (narrowed). Two statements are superseded (the $C_{PP}$ power, and "with ASE there is no squeezing"), the edge remainder is unverified, and the $N_0$ regime is corrected.
- **C-20261010-claude-a-01:** proposed → sim-verified (narrowed). It records gpt-a's verdicts on items 1–5 and GPT 6 Pro's item 5; the finite 3(b) regime is refuted.
- **C-20261010-claude-b-01:** proposed → sim-verified (narrowed). The post-breaking definition of $C_Z$ is narrowed; notes on basis bias and $\lambda_{\rm pass}$ are added.
- **New:** C-20261019-pi-chatgpt-01 ($c_2(\Phi)$) and C-20261019-pi-chatgpt-02 (matched-LO $G^{7/3}$, short-gain criterion, $G^{1/3}$ envelope), both cheap-checks-passed, with held-out predictions frozen.
- **P-001 and P-20261010-claude-interactive-01:** claim lists completed from the claim files; audit-trail rows added.

## Not verified

- I did not rerun the full suites: the long similariton covariance, the weak sweep, and the strong-dispersion $N=10$–40 cases. Their numbers are the archive's.
- The model name is recorded as "GPT 6 Pro according to the PI; self-reported GPT-6 Astra Pro".
- The downloaded 26-page PDF (616 KB) is a different build from the archive's report PDF (531 KB, hash in `SHA256SUMS.txt`). The archive's version is committed.

## Loose ends

- T-20261019-claude-interactive-02: verify C-20261019-pi-chatgpt-01 (claude).
- T-20261019-claude-interactive-03: verify C-20261019-pi-chatgpt-02 (claude).
- T-20261019-claude-interactive-04: clean-context GPT audits of the three narrowed claims, for `audited`.
- T-20261019-claude-interactive-05: read the SPIE 2016 lead.
- T-20261019-claude-interactive-06 (PI): the model name.
