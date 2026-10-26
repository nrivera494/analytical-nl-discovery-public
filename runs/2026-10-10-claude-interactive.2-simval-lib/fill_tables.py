"""Insert (or refresh) the generated tables in the exploration note between <!-- TABLE:x --> and <!-- /TABLE:x -->."""
import os, re
import make_tables as T

NOTE = os.path.join(os.path.dirname(T.RUNS), "explorations", "2026-10-10-claude-interactive.2-similariton-validation.md")
s = open(NOTE).read()
for key in ("noise", "spectral", "shape"):
    tab = getattr(T, key + "_tables")()
    block = f"<!-- TABLE:{key} -->\n{tab}\n<!-- /TABLE:{key} -->"
    pat = re.compile(rf"<!-- TABLE:{key} -->.*?<!-- /TABLE:{key} -->", re.S)
    if pat.search(s):
        s = pat.sub(lambda m: block, s)
    else:
        s = s.replace(f"<!-- TABLE:{key} -->", block)
open(NOTE, "w").write(s)
print("filled")
