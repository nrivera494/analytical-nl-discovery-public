---
date: 2026-10-19
agent: claude-interactive
model: claude-opus-5-5
family: claude
task: T-20261019-claude-interactive-11
duration_min: 10
---

## Did

claude-interactive.14 found control characters in C-20261008-claude-a-02, and repaired them in PR #71. I then scanned every text file in the repository for control bytes.

## Found

Three Markdown files had LaTeX backslashes turned into control characters. The cause was my own edit scripts, which used non-raw Python strings: `\r` became a carriage return, `\v` a vertical tab, and `\b` a backspace.
- C-20261008-claude-a-02: fixed in PR #71.
- C-20261010-claude-a-01: one `\rm` (from my 2026-10-19 edit).
- P-20261016-claude-interactive-01: three `\beta` (from my commit 2c8a6c9 of 2026-10-16).

## Changed

Restored the two remaining files. No other file has control bytes.

## Not verified

Nothing else.

## Loose ends

None. In future the orchestrator writes LaTeX through raw strings or the Edit tool.
