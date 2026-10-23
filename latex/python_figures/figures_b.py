"""Recreate Ufimtsev figures 24--46 as editable vector artwork.

Run this file offline after installing numpy, scipy, matplotlib and Pillow.
Theoretical plots evaluate the numbered book formulas. Experimental curves
are explicitly identified as manually digitized visual estimates, not data
reported numerically by Ufimtsev. The source bitmap is never embedded.
"""
from __future__ import annotations
import argparse
from common import np, plt, canvas, aspect, arrow, label, finish
from matplotlib.patches import Polygon, Rectangle
from matplotlib.ticker import MultipleLocator, FuncFormatter
from scipy.special import jv
from scipy.interpolate import PchipInterpolator

STEMS = {
 24:'b-0091-fig24',25:'b-0104-fig25',26:'b-0104-fig26',27:'b-0105-fig27',
 28:'b-0109-fig28',29:'b-0109-fig29',30:'b-0111-fig30',31:'b-0116-fig31',
 32:'b-0117-fig32',33:'b-0117-fig33',34:'b-0118-fig34',35:'b-0118-fig35',
 36:'b-0121-fig36',37:'b-0122-fig37',38:'b-0123-fig38',39:'b-0124-fig39',
 40:'b-0125-fig40',41:'b-0126-fig41',42:'b-0126-fig42',43:'b-0128-fig43',
 44:'b-0128-fig44',45:'b-0133-fig45',46:'b-0135-fig46'}


class Drawing:
    def __init__(self, number):
        self.number=number; self.stem=STEMS[number]
        self.fig,self.ax=canvas(self.stem)
        self.r=aspect(self.stem)
    def xy(self,p): return (p[0],p[1]*self.r)
    def line(self,points,**kw):
        p=np.asarray([self.xy(t) for t in points])
        self.ax.plot(p[:,0],p[:,1],color='black',lw=kw.pop('lw',1.45),**kw)
    def ray(self,a,b,**kw): return arrow(self.ax,self.xy(a),self.xy(b),**kw)
    def text(self,p,s,**kw): return label(self.ax,*self.xy(p),s,fontsize=kw.pop('fontsize',11),**kw)
    def dot(self,p): self.ax.plot(*self.xy(p),'ko',ms=2.3)
    def arc(self,c,r,start,end,txt=None,label_angle=None,arrowhead=False):
        t=np.deg2rad(np.linspace(start,end,70)); center=np.asarray(self.xy(c))
        p=center[:,None]+r*np.array([np.cos(t),np.sin(t)])
        self.ax.plot(p[0],p[1],color='black',lw=.8)
        if arrowhead: arrow(self.ax,p[:,-5],p[:,-1],lw=.8)
        if txt:
            a=np.deg2rad((start+end)/2 if label_angle is None else label_angle)
            label(self.ax,*(center+1.3*r*np.array([np.cos(a),np.sin(a)])),txt,fontsize=11)
    def dim(self,a,b,s,offset=(0,0)):
        self.ray(a,b,style='<->',lw=.7)
        mid=((a[0]+b[0])/2+offset[0],(a[1]+b[1])/2+offset[1])
        self.text(mid,s,fontsize=10,bbox=dict(facecolor='white',edgecolor='none',pad=.6))
    def axes(self,o=(.1,.15),right=(.94,.15),top=(.1,.94),x=r'$z$',y=r'$y$'):
        self.ray(o,right);self.ray(o,top)
        self.text((right[0]+.02,right[1]),x);self.text((top[0]-.025,top[1]),y)
    def save(self,desc,details=None):
        return finish(self.fig,self.stem,figure=self.number,method='vector schematic',
                      description=desc,details=details or {'construction':'Independently redrawn paths, dimension arrows, angle arcs and editable labels from the source figure.'})


def fig24():
    d=Drawing(24);o=(.48,.49)
    d.line([(.10,.23),(.83,.23),(.83,.77),(.10,.77),(.10,.23)])
    d.axes(o,(.94,.49),(.48,.96))
    d.ray(o,(.74,.67),lw=1.5);d.text((.77,.70),r'$\mathbf{n}$')
    d.ray(o,(.22,.08),lw=1.4)
    d.arc(o,.16,0,28,r'$\gamma$',arrowhead=True)
    d.arc(o,.12,-130,0,r'$\vartheta$',label_angle=-75,arrowhead=True)
    for p,s in [((.075,.79),'1'),((.075,.19),'2'),((.85,.19),'3')]:d.text(p,s)
    d.save('Finite cylinder, source normal, observation angle and the three luminous edge points.')


