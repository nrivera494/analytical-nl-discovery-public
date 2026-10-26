#!/usr/bin/env python3
"""agent: gpt-a; model: gpt-6-astra; family: gpt.
Read vector circle centres in Roy et al. Fig. 3(b); no image fitting.
Source: DOI 10.1103/PhysRevA.79.023824, full text, APS PDF.
"""
import hashlib
import json
import math
from pathlib import Path
import shutil
import fitz
import yaml

folder=Path(__file__).resolve().parent
raw=Path('~/analytical-nl-discovery-data')/folder.name
raw.mkdir(parents=True,exist_ok=True)
pdf=raw/'roy-2009.pdf'
if not pdf.exists():
    shutil.copyfile('/private/tmp/roy-aps.pdf',pdf)
doc=fitz.open(pdf)
page=doc[3]
drawings=page.get_drawings()
frame=drawings[18]['rect']
assert abs(frame.x0-95.15)<.001 and abs(frame.y0-209.8351)<.001

def read_circles(drawing):
    curves=[v for v in drawing['items'] if v[0]=='c']
    assert len(curves)%4==0
    rows=[]
    for j in range(0,len(curves),4):
        points=[v for curve in curves[j:j+4] for v in curve[1:]]
        x=(min(p.x for p in points)+max(p.x for p in points))/2
        y=(min(p.y for p in points)+max(p.y for p in points))/2
        delta=.01+.09*(x-frame.x0)/frame.width
        db=-80*(y-frame.y0)/frame.height
        nominal=round(delta/.0025)*.0025
        rows.append(dict(delta3_vector=delta,delta3=nominal,peak_db=db,
                         vector_x=x,vector_y=y))
    return rows

full=read_circles(drawings[32])
tod=read_circles(drawings[30])
assert drawings[32]['color']==(0.,0.,0.)
assert drawings[30]['color']==(0.,0.,1.)

# Independent frequency check from Fig. 3(a)'s black circles.
top_frame=drawings[2]['rect']
curves=[v for v in drawings[14]['items'] if v[0]=='c']
full_frequency=[]
for j in range(0,len(curves),4):
    points=[v for curve in curves[j:j+4] for v in curve[1:]]
    x=(min(p.x for p in points)+max(p.x for p in points))/2
    y=(min(p.y for p in points)+max(p.y for p in points))/2
    delta=.01+.09*(x-top_frame.x0)/top_frame.width
    frequency=1+4.5*(top_frame.y1-y)/top_frame.height
    full_frequency.append(dict(delta3=round(delta/.0025)*.0025,
        delta3_vector=delta,peak_cycles=frequency,vector_x=x,vector_y=y))

def eq6(delta,N=2):
    return (5*math.pi*N/(4*delta))**2*(1-2*math.pi/5*(2*N-1)*delta)**2*math.exp(-math.pi/(2*(2*N-1)*delta))

for row in full+tod:
    row['eq6_db']=10*math.log10(eq6(row['delta3']))
identity=dict(agent='gpt-a',model='gpt-6-astra',family='gpt',run_id=folder.name)
summary=dict(**identity,source_doi='10.1103/PhysRevA.79.023824',access='full text',
    pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),
    source_url='https://journals.aps.org/pra/pdf/10.1103/PhysRevA.79.023824',
    equation6='(5*pi*N/(4*d))^2 * (1-2*pi*(2*N-1)*d/5)^2 * exp(-pi/(2*(2*N-1)*d))',
    paper_shock='1/(2*pi*nu0*T0) = 1/(omega0*T0)',
    shock_paper=835/(2*math.pi*299.792458*50),
    shock_assignment=2*835/(2*math.pi*299.792458*50),
    figure3b_full=full,figure3b_tod=tod,figure3a_full=full_frequency,
    extraction='Cubic-Bezier circle centres, affine mapping from vector plot axes; visual check of pages 2 and 4.',
    vector_coordinate_resolution_db=.03)
(folder/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
(folder/'config.yaml').write_text(yaml.safe_dump(dict(**identity,source=summary['source_url'],
    page_index=3,frame_drawing=18,full_drawing=32,tod_drawing=30,
    frequency_frame_drawing=2,frequency_full_drawing=14,frequency_axis=[1,5.5]),sort_keys=False))
(folder/'meta.yaml').write_text(yaml.safe_dump(dict(**identity,
    solver_commit='b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa',solver_dirty=False,
    computation='reference extraction; no propagation',raw_location=str(raw),
    claim='C-20261016-claude-b-01'),sort_keys=False))
for row in full:
    print(row['delta3'],round(row['peak_db'],3),round(row['eq6_db'],3))
