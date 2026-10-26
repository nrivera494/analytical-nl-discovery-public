---
date: 2026-10-04
agent: claude-interactive
model: claude-opus-5-5
family: claude
task: T-20261004-root-02
duration_min: 90
---

## Did

This was an interactive session run by the PI. I reviewed the four multimode-squeezing cards that /root (gpt) added on the branch `task/T-20261004-root-01`, and read the archive reports they cite: the 2026-09-26 analytics report and the 2026-09-28 theory-campaign report. A read of the joint-fit report together with an archive .docx file was declined by this session's safety check, so the joint-fit report was not read. The PI then chose four problems, and I rewrote or created the cards to match. The branch `task/T-20261004-root-02` is based on `main` after PR #2 merged the gpt branch.

## Found

- **Parabolic-profile overlaps.** Exact overlap integrals give, relative to $S_{01,01}$:
  - $S_{01,02}=S_{01,11}=1/2$, so a weak LP02 or LP11 admixture sees exactly the LP01 self-phase potential ($\sigma=1$): a reflectionless Pöschl–Teller well with $\nu=1$;
  - self-overlaps $S_{02,02}=1/2$ and $S_{11a,11a}=3/4$;
  - $S_{11a,11b}=1/4$;
  - the phase-matched 01+03↔02+02 mixing overlap is 1/4.

  The LP01/LP02 coefficient matrix [[1,1],[1,1/2]] reproduces the archive's effective drive of 0.955P for a 70/30 launch.
- **Capture formula.** The bound minority fraction under walk-off $\delta$ is $[\pi\delta/(2\sinh(\pi\delta/2))]^2$, checked by quadrature at $\delta$ = 0.5, 1 and 2.
- **Length scaling.** The archive's normal-dispersion minimum positions (about 180, 142 and 120 mW at 0.75, 1 and 1.25 m) fit $P_{\min}\propto L^{-0.79}$. That lies between the two simplest mechanisms (exponents 1 and 0).
- **Literature.** The mean-field part of the weak-admixture problem is prior art (Steiglitz & Rand 2009, not accessed). The PI's group has directly relevant multimode-fiber noise papers (Nat. Photon. 19, 751 (2025), DOI 10.1038/s41566-025-01677-2, preprint arXiv:2311.05535; arXiv:2509.03482; abstracts only).

## Changed

- `problems/P-20261004-root-01`: rewritten as "Minimum noise under spectral filtering in normal dispersion"; unaudited → partial.
- `problems/P-20261004-root-03`: rewritten as "Minimum noise for a multimode soliton launch in anomalous dispersion"; unaudited → partial.
- `problems/P-20261004-claude-interactive-01` (new): weak LP02/LP11 admixture.
- `problems/P-20261004-claude-interactive-02` (new): vacuum-, gain- and Raman-driven collective-coordinate noise.
- `problems/P-20261004-root-02` and `-04`: candidate → parked, each with its reactivation question.
- `docs/multimode-squeezing-scope.md`: cut to the shared definitions, the overlap table and archive pointers.
- Tasks T-20261004-root-02 (progress note; still open) and T-20261004-root-03 (new oracle requirements).
- Later in the session, on PI request:
  - updated Uddin et al. to the published version (Nat. Photon. 19, 751 (2025));
  - added `docs/references.md`, a reference shelf with arXiv:2609.16502 (the CP-decomposition solver method) and DOI 10.1515/nanoph-2024-0634 (quantum light injection; for a problem the PI will add);
  - created the first manual-run tasks: T-20261004-claude-interactive-02 (weak-LP02 capture test, not-claude) and T-20261004-claude-interactive-03 (P_min(L) map).
- Generated files are untouched. The gpt branch's regenerated `problems/INDEX.md` and `STATUS.md` were merged to `main` with PR #2; CI rebuilds them once the infrastructure branch is merged.

## Not verified

- The overlap ratios and the capture formula were derived in this session and have not been independently checked.
- The $L^{-0.79}$ exponent is a fit to three archive points and is not a registered run.
- Every literature item is abstract-level or bibliographic; access levels are recorded per card.
- The interpretation of the $L^{-0.79}$ exponent as a crossover is a hypothesis.

## Loose ends

- Full texts: Levandovsky et al. 1999, Lantz et al., Steiglitz & Rand 2009, Sloan et al., Gordon–Haus 1986. These are tracked under T-20261004-root-02, which stays open.
- A second-family review of P-20261004-claude-interactive-01 and -02: new task T-20261004-claude-interactive-01 (not-claude).
- Overlap values for the measured GIF625 profile, and registration of the archive runs: T-20261004-root-03.