def fig28():
    d=Drawing(28);o=(.10,.50);a=(.64,.82);b=(.89,.50);c=(.64,.18)
    d.line([o,a,b,c,o]);d.axes(o,(.97,.50),(.10,.97))
    d.line([a,(.84,.94)],lw=.9);d.line([a,(.86,.82)],ls='--',lw=.7)
    d.dim((.64,.50),a,r'$a$',(.015,0))
    d.line([(.10,.50),(.10,.06),(.64,.06),c],lw=.7)
    d.dim((.10,.06),(.64,.06),r'$l$')
    d.dim((.10,.44),(.64,.12),r'$l_1$',(0,-.025))
    d.dim((.69,.14),(.94,.46),r'$l_2$',(.025,0))
    d.arc(o,.13,0,21.7,r'$\omega$')
    d.arc(a,.10,0,21.7,r'$\omega$',label_angle=15)
    d.arc(a,.09,-40,0,r'$\Omega$',label_angle=-25)
    d.save('Conical body: axial length, both slant lengths, rim radius and illuminated/shadowed face angles.')


def fig29():
    d=Drawing(29);a=(.62,.83);left=(.08,.12);right=(.92,.12)
    pts=np.asarray([d.xy(p) for p in [left,a,right,(.92,.03),(.08,.03)]])
    d.ax.add_patch(Polygon(pts,closed=True,facecolor='white',edgecolor='none',hatch='////',lw=.4))
    d.line([left,a,right]);d.ray((.05,.34),(.96,.34));d.text((.98,.34),r'$z$')
    p=(.06,.61);d.line([p,a],lw=1.1);d.dot(p);d.text((.04,.66),r'$P$');d.text((.34,.78),r'$r_1$')
    d.arc(a,.12,189.7,209.9,r'$\phi_1$',label_angle=197)
    d.arc((.25,.34),.11,0,29.9,r'$\omega$')
    d.save('Local dihedral wedge, observation ray and local cylindrical angle; hatching restored from the clearer GWU scan.')


def fig30():
    d=Drawing(30);o=(.13,.12);R=.58;cp=np.asarray(d.xy(o))
    th=np.linspace(0,np.pi/2,120);d.ax.plot(cp[0]+R*np.cos(th),cp[1]+R*np.sin(th),'k',lw=1.1)
    d.axes(o,(.96,.12),(.13,.97),x=r'$x$')
    p=cp+R/np.sqrt(2)*np.array([1,1]);q=cp+.82/np.sqrt(2)*np.array([1,1])
    arrow(d.ax,cp,q,lw=1.5);label(d.ax,q[0]+.02,q[1],r'$\mathbf{e}_{\phi_1}\ (\vartheta=\pi)$',ha='left',fontsize=9)
    arrow(d.ax,p-.03,p-.18,lw=1.2)
    label(d.ax,p[0]-.13,p[1]-.17,r'$\mathbf{e}_{\phi_1}\ (\vartheta=0)$',ha='center',fontsize=9)
    t=p+.19*np.array([1,-1]);arrow(d.ax,p,t,lw=1.4)
    label(d.ax,t[0]+.025,t[1],r'$\mathbf{e}_{z_1}$',ha='left',fontsize=11)
    d.arc(o,.13,0,45,r'$\psi$',arrowhead=True);d.text((.10,.095),r'$O$')
    d.save('Relative orientation of the local unit vectors for forward and backward observation.')


def fig34():
    d=Drawing(34);d.axes((.10,.16),(.94,.16),(.10,.95))
    d.line([(.10,.16),(.22,.67),(.70,.79),(.73,.43)])
    d.line([(.22,.67),(.27,.89)],ls='--',lw=.7)
    d.line([(.22,.67),(.36,.67)],ls='--',lw=.6)
    d.line([(.22,.16),(.22,.67)],ls='--',lw=.7)
    d.line([(.70,.16),(.70,.79)],lw=.8)
    d.line([(.70,.79),(.90,.79)],ls='--',lw=.7)
    d.line([(.70,.79),(.89,.835)],lw=.8)
    d.dim((.22,.16),(.22,.67),r'$a_1$',(.025,0))
    d.dim((.89,.16),(.89,.79),r'$a_2$')
    d.dim((.10,.07),(.22,.07),r'$l_1$');d.dim((.22,.07),(.70,.07),r'$l_2$')
    d.line([(.10,.16),(.10,.05)],lw=.6);d.line([(.22,.16),(.22,.05)],lw=.6);d.line([(.70,.16),(.70,.05)],lw=.6)
    d.arc((.22,.67),.065,0,69,r'$\omega$',label_angle=50)
    d.arc((.70,.79),.14,0,8,r'$\omega_1$',label_angle=9)
    d.arc((.70,.79),.08,-80,0,r'$\Omega$',label_angle=-50)
    d.save('Composite conical generatrix with two axial intervals, radii and discontinuity angles.')


