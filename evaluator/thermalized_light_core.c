/* agent: gpt-b; model: gpt-6-astra; family: gpt; 2026-10-17.
   Independent HG resonant Hamiltonian; no proposer source was read.
   clang -O3 -std=c11 -fPIC -shared thermalized_light_core.c -o /tmp/thermalized_light_core.dylib
   Complex pair basis gives an exact sparse contraction, not a tensor fit. */
#include <complex.h>
#include <math.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

typedef double complex Z;
typedef struct {
    int m, np;
    const int *p, *q, *offset, *column, *group;
    const double *value;
    const Z *lz, *linear;
} Model;

static void force(const Model *md, const Z *a, Z *f, Z *b, Z *v) {
    for(int j=0;j<md->np;j++) b[j]=a[md->p[j]]*a[md->q[j]];
    for(int j=0;j<md->np;j++) {
        Z t=0;
        for(int k=md->offset[j];k<md->offset[j+1];k++) t+=md->value[k]*b[md->column[k]];
        v[j]=t;
    }
    for(int j=0;j<md->m;j++) f[j]=0;
    for(int j=0;j<md->np;j++) {
        int p=md->p[j],q=md->q[j];
        f[p] += conj(a[q])*v[j];
        if(p!=q) f[q] += conj(a[p])*v[j];
    }
    for(int j=0;j<md->m;j++) f[j] *= -I;
    if(md->linear) for(int j=0;j<md->m;j++)for(int k=0;k<md->m;k++)
        f[j]+=I*md->linear[j*md->m+k]*a[k];
}

static void rk4(const Model *md,Z *a,double dt,Z *work) {
    int m=md->m;
    Z *k1=work,*k2=work+m,*k3=work+2*m,*k4=work+3*m,*t=work+4*m;
    Z *b=work+5*m,*v=b+md->np;
    force(md,a,k1,b,v);
    for(int j=0;j<m;j++) t[j]=a[j]+dt*.5*k1[j];
    force(md,t,k2,b,v);
    for(int j=0;j<m;j++) t[j]=a[j]+dt*.5*k2[j];
    force(md,t,k3,b,v);
    for(int j=0;j<m;j++) t[j]=a[j]+dt*k3[j];
    force(md,t,k4,b,v);
    for(int j=0;j<m;j++) a[j]+=dt/6*(k1[j]+2*k2[j]+2*k3[j]+k4[j]);
}

/* xoshiro256** initialized with splitmix64; Box--Muller normal draws. */
typedef struct {uint64_t s[4]; int ready; double spare;} RNG;
static uint64_t rotl(uint64_t x,int k) {return (x<<k)|(x>>(64-k));}
static uint64_t splitmix(uint64_t *x) {
    uint64_t z=(*x+=UINT64_C(0x9e3779b97f4a7c15));
    z=(z^(z>>30))*UINT64_C(0xbf58476d1ce4e5b9);
    z=(z^(z>>27))*UINT64_C(0x94d049bb133111eb); return z^(z>>31);
}
static void init_rng(RNG *r,uint64_t seed) {
    for(int j=0;j<4;j++)r->s[j]=splitmix(&seed);r->ready=0;
}
static double uniform(RNG *r) {
    uint64_t out=rotl(r->s[1]*5,7)*9,t=r->s[1]<<17;
    r->s[2]^=r->s[0];r->s[3]^=r->s[1];r->s[1]^=r->s[2];r->s[0]^=r->s[3];
    r->s[2]^=t;r->s[3]=rotl(r->s[3],45);
    return ((out>>11)+.5)*0x1.0p-53;
}
static double normal(RNG *r) {
    if(r->ready){r->ready=0;return r->spare;}
    double t=6.2831853071795864769*uniform(r),q=sqrt(-2*log(uniform(r)));
    r->spare=q*sin(t);r->ready=1;return q*cos(t);
}

