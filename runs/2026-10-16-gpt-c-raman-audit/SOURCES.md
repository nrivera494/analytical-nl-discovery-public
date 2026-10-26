Agent: gpt-c. Model: gpt-6-astra. Family: gpt.

This is an implementation-source record, not the delegated novelty review.

- Hollenbeck and Cantrell (2002), DOI **10.1364/JOSAB.19.002886**,
  **full text** read (equations and table read; figures not separately visually audited). Equation 9 and Table 1 specify the thirteen damped modes. The
  exact Gaussian-damped oscillator transform is evaluated with complex erfcx
  and normalized at zero frequency. The table footnote defines linewidth
  conversion; its Gaussian width is used as printed, without a separate
  FWHM-to-standard-deviation conversion.
  [Author-hosted copy](https://www.researchgate.net/profile/Cyrus-Cantrell/publication/235429509_Multiple-vibrational-mode_model_for_fiber-optic_Raman_gain_spectrum_and_response_function/links/0fcfd5118eb6d16065000000/Multiple-vibrational-mode-model-for-fiber-optic-Raman-gain-spectrum-and-response-function.pdf).
- Lin and Agrawal (2006), DOI **10.1364/OL.31.003086**, **full text** read.
  Equations 2–4 define the oscillator plus Boson response and its weights.
  [Author copy](https://sites.rochester.edu/agrawal/wp-content/uploads/2019/08/paper_2006_10.pdf).
- Corning **PI-1424-AEN**, SMF-28 Ultra product information, **full text**
  accessed 2026-10-16 (manufacturer specification, no DOI/arXiv assigned).
  This supplies bounds at telecom wavelengths, not a measured broadband
  beta curve for the PI's particular spool. The zero-dispersion wavelength
  chosen for the independent model is within its range, and the slope is
  chosen to reproduce the claim's launch beta2. Extrapolation far beyond the
  specified band is explicitly a model sensitivity test, not a certified
  SMF-28 prediction.
  [Manufacturer PDF](https://www.corning.com/content/dam/corning/media/worldwide/coc/documents/Fiber/product-information-sheets/PI-1424-AEN.pdf).

No claim-02 novelty search was performed; gpt-b owns that task. Its report
in PR #52 was read only after independent verdict commit `143cc58`. The
audit report's post-commit section records the review commit and distinguishes
gpt-b's source access from sources actually accessed by gpt-c.

- Boilard, Vallée and Bernier (2022), DOI **10.1038/s41598-022-08329-3**,
  arXiv:**2109.13366**, **full text** read (arXiv text plus published XML).
  The published Table 3 supplies a rational fit to the measured-index-derived
  SMF-28 dispersion. The independent implementation integrates this fit in
  angular frequency; it does not truncate at beta3 and does not force its
  launch beta2 to equal the card's value. Its comparison with earlier SMF-28
  dispersion measurements supports use through the near infrared, with the
  paper's stated fit uncertainty and sample specificity.
  [Paper](https://doi.org/10.1038/s41598-022-08329-3);
  [published XML](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8921235/fullTextXML).
  The downloaded XML is retained with the raw output.
  Published text and tables were read via that XML because the journal HTML
  redirected through an unavailable authentication endpoint; no paywall was
  bypassed. The freely available author preprint was also read.

- Gordon (1986), DOI **10.1364/OL.11.000662**, **abstract only** accessed.
  The independent long-pulse moment calculation uses the normalized slope
  8 T_R/(15 T0); this coefficient is also obtained directly by integrating
  the sech intensity-gradient moment, rather than inferred from the abstract.
  [Publisher abstract](https://opg.optica.org/ol/abstract.cfm?uri=ol-11-10-662).