def fig35():
    d=Drawing(35);d.axes((.10,.18),(.95,.18),(.10,.95))
    d.line([(.30,.18),(.30,.64),(.72,.82),(.72,.18)])
    d.dim((.23,.18),(.23,.64),r'$a_1$');d.dim((.83,.18),(.83,.82),r'$a_2$')
    d.line([(.23,.64),(.42,.64)],ls='--',lw=.7);d.line([(.72,.82),(.86,.82)],lw=.7)
    d.dim((.10,.08),(.30,.08),r'$l_1$');d.dim((.30,.08),(.72,.08),r'$l_2$')
    d.line([(.30,.18),(.30,.06)],lw=.6);d.line([(.72,.18),(.72,.06)],lw=.6)
    d.arc((.30,.64),.19,0,14.6,r'$\omega_1$',label_angle=16)
    d.save('Truncated conical surface and its two radii and axial intervals.')


def fig36():
    d=Drawing(36);d.axes((.10,.50),(.81,.50),(.10,.95))
    t=np.linspace(0,1,160);x=.10+.54*t*t;y=.50+.32*t
    d.line(list(zip(x,y)));d.line(list(zip(x,1-y)))
    d.line([(.64,.82),(.75,.64)]);d.line([(.64,.18),(.75,.36)])
    d.line([(.64,.82),(.88,.82)],ls='--',lw=.7);d.line([(.64,.18),(.88,.18)],ls='--',lw=.7)
    d.line([(.64,.82),(.79,.865)],lw=.8)
    d.dim((.89,.18),(.89,.82),r'$2a$')
    d.line([(.10,.50),(.10,.08),(.64,.08),(.64,.18)],lw=.7);d.dim((.10,.08),(.64,.08),r'$l$')
    d.arc((.64,.82),.11,0,13.1,r'$\omega$',label_angle=23);d.arc((.64,.82),.09,-51.8,0,r'$\Omega$',label_angle=-32)
    d.save('Paraboloid illuminated along its symmetry axis, including rim angles and dimensions.')


def fig40():
    d=Drawing(40);d.axes((.10,.18),(.94,.18),(.10,.96))
    t=np.linspace(0,1,150);x=.25+.46*t;y=.55+.28*(1-np.exp(-1.6*t))/(1-np.exp(-1.6))
    d.line(list(zip(x,y)));d.line([(.25,.18),(.25,.55)],ls='--',lw=.8);d.line([(.71,.18),(.71,.83)],lw=.8)
    d.dim((.25,.18),(.25,.55),r'$a_1$');d.dim((.71,.18),(.71,.83),r'$a_2$')
    d.line([(.20,.50),(.42,.80)],lw=.8);d.line([(.19,.55),(.41,.55)],lw=.7)
    d.line([(.71,.83),(.92,.91)],lw=.8);d.line([(.71,.83),(.92,.83)],lw=.7)
    d.arc((.25,.55),.11,0,44,r'$\omega_1$',label_angle=30)
    d.arc((.71,.83),.16,0,16,r'$\omega_2$',label_angle=18)
    d.line([(.10,.18),(.10,.07)],lw=.6);d.line([(.25,.18),(.25,.07)],lw=.6);d.line([(.71,.18),(.71,.07)],lw=.6)
    d.dim((.10,.08),(.25,.08),r'$l_1$');d.dim((.25,.08),(.71,.08),r'$l_2$')
    d.save('Truncated paraboloid generatrix: radii, tangents and axial lengths.')


def fig41():
    d=Drawing(41);d.axes((.11,.46),(.95,.46),(.11,.96))
    x=np.linspace(.25,.41,100);s=(x-.25)/.16;top=.73+.09*np.sin(s*np.pi/2)
    d.line(list(zip(x,top)));d.line(list(zip(x,.92-top)))
    d.line([(.25,.73),(.25,.19)]);d.line([(.41,.82),(.41,.10)])
    d.line([(.21,.68),(.43,.94)],lw=.8);d.line([(.35,.81),(.60,.89)],lw=.8)
    d.line([(.25,.73),(.38,.73)],lw=.65);d.line([(.41,.82),(.67,.82)],lw=.65)
    d.dim((.32,.46),(.32,.73),r'$a_1$');d.dim((.67,.46),(.67,.82),r'$a_2$')
    d.line([(.41,.82),(.49,.46)],lw=.9);d.text((.46,.66),r'$\rho$');d.dot((.49,.46));d.text((.51,.48),r'$O$')
    d.arc((.25,.73),.07,0,45,r'$\omega_1$',label_angle=27);d.arc((.41,.82),.12,0,15,r'$\omega_2$',label_angle=20)
    d.dim((.11,.36),(.25,.36),r'$l_1$');d.dim((.25,.36),(.41,.36),r'$l_2$')
    d.save('Spherical ring between two cutting planes, tangents, normal radius and axial dimensions.')