static void disorder(const Model *md,Z *a,double scale,RNG *r) {
    /* All generators have the GUE covariance dB_ij dB_kl=delta_il delta_jk dt/d.
       Each elementary flow is unitary. Reverse order on alternating steps
       is unnecessary for stationarity: every flow preserves the shell measure.
       Dynamical weak errors are checked by step halving. */
    for(int j=0;j<md->m;j++) {
        double th=scale/sqrt(md->group[j]+1.)*normal(r);
        a[j] *= cos(th)-I*sin(th);
    }
    for(int j=0;j<md->m;j++) for(int k=j+1;k<md->m;k++) {
        if(md->group[j]!=md->group[k])continue;
        double s=scale/sqrt(2*(md->group[j]+1.));
        double th=s*normal(r),c=cos(th),t=sin(th); Z aj=a[j],ak=a[k];
        a[j]=c*aj-I*t*ak;a[k]=c*ak-I*t*aj;
        th=s*normal(r);c=cos(th);t=sin(th);aj=a[j];ak=a[k];
        a[j]=c*aj+t*ak;a[k]=c*ak-t*aj;
    }
}

static void invariants(const Model *md,const Z *a,double *out,Z *work) {
    double n=0,e=0,l=0;
    for(int j=0;j<md->m;j++) {
        double v=creal(conj(a[j])*a[j]); n+=v;e+=md->group[j]*v;
        for(int k=0;k<md->m;k++)l+=creal(conj(a[j])*md->lz[j*md->m+k]*a[k]);
    }
    force(md,a,work,work+md->m,work+md->m+md->np);
    double h=0; for(int j=0;j<md->m;j++)h+=creal(conj(a[j])*I*work[j])*.5;
    out[0]=n;out[1]=e;out[2]=h;out[3]=l;
}

void tl_rhs(int m,int np,const int *p,const int *q,const int *offset,
 const int *column,const double *value,int batch,const Z *a,Z *out) {
    Model md={m,np,p,q,offset,column,NULL,value,NULL,NULL};
    Z *work=malloc(sizeof(Z)*2*np);
    for(int j=0;j<batch;j++)force(&md,a+j*m,out+j*m,work,work+np);
    free(work);
}

int tl_run(int m,int np,const int *p,const int *q,const int *offset,
 const int *column,const double *value,const int *group,const Z *lz,
 Z *a,double dt,int steps,int sample_steps,int block_steps,double sigma,
 uint64_t seed,double *moments,Z *checkpoints,double *checks) {
    Model md={m,np,p,q,offset,column,group,value,lz,NULL};
    Z *work=calloc(8*m+2*np,sizeof(Z));
    double *powers=calloc(m,sizeof(double)), ini[4], now[4];
    RNG rng;init_rng(&rng,seed);
    int width=1+m+m*m;
    invariants(&md,a,ini,work);memcpy(checks,ini,4*sizeof(double));
    memcpy(checkpoints,a,m*sizeof(Z));
    for(int s=1;s<=steps;s++) {
        if(sigma) {rk4(&md,a,dt/2,work);disorder(&md,a,sigma*sqrt(dt),&rng);rk4(&md,a,dt/2,work);}
        else rk4(&md,a,dt,work);
        if(s%sample_steps==0) {
            int b=(s-1)/block_steps;
            double *out=moments+b*width; out[0]++;
            for(int j=0;j<m;j++) {powers[j]=creal(a[j]*conj(a[j]));out[1+j]+=powers[j];}
            for(int j=0;j<m;j++)for(int k=0;k<m;k++)out[1+m+j*m+k]+=powers[j]*powers[k];
            invariants(&md,a,now,work);
            for(int j=0;j<4;j++) {
                double d=fabs(now[j]-ini[j]);if(d>checks[4+j])checks[4+j]=d;
            }
            if(!isfinite(now[0])) {free(work);free(powers);return s;}
        }
        if(s%block_steps==0)memcpy(checkpoints+(s/block_steps)*m,a,m*sizeof(Z));
    }
    invariants(&md,a,checks+8,work);
    free(work);free(powers);return 0;
}

