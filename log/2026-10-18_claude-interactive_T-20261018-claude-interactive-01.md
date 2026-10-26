---
date: 2026-10-18
agent: claude-interactive
model: claude-opus-5-5
family: claude
task: T-20261018-claude-interactive-01
duration_min: 45
---

## Did

On the PI's instruction, filed the PI's GPT 6 Pro result as claim C-20261018-pi-chatgpt-01 (proposer family gpt). The result is a passive-mask bound on Zakharov–Shabat eigenvalues, from the PI's own ChatGPT session, which was shared as https://chatgpt.com/s/t_6ad4b5574cc48191946a991871e10790.
- **Reading the source.** `WebFetch` returned only page chrome. The built-in browser rendered the final answer in full.
- **The derivation note.** The PI supplied the README in chat. It is committed as `claims/notes/C-20261018-pi-chatgpt-01-derivation.md`, with LaTeX delimiters converted to `$`/`$$` for GitHub and a provenance note. The text is otherwise unchanged.
- **The counterexample.** Recorded the reported counterexample to C-20261016-claude-a-01: the asymmetric unimodal source $S=\pi\cos(1)e^k\mathrm{sech}(\pi k/2)$, with an improvement of about 1%. It is on that card's Checks table and audit trail. The status is unchanged until it is reproduced.
- **Tasks.** Created T-20261018-claude-interactive-02 (verification; family claude) and -03 (novelty audit; family claude). Added the claim to the claims list of P-20261016-claude-interactive-03.

## Found

- **The steps check out.** I checked them by hand:
  - the spinor-angle inequality $\theta'\le|q|-\eta\sin2\theta$;
  - the convexity inequality and its equality point;
  - the antiderivative argument, which does not need monotone $\theta$;
  - the $p=2N$ cancellation that gives $U_{2N}=N-\tfrac12$ for integer-$N$ sech.
- **The numbers reproduce.** Closed-form evaluation (run `2026-10-18-claude-interactive-zs-moment-bound-check`) reproduces every bound value the source quotes:
  - the non-integer-sech headroom ceilings at $N=2.5$, 3.5, 5.5 and 9.5;
  - the Gaussian fraction ceilings at $N=2$, 3, 4, 6 and 10.

  New values were frozen for the verifier: sech at $N=4.5$ and 7.5, and Gaussian at $N=1.5$, 5 and 8.
- **No eigenvalue was computed here.** The TL baselines and the counterexample are not yet checked in the repository.

## Changed

- New: `claims/C-20261018-pi-chatgpt-01-passive-mask-zs-eigenvalue-bound.md` (status cheap-checks-passed).
- New: `claims/notes/C-20261018-pi-chatgpt-01-derivation.md`.
- New: `runs/2026-10-18-claude-interactive-zs-moment-bound-check/` (`check.py`, `summary.json`, `config.yaml`, `meta.yaml`).
- Edited: `claims/C-20261016-claude-a-01-*.md` (a Checks row, the Outcome, and a new audit-trail section); its status is unchanged.
- Edited: `problems/P-20261016-claude-interactive-03-*.md` (the claims list and an audit-trail row).
- New tasks: T-20261018-claude-interactive-02 and -03.

## Not verified

- **The counterexample**, which needs an independent ZS solver and a mask search.
- **The source's TL eigenvalue baselines.**
- **Each limit:** $p=2$, $p\to\infty$ and $p\to1$.
- **The sharp Hausdorff–Young constant form in (E).**
- **Publication priority.**

All of these belong to T-20261018-claude-interactive-02 and -03.

## Loose ends

- The earlier turns of the PI's conversation, which give the counterexample's mask and enclosures, are not in the repository. The verifier must reproduce the counterexample independently (T-20261018-claude-interactive-02).
- The reproduction scripts the README names (`compute_bounds.py`, `explore.py`) were not supplied.
- PI instruction: once the verification and the novelty audit are complete, the claim moves to verified.