def fig42():
    d=Drawing(42);d.axes((.14,.51),(.94,.51),(.14,.95))
    t=np.linspace(0,1,150);x=.14+.28*t*t;y=.51+.33*t
    d.line(list(zip(x,y)));d.line(list(zip(x,1.02-y)))
    d.line([(.42,.84),(.55,.65)]);d.line([(.42,.18),(.55,.37)])
    d.line([(.42,.84),(.59,.88)],lw=.9);d.line([(.42,.84),(.59,.84)],lw=.7)
    d.dim((.42,.51),(.42,.84),r'$a$')
    d.line([(.14,.51),(.14,.09),(.42,.09),(.42,.18)],lw=.7);d.dim((.14,.09),(.42,.09),r'$l$')
    d.arc((.42,.84),.10,0,14.2,r'$\omega$',label_angle=30);d.arc((.42,.84),.10,-57.6,0,r'$\Omega$',label_angle=-30)
    d.save('Spherical segment with conical base, rim radius, length and two edge angles.')


def fig45():
    d=Drawing(45);o=(.18,.39)
    d.line([(.18,.07),(.18,.94)],lw=1.8);d.ray((.18,.90),(.18,.98));d.text((.14,.96),r'$y$')
    d.ray(o,(.95,.39));d.text((.96,.36),r'$x$')
    d.ray(o,(.69,.57),lw=1.5);d.text((.72,.59),r'$\mathbf{n}$')
    d.ray(o,(.81,.94),lw=1.5);d.text((.84,.95),r'$P$');d.text((.50,.75),r'$r$')
    d.arc(o,.26,0,24.8,r'$\alpha$',label_angle=12,arrowhead=True)
    d.arc(o,.19,0,48.8,r'$\varphi$',label_angle=45,arrowhead=True)
    d.text((.12,.76),r'$a$');d.text((.11,.08),r'$-a$')
    d.save('Strip cross-section, incident normal and observation direction.')


def fig46():
    d=Drawing(46);p=(.05,.92);o=(.43,.27);q=(.91,.52);q0=(.91,.27);qs=(.91,.055)
    for target in [o,q,q0,qs]: d.line([p,target],lw=.95)
    d.line([o,q],lw=1.4);d.line([o,qs],lw=1.1);d.line([o,(.97,.27)],lw=1.6)
    d.line([q,qs],ls='--',lw=.8)
    for pt,name,off in [(p,r'$P$',(-.01,.045)),(o,r'$O$',(-.03,-.035)),(q,r'$Q$',(.02,.03)),(q0,r'$Q_0$',(.03,-.02)),(qs,r'$Q^*$',(.03,-.015))]:
        d.dot(pt);d.text((pt[0]+off[0],pt[1]+off[1]),name,fontsize=10)
    d.text((.24,.57),r'$R$');d.text((.72,.67),r'$R_1$');d.text((.49,.61),r'$R_0$');d.text((.36,.60),r'$R_2$')
    d.text((.68,.45),r'$d$');d.text((.94,.40),r'$h$')
    d.arc(o,.13,0,21,r"$\varphi'$")
    d.arc(o,.16,21,128,r"$\varphi''$",label_angle=95)
    d.arc(q0,.16,154,180,r'$\varphi$',label_angle=156)
    d.save('Diffraction by a half-plane: source, image source, observer, four propagation distances and local angles.')


def db(s): return 10*np.log10(np.maximum(np.asarray(s),1e-20))


def wedge(omega,Omega):
    n=1+(omega+Omega)/np.pi
    return (2/n)*np.sin(np.pi/n)/(np.cos(np.pi/n)-np.cos(2*omega/n))


