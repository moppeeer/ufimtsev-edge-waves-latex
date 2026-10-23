"""Recreate Ufimtsev figures 47--72 as editable vector graphics.

Run offline: python figures_c.py [--only 47 48 ...]
Only common.aspect reads the old crop (to preserve the page canvas).
All axes, lettering, geometry and curves are independently drawn. Numerical
approximations use the book's equations. Published rigorous/experimental
comparisons are explicitly identified as manually digitized control points.
"""
from __future__ import annotations
import argparse
from common import canvas, aspect, arrow, label, finish, np, plt
from matplotlib.patches import Arc, Polygon
from matplotlib.ticker import MultipleLocator, FuncFormatter
from scipy.special import fresnel, jv
from scipy.interpolate import PchipInterpolator

STEMS={47:'c-0138-fig',48:'c-0150-fig',49:'c-0153-fig49',50:'c-0153-fig50',
51:'c-0154-fig51',52:'c-0155-fig52',53:'c-0155-fig53',54:'c-0156-fig54',
55:'c-0157-fig55',56:'c-0157-fig56',57:'c-0158-fig57',58:'c-0158-fig58',
59:'c-0158-fig59',60:'c-0159-fig60',61:'c-0159-fig61',62:'c-0160-fig62',
63:'c-0162-fig63',64:'c-0162-fig64',65:'c-0169-fig65',66:'c-0170-fig66',
67:'c-0171-fig67',68:'c-0172-fig68',69:'c-0183-fig69',70:'c-0183-fig70',
71:'c-0188-fig71',72:'c-0189-fig72'}

def arc(ax,o,r,a,b,txt=None,offset=1.25):
    ax.add_patch(Arc(o,2*r,2*r,theta1=a,theta2=b,lw=.9,color='black'))
    if txt:
        t=np.deg2rad((a+b)/2)
        label(ax,o[0]+offset*r*np.cos(t),o[1]+offset*r*np.sin(t),txt,fontsize=12)

def seg(ax,a,b,lw=1.3,**kw):
    ax.plot([a[0],b[0]],[a[1],b[1]],color='black',lw=lw,**kw)

