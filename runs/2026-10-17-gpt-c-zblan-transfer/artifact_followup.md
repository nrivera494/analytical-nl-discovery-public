# Window qualification correction and recovery design

gpt-c / gpt-6-astra / gpt, 2026-10-17, before the wider-window reruns.

The coarse reference N=6 r=1.5 and r=2 cases reached the edge of the
96*T0 window at zN=4. They are retained and excluded. Inspection also
found that the new analyzer tested the periodically accumulated edge
maximum but omitted the separately recorded instantaneous checkpoint
fraction. It now checks both, as required by the frozen threshold. No
forward equation or material prediction changes. The runner's early-stop
test is corrected identically for subsequent cases.

The phase-1 analyzer already included all four edge diagnostics. A fresh
read-only check of every accepted phase-1 peak bracket endpoint found no
instantaneous threshold violations; its conclusions are unaffected.

Rerun reference N=6 at r=1.2,1.5,2 with width120*T0 and n32768, retaining
dt<=2.5 fs. Future midpoint localization for this reference branch uses
the wider window. A double-window control at r=2 uses width240*T0 and
n65536, preserving dt. This is the **one explicitly justified exception**
to the preferred 32768-point limit: the narrow window has failed, and
doubling both window and grid is needed to isolate temporal-window error.
It remains serial and far below the memory budget. Require relative
share/gated-energy change<0.2% and each width change<1%, as for the
physical controls. No edge-affected point may define a peak or error bar.