def cone(a,l,Omega=np.pi/2,k=np.pi):
    a=np.asarray(a);l=np.asarray(l);om=np.arctan2(a,np.maximum(l,1e-7))
    t=np.tan(om);ph=np.exp(2j*k*l)
    first=t*t/(k*a)*np.sin(k*l)*np.exp(1j*k*l)
    s=first+wedge(om,Omega)*ph;s0=first-t*ph
    return np.pi*a*a*abs(s)**2,np.pi*a*a*abs(s0)**2


def paraboloid(a,l,Omega=np.pi/2,k=np.pi):
    a=np.asarray(a);l=np.asarray(l);om=np.arctan2(a,2*np.maximum(l,1e-7))
    t=np.tan(om);ph=np.exp(2j*k*l)
    s=t*(1-ph)+(wedge(om,Omega)+t)*ph
    return np.pi*a*a*abs(s)**2,np.pi*a*a*abs(t*(1-ph))**2


def sphere(a,l,Omega=np.pi/12,k=np.pi):
    l=np.asarray(l);om=np.pi/2-2*np.arctan(l/a)
    ph=np.exp(2j*k*l);sec=1/np.cos(om);t=np.tan(om)
    s=sec+wedge(om,Omega)*ph;s0=sec-t*ph
    return np.pi*a*a*abs(s)**2,np.pi*a*a*abs(s0)**2


def cylinder(theta,kind='E',ka=np.pi,kl=10*np.pi):
    t=np.deg2rad(theta);n=1.5;fac=np.sin(np.pi/n)/n;C=np.cos(np.pi/n)
    a=1/(C-np.cos((np.pi-2*t)/n));b=1/(C-np.cos(2*t/n));c=1/(C-np.cos((np.pi+2*t)/n))
    sign=-1 if kind=='E' else 1
    M=fac*sign*(a-b);N=fac*(2/(C-1)+sign*(a+b));f3=fac*(1/(C-1)+sign*c)
    z=2*ka*np.sin(t);j1=jv(1,z);j2=jv(2,z)
    S=(M*j1+1j*N*j2)*np.exp(1j*kl*np.cos(t))-f3*(j1-1j*j2)*np.exp(-1j*kl*np.cos(t))
    return abs(S)**2


def cylinder_po(theta,ka=np.pi,kl=10*np.pi):
    t=np.deg2rad(theta);z=2*ka*np.sin(t)
    # Printed Figure27 has the monotone asymptotic envelope of13.25.
    # Its caption cites13.26, whose exact Bessel envelope has an extra dip.
    # sin(kl cos(theta))/cos(theta) is evaluated stably through sinc.
    return np.sin(t)/(np.pi*ka)*(kl*np.sinc(kl*np.cos(t)/np.pi))**2


def graph(num,xlim,ylim,xticks,yticks,*,minor=None,right=False,zero=False,xlabel=r'$l$',ylabel=r'$10\lg\sigma$'):
    stem=STEMS[num];fig,ax=canvas(stem,plot=True)
    ax.set_position([.11,.10,.80,.84] if right else [.13,.11,.83,.83])
    ax.set_xlim(*xlim);ax.set_ylim(*ylim);ax.set_xticks(xticks)
    ax.set_yticks([v for v in yticks if ylim[0]<=v<=ylim[1]])
    ax.grid(True,color='.35',lw=.6)
    if minor:
        ax.xaxis.set_minor_locator(MultipleLocator(minor[0]));ax.yaxis.set_minor_locator(MultipleLocator(minor[1]));ax.grid(which='minor',color='.70',lw=.3)
    if right: ax.yaxis.tick_right();ax.tick_params(axis='y',labelleft=False,labelright=True)
    ax.set_axisbelow(True);ax.tick_params(labelsize=9,pad=4,length=3)
    if zero:
        ax.spines['bottom'].set_position(('data',0));ax.add_patch(Rectangle((min(xlim),ylim[0]),abs(xlim[1]-xlim[0]),ylim[1]-ylim[0],fill=False,lw=.7,color='black',clip_on=False))
        ax.text(.02,(0-ylim[0])/(ylim[1]-ylim[0])-.04,xlabel,transform=ax.transAxes,ha='left',va='top',fontsize=11)
    else: ax.set_xlabel(xlabel,loc='right',labelpad=3)
    ax.text(1.02 if right else -.09,1.015,ylabel,transform=ax.transAxes,ha='right' if right else 'left',va='bottom',fontsize=10)
    return fig,ax