def diagram(number):
    stem=STEMS[number]; fig,ax=canvas(stem); r=aspect(stem)
    if number==47:
        # The two half-plane constructions are offset, as in the original.
        for x,y,sgn,edge in [(.17,.50*r,-1,1),(.64,.50*r,1,2)]:
            seg(ax,(x,.06*r),(x,.94*r),1.8)
            arrow(ax,(x,y),(x+.31,y),lw=1.4)
            label(ax,x+.325,y-.018*r,r'$x$',fontsize=13)
            end=(x+.25,y+sgn*.39*r)
            seg(ax,(x,y),end,1.5)
            label(ax,end[0]+.015,end[1],"$P$",ha='left',fontsize=12)
            label(ax,x+.14,y+sgn*.20*r,r'$r$',fontsize=12)
            arc(ax,(x,y),.105,-58 if sgn<0 else 0,0 if sgn<0 else 58,r'$\varphi$')
            my=y+(.29*r if edge==1 else -.29*r)
            ax.plot([x-.015,x+.015],[my,my],'.',color='black',ms=3)
            label(ax,x-.055,my,rf'$m_{{{edge}z}}^+$',ha='right',fontsize=10)
            label(ax,x+.045,my,rf'$m_{{{edge}z}}^-$',ha='left',fontsize=10)
            label(ax,x-.045,y+(-.24*r if edge==1 else .24*r),r'$y=-a$' if edge==1 else r'$y=a$',ha='right',fontsize=10)
    elif number==48:
        y0=.17*r; y1=.77*r
        for idx,x in enumerate([.17,.40,.63,.85]):
            seg(ax,(x,y0),(x,y1),1.7)
            if idx in (0,1): arrow(ax,(x-.14,y1-.065*r),(x,y1),lw=1.4)
            else: arrow(ax,(x-.14,y0-.065*r),(x,y0),lw=1.4)
            if idx in (0,2): arrow(ax,(x,y1),(x+.10,y1+.16*r),lw=1.4)
            else: arrow(ax,(x,y0),(x+.10,y0+.16*r),lw=1.4)
            if idx==1: arrow(ax,(x,y1),(x,y0),lw=1.2)
            if idx==2: arrow(ax,(x,y0),(x,y1),lw=1.2)
            if idx==3:
                arrow(ax,(x-.005,y0),(x-.005,y1),lw=.8)
                arrow(ax,(x+.009,y1),(x+.009,y0),lw=.8)
            label(ax,x,y0-.12*r,chr(97+idx)+')',fontsize=13)
    elif number==63:
        o=(.14,.38*r)
        arrow(ax,(o[0],.06*r),(o[0],.92*r),lw=1.4)
        arrow(ax,(.04,o[1]),(.94,o[1]),lw=1.4)
        label(ax,.95,o[1]-.03*r,r'$z$',fontsize=13)
        label(ax,o[0]+.03,.94*r,r'$y$',fontsize=13)
        for yy,tx in [(.72*r,r'$a$'),(.10*r,r'$-a$')]:
            ax.plot(o[0],yy,'ko',ms=3);label(ax,o[0]-.04,yy,tx,ha='right',fontsize=12)
        ray=(.75,.92*r); seg(ax,o,ray,1.4);label(ax,.43,.68*r,r'$R$',fontsize=12)
        arrow(ax,o,(.80,.57*r),lw=1.4);label(ax,.79,.61*r,r'$\mathbf{n}$',fontsize=12)
        arc(ax,o,.29,0,49,r'$\vartheta$');arc(ax,o,.43,0,20,r'$\gamma$',offset=1.08)
    elif number==64:
        o=(.47,.21*r); p=(.09,.83*r); q=(.86,.47*r)
        seg(ax,o,(.96,o[1]),1.4);seg(ax,o,p,1.4);seg(ax,o,q,1.4)
        label(ax,p[0]-.01,p[1]+.07*r,r'$P$',fontsize=12)
        label(ax,q[0],q[1]+.08*r,r'$Q$',fontsize=12)
        label(ax,o[0]-.01,o[1]-.10*r,r'$O$',fontsize=12)
        label(ax,.26,.59*r,r'$R$',fontsize=12);label(ax,.67,.41*r,r'$d$',fontsize=12)
        arc(ax,o,.15,0,25,r"$\varphi''$",offset=1.2)
        arc(ax,o,.26,25,145,r"$\varphi'$",offset=1.18)
    elif number==69:
        o=np.array([.57,.42*r]); q=np.array([.13,.17*r]); p=np.array([.73,.88*r])
        arrow(ax,o,(.92,o[1]),lw=1.1);label(ax,.94,o[1],r'$z$',fontsize=12)
        arrow(ax,(o[0],.23*r),(o[0],.87*r),lw=1.1);label(ax,o[0]+.015,.89*r,r'$y$',fontsize=12)
        arrow(ax,o,(.28,.68*r),lw=1.1);label(ax,.26,.69*r,r'$x$',fontsize=12)
        arrow(ax,o,(.87,.60*r),lw=1.3);label(ax,.89,.61*r,r'$\mathbf{N}$',fontsize=12)
        seg(ax,q,o,1.3);seg(ax,o,p,1.3);seg(ax,q,p,1.3)
        label(ax,.32,.20*r,r'$R$',fontsize=12);label(ax,.70,.66*r,r'$\rho$',fontsize=12)
        label(ax,.37,.55*r,r'$r$',fontsize=12)
        poly=p+np.array([[-.028,0],[0,.035],[.035,0],[.007,-.035]])
        ax.add_patch(Polygon(poly,fill=False,lw=1.1));label(ax,.79,.88*r,r'$dS$',fontsize=11)
        arrow(ax,p,p+[-.065,.045],lw=.9);label(ax,.65,.94*r,r'$\mathbf{n}$',fontsize=11)
        polar=q+np.array([[-.05,-.015],[-.05,.12],[.08,.015],[.08,-.11]])
        ax.add_patch(Polygon(polar,fill=False,lw=1.0));label(ax,.07,.32*r,r'$P$',fontsize=12)
        label(ax,.08,.105*r,r'$Q$',fontsize=12)
        arrow(ax,q,q+[-.09,.06],lw=.9);arrow(ax,q,q+[0,.16*r],lw=.9)
        label(ax,.045,.27*r,r'$\mathbf{e}_\tau$',fontsize=10)
        label(ax,.14,.36*r,r'$\mathbf{e}_\eta$',fontsize=10)
        arc(ax,o,.13,0,30,r'$\gamma$',offset=1.35)
        arc(ax,o,.10,65,203,r'$\Omega$',offset=1.3)
        arc(ax,o,.16,200,358,r'$\vartheta=\pi-\gamma$',offset=1.15)
    elif number==70:
        o=(.40,.20*r)
        for end,tx in [((.40,.91*r),r'$\mathbf{e}_x$'),((.89,.20*r),r'$\mathbf{e}_\vartheta$'),((.10,.20*r+.30),r'$\mathbf{e}_\eta$'),((.77,.20*r+.37),r'$\mathbf{e}_\tau$')]:
            arrow(ax,o,end,lw=1.3);label(ax,end[0]+(.03 if end[0]>.4 else -.04),end[1]+.025*r,tx,fontsize=13)
        arc(ax,o,.16,0,45,r'$45^\circ$',offset=1.35)
    elif number==72:
        o=(.52,.16*r)
        arrow(ax,o,(.06,.16*r),lw=1.3);label(ax,.065,.10*r,r'$\mathbf{e}_x$',fontsize=13)
        arrow(ax,o,(.52,.90*r),lw=1.3);label(ax,.55,.92*r,r'$\mathbf{e}_\gamma$',fontsize=13)
        arrow(ax,o,(.93,.52*r),lw=1.3);label(ax,.94,.57*r,r'$\mathbf{N}$',fontsize=13)
        arrow(ax,o,(.10,.64*r),lw=1.3);label(ax,.10,.72*r,r'$\mathbf{E}_0$',fontsize=13)
        arc(ax,o,.11,90,150,r'$\alpha$',offset=1.3)
    finish(fig,stem,method='geometry',figure=number,description='Independent vector reconstruction of the original scientific diagram.',details={'source':'Original scanned figure, geometry and labels redrawn independently; no raster embedded.'})

