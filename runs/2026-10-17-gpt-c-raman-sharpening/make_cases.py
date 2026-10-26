"""Frozen design. gpt-c / gpt-6-astra / gpt."""
import json,math
from pathlib import Path
HERE=Path(__file__).resolve().parent
IDENT={'agent':'gpt-c','model':'gpt-6-astra','family':'gpt'}
def make(N,T,raman='bw',shape='sech',split='calibration',suffix='',**extra):
    maxwidth=160 if N<=6 else 100 if N<=11 else 70
    width=min(maxwidth,32768*2.7/T)
    n=min(32768,max(8192,2**math.ceil(math.log2(width*T/2.7))))
    zs=[2.5,3,4,6,8] if N==3 else [2,2.5,3,4] if N<=6 else [1.5,2,2.5] if N<=9 else [1.25,1.5,1.75] if N<=11 else [1.1,1.25,1.4]
    if raman=='as2s3':zs=sorted(set(zs+[min(4,zs[-1]*1.3)]))
    name=f'{raman}_{shape}_N{N:g}_T{T:.3f}'+suffix
    return dict(IDENT,id=name,N=N,T0_fs=T,raman=raman,shape=shape,n=n,width=width,zN=zs,tol=2e-9,zs_points=2048,split=split,**extra)

def main():
    cal=[];hold=[]
    for N in range(3,17):
        split='heldout' if N in [9,11,13,15] else 'calibration'
        for f in [.82,.91,1.,1.09,1.18]:
            c=make(N,round(21*N**1.62*f,3),split=split)
            (hold if split=='heldout' else cal).append(c)
    for raman,shape in [('hc','sech'),('as2s3','sech'),('bw','gaussian')]:
        for N in [3,4,6,8,12,16]:
            split='heldout' if (raman=='hc' and N in [8,12]) or (raman=='as2s3' and N in [6,8]) or (shape=='gaussian' and N==8) else 'calibration'
            for f in [.72,.86,1.,1.14,1.3]:
                tau=15.5 if raman=='as2s3' else 12.2
                c=make(N,round(21*N**1.62*tau/12.2*f,3),raman,shape,split)
                (hold if split=='heldout' else cal).append(c)
    # Save groups separately so heldouts cannot accidentally run during fitting.
    for name,items in [('calibration_cases',cal),('heldout_cases',hold)]:
        (HERE/(name+'.json')).write_text(json.dumps(items,indent=2)+'\n')
    print('calibration',len(cal),'heldout',len(hold))
if __name__=='__main__':main()