# Hand-selected points on the dashed experimental curves; axes calibrated from
# the original frame and zero-dB line. PCHIP only interpolates these controls.
EXPERIMENT = {
25: [(90,20),(91.5,17.3),(93,10),(94.3,-5.8),(95.7,9.7),(97.7,-7.0),(99.5,5.8),(102.0,-8.8),(104.0,2.7),(106.2,-9.0),(108.5,.0),(111.0,-9.0),(113.8,-2.5),(116.5,-9.0),(119.8,-4.0),(123,-9.0),(127,-4.5),(131.0,-9.0),(135,-4.6),(140,-8.0),(145,-3.1),(150,2.2),(155,7.0),(160,9.1),(165,9.7),(170,9.9),(175,10),(180,10)],
26: [(90,20),(91.6,16.5),(93,6),(94.2,-7),(95.8,6.8),(98,-7.8),(100,2.6),(103,-8.8),(105.5,1.0),(108,-10),(111,-.2),(114,-8),(117,-1.5),(120,-11),(123,-1.3),(126,-11),(130,-3),(134,-12),(138,-3.5),(142,-8.0),(146,2.0),(149,-1),(153,4.0),(157,9.1),(161,10.1),(166,9.4),(171,8.8),(176,9.1),(180,10)]}


def cylinders():
    th=np.linspace(90.0001,179.9999,12001)
    for num,kind,ylim in [(25,'E',(-9,22)),(26,'H',(-12,21))]:
        fig,ax=graph(num,(180,90),ylim,[180,160,140,120,100,90],np.arange(-10,21,5),minor=(3,1),right=True,zero=True,xlabel=r'$\vartheta$',ylabel=rf'$10\lg\,\sigma_{kind}/(\pi a^2)$')
        ax.xaxis.set_major_formatter(FuncFormatter(lambda x,p:f'{x:g}°'))
        ax.plot(th,db(cylinder(th,kind)),'k-',lw=1.6,label='theoretical')
        controls=np.asarray(EXPERIMENT[num]);x=np.linspace(90,180,3000);y=PchipInterpolator(controls[:,0],controls[:,1])(x)
        ax.plot(x,y,'k--',lw=1.15,label='experimental')
        ax.legend(loc='upper left',bbox_to_anchor=(.03,.83),frameon=True,facecolor='white',edgecolor='none',fontsize=10)
        ax.text(.48,.56,r'$ka=\pi$'+'\n'+r'$kl=10\pi$',transform=ax.transAxes,fontsize=10,bbox=dict(facecolor='white',edgecolor='none',pad=3))
        finish(fig,STEMS[num],figure=num,method='mixed: formula and manually digitized experiment',description=f'Finite-cylinder radar scattering, {kind}-polarization.',equations=['15.02','15.04','15.05','15.08' if kind=='E' else '15.09'],details={'ka':'pi','kl':'10*pi','theory':'direct Bessel-function evaluation','experimental_control_points_theta_deg_dB':controls.tolist(),'experimental_uncertainty':'Visual estimates from a damaged print; approximately 1–2 dB, larger in narrow minima. No original numerical measurement table exists in the supplied book.'})
    fig,ax=graph(27,(180,90),(-25,20),[180,160,140,120,100,90],range(-25,21,5),minor=(3,1),right=True,zero=True,xlabel=r'$\vartheta$',ylabel=r'$10\lg\,\sigma^0/(\pi a^2)$')
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x,p:f'{x:g}°'));ax.plot(th,db(cylinder_po(th)),'k-',lw=1.5)
    ax.text(.13,.85,r'$ka=\pi$'+'\n'+r'$kl=10\pi$',transform=ax.transAxes,bbox=dict(facecolor='white',edgecolor='none',pad=4))
    finish(fig,STEMS[27],figure=27,method='formula',description='Physical-optics scattering by the cylindrical lateral surface.',equations=['13.25','13.23'],details={'ka':'pi','kl':'10*pi','normalization':'sigma/(pi*a^2)','source_discrepancy':'Original caption cites interpolation13.26. The printed monotonically rising lobe envelope instead matches asymptotic13.25, evaluated here. Direct13.26 produces a Bessel-envelope dip near140 degrees absent from the original plot. Original book caption is preserved.'})