def shading(ka,t,kind='h'):
    """G(1,t),G(2,t) or F(1,t),F(2,t), Eqs21.22/23 and22.13."""
    t=np.asarray(t); vals=[]
    for sign in [-1,1]:
        c=np.cos(np.pi/4+sign*t/2)
        z=2*np.sqrt(ka)*c
        ss,cc=fresnel(z*np.sqrt(2/np.pi))
        integ=np.sqrt(np.pi/2)*(cc+1j*ss)
        if kind=='e': integ=integ+1j*np.exp(1j*z*z)/(4*np.sqrt(ka)*c)
        vals.append(2/np.sqrt(np.pi)*np.exp(-1j*np.pi/4)*integ)
    return vals

def strip_curves(ka,alpha,phi,kind='h'):
    p=np.asarray(phi,dtype=float); a=float(alpha)
    a=np.clip(a,-np.pi/2+2e-6,np.pi/2-2e-6)
    p=np.clip(p,-np.pi/2+2e-6,np.pi/2-2e-6)
    d=np.sin(a)-np.sin(p); phase=ka*d
    c0=(np.cos(a) if kind=='e' else np.cos(p))*np.sinc(phase/np.pi)
    den=np.sin((a-p)/2)
    safe=np.abs(a-p)<1e-7
    ratio=np.divide(np.sin(phase),den,out=np.full_like(p,2*ka*np.cos(a)),where=~safe)
    c1=(ratio+(1j if kind=='e' else -1j)*np.cos(phase)/np.cos((a+p)/2))/(2*ka)
    pp=np.where(safe,p+1e-6,p)
    dd=np.sin(a)-np.sin(pp)
    f1=(np.cos((a+pp)/2)-np.sin((a-pp)/2))/dd
    f2=-(np.cos((a+pp)/2)+np.sin((a-pp)/2))/dd
    b1,b2=(f1,f2) if kind=='e' else (-f2,-f1)
    s1,s2=shading(ka,pp,kind); q1,q2=shading(ka,a,kind)
    c2=(s1*q2*b1*np.exp(1j*ka*dd)+s2*q1*b2*np.exp(-1j*ka*dd))/(2j*ka)
    return np.abs(c0),np.abs(c1),np.abs(c2)

def strip_back(ka,alpha,kind='h'):
    a=np.asarray(alpha); aa=np.clip(a,1e-6,np.pi/2-1e-6)
    s=np.sin(aa); g1=-(1+s)/(2*s);g2=(1-s)/(2*s)
    b1,b2=(g2,g1) if kind=='e' else (g1,g2)
    s1,s2=shading(ka,aa,kind)
    return np.abs((s2*s2*b1*np.exp(2j*ka*s)+s1*s1*b2*np.exp(-2j*ka*s))/(2j*ka))

def plot_canvas(number,xlim,ylim,yticks,*,xlabel=r'$\varphi$',ylabel=None):
    stem=STEMS[number];fig=plt.figure(figsize=(6,6*aspect(stem)))
    # Keep publication-lettering readable on the very wide, shallow charts.
    ax=fig.add_axes([.075,.20,.90,.68] if aspect(stem)<.5 else [.12,.10,.84,.85])
    ax.set_xlim(*xlim);ax.set_ylim(*ylim)
    ax.set_xticks(np.arange(xlim[0],xlim[1]+.1,30));ax.xaxis.set_minor_locator(MultipleLocator(5))
    ax.set_yticks(yticks);ax.yaxis.set_minor_locator(MultipleLocator(.1 if ylim[1]<=1.3 else 2.5))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v,p:f'{v:g}°'))
    ax.tick_params(labelsize=8,pad=2,length=3);ax.tick_params(which='minor',length=0)
    ax.grid(which='major',color='.30',lw=.65);ax.grid(which='minor',color='.65',lw=.40)
    ax.set_axisbelow(True)
    ax.text(1,-.14 if aspect(stem)<.5 else -.055,xlabel,transform=ax.transAxes,ha='right',va='top',fontsize=9)
    if ylabel:ax.text(-.055,1.0,ylabel,transform=ax.transAxes,ha='left',va='bottom',fontsize=9)
    return fig,ax