int tl_mcmc(int m,int np,const int *p,const int *q,const int *offset,
 const int *column,const double *value,const int *group,const Z *lz,
 Z *a,double energy,double target_h,double target_l,double width_h,double width_l,
 int steps,int block_steps,uint64_t seed,double *blocks,double *diagnostics) {
    Model md={m,np,p,q,offset,column,group,value,lz,NULL};
    Z *work=calloc(8*m+2*np,sizeof(Z)),*proposal=calloc(m,sizeof(Z));
    double *x=calloc(m,sizeof(double)),*phi=calloc(m,sizeof(double));
    double inv[4],pi[4];RNG rng;init_rng(&rng,seed);
    for(int j=0;j<m;j++) {x[j]=group[j]*creal(a[j]*conj(a[j]))/energy;phi[j]=carg(a[j]);}
    invariants(&md,a,inv,work);
    double cost=.5*pow((inv[2]-target_h)/width_h,2);
    if(width_l>0)cost+=.5*pow((inv[3]-target_l)/width_l,2);
    for(int s=1;s<=steps;s++) {
        memcpy(proposal,a,m*sizeof(Z));
        int i=1+(int)(uniform(&rng)*(m-1)),j=1+(int)(uniform(&rng)*(m-2));
        if(j>=i)j++;
        int phase=uniform(&rng)<.5;
        double xp=x[i],xq=x[j],ph=phi[i];int valid=1;
        if(phase) {
            ph+=.8*(uniform(&rng)-.5);
            proposal[i]=sqrt(energy*x[i]/group[i])*(cos(ph)+I*sin(ph));
        } else {
            if(uniform(&rng)<.1)xp=(x[i]+x[j])*uniform(&rng);
            else xp=x[i]+.08*(uniform(&rng)-.5);
            xq=x[i]+x[j]-xp;
            if(xp<0||xq<0)valid=0;
            else {
                proposal[i]=sqrt(energy*xp/group[i])*(cos(phi[i])+I*sin(phi[i]));
                proposal[j]=sqrt(energy*xq/group[j])*(cos(phi[j])+I*sin(phi[j]));
                double p0=creal(a[0]*conj(a[0]))+
                  energy*((x[i]-xp)/group[i]+(x[j]-xq)/group[j]);
                if(p0<0)valid=0;
                else proposal[0]=sqrt(p0)*(cos(phi[0])+I*sin(phi[0]));
            }
        }
        if(valid) {
            invariants(&md,proposal,pi,work);
            double newcost=.5*pow((pi[2]-target_h)/width_h,2);
            if(width_l>0)newcost+=.5*pow((pi[3]-target_l)/width_l,2);
            if(log(uniform(&rng))<cost-newcost) {
                memcpy(a,proposal,m*sizeof(Z));memcpy(inv,pi,4*sizeof(double));cost=newcost;
                x[i]=xp;x[j]=xq;phi[i]=ph;diagnostics[phase?0:1]++;
            }
        }
        double *out=blocks+((s-1)/block_steps)*4;
        out[0]+=creal(a[0]*conj(a[0]));out[1]+=inv[2];out[2]+=inv[3];out[3]+=cost;
    }
    diagnostics[2]=inv[0];diagnostics[3]=inv[1];diagnostics[4]=inv[2];diagnostics[5]=inv[3];
    free(work);free(proposal);free(x);free(phi);return 0;
}

static void disorder_batch(const Model *md,Z *a,int batch,double scale,const double *draws) {
    int m=md->m;
    int index=0;
    for(int j=0;j<m;j++) {
        double th=scale/sqrt(md->group[j]+1.)*draws[index++];Z u=cos(th)-I*sin(th);
        for(int b=0;b<batch;b++)a[b*m+j]*=u;
    }
    for(int j=0;j<m;j++)for(int k=j+1;k<m;k++) {
        if(md->group[j]!=md->group[k])continue;
        double s=scale/sqrt(2*(md->group[j]+1.));
        double th=s*draws[index++],c=cos(th),t=sin(th);
        for(int b=0;b<batch;b++) {Z aj=a[b*m+j],ak=a[b*m+k];
            a[b*m+j]=c*aj-I*t*ak;a[b*m+k]=c*ak-I*t*aj;}
        th=s*draws[index++];c=cos(th);t=sin(th);
        for(int b=0;b<batch;b++){Z aj=a[b*m+j],ak=a[b*m+k];
            a[b*m+j]=c*aj+t*ak;a[b*m+k]=c*ak-t*aj;}
    }
}

static int noise_dimension(const Model *md) {
    int n=md->m;
    for(int j=0;j<md->m;j++)for(int k=j+1;k<md->m;k++)
        if(md->group[j]==md->group[k])n+=2;
    return n;
}

/* Refinement 2 couples two half steps to each original increment through
   an independent Brownian bridge. Coarse-step draws remain unchanged. */