def cones():
    l=np.linspace(.05,20,2500);om=np.deg2rad(10+25/60);a=l*np.tan(om);s,s0=cone(a,l)
    fig,ax=graph(31,(0,20),(-20,20),[0,5,10,15,20],range(-20,21,5),zero=True)
    ax.plot(l,db(s),'k-',label=r'$10\lg\sigma$');ax.plot(l,db(s0),'k--',label=r'$10\lg\sigma^0$')
    # Small crosses read from the source, kept as independent approximate data.
    mx=np.array([4.0,6.1,10.0,15.0]);my=np.array([.0,5.1,8.4,12.0]);ax.plot(mx,my,'kx',ms=4,ls='none')
    ax.text(.33,.77,r'$k=\pi$'+'\n'+r'$\omega=10^\circ25^\prime$',transform=ax.transAxes,fontsize=10)
    ax.text(15.5,14.2,r'$10\lg\sigma$');ax.text(11,-5.5,r'$10\lg\sigma^0$')
    finish(fig,STEMS[31],figure=31,method='mixed: formula and manually digitized experiment',description='Finite cone effective scattering area versus length.',equations=['17.08','17.09','17.13'],details={'k':'pi','omega_degrees':10+25/60,'Omega_degrees':90,'a':'l*tan(omega)','normalization':'sigma=pi*a^2*|Sigma|^2; dimensionally consistent factor from17.13, rather than missing square in17.06','experimental_points_l_dB':list(zip(mx.tolist(),my.tolist()))})
    omdeg=np.linspace(.12,89.999,4000);a=2.75;l=a/np.tan(np.deg2rad(omdeg));s,s0=cone(a,l)
    fig,ax=graph(32,(0,90),(-30,38),range(0,91,10),range(-30,36,5),xlabel=r'$\omega$')
    ax.plot(omdeg,db(s),'k-',lw=1.5);ax.plot(omdeg,db(s0),'k--',lw=1.2)
    mx=np.array([10,20,30,35,45,55,60,70,80]);my=np.array([11.8,12.1,13.9,14.4,16.3,17.0,19.0,21.7,27.5]);ax.plot(mx,my,'kx',ls='none',ms=5)
    ax.text(.45,.91,r'$ka=2.75\pi$',transform=ax.transAxes);ax.text(40,16,r'$10\lg\sigma$');ax.text(43,10,r'$10\lg\sigma^0$')
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x,p:f'{x:g}°'))
    finish(fig,STEMS[32],figure=32,method='mixed: formula and manually digitized experiment',description='Finite cone deformed into a disk at fixed base radius.',equations=['17.08','17.09','17.10'],details={'ka':'2.75*pi','k':'pi','a':2.75,'Omega_degrees':90,'l':'a*cot(omega)','experimental_points_omega_deg_dB':list(zip(mx.tolist(),my.tolist()))})
    Omega=np.deg2rad(np.linspace(.001,170,2500));om=np.deg2rad(10);a=10*np.tan(om);s,s0=cone(a,10,Omega)
    fig,ax=graph(33,(0,180),(-8,11),range(0,181,30),[-5,0,5,10],minor=(10,1),xlabel=r'$\Omega$')
    ax.plot(np.rad2deg(Omega),db(s),'k-',lw=1.7);ax.plot(np.rad2deg(Omega),np.full(Omega.shape,db(s0)),'k--',lw=1.2)
    ax.text(.56,.55,r'$kl=10\pi$'+'\n'+r'$\omega=10^\circ$',transform=ax.transAxes)
    ax.text(138,9.2,r'$10\lg\sigma$');ax.text(135,-4.4,r'$10\lg\sigma^0$')
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x,p:f'{x:g}°'))
    sec=ax.secondary_xaxis('top',functions=(lambda x:1+(x+10)/180,lambda n:(n-1)*180-10));sec.set_xticks(np.arange(1.1,2.01,.1));sec.set_xlabel(r'$n$',loc='right',labelpad=2);sec.tick_params(labelsize=8)
    finish(fig,STEMS[33],figure=33,method='formula',description='Cone scattering versus shape of the shadowed face.',equations=['17.08','17.09','17.04'],details={'omega_degrees':10,'kl':'10*pi','k':'pi','Omega_range_degrees':[0,170],'upper_axis':'n=1+(omega+Omega)/pi'})