def pchip(points,x):
    pts=np.array(points,dtype=float)
    return PchipInterpolator(pts[:,0],pts[:,1],extrapolate=False)(x)

# Published rigorous-solution comparisons manually read from the scan grid.
# These are independent control points, not samples of the approximation.
RIGOROUS={
49:[[-90,0],[-80,.06],[-70,.13],[-60,.21],[-55,.23],[-50,.22],[-45,.17],[-40,.10],[-35,.045],[-30,.14],[-25,.34],[-20,.56],[-15,.77],[-10,.93],[-5,1.03],[0,1.055]],
50:[[-90,0],[-80,.12],[-70,.30],[-60,.51],[-55,.62],[-50,.70],[-45,.75],[-40,.75],[-35,.68],[-30,.55],[-25,.38],[-20,.22],[-15,.10],[-11,.09],[-5,.17],[2,.23],[10,.20],[20,.10],[28,.08],[35,.13],[45,.18],[55,.17],[65,.13],[75,.08],[85,.025],[90,0]],
51:[[0,1.03],[5,.91],[10,.62],[15,.31],[20,.11],[25,.17],[30,.12],[35,.075],[40,.115],[45,.16],[50,.19],[55,.18],[60,.15],[65,.11],[70,.065],[80,.012],[90,0]],
52:[[-90,0],[-80,.035],[-70,.08],[-60,.12],[-55,.13],[-50,.09],[-45,.025],[-40,.065],[-35,.15],[-30,.20],[-25,.13],[-21,.015],[-15,.35],[-10,.70],[-5,.92],[0,1.0]],
53:[[-90,0],[-80,.09],[-70,.27],[-60,.49],[-55,.60],[-50,.70],[-45,.75],[-40,.69],[-35,.51],[-30,.28],[-25,.09],[-21,.05],[-15,.16],[-10,.17],[-5,.11],[0,.025],[5,.09],[10,.12],[15,.10],[20,.05],[24,.015],[30,.06],[35,.065],[40,.055],[45,.025],[50,.012],[60,.035],[70,.03],[80,.018],[90,0]],
54:[[0,1.0],[3,.92],[6,.68],[9,.36],[12,.08],[15,.23],[18,.15],[21,.06],[25,.13],[30,.09],[35,.07],[40,.03],[44,.025],[50,.06],[56,.08],[62,.07],[70,.04],[80,.008],[90,0]],
55:[[-90,.09],[-80,.115],[-70,.145],[-60,.185],[-55,.195],[-50,.19],[-45,.17],[-40,.13],[-35,.115],[-30,.21],[-25,.39],[-20,.60],[-15,.78],[-10,.91],[-5,.98],[0,1.0]],
56:[[-90,.25],[-80,.30],[-70,.40],[-60,.52],[-55,.61],[-50,.69],[-45,.74],[-40,.73],[-35,.66],[-30,.52],[-25,.34],[-20,.17],[-15,.11],[-10,.12],[-5,.16],[2,.20],[10,.17],[20,.105],[30,.10],[40,.14],[50,.14],[60,.12],[75,.085],[90,.055]],
59:[[-90,.055],[-80,.06],[-70,.07],[-60,.10],[-55,.105],[-50,.08],[-45,.055],[-40,.075],[-35,.15],[-30,.21],[-25,.17],[-21,.07],[-15,.33],[-10,.65],[-5,.91],[0,1.0]],
60:[[-90,.12],[-80,.14],[-70,.23],[-60,.43],[-55,.57],[-50,.68],[-45,.74],[-40,.72],[-35,.55],[-30,.31],[-25,.13],[-21,.09],[-15,.17],[-10,.20],[-5,.15],[0,.07],[5,.095],[10,.13],[15,.11],[20,.065],[25,.045],[30,.08],[35,.09],[40,.075],[45,.05],[50,.045],[60,.06],[70,.05],[80,.035],[90,.03]],
}

