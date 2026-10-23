"""Numerical evaluation of Ufimtsev's thin-wire approximation, sections28,32,34.

Dimensionless arguments: x=kL, b=ka. Euler's gamma in this book is exp(C),
not the Euler-Mascheroni constant C itself. No curves are fitted here.
The direct resummed approximation is used in the ranges of Figures76–80.
It is not a uniform numerical approximation as kL approaches zero: cancellation
of higher-order inverse-log terms spoils the tiny static limit. Use static_F
(33.18) separately for that regime; do not extrapolate the plotted model there.
"""
from common import np
from scipy.special import sici

GAMMA=np.exp(np.euler_gamma)

def static_F(x,length_over_radius):
    """Leading broadside electrostatic approximation, Equation33.18."""
    return np.asarray(x,float)**3/(24*(np.log(2*length_over_radius)-7/3))

def E(y):
    """Equation28.24: Ci(y)+i[Si(y)-pi/2], y>0."""
    si,ci=sici(np.asarray(y,dtype=float))
    return ci+1j*(si-np.pi/2)

def psi(x,b,qfactor=1.):
    """Equation28.21 at z=L; qfactor=(1∓cos(theta))/2 for psi±."""
    x,b,qfactor=np.broadcast_arrays(np.asarray(x,float),np.asarray(b,float),np.asarray(qfactor,float))
    q=b*b
    qp=q*qfactor
    y=2*x*qfactor
    with np.errstate(divide='ignore',invalid='ignore'):
        value=np.log(-1/(GAMMA*GAMMA*qp)+0j)/(np.log(2j*x/(GAMMA*q))-E(y)*np.exp(-1j*y))
    return np.where(qfactor<1e-14,1.+0j,value)

def normal_F(x,b):
    """Equation32.08, including the continuation on the following page."""
    x,b=np.broadcast_arrays(np.asarray(x,float),np.asarray(b,float))
    p=psi(x,b)
    pb=psi(x,b,.5)
    t=np.log(2j/(GAMMA*b))
    t0=np.log(1j/(GAMMA*b))
    return (-x/(2*t)+x*pb**2*E(x)/(2*t*t)
            +1j/(t*t)*(t-.5+(.5*pb-2*np.log(np.sqrt(2)*1j/(GAMMA*b)))*pb*np.exp(1j*x)
            +2*pb**2*t0/(1+p*np.exp(1j*x))*np.exp(2j*x)))

def radar_F(theta,x,b):
    """Equation32.09 for theta0=theta, with the analytic theta=pi/2 limit."""
    theta=np.asarray(theta,float)
    ct,st=np.cos(theta),np.sin(theta)
    ch,sh=np.cos(theta/2),np.sin(theta/2)
    near=np.abs(ct)<1e-5
    endpoints=np.abs(st)<1e-7
    safe=np.where(near,np.pi/2+2e-5,np.where(endpoints,1e-6,theta))
    ct,st=np.cos(safe),np.sin(safe)
    ch,sh=np.cos(safe/2),np.sin(safe/2)
    p=psi(x,b)
    pp=psi(x,b,(1-ct)/2)
    pm=psi(x,b,(1+ct)/2)
    D=1-p*p*np.exp(2j*x)
    log0=np.log(1j/(GAMMA*b))
    # Coordinate origin is at the wire midpoint: kz1=-x/2, kz2=x/2.
    bracket=(ch**4*np.log(1j/(GAMMA*b*ch**2))*np.exp(1j*x*ct)
             -sh**4*np.log(1j/(GAMMA*b*sh**2))*np.exp(-1j*x*ct)
             +2*(sh**4*np.log(1j/(GAMMA*b*sh))*pm-ch**4*np.log(1j/(GAMMA*b*ch))*pp)*np.exp(1j*x)
             -2*ct/D*log0*p*pp*pm*np.exp(3j*x)
             +ct/D*log0*(pm**2*np.exp(1j*x*ct)+pp**2*np.exp(-1j*x*ct))*np.exp(2j*x))
    result=1j*bracket/(st*np.log(2j/(GAMMA*b*st)))**2/ct
    result=np.where(near,normal_F(x,b),result)
    return np.where(endpoints,0.+0j,result)

def sigma_normalized(theta,x,b):
    """Equation34.12: average radar area divided by wavelength squared."""
    return 3/(8*np.pi)*np.abs(radar_F(theta,x,b))**2

def integral_normalized(r,chi):
    """Equation34.07: S/L², alpha=0, normal incidence, chi=1/(2lnka)."""
    r=np.asarray(r,float)
    return np.imag(normal_F(2*np.pi*r,np.exp(1/(2*chi))))/(np.pi*r*r)

if __name__=='__main__':
    for chi in [-.05,-.1]:
        r=np.linspace(.1,3.,6000)
        y=integral_normalized(r,chi)
        print('chi',chi,'S/L² peak',float(y.max()),'at L/lambda',float(r[y.argmax()]))
    r=np.linspace(.1,2.5,6000)
    x=2*np.pi*r
    y=100*3/(8*np.pi)*np.abs(normal_F(x,2*x*np.exp(-7.5)))**2
    print('Fig77 first peak',float(y[r<.7].max()))
    for r0 in [.5,2.]:
        th=np.linspace(.001,np.pi-.001,4001)
        z=sigma_normalized(th,2*np.pi*r0,2*np.pi*r0/900)
        print('radar r',r0,'peak',float(z.max()),'angle',float(np.degrees(th[z.argmax()])))
