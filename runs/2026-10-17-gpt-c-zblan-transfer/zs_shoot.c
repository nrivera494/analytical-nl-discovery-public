/* agent gpt-c; model gpt-6-astra; family gpt.
 * Two-sided Evans determinant for the focusing Zakharov-Shabat system.
 * Exact transfer on each constant midpoint cell. No external solver code. */
#include <complex.h>
#include <math.h>
static void step(double complex q, double complex z, double h,
                 double complex *u, double complex *v) {
    double complex k=csqrt(z*z+creal(q*conj(q)));
    double complex a=ccos(k*h), b=cabs(k)<1e-14 ? h : csin(k*h)/k;
    double complex x=(a-I*z*b)*(*u)+b*q*(*v);
    double complex y=-b*conj(q)*(*u)+(a+I*z*b)*(*v);
    double norm=hypot(cabs(x),cabs(y));
    *u=x/norm; *v=y/norm;
}
void evans(int n, const double *qr, const double *qi, double h,
           double zr, double zi, double *out) {
    double complex z=zr+I*zi, a=1, b=0, c=0, d=1;
    int mid=n/2;
    for(int j=0;j<mid;j++) step(qr[j]+I*qi[j],z,h,&a,&b);
    for(int j=n-1;j>=mid;j--) step(qr[j]+I*qi[j],z,-h,&c,&d);
    double complex v=a*d-b*c;
    out[0]=creal(v); out[1]=cimag(v);
}