def strip_figure(number):
    kind='h' if number<=54 else 'e';ka=np.sqrt(28 if number in [49,50,51,55,56,57,58] else 80)
    back=number in [51,54,58,62];grazing=number in [57,61]
    alpha=-np.pi/2 if grazing else (-np.pi/4 if number in [50,53,56,60] else 0)
    xmax=(0,90) if back else (-90,90);x=np.linspace(*xmax,1801)
    ymax=.6 if grazing else 1.1
    fig,ax=plot_canvas(number,xmax,(0,ymax),[0,.5,1] if not grazing else [0,.5],xlabel=r'$\alpha$' if back else r'$\varphi$',ylabel=rf'$|{kind}(\varphi)|$' if not back else rf'$|{kind}|$')
    curves={}
    if back:
        curves[kind+'2']=strip_back(ka,np.deg2rad(x),kind)
        ax.plot(x,curves[kind+'2'],':',color='black',lw=1.1,label=rf'${kind}_2$')
    else:
        vals=strip_curves(ka,alpha,np.deg2rad(x),kind)
        if not grazing:
            for k,ls,v in zip([0,1],['-.','--'],vals[:2]):
                curves[kind+str(k)]=v;ax.plot(x,v,ls,color='black',lw=1.0,label=rf'${kind}_{k}$')
        curves[kind+'2']=vals[2]
        if kind=='h':ax.plot(x,vals[2],':',color='black',lw=1.1,label=r'$h_2$')
    if number in RIGOROUS:
        pts=RIGOROUS[number]
        if number in [49,52,55,59]:pts=pts+[[ -xx,yy] for xx,yy in reversed(pts[:-1])]
        rigorous=pchip(pts,x)
        ax.plot(x,rigorous,'k-',lw=1.5,label=rf'${kind}$',zorder=4)
        method='mixed';rig={'label':kind,'control_points':pts,'interpolation':'PCHIP','qualification':'Manual grid reading of published rigorous reference; approximate digitization, not a new rigorous solver.'}
    else:
        ax.plot(x,curves[kind+'2'],'k-',lw=1.5,label=rf'${kind}$');method='formula';rig=None
    if number in RIGOROUS and not back:
        handles,labels=ax.get_legend_handles_labels();order=[len(handles)-1]+list(range(len(handles)-1))
        ax.legend([handles[i] for i in order],[labels[i] for i in order],loc='upper left',fontsize=7,frameon=True,fancybox=False,edgecolor='black',facecolor='white',framealpha=1,borderpad=.25,labelspacing=.15,handlelength=2.5)
    elif kind=='h' and back:ax.legend(loc='upper left',fontsize=8,frameon=True,fancybox=False,edgecolor='black',framealpha=1)
    atext=r'\varphi=-\pi+\alpha' if back else (r'\alpha=-\pi/2' if grazing else r'\alpha=-\pi/4' if alpha else r'\alpha=0')
    ktext='28' if np.isclose(ka,np.sqrt(28)) else '80'
    ax.text(.31 if alpha==0 and not back else .56,.94 if alpha==0 and not back else .86,rf'${atext},\quad ka=\sqrt{{{ktext}}}$',transform=ax.transAxes,ha='center',va='top',fontsize=8,bbox=dict(facecolor='white',edgecolor='black',lw=.5,pad=3))
    drawn=list(curves) if kind=='h' or back or grazing else [kind+'0',kind+'1']
    shown_label={'label':kind,'provenance':'Independently digitized published rigorous reference.' if rig else 'Calculated secondary-diffraction approximation (subscript2), displayed under the original unsuffixed figure label. No new rigorous solution is claimed; the source reports close agreement.'}
    finish(fig,STEMS[number],method=method,figure=number,description='Strip scattering magnitudes, with independently redrawn axes and comparison curves.',equations=['20.04','20.05','21.22','21.23','22.13','23.02','23.10','23.13','23.14','23.15'],details={'ka':float(ka),'alpha_degrees':None if back else float(np.rad2deg(alpha)),'backscatter':back,'drawn_computed_curves':drawn,'unsuffixed_curve':shown_label,'rigorous_reference':rig,'endpoint_evaluation':'One-sided numerical angular limit, 2e-6 radians; removable forward singularity evaluated at1e-6 radians.'})

def smoothstep(x):
    x=np.clip(x,0,1);return x*x*(3-2*x)

def disk_back(gamma,ka=5):
    """Sigma-bar and Sigma: Eq24.25, joined to12.15 near the z axis."""
    t=np.clip(np.asarray(gamma),1e-6,np.pi/2-1e-6);s=np.sin(t);z=2*ka*s
    f1=-(1+s)/(2*s);f2=(1-s)/(2*s)
    e1,e2=shading(ka,-t,'e');h1,h2=shading(ka,-t,'h')
    eb=(e1*e1*f2-e2*e2*f1)*jv(1,z)+1j*(e1*e1*f2+e2*e2*f1)*jv(2,z)
    hb=(h1*h1*f1-h2*h2*f2)*jv(1,z)+1j*(h1*h1*f1+h2*h2*f2)*jv(2,z)
    ep=jv(1,z)/s-1j*jv(2,z);hp=-jv(1,z)/s-1j*jv(2,z)
    blend=smoothstep(np.rad2deg(t)/20)
    return ep*(1-blend)+eb*blend,hp*(1-blend)+hb*blend