static void noise_draws(int count,int step,int refinement,RNG *parent,RNG *bridge,
                        double *draws,double *coarse,double *bridge_values) {
    for(int j=0;j<count;j++) {
        if(refinement==1)draws[j]=normal(parent);
        else {
            if(step%2) {coarse[j]=normal(parent);bridge_values[j]=normal(bridge);}
            draws[j]=(coarse[j]+(step%2?1:-1)*bridge_values[j])/sqrt(2.);
        }
    }
}

static void ensemble_moments(const Z *a,int m,int batch,double *out) {
    for(int b=0;b<batch;b++)for(int j=0;j<m;j++) {
        Z aj=a[b*m+j],cross=conj(a[b*m])*aj;double power=creal(conj(aj)*aj);
        out[j]+=creal(aj)/batch;out[m+j]+=cimag(aj)/batch;
        out[2*m+j]+=power/batch;out[3*m+j]+=power*power/batch;
        out[4*m+j]+=creal(cross)/batch;out[5*m+j]+=cimag(cross)/batch;
    }
}

int tl_ensemble(int m,int np,const int *p,const int *q,const int *offset,
 const int *column,const double *value,const int *group,const Z *linear,
 Z *a,int batch,double dt,int steps,int sample_steps,double sigma,uint64_t seed,int refinement,
 double *out) {
    Model md={m,np,p,q,offset,column,group,value,NULL,linear};
    int nonzero_linear=0;
    for(int j=0;j<m*m;j++)if(cabs(linear[j])>0) {nonzero_linear=1;break;}
    if(!nonzero_linear)md.linear=NULL;
    Z *work=calloc(8*m+2*np,sizeof(Z));RNG rng,bridge;init_rng(&rng,seed);
    init_rng(&bridge,seed^UINT64_C(0x83a5c91f4bb2476d));
    int count=noise_dimension(&md);double *noise=calloc(3*count,sizeof(double));
    ensemble_moments(a,m,batch,out);
    for(int s=1;s<=steps;s++) {
        if(sigma) {
            for(int b=0;b<batch;b++)rk4(&md,a+b*m,dt/2,work);
            noise_draws(count,s,refinement,&rng,&bridge,noise,noise+count,noise+2*count);
            disorder_batch(&md,a,batch,sigma*sqrt(dt),noise);
            for(int b=0;b<batch;b++)rk4(&md,a+b*m,dt/2,work);
        } else for(int b=0;b<batch;b++)rk4(&md,a+b*m,dt,work);
        if(s%sample_steps==0)ensemble_moments(a,m,batch,out+(s/sample_steps)*6*m);
    }
    free(work);free(noise);return 0;
}

int tl_lyapunov(int m,int np,const int *p,const int *q,const int *offset,
 const int *column,const double *value,const int *group,Z *a,double dt,int steps,
 int reset_steps,double epsilon,double sigma,uint64_t seed,int refinement,double *growth) {
    Model md={m,np,p,q,offset,column,group,value,NULL,NULL};
    Z *work=calloc(8*m+2*np,sizeof(Z));RNG rng,bridge;init_rng(&rng,seed);
    init_rng(&bridge,seed^UINT64_C(0x83a5c91f4bb2476d));
    int count=noise_dimension(&md);double *noise=calloc(3*count,sizeof(double));
    for(int s=1;s<=steps;s++) {
        if(sigma) {
            rk4(&md,a,dt/2,work);rk4(&md,a+m,dt/2,work);
            noise_draws(count,s,refinement,&rng,&bridge,noise,noise+count,noise+2*count);
            disorder_batch(&md,a,2,sigma*sqrt(dt),noise);
            rk4(&md,a,dt/2,work);rk4(&md,a+m,dt/2,work);
        }else{rk4(&md,a,dt,work);rk4(&md,a+m,dt,work);}
        if(s%reset_steps==0) {
            double norm=0;for(int j=0;j<m;j++){Z d=a[m+j]-a[j];norm+=creal(d*conj(d));}
            norm=sqrt(norm);growth[s/reset_steps-1]=log(norm/epsilon);
            for(int j=0;j<m;j++)a[m+j]=a[j]+(a[m+j]-a[j])*epsilon/norm;
        }
    }
    free(work);free(noise);return 0;
}
