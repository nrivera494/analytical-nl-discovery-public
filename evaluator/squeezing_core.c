/* gpt-b / gpt-6-astra / gpt, 2026-10-18. Independent tangent and snapshot extension.
   Reuses only our previous Hamiltonian, noise generators and RK4 implementation. */
#include "thermalized_light_core.c"

/* Nested bridges share the original .02 root and every coarser path.
   Level zero preserves the previously used .02/.01 bridge seed exactly. */
static void sq_noise(int count,int step,int refinement,RNG *parent,RNG *bridges,
                     double *draws,double *block) {
    int sub=(step-1)%refinement;
    if(sub==0)for(int j=0;j<count;j++) {
        double values[32];values[0]=normal(parent);int width=1,level=0;
        while(width<refinement) {
            for(int k=width-1;k>=0;k--) {
                double d=normal(bridges+level),v=values[k];
                values[2*k]=(v+d)/sqrt(2.);values[2*k+1]=(v-d)/sqrt(2.);
            }
            width*=2;level++;
        }
        for(int k=0;k<refinement;k++)block[k*count+j]=values[k];
    }
    memcpy(draws,block+sub*count,count*sizeof(double));
}
static void sq_init_bridges(RNG *bridges,uint64_t seed) {
    for(int level=0;level<5;level++)init_rng(bridges+level,
        seed^UINT64_C(0x83a5c91f4bb2476d)^(UINT64_C(0x9e3779b97f4a7c15)*level));
}

static void tangent_force(const Model *md,const Z *x,Z *y,Z *work) {
    int m=md->m,np=md->np; const Z *a=x;
    Z *b=work,*v=b+np,*db=v+np,*dv=db+np;
    force(md,a,y,b,v);
    for(int col=0;col<2*m;col++) {
        const Z *d=x+(col+1)*m;Z *f=y+(col+1)*m;
        for(int j=0;j<np;j++)db[j]=d[md->p[j]]*a[md->q[j]]+a[md->p[j]]*d[md->q[j]];
        for(int j=0;j<np;j++) {dv[j]=0;for(int k=md->offset[j];k<md->offset[j+1];k++)dv[j]+=md->value[k]*db[md->column[k]];}
        for(int j=0;j<m;j++)f[j]=0;
        for(int j=0;j<np;j++) {
            int p=md->p[j],q=md->q[j];
            f[p]+=conj(d[q])*v[j]+conj(a[q])*dv[j];
            if(p!=q)f[q]+=conj(d[p])*v[j]+conj(a[p])*dv[j];
        }
        for(int j=0;j<m;j++)f[j]*=-I;
    }
}
static void tangent_rk4(const Model *md,Z *x,double h,Z *work) {
    int size=md->m*(1+2*md->m);
    Z *k1=work,*k2=k1+size,*k3=k2+size,*k4=k3+size,*tmp=k4+size,*scratch=tmp+size;
    tangent_force(md,x,k1,scratch);
    for(int j=0;j<size;j++)tmp[j]=x[j]+h*.5*k1[j];
    tangent_force(md,tmp,k2,scratch);
    for(int j=0;j<size;j++)tmp[j]=x[j]+h*.5*k2[j];
    tangent_force(md,tmp,k3,scratch);
    for(int j=0;j<size;j++)tmp[j]=x[j]+h*k3[j];
    tangent_force(md,tmp,k4,scratch);
    for(int j=0;j<size;j++)x[j]+=h/6*(k1[j]+2*k2[j]+2*k3[j]+k4[j]);
}
int sq_tangent(int m,int np,const int *p,const int *q,const int *offset,const int *column,
 const double *value,const int *group,Z *x,double dt,int steps,double sigma,uint64_t seed,
 int refinement,int nc,const int *checkpoints,Z *out) {
    Model md={m,np,p,q,offset,column,group,value,NULL,NULL};int batch=1+2*m,size=m*batch;
    Z *work=calloc(5*size+4*np,sizeof(Z));RNG rng,bridges[5];init_rng(&rng,seed);
    sq_init_bridges(bridges,seed);
    int count=noise_dimension(&md);double *noise=calloc((refinement+1)*count,sizeof(double));int cp=0;
    for(int s=0;s<=steps;s++) {
        if(cp<nc && s==checkpoints[cp]){memcpy(out+cp*size,x,size*sizeof(Z));cp++;}
        if(s==steps)break;
        if(sigma) {
            tangent_rk4(&md,x,dt/2,work);
            sq_noise(count,s+1,refinement,&rng,bridges,noise,noise+count);
            disorder_batch(&md,x,batch,sigma*sqrt(dt),noise);
            tangent_rk4(&md,x,dt/2,work);
        }else tangent_rk4(&md,x,dt,work);
    }
    free(work);free(noise);return cp;
}
static void loss_batch(Z *a,int size,double alpha,double h,double n,RNG *rng) {
    double eta=exp(-alpha*h),scale=sqrt((1-eta)/(4*n)),amp=sqrt(eta);
    for(int j=0;j<size;j++)a[j]=amp*a[j]+scale*(normal(rng)+I*normal(rng));
}
int sq_ensemble(int m,int np,const int *p,const int *q,const int *offset,const int *column,
 const double *value,const int *group,const Z *linear,Z *a,int batch,double dt,int steps,
 double sigma,uint64_t seed,int refinement,int nc,const int *checkpoints,Z *out,
 double alpha,double n,uint64_t loss_seed) {
    Model md={m,np,p,q,offset,column,group,value,NULL,linear};
    Z *work=calloc(8*m+2*np,sizeof(Z));RNG rng,bridges[5],loss;init_rng(&rng,seed);
    sq_init_bridges(bridges,seed);init_rng(&loss,loss_seed);
    int count=noise_dimension(&md);double *noise=calloc((refinement+1)*count,sizeof(double));int cp=0;
    for(int s=0;s<=steps;s++) {
        if(cp<nc && s==checkpoints[cp]){memcpy(out+cp*batch*m,a,batch*m*sizeof(Z));cp++;}
        if(s==steps)break;
        if(alpha>0)loss_batch(a,batch*m,alpha,dt/2,n,&loss);
        if(sigma) {
            for(int b=0;b<batch;b++)rk4(&md,a+b*m,dt/2,work);
            sq_noise(count,s+1,refinement,&rng,bridges,noise,noise+count);
            disorder_batch(&md,a,batch,sigma*sqrt(dt),noise);
            for(int b=0;b<batch;b++)rk4(&md,a+b*m,dt/2,work);
        }else for(int b=0;b<batch;b++)rk4(&md,a+b*m,dt,work);
        if(alpha>0)loss_batch(a,batch*m,alpha,dt/2,n,&loss);
    }
    free(work);free(noise);return cp;
}