def disk_v(theta,pol=1,ka=5):
    """Normal incidence: physical optics, primary and secondary approximations."""
    tt=np.asarray(theta);t=np.clip(np.minimum(tt,np.pi-tt),1e-6,np.pi/2-1e-6)
    z=ka*np.sin(t);s=np.sin(t)
    v0=2*jv(1,z)/z
    if pol==2:v0=v0*np.cos(tt)
    v1=(jv(1,z)/np.sin(t/2)+(-1j if pol==1 else 1j)*jv(2,z)/np.cos(t/2))/ka
    f1=-(np.cos(t/2)+np.sin(t/2))/s
    f2=(np.cos(t/2)-np.sin(t/2))/s
    kind='e' if pol==1 else 'h';a,b=shading(ka,t,kind);a0,b0=shading(ka,0,kind)
    c1,c2=(f1,f2) if pol==1 else (-f2,-f1)
    v2=((b*a0*c2-a*b0*c1)*jv(1,z)+1j*(b*a0*c2+a*b0*c1)*jv(2,z))/ka
    blend=smoothstep(np.rad2deg(t)/22)
    v2=(1-blend)*v1+blend*v2
    if pol==2:
        v1=v1*np.where(tt>np.pi/2,-1,1);v2=v2*np.where(tt>np.pi/2,-1,1)
        v2=np.where(np.abs(tt-np.pi/2)<1e-7,0,v2)
    return v0,v1,v2

EXPERIMENT65=[
[[0,13.8],[5,13],[10,11.5],[15,7.5],[18,2],[20,-5],[22,-11],[23,-18],[25,-9],[28,-6],[32,-5.5],[38,-6.2],[42,-6.5],[50,-5.8],[55,-5.6],[60,-6.5],[65,-8.7],[70,-12],[75,-17],[80,-21],[85,-28],[90,-38]],
[[0,13.8],[5,13.2],[10,11.9],[15,8.3],[18,3],[21,-3],[23,-10],[24,-11.4],[26,-8.2],[29,-5.5],[32,-4.2],[35,-4.3],[40,-5.2],[45,-6],[50,-5.8],[55,-5.4],[60,-6.1],[65,-8.3],[70,-11.7],[75,-16.4],[80,-21.2],[85,-28],[90,-38]]]
EXPERIMENT71=[[-90,-10],[-80,-10.5],[-70,-14],[-65,-23],[-60,-20],[-55,-9],[-48,-3],[-44,-2.5],[-40,-4],[-35,-10],[-30,-16],[-27,-10],[-23,-1],[-18,0],[-13,-4],[-8,-13],[-4,-20],[0,-30],[4,-15],[10,-5],[15,-.5],[18,-1],[22,-6],[27,-17],[30,-13],[35,-5],[40,-2],[44,-3],[50,-10],[58,-23],[63,-18],[70,-12],[80,-10.5],[90,-10]]
THEORY71_HALF=[[-90,-10],[-80,-10.5],[-75,-12],[-70,-16],[-65,-22],[-60,-18],[-55,-8],[-50,-3.5],[-45,-2.4],[-40,-3.5],[-35,-8],[-30,-16],[-27,-11],[-23,-1.5],[-18,0],[-13,-4],[-8,-14],[-4,-21],[0,-45]]
MEASURED71=[[-90,-7],[-80,-6.4],[-75,-7],[-70,-9.5],[-65,-13.5],[-62,-15],[-60,-14],[-55,-7.5],[-50,-4],[-45,-3.2],[-41,-3.2],[-36,-6],[-33,-13],[-31,-15.5],[-28,-9],[-24,-1],[-20,0],[-17,-1],[-13,-5],[-9,-13],[-6,-14.5],[-4,-12],[0,-30],[4,-8],[10,-2],[15,1.7],[20,2.2],[24,-.5],[28,-8.5],[31,-8],[35,-2.5],[40,0],[44,-.2],[48,-3],[53,-9],[58,-13.5],[64,-15],[68,-12],[75,-9],[80,-6.7],[90,-6.4]]

