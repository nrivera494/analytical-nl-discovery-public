---
agent: claude-interactive
model: claude-opus-5-5
family: claude
date: 2026-10-19
task: T-20261019-claude-interactive.14-02
supersedes_access_level_of: docs/review-2026-10-19-claude-interactive.14-spie2016-similariton-noise.md
---

# Full-text check of the Wang et al. (2016) similariton-amplifier noise papers

**What was read, in full.** The PI downloaded both papers through institutional access on 2026-10-19. They are kept locally at `~/analytical-nl-discovery-data/spie2016/` and are not committed, for copyright reasons.
1. S. Wang, B. Liu, Y. Song and M. Hu, "Intensity noise reduction of a high-power nonlinear femtosecond fiber amplifier based on spectral-breathing self-similar parabolic pulse evolution," *Proc. SPIE* 9893, 98930J (2016), DOI 10.1117/12.2227743. **Full text**, 7 pages: text, all figures and references.
2. S. Wang, W. Chen, P. Qin, Y. Song, M. Hu and B. Liu, "Spectral and temporal breathing self-similar evolution in a fiber amplifier for low-noise transform-limited pulse generation," *Opt. Lett.* 41, 5286–5289 (2016), DOI 10.1364/OL.41.005286. **Full text**, 4 pages.

**Purpose.** claude-interactive.14 had read both at abstract level only. This note checks its verdicts against the full texts, for C-20261008-claude-a-02 (result R-0011) and C-20261019-pi-chatgpt-02 (result R-0014).

## What the papers do

- **System.** A 2 m Yb-doped large-mode-area photonic-crystal-fibre amplifier at 82 MHz, with about 25–26 dB of gain, 27–32 W output, and grating pre-chirper and compressor.
- **Variable.** The sign and size of the pre-chirp. An optimized negative pre-chirp produces a "spectral-breathing" evolution: spectral compression first, then rapid self-similar broadening in the last part of the fibre.
- **Noise measured.** Classical relative intensity noise (RIN) of the total output power: a photodiode with a 10 MHz low-pass filter, FFT and RF spectrum analyzers, and integrated rms RIN (10 Hz–10 MHz, or 1 kHz–5 MHz).
  - Headline numbers: an rms RIN reduction of about 20.5% (SPIE) and about 31% (Opt. Lett.) with the negative pre-chirp; minimum rms RIN 0.025% and 0.029%.
  - In the SPIE paper RIN rises as the input energy falls (1.2 nJ to 0.6 nJ), attributed to ASE. The rise is smaller with negative pre-chirp (23.2% against 38.8%).
- **Simulations.** A spectrally resolved steady-state rate- and power-equation model for gain and ASE, coupled to an NLSE; a parabolic misfit parameter $M$; and a deterministic sensitivity analysis.
  - SPIE Fig. 5: the output relative ASE-power fluctuation for a 50% input-energy fluctuation, against chirp.
  - Opt. Lett. Fig. 5: the output relative fluctuation of pulse energy and of rms spectral width for a 0.5% fluctuation in pump power or pump wavelength, against chirp.

  All noise is classical: there is no Langevin quantum noise, no shot-noise normalization, and no quadrature.
- **Mechanism offered.**
  - SPIE: lower overall chirp, a shorter spectral-broadening distance, and the attracting nature of self-similar amplification.
  - Opt. Lett.: higher peak power (lower pump sensitivity) and a shorter broadening distance (less noise accumulation). It does not invoke the attraction.
- **Not in either paper:**
  - any dependence of noise on gain (only one gain is used);
  - any modal or shape decomposition of the noise;
  - spectral covariance;
  - any phase-noise measurement (the SPIE paper says phase-noise experiments are in progress);
  - quantum noise or squeezing.

## Verdicts

The verdicts are unchanged from the abstract-level review; their confidence is raised from abstract-level to full-text.

| Statement | Verdict | Evidence from the full text |
|---|---|---|
| C-20261008-claude-a-02 (a): shape-mode variance envelopes $G^{1/3}$, $G^{5/3}$ | **Not anticipated** | Only total-power RIN at one gain; no shape modes, no gain law |
| (a), interpretive sentence: the attraction suppresses intensity noise | **Partly anticipated, qualitatively, for a different observable** | The SPIE paper credits the attraction among three causes for lower ASE-driven RIN. The measured quantity is total-energy noise below 10 MHz, which in the claim's flat-gain model equals linear-amplifier energy noise. The observed chirp dependence comes from spectral gain shaping, the ASE spectrum and pump coupling, which the claim's model excludes. The Opt. Lett. version drops the attraction argument |
| (b): single-shot spectral covariance tends to rank one, $\mu_2/\mu_1=\Theta(G^{-2/3})$ | **Not anticipated** | The nearest item is the Opt. Lett. Fig. 5(b): a deterministic rms spectral-width response to a pump perturbation, a one-parameter classical sensitivity. It reports no covariance and no gain law |
| (c): matched-LO phase locked to energy, $1-r^2=\Theta(G^{-2/3})$ | **Not anticipated** | No phase or homodyne quantity |
| C-20261019-pi-chatgpt-02 (i): $C_{PP}\propto G^{7/3}/\varepsilon_0^2$ | **Not anticipated** | No phase noise |
| (ii): matched-mode squeezing at short length despite full ASE, when $\gamma\int P^2/\int P>n_{sp}g$ | **Not anticipated** | No quantum noise; ASE appears only as a classical RIN source |
| (iii): matched-mode minimum variance $\Theta(G^{1/3})$ | **Not anticipated** | No quadrature variance, no gain law |

**References.** Both reference lists were read in full, and the antecedents agree with claude-interactive.14's reference-chain check. The only similariton-theory references are Fermann et al. (2000) and, in Opt. Lett., Finot et al. (2006). Andresen et al. (2011) and Korobko et al. (2016) treat nonlinear spectral compression, not noise.

## Effect on the results

- **R-0011 (C-20261008-claude-a-02).** One of the two unread leads behind its open G6 is now read in full. G6 stays open for the other: the full journal text of Wabnitz (2007) (task T-20261008-claude-a-05).
- **R-0014 (C-20261019-pi-chatgpt-02).** The full-text gap is closed. G6 stays open for the targeted prior-art search on (ii) (task T-20261019-claude-interactive.14-03).
- Tasks T-20261019-claude-interactive.14-01 (the PI's download) and .14-02 (this reading) are done.
