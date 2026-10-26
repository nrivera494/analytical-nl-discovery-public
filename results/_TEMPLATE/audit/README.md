Cross-family reports go here: `cheap-checks.md`, one `audit-<date>-<agent>.md` per clean-context adversarial audit (gate G5), and one `verification-<date>-<agent>.md` per cross-family verification that was not a clean-context audit. Each audit file starts with front matter:

    ---
    auditor: agent-id
    model: model-name
    family: gpt
    date: 2026-01-01
    verdict: pass        # pass | pass-reduced-regime | fail
    ---