def disk_figure(number):
    if number==71:
        # The published ordinate is sigma+, dB, not the dimensionless
        # sigma+/(pi*a^2). Its absolute dB reference is not stated. Preserve
        # that published ordinate by independently digitizing both traces.
        x=np.linspace(-90,90,2401)
        theory=THEORY71_HALF+[[-t,y] for t,y in reversed(THEORY71_HALF[:-1])]
        fig,ax=plot_canvas(number,(-90,90),(-30,10),[-30,-20,-10,0,10],xlabel=r'$\gamma$',ylabel=r'$\sigma^+,\ \mathrm{dB}$')
        ax.xaxis.set_minor_locator(MultipleLocator(10));ax.yaxis.set_minor_locator(MultipleLocator(10))
        ax.texts[1].set_position((0,1.015))
        ax.plot(x,pchip(theory,x),'k--',lw=1.25,label='theoretical')
        ax.plot(x,pchip(MEASURED71,x),'k-',lw=1.4,label='measured')
        ax.text(.43,.91,r'$ka=5$',transform=ax.transAxes,ha='center',fontsize=10)
        ax.annotate('theoretical',xy=(-44,-2.5),xytext=(-67,1),fontsize=10,ha='center',arrowprops=dict(arrowstyle='-',lw=.7),bbox=dict(facecolor='white',edgecolor='none',pad=2))
        ax.annotate('measured',xy=(20,2.2),xytext=(43,4.0),fontsize=10,ha='center',arrowprops=dict(arrowstyle='-',lw=.7),bbox=dict(facecolor='white',edgecolor='none',pad=2))
        finish(fig,STEMS[number],method='digitized',figure=number,description='Published nonuniform-current scattering diagram, with theoretical dashed and measured solid traces independently digitized.',equations=['26.19'],details={'ka':5,'axis':'sigma+, dB as printed; absolute dB normalization unspecified in figure','theoretical_control_points':theory,'measured_control_points':MEASURED71,'interpolation':'PCHIP','qualification':'Approximate readings from the original plot, preserving its ordinate and visible extrema. Eq26.19 defines the quantity; no unsupported absolute-area normalization inferred.'})
        return
    if number in [65,66,71]:
        x=np.linspace(-90,90,2401) if number==71 else np.linspace(0,90,1801)
        e,h=disk_back(np.deg2rad(np.abs(x)))
        y=20*np.log10(np.maximum(np.abs((e+h)/2 if number==71 else h if number==65 else e),1e-12))
        if number==71:y[np.abs(x)<.01]=-80
        yr=(-30,10) if number==71 else (-25,15) if number==65 else (-15,15)
        fig,ax=plot_canvas(number,(-90,90) if number==71 else (0,90),yr,np.arange(yr[0],yr[1]+.1,10 if number==71 else 5),xlabel=r'$\gamma$',ylabel=r'$10\log_{10}(\sigma^+/\pi a^2)$' if number==71 else r'$10\log_{10}(\sigma/\pi a^2)$')
        ax.xaxis.set_minor_locator(MultipleLocator(10 if number==71 else 10));ax.yaxis.set_minor_locator(MultipleLocator(10 if number==71 else 2.5))
        ax.plot(x,y,'k-',lw=1.5,label='theoretical')
        control=[]
        if number==65:
            for i,pts in enumerate(EXPERIMENT65):ax.plot(x,pchip(pts,x),'k--',lw=1.15,label='experimental' if i==0 else '_nolegend_')
            control=EXPERIMENT65
        if number==71:
            ax.plot(x,pchip(EXPERIMENT71,x),'k--',lw=1.15,label='measured');control=[EXPERIMENT71]
        if number in [65,66]:
            ax.spines['bottom'].set_position(('data',0));ax.axhline(yr[0],color='black',lw=.7)
            ax.text(.97,(0-yr[0])/(yr[1]-yr[0])-.035,r'$\gamma$',transform=ax.transAxes,ha='right',fontsize=10)
            # Remove the standard bottom gamma; source horizontal angle-axis lies at0dB.
            ax.texts[0].set_visible(False)
        ax.text(.40,.91,r'$ka=5$',transform=ax.transAxes,ha='center',fontsize=10,bbox=dict(facecolor='white',edgecolor='none',pad=2))
        if number in [65,71]:ax.legend(loc='upper right' if number==65 else 'upper center',fontsize=9,frameon=True,fancybox=False,edgecolor='black',facecolor='white',framealpha=1)
        finish(fig,STEMS[number],method='mixed' if control else 'formula',figure=number,description='Disk backscattering cross section reconstructed from the published diffraction formulas; experimental traces independently digitized.',equations=['12.15','12.17','21.22','21.23','22.13','24.25','24.26','26.19'],details={'ka':5,'axis':'10log10 cross section normalized by pi*a^2','near_axis_join':'Per paragraph following24.26, smoothly join12.15 to24.25 over0–20degrees. smoothstep makes the switch explicit and reproducible.','experimental_control_points':control,'interpolation':'PCHIP for experimental traces only','precision':'Experimental traces are approximate visual grid readings, not original measurement tables.'})
    else:
        pol=1 if number==67 else 2;x=np.linspace(0,180,1801);v0,v1,v2=disk_v(np.deg2rad(x),pol)
        fig,ax=plot_canvas(number,(0,180),(0,1.2),[0,.5,1],xlabel=r'$\vartheta$',ylabel=rf'$|V^{{({pol})}}(\vartheta)|$')
        ax.xaxis.set_minor_locator(MultipleLocator(10));ax.yaxis.set_minor_locator(MultipleLocator(.05))
        ax.set_position([.10,.08,.80,.86]);right=ax.twinx();right.set_ylim((-230,10) if pol==1 else (-50,180))
        right.set_yticks([-180,-90,0] if pol==1 else [0,90,180]);right.yaxis.set_major_formatter(FuncFormatter(lambda v,p:f'{v:g}°'));right.tick_params(labelsize=8,pad=2)
        right.text(1.02,1.015,rf'$\arg V^{{({pol})}}(\vartheta)$',transform=right.transAxes,ha='right',fontsize=9)
        for value,ls,lab in [(v0,'-.','2'),(v1,'--','3'),(v2,':','4')]:
            ax.plot(x,np.abs(value),color='black',ls=ls,lw=1.15,label=lab)
            if lab!='2':
                # Both hemispheres shown with the phase convention printed in Figure68.
                phase=np.rad2deg(np.angle(value))
                if pol==1:phase=np.where(phase>0,phase-360,phase)
                else:phase=np.where(x>90,phase+180,phase)
                phase[np.abs(x-90)<.11]=np.nan if pol==2 else phase[np.abs(x-90)<.11]
                right.plot(x,phase,color='black',ls=ls,lw=1.15)
        amp=[[0,1.04],[10,.91],[20,.66],[30,.35],[40,.13],[47,.085],[55,.10],[65,.11],[80,.115],[90,.11]] if pol==1 else [[0,1.04],[10,.91],[20,.67],[30,.35],[40,.16],[50,.11],[60,.075],[70,.04],[80,.018],[90,0]]
        ph=[[0,-3],[10,-4],[20,-8],[30,-16],[40,-36],[50,-91],[60,-141],[70,-161],[80,-171],[90,-173]] if pol==1 else [[0,-3],[10,-2],[20,5],[30,20],[40,65],[50,110],[60,128],[70,135],[80,138],[90,138]]
        apts=amp+[[-t+180,y] for t,y in reversed(amp[:-1])];ppts=ph+[[-t+180,y] for t,y in reversed(ph[:-1])]
        ax.plot(x,pchip(apts,x),'k-',lw=1.6,label='1');right.plot(x,pchip(ppts,x),'k-',lw=1.6)
        handles,labels=ax.get_legend_handles_labels();ax.legend([handles[-1]]+handles[:-1],[labels[-1]]+labels[:-1],loc='center',bbox_to_anchor=(.5,.62 if pol==1 else .30),frameon=True,fancybox=False,facecolor='white',edgecolor='black',framealpha=1,fontsize=9)
        ax.text(.5,.95,r'$ka=5$',transform=ax.transAxes,ha='center',fontsize=10)
        ax.text(.10,.85,rf'$|V^{{({pol})}}|$',transform=ax.transAxes,fontsize=9,bbox=dict(facecolor='white',edgecolor='none',pad=1))
        right.text(.42,.30 if pol==1 else .79,rf'$\arg V^{{({pol})}}$',transform=right.transAxes,fontsize=9,bbox=dict(facecolor='white',edgecolor='none',pad=1))
        if pol==2:right.text(.70,.92,r'$\arg V^{(2)}+180^\circ$',transform=right.transAxes,fontsize=8,ha='center')
        finish(fig,STEMS[number],method='mixed',figure=number,description='Disk normal-incidence amplitude and phase, computed approximations with independently digitized rigorous-reference traces.',equations=['7.11','9.03','9.05','9.07','24.20','24.21'],details={'ka':5,'curve1':'Published rigorous reference manually digitized from scan grid','curve2':'Physical optics,7.11 (amplitude)','curve3':'Primary diffraction,9.03/9.05','curve4':'Secondary diffraction,24.20/24.21 with near-axis join recommended in24','rigorous_amplitude_control_points':apts,'rigorous_phase_control_points_degrees':ppts,'interpolation':'PCHIP for curve1; computed complex amplitudes for3/4','near_axis_join_degrees':22,'phase_convention':'For V2 second hemisphere add180degrees, as annotated in original.'})

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--only',nargs='*',type=int);args=ap.parse_args()
    selected=args.only or list(STEMS)
    for n in selected:
        if n in [47,48,63,64,69,70,72]:diagram(n)
        elif 49<=n<=62:strip_figure(n)
        else:disk_figure(n)

if __name__=='__main__':main()
