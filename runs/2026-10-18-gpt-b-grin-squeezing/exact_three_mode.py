#!/usr/bin/env python3
"""gpt-b / gpt-6-astra / gpt. Exchange-Hamiltonian exact Fock benchmark."""
import sys,time,copy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'evaluator'))
from squeezing import *
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import expm_multiply
from scipy.special import gammaln
RUN=Path(__file__).resolve().parent;DATA=RAW/RUN.name

def subset():
    m=Model(3);ix=[0,2,5];m.tensor=m.tensor[np.ix_(ix,ix,ix,ix)];m.M=3;m.q=np.arange(3,dtype=np.int32)
    m.p,m.r=np.triu_indices(3);m.p=m.p.astype(np.int32);m.r=m.r.astype(np.int32)
    pair=m.tensor[m.p[:,None],m.r[:,None],m.p[None,:],m.r[None,:]]*np.where(m.p==m.r,1.,2.)[None,:]
    row,col=np.nonzero(pair);m.column=col.astype(np.int32);m.offset=np.r_[0,np.cumsum(np.bincount(row,minlength=len(m.p)))].astype(np.int32);m.value=np.asarray(pair[row,col]);return m

def fock(n,extra=0):
    memory_gate();start=time.time();m=subset();cut=int(n+10*np.sqrt(n)+20)+extra
    states=np.array([(i,j,k) for i in range(cut+1) for j in range(cut+1-i) for k in range(cut+1-i-j)],dtype=np.int16)
    dim=len(states);lookup=np.full((cut+2,cut+2,cut+2),-1,dtype=np.int32);lookup[tuple(states.T)]=np.arange(dim,dtype=np.int32)
    rows=[];cols=[];vals=[]
    for p in range(3):
     for q in range(p,3):
      for r in range(3):
       for s in range(r,3):
        v=m.tensor[p,q,r,s]*(1 if p==q else 2)*(1 if r==s else 2)/(2*n)
        if abs(v)<1e-14:continue
        b=states.copy();coef=b[:,s].astype(float);b[:,s]-=1;coef*=b[:,r];b[:,r]-=1
        valid=np.all(b>=0,axis=1);b[:,q]+=1;coef*=b[:,q];b[:,p]+=1;coef*=b[:,p]
        ii=np.flatnonzero(valid);rows.append(lookup[tuple(b[ii].T)]);cols.append(ii);vals.append(v*np.sqrt(coef[ii]))
    H=coo_matrix((np.concatenate(vals),(np.concatenate(rows),np.concatenate(cols))),shape=(dim,dim)).tocsr()
    herm=float(abs(H-H.T).max());a=np.sqrt(np.array([.7,.2,.1]))*np.exp(1j*np.array([0,.7,1.9]))
    psi=np.exp(-n/2+np.sum(states*np.log(np.sqrt(n)*a)-.5*gammaln(states.astype(np.float64)+1),axis=1));norm=float(np.vdot(psi,psi).real);psi/=np.sqrt(norm)
    vals=expm_multiply(-1j*H,psi,start=0,stop=10,num=11,traceA=-1j*H.diagonal().sum())
    maps=[]
    for p in range(3):
      valid=states[:,p]>0;src=np.flatnonzero(valid);b=states[src].copy();b[:,p]-=1;dst=lookup[tuple(b.T)];maps.append((src,dst,np.sqrt(states[src,p].astype(np.float64))))
    def annihilate(v,p):
      src,dst,c=maps[p];out=np.zeros_like(v);out[dst]=v[src]*c;return out
    out=[]
    for z in [0,1,2,5,10]:
      v=vals[z];av=np.array([annihilate(v,p) for p in range(3)]);mean=av@v.conj();C=av.conj()@av.T;B=np.array([[np.vdot(v,annihilate(av[q],p)) for q in range(3)] for p in range(3)])
      V=np.block([[np.eye(3)+2*(B+C).real,2*(B+C).imag],[2*(B+C).imag.T,np.eye(3)+2*(C-B).real]])-4*np.outer(np.r_[mean.real,mean.imag],np.r_[mean.real,mean.imag])
      prob=abs(v)**2;mn=prob@states;cn=(states.T*prob)@states-np.outer(mn,mn);F=cn/np.sqrt(mn[:,None]*mn[None,:])
      out.append(dict(z=z,lambda_quad=np.linalg.eigvalsh(V)[0],lambda_gen=np.linalg.eigvalsh(F)[0],V=V,F=F,mean_photons=mn,
          total_Fano=float(cn.sum()/mn.sum()),norm=float(prob.sum())))
    rec=dict(**IDENTITY,reference_valid=True,precision='Float64 factorials and ladder coefficients; Complex128 propagation',n=n,extra=extra,cutoff=cut,dimension=dim,nnz=H.nnz,hermiticity_error=herm,input_norm=norm,rows=out,wall_seconds=time.time()-start)
    save_json(RUN/f'exact3_n{n}_extra{extra}.json',rec);print('exact3',n,dim,'seconds',time.time()-start,flush=True)

def twa(n):
    memory_gate();m=subset();a=np.sqrt([.7,.2,.1])*np.exp(1j*np.array([0,.7,1.9]));zs=[0,1,2,5,10];records=[]
    for dt in [.02,.01]:
      t=tangent_run(m,a,zs,dt=dt,sigma=0)
      for b in range(4):
        ini,noise=wigner_initial(a,n,power=13,seed=8751+b);fields=ensemble_run(m,ini,n,zs,dt=dt,sigma=0);rows=[]
        for z,ff,xx in zip(zs,fields,t):
          r=sample_observables(ff,n,tangent_observables(xx),noise);r.pop('V');r.pop('F');r.pop('mean_photons');r['z']=z;rows.append(r)
        records.append(dict(dt=dt,batch=b,rows=rows))
    save_json(RUN/f'twa3_n{n}.json',dict(**IDENTITY,n=n,shots_per_step=32768,records=records))
if __name__=='__main__':
    if sys.argv[1]=='fock':
      for n in [8,16,32,48,64]:fock(n)
      fock(16,20)
    else:
      for n in [8,16,32,48,64]:twa(n)