def paraboloids():
    l=np.linspace(.025,20,7000);a=.2*l;s,s0=paraboloid(a,l)
    fig,ax=graph(37,(0,20),(-40,20),np.arange(0,20.1,2.5),range(-40,21,10),zero=True)
    ax.plot(l,db(s),'k-',lw=1.6,label=r'$10\lg\sigma$');ax.plot(l,db(s0),'k--',lw=1.15,label=r'$10\lg\sigma^0$');ax.legend(loc='upper left',frameon=False)
    ax.text(.21,.88,r'$k=\pi$'+'\n'+r'$a=0.2l$',transform=ax.transAxes)
    finish(fig,STEMS[37],figure=37,method='formula',description='Paraboloid scattering versus length with fixed rim angle.',equations=['18.04','18.06'],details={'k':'pi','Omega_degrees':90,'tan(omega)':.1,'a':'0.2*l'})
    l=np.linspace(.0001,15,7000);s,s0=paraboloid(3,l)
    fig,ax=graph(38,(0,15),(-10,35),np.arange(0,15.1,2.5),range(-10,36,5))
    ax.plot(l,db(s),'k-',lw=1.6,label=r'$10\lg\sigma$');ax.plot(l,db(s0),'k--',lw=1.15,label=r'$10\lg\sigma^0$');ax.legend(loc='upper center',bbox_to_anchor=(.36,.99),frameon=False)
    ax.text(.60,.92,r'$a=3,\quad k=\pi$'+'\n'+r'$l=\frac{a}{2}\cot\omega$',transform=ax.transAxes,fontsize=10)
    # Second coordinate read from the original: omega decreases as l increases.
    vals=np.array([45,30,20,15,10,8,7,6]);pos=1.5/np.tan(np.deg2rad(vals))
    for x,v in zip(pos,vals):
        if x<=15:ax.text(x,-9.45,f'{v}°',ha='center',va='bottom',fontsize=8)
    ax.text(.98,.025,r'$\omega$',transform=ax.transAxes,ha='right',fontsize=9)
    finish(fig,STEMS[38],figure=38,method='formula',description='Paraboloid of fixed base radius, varying height and rim angle.',equations=['18.04','18.06','18.05'],details={'k':'pi','a':3,'Omega_degrees':90,'omega':'atan(a/(2*l))'})
    O=np.linspace(.01,174.2,3000);s,_=paraboloid(2,10,np.deg2rad(O))
    fig,ax=graph(39,(0,180),(-40,10),range(0,181,40),range(-40,11,10),xlabel=r'$\Omega$')
    ax.plot(O,db(s),'k-',lw=1.8)
    ax.text(.43,.44,r'$ka=2\pi,\quad kl=10\pi$'+'\n'+r'$\tan\omega=0.1$'+'\n'+r'$k=\pi$',transform=ax.transAxes,fontsize=10)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x,p:f'{x:g}°'))
    finish(fig,STEMS[39],figure=39,method='formula',description='Paraboloid scattering versus the shadowed-face angle.',equations=['18.04'],details={'ka':'2*pi','kl':'10*pi','tan(omega)':.1,'k':'pi'})


def spherical_plots():
    a=2.75;l=np.linspace(.0001,2.75,4000);s,s0=sphere(a,l)
    fig,ax=graph(43,(0,3),(0,35),np.arange(0,3.01,.5),range(0,36,5))
    ax.plot(l,db(s),'k-',lw=1.6,label=r'$10\lg\sigma$');ax.plot(l,db(s0),'k--',lw=1.2,label=r'$10\lg\sigma^0$');ax.legend(loc='upper right',bbox_to_anchor=(1,.82),frameon=False)
    ax.text(.55,.91,r'$ka=2.75\pi$'+'\n'+r'$\Omega=15^\circ$',transform=ax.transAxes,fontsize=10)
    finish(fig,STEMS[43],figure=43,method='formula',description='Spherical segment scattering at fixed base radius.',equations=['19.12','19.13'],details={'a':2.75,'ka':'2.75*pi','k':'pi','Omega_degrees':15,'omega':'pi/2-2*atan(l/a)'})
    lc=np.linspace(.0001,3.35,4000);sc,_=cone(a,lc,np.pi/12)
    fig,ax=graph(44,(0,3.5),(0,35),np.arange(0,3.51,.5),range(0,36,5))
    ax.plot(l,db(s),'k-',lw=1.7,label='spherical segment');ax.plot(lc,db(sc),'k--',lw=1.15,label='cone')
    ax.text(.36,.91,r'$ka=2.75\pi$'+'\n'+r'$\Omega=15^\circ$',transform=ax.transAxes,fontsize=10)
    finish(fig,STEMS[44],figure=44,method='formula',description='Spherical-segment and cone scattering for the same base dimensions and shadow angle.',equations=['19.12','17.08'],details={'a':2.75,'ka':'2.75*pi','k':'pi','Omega_degrees':15,'solid':'spherical segment','dashed':'cone'})


SCHEMATICS=[fig24,fig28,fig29,fig30,fig34,fig35,fig36,fig40,fig41,fig42,fig45,fig46]


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--only',choices=['schematics','graphs','all'],default='all');args=ap.parse_args()
    if args.only in ['schematics','all']:
        for f in SCHEMATICS:f()
    if args.only in ['graphs','all']:
        cylinders();cones();paraboloids();spherical_plots()


if __name__=='__main__':main()
