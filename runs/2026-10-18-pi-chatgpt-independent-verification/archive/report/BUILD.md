# Build the technical report

The completed PDF is included. Rebuilding is optional and requires a normal LaTeX installation with `pdflatex`, Latin Modern, AMS packages, `fontenc`, `geometry`, `booktabs`, `longtable`, `tabularx`, `array`, `graphicx`, `xcolor`, `hyperref`, `microtype`, `enumitem`, and `fancyhdr`.

From this `report` directory, run twice to resolve the contents and references:

```bash
pdflatex -interaction=nonstopmode -halt-on-error independent_verification_report.tex
pdflatex -interaction=nonstopmode -halt-on-error independent_verification_report.tex
```

The source references the three supplied vector figures in the sibling calculation directories. The figures plot independent numerical results alongside explicitly labeled theoretical and repository comparison curves. No copyrighted primary-paper figures are reproduced.

The numerical calculations themselves need only Python and the dependencies in `../requirements.txt`; LaTeX is not needed to reproduce them.
