"""Equal input energy and intensity-FWHM comparison. gpt-c / gpt-6-astra / gpt."""
import json,numpy as np
from pathlib import Path
from make_cases import make
HERE=Path(__file__).resolve().parent
k=np.arccosh(np.sqrt(2))/np.sqrt(np.log(2));g=np.sqrt(2*k/np.sqrt(np.pi));out=[]
for Ns in [4,6]:
    for f in [.75,.9,1.,1.1,1.3]:
        Ts=21*Ns**1.62*f;Tg=k*Ts;Ng=g*Ns
        c=make(Ng,Tg,'bw','gaussian','matched_shape',suffix=f'_matchedNs{Ns}')
        c.update(reference_sech_N=Ns,reference_sech_T0_fs=Ts,matched_input_energy=True,matched_intensity_FWHM=True,zN=[3*g/k**2,4*g/k**2])
        out.append(c)
(HERE/'matched_shape_cases.json').write_text(json.dumps(out,indent=2)+'\n')
print('shape duration ratio',k,'Gaussian peak-order ratio',g,'cases',len(out))
