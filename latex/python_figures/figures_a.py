"""Editable vector reconstructions of Ufimtsev Figures 1--23.

Run with Python; numpy/scipy/matplotlib are the only scientific dependencies.
No network calls, OCR, embedded scan images, or pixel tracing are used. Curves in
Figs. 8--13 are evaluated from the printed equations. Figs. 20--21 combine the
printed approximations with manually sampled published rigorous-theory curves.
"""
from __future__ import annotations
import argparse
import math
import numpy as np
from common import canvas, aspect, arrow, label, finish, plt
from matplotlib.patches import Polygon, Ellipse, Arc, PathPatch, Rectangle
from matplotlib.path import Path
from scipy.interpolate import PchipInterpolator
from scipy.special import jv

STEMS={1:'a-0020-fig',2:'a-0026-fig2',3:'a-0026-fig3',4:'a-0028-fig4',
5:'a-0028-fig5',6:'a-0028-fig6',7:'a-0038-fig7',8:'a-0047-fig8',9:'a-0047-fig9',
10:'a-0048-fig10',11:'a-0048-fig11',12:'a-0049-fig12',13:'a-0049-fig13',
14:'a-0050-fig14',15:'a-0053-fig15',16:'a-0053-fig16',17:'a-0061-fig17',
18:'a-0063-fig18',19:'a-0067-fig19',20:'a-0072-fig20',21:'a-0073-fig21',
22:'a-0075-fig22',23:'a-0077-fig23'}

def drawing(num):
    fig,ax=canvas(STEMS[num]); ax.set_aspect('auto'); ax.set_ylim(0,1)
    return fig,ax

def stroke(ax,xy,**kw):
    xy=np.array(xy); return ax.plot(xy[:,0],xy[:,1],color='black',**kw)

def polygon(ax,xy,hatch=None,**kw):
    p=Polygon(xy,closed=True,facecolor='white',edgecolor='black',lw=1.1,hatch=hatch,**kw)
    ax.add_patch(p);return p

def arc(ax,c,rx,ry,a,b,*,head=False,**kw):
    t=np.deg2rad(np.linspace(a,b,120));xy=np.c_[c[0]+rx*np.cos(t),c[1]+ry*np.sin(t)]
    stroke(ax,xy,**kw)
    if head: arrow(ax,xy[-6],xy[-1],lw=1.0)

def ray_arc(ax,o,p0,p1,r,text=None,*,text_scale=1.18,fontsize=10):
    """Angle mark with endpoints lying exactly on the two projected rays."""
    ratio=ax.figure.get_figheight()/ax.figure.get_figwidth()
    a=np.degrees(np.arctan2((p0[1]-o[1])*ratio,p0[0]-o[0]))
    b=np.degrees(np.arctan2((p1[1]-o[1])*ratio,p1[0]-o[0]))
    while b<a:b+=360
    if b-a>180:a,b=b,a+360
    arc(ax,o,r,r/ratio,a,b)
    if text:
        t=np.deg2rad((a+b)/2)
        label(ax,o[0]+r*text_scale*np.cos(t),o[1]+r/ratio*text_scale*np.sin(t),text,fontsize=fontsize)

def dot(ax,p,txt=None,offset=(0,.025)):
    ax.plot(*p,'ko',ms=2.5)
    if txt: label(ax,p[0]+offset[0],p[1]+offset[1],txt)

def bezier(ax,pts,**kw):
    codes=[Path.MOVETO]+[Path.CURVE4]*(len(pts)-1)
    p=PathPatch(Path(pts,codes),fill=False,edgecolor='black',lw=kw.pop('lw',1.5),**kw);ax.add_patch(p)

def save(fig,num,description,equations=None,method='schematic',details=None):
    finish(fig,STEMS[num],method=method,description=description,figure=num,equations=equations,details=details)

def wedge(ax,o=(.24,.45),end=.94,lower=.1):
    polygon(ax,[o,(end,o[1]),(end,lower)],hatch='////')
    arrow(ax,o,(.98,o[1]),lw=1.3)

def fig1():
    fig,ax=drawing(1);o=(.34,.40)
    wedge(ax,o,.91,.08)
    label(ax,.93,.42,r'$\varphi=0$',ha='left',fontsize=9)
    label(ax,.91,.055,r'$\varphi=\alpha$',ha='left',fontsize=9)
    arrow(ax,o,(.04,.25));label(ax,.025,.22,r'$P$')
    arrow(ax,o,(.58,.77));dot(ax,(.50,.64),r'$Q$',(-.025,.025))
    label(ax,.455,.57,r'$r_0$',rotation=45)
    arc(ax,o,.09,.12,0,50);label(ax,.465,.455,r'$\varphi_0$')
    arc(ax,o,.16,.20,0,206,head=True);label(ax,.25,.55,r'$\varphi$')
    # Annular Green contour, inner/outer radii r1/r2 centered on the edge.
    th=np.deg2rad(np.linspace(30,82,100))
    outer=np.c_[o[0]+.40*np.cos(th),o[1]+.55*np.sin(th)]
    inner=np.c_[o[0]+.28*np.cos(th),o[1]+.39*np.sin(th)]
    polygon(ax,np.vstack([outer,inner[::-1]]))
    label(ax,.56,.91,r'$r=r_2$',rotation=-26,fontsize=9)
    label(ax,.45,.72,r'$r=r_1$',rotation=-28,fontsize=9)
    label(ax,.62,.65,r'$L$');arrow(ax,(.36,.84),(.415,.82))
    save(fig,1,'Wedge, source and observation directions, and annular Green integration contour',['1.10'])

def band(ax,x0,x1,y0,y1):
    ax.add_patch(Rectangle((x0,y0),x1-x0,y1-y0,facecolor='none',edgecolor='black',lw=.35,hatch='////'))

def complex_axes(ax,xlim,ylim=(-1.6,1.6),ticks=(),variable=r'$\beta$'):
    ax.set_xlim(*xlim);ax.set_ylim(*ylim);ax.axis('off')
    arrow(ax,(xlim[0],0),(xlim[1],0),lw=.9)
    stroke(ax,[(0,ylim[0]),(0,ylim[1])],lw=.8)
    for x,s in ticks:label(ax,x,-.10,s,fontsize=9)
    label(ax,xlim[1]-.05,.12,variable,fontsize=10)

def fig2():
    stem=STEMS[2];fig=plt.figure(figsize=(6,6*aspect(stem)))
    for j,shift in enumerate([0,-1]):
        ax=fig.add_axes([.04+j*.51,.07,.43,.85]);lo=-1.25+shift;hi=2.35+shift
        complex_axes(ax,(lo,hi),ticks=[(x+shift,t) for x,t in [(-1,r'$-\pi$'),(0,'0'),(1,r'$\pi$'),(2,r'$2\pi$')]] if not j else [(-2,r'$-2\pi$'),(-1,r'$-\pi$'),(0,'0'),(1,r'$\pi$')],variable=r'$\beta$' if not j else r"$\beta'$ ")
        for a,b in [(-1,0),(1,2)]:band(ax,a+shift,b+shift,0,1.5)
        for a,b in [(-2,-1),(0,1),(2,3)]:band(ax,max(a+shift,lo),min(b+shift,hi),-1.5,0) if b+shift>lo and a+shift<hi else None
        xy=[(-.5+shift,1.5),(-.5+shift,.50),(1.5+shift,.50),(1.5+shift,1.5)]
        stroke(ax,xy,lw=1.8);arrow(ax,(.15+shift,.50),(.65+shift,.50),lw=1.7)
        label(ax,-.68+shift,1.20,r'$\mathrm{I}$');label(ax,1.75+shift,1.20,r'$\mathrm{III}$')
        label(ax,.40+shift,1.52,r'$(\beta)$' if not j else r"$(\beta')$")
    save(fig,2,'Translated Sommerfeld integration paths and alternating convergence half-strips',['1.27'])

def fig3():
    fig,ax=drawing(3);ax.set_xlim(-2.15,2.35);ax.set_ylim(-1.7,1.7)
    complex_axes(ax,(-2.15,2.35),(-1.7,1.7),[(-2,r'$-2\pi$'),(-1,r'$-\pi$'),(0,'0'),(1,r'$\pi$'),(2,r'$2\pi$')],r'$\beta$')
    for a,b in [(-2,-1),(0,1),(2,2.12)]:band(ax,a,b,0,1.6)
    for a,b in [(-2.12,-2),(-1,0),(1,2)]:band(ax,a,b,-1.6,0)
    stroke(ax,[(-1.5,1.6),(-1.5,.50),(.5,.50),(.5,1.6)],lw=1.6)
    stroke(ax,[(1.5,-1.6),(1.5,-.50),(-.5,-.50),(-.5,-1.6)],lw=1.6)
    arrow(ax,(.9,-.5),(.25,-.5),lw=1.5)
    stroke(ax,[(-1.5,.5),(-1,0),(-.5,-.5)],lw=1.7)
    stroke(ax,[(.5,.5),(1,0),(1.5,-.5)],lw=1.7)
    label(ax,-.5,.66,r'$C$');label(ax,.48,-.68,r'$C$')
    label(ax,1.11,.16,r'$D$');label(ax,-.67,-.55,r'$D$')
    label(ax,-.28,1.47,r'$(\beta)$')
    save(fig,3,'Sommerfeld contour C and deformation D through the saddle points',['1.28','1.29'])

def fig4():
    fig,ax=drawing(4);ax.set_xlim(-1.95,1.95);ax.set_ylim(-3.2,3.2)
    arrow(ax,(-1.8,0),(1.85,0));stroke(ax,[(0,-3),(0,3)])
    for x in [-np.pi/2,np.pi/2]:stroke(ax,[(x,-2.95),(x,2.95)],ls='--',lw=.8)
    x=np.linspace(-1.565,1.565,600);y=-np.arcsinh(np.tan(x))
    ax.plot(x,y,'k',lw=1.8);arrow(ax,(.55,-np.arcsinh(np.tan(.55))),(.82,-np.arcsinh(np.tan(.82))),lw=1.4)
    label(ax,-np.pi/2,-.25,r'$-\frac{\pi}{2}$');label(ax,np.pi/2,-.25,r'$\frac{\pi}{2}$')
    label(ax,-.13,-.2,'0');label(ax,.17,.18,r'$D_0$');label(ax,.1,3,r'$\zeta$')
    save(fig,4,'Steepest descent contour with asymptotes at Re(zeta)=+/-pi/2',['1.30'],method='analytic',details={'curve':'Im(zeta)=-asinh(tan(Re(zeta)))'})

def fig5():
    fig,ax=drawing(5);o=(.22,.46);wedge(ax,o,.91,.08)
    arrow(ax,o,(.22,.96));label(ax,.255,.96,r'$y$');label(ax,.96,.425,r'$x$')
    stroke(ax,[(.07,.94),o,(.06,.07)],lw=1.4)
    arrow(ax,(.36,.93),o,lw=1.5)
    arc(ax,o,.12,.16,0,72);label(ax,.38,.62,r'$\varphi_0$')
    arc(ax,o,.075,.10,0,110,head=True)
    arc(ax,o,.075,.10,0,249,head=True)
    label(ax,.08,.73,r'$\varphi=\pi-\varphi_0$',rotation=67,fontsize=9)
    label(ax,.10,.23,r'$\varphi=\pi+\varphi_0$',rotation=70,fontsize=9)
    save(fig,5,'Single illuminated wedge face, incident ray, reflection and shadow boundaries')

def fig6():
    fig,ax=drawing(6);o=(.30,.63);wedge(ax,o,.93,.20)
    arrow(ax,(.03,.70),o,lw=1.4)
    stroke(ax,[o,(.93,.91)],lw=1.4);stroke(ax,[o,(.92,.08)],lw=1.4)
    arc(ax,o,.19,.26,0,162,head=True);label(ax,.22,.94,r'$\varphi_0$')
    arc(ax,o,.10,.17,0,310,head=True)
    label(ax,.97,.65,r'$\varphi=0$',ha='right',fontsize=9)
    label(ax,.95,.19,r'$\varphi=\alpha$',fontsize=9)
    label(ax,.69,.94,r'$\varphi=\pi-\varphi_0$',rotation=13,fontsize=9)
    label(ax,.65,.25,r'$\varphi=2\alpha-\pi-\varphi_0$',rotation=-24,fontsize=9)
    save(fig,6,'Both illuminated wedge faces and their specular-ray boundaries')

def fig7():
    stem=STEMS[7];fig=plt.figure(figsize=(6,6*aspect(stem)))
    for j in range(2):
        split=.36 if not j else .84
        lo=split-1.12;hi=split+1.12
        ax=fig.add_axes([.04+j*.49,.08,.44,.86]);complex_axes(ax,(lo,hi),(-1.1,1.1),variable=r'$\xi$')
        band(ax,split-1,split,0,1.02);band(ax,split,split+1,-1.02,0)
        band(ax,split+1,split+1.06,0,1.02);band(ax,split-1.06,split-1,-1.02,0)
        # F is the real-w path mapped by w=-k cos(xi): vertical ends,
        # real-axis segment 0..pi, and an upper indentation at pi-phi0.
        pole=.66;eps=.055
        stroke(ax,[(0,1.02),(0,0),(pole-eps,0)],lw=1.2)
        arc(ax,(pole,0),eps,.065,180,0)
        stroke(ax,[(pole+eps,0),(1,0),(1,-1.02)],lw=1.2)
        q=np.linspace(-.465,.465,400);yy=-np.arcsinh(np.tan(np.pi*q))/3.0
        ax.plot(split+q,yy,'k',lw=1.6)
        k=270;arrow(ax,(split+q[k-8],yy[k-8]),(split+q[k],yy[k]),lw=1.2)
        label(ax,1.07,-.64,r'$F$');label(ax,split-.25,.62,r'$G_1$' if not j else r'$G_2$')
        label(ax,-.045,-.11,'0',fontsize=8)
        label(ax,pole,.14,r'$\pi-\varphi_0$',fontsize=7,bbox=dict(facecolor='white',edgecolor='none',pad=.2))
        label(ax,split,-.10,r'$\varphi$' if not j else r'$2\pi-\varphi$',fontsize=7,bbox=dict(facecolor='white',edgecolor='none',pad=.2))
        label(ax,split-1,.08,r'$-\pi+\varphi$' if not j else r'$\pi-\varphi$',fontsize=7)
        label(ax,split+1,-.10,r'$\pi+\varphi$' if not j else '',fontsize=7,bbox=dict(facecolor='white',edgecolor='none',pad=.2))
        label(ax,split-.25,1.04,r'$(\xi)$',fontsize=9);label(ax,split,-1.08,'a)' if not j else 'b)')
    save(fig,7,'Integration contour F and its deformations G1/G2 in the complex xi plane',['3.14','3.15'],details={'schematic_parameters':'Representative placements preserve labeled boundaries and path topology; not a quantitative complex-plane scale.'})

def edge_coefficients(phi,phi0,alpha):
    """Printed 4.07--4.10; sample away from removable singularities."""
    n=alpha/np.pi;p=np.asarray(phi);q=np.asarray(phi0)
    a=np.sin(np.pi/n)/n/(np.cos(np.pi/n)-np.cos((p-q)/n))
    b=np.sin(np.pi/n)/n/(np.cos(np.pi/n)-np.cos((p+q)/n))
    f0=np.sin(q)/(np.cos(p)+np.cos(q));g0=-np.sin(p)/(np.cos(p)+np.cos(q))
    both=q>alpha-np.pi
    f0=f0+np.where(both,np.sin(alpha-q)/(np.cos(alpha-p)+np.cos(alpha-q)),0)
    g0=g0-np.where(both,np.sin(alpha-p)/(np.cos(alpha-p)+np.cos(alpha-q)),0)
    return a-b-f0,a+b-g0

def stable_coefficients(phi,phi0,alpha):
    with np.errstate(all='ignore'):f,g=edge_coefficients(phi,phi0,alpha)
    for v in (f,g):
        good=np.isfinite(v)&(np.abs(v)<100)
        if not good.all():v[~good]=np.interp(np.flatnonzero(~good),np.flatnonzero(good),v[good])
    return f,g

def polar_figure(num,alpha_deg,phi0_deg=None):
    stem=STEMS[num];fig,ax=canvas(stem);ax.set_axis_off()
    alpha=np.deg2rad(alpha_deg);p=np.linspace(.000013,alpha-.000019,5001)
    if phi0_deg is None:
        q=np.minimum(p,alpha-p)
        # Symmetry under reflection in the wedge bisector puts incidence in0..pi.
        f,g=stable_coefficients(q+2e-8,q,alpha)
    else:f,g=stable_coefficients(p,np.full_like(p,np.deg2rad(phi0_deg)),alpha)
    # Radius is magnitude; sign is encoded only by the line style, as in pp30--32.
    x1=np.abs(f)*np.cos(p);y1=np.abs(f)*np.sin(p)
    x2=np.abs(g)*np.cos(p);y2=np.abs(g)*np.sin(p)
    ax.plot(x1,y1,'k',lw=1.7,label=r'$f^1<0$')
    ax.plot(np.where(g<0,x2,np.nan),np.where(g<0,y2,np.nan),'k--',lw=1.4,label=r'$g^1<0$')
    ax.plot(np.where(g>=0,x2,np.nan),np.where(g>=0,y2,np.nan),'k-.',lw=1.4,label=r'$g^1>0$')
    maxr=max(np.max(np.abs(f)),np.max(np.abs(g)))
    if alpha_deg<360:
        t=np.linspace(alpha,2*np.pi,120);r=maxr*100
        region=np.vstack([[0,0],np.c_[r*np.cos(t),r*np.sin(t)],[0,0]])
        polygon(ax,region,hatch='////',zorder=-2)
    if num==8: limits=(-.95,4.8,-1.65,1.65);ticks=np.arange(1,5);legendloc=(.78,.91)
    elif num==9: limits=(-1.08,1.13,-.69,.69);ticks=np.arange(.2,1.01,.2);legendloc=(.17,.10)
    elif num==10:limits=(-.63,.94,-1.58,.30);ticks=np.arange(.2,.81,.2);legendloc=(.80,.47)
    elif num==11:limits=(-.68,2.16,-1.20,.91);ticks=np.arange(.5,2.01,.5);legendloc=(.77,.23)
    elif num==12:limits=(-.52,.96,-.94,.61);ticks=np.arange(.2,.81,.2);legendloc=(.78,.23)
    else:limits=(-.52,.63,-.29,.44);ticks=np.arange(.1,.51,.1);legendloc=(.78,.91)
    # Preserve exact source canvas while fitting geometrically without stretching curves.
    xmin,xmax,ymin,ymax=limits;ratio=aspect(stem)
    xmin=min(xmin,float(min(x1.min(),x2.min()))-.07*maxr)
    xmax=max(xmax,float(max(x1.max(),x2.max()))+.07*maxr)
    ymin=min(ymin,float(min(y1.min(),y2.min()))-.07*maxr)
    ymax=max(ymax,float(max(y1.max(),y2.max()))+.07*maxr)
    spanx=xmax-xmin;spany=ymax-ymin
    if spany/spanx<ratio:
        extra=(spanx*ratio-spany)/2;ymin-=extra;ymax+=extra
    else:
        extra=(spany/ratio-spanx)/2;xmin-=extra;xmax+=extra
    ax.set_xlim(xmin,xmax);ax.set_ylim(ymin,ymax);ax.set_aspect('equal')
    arrow(ax,(0,0),(max(ticks)*1.10,0),lw=.8)
    label(ax,-.035*maxr,-.05*maxr,'0',fontsize=8)
    for v in ticks:
        stroke(ax,[(v,-.012*maxr),(v,.012*maxr)],lw=.6);label(ax,v,.045*maxr,f'{v:g}',fontsize=8)
    if alpha_deg<360:
        end=np.array([np.cos(alpha),np.sin(alpha)])
        step=.2 if num in [10,12] else .5 if num==11 else .2
        for v in np.arange(step,(1.0 if num==11 else maxr)+.01,step):
            pos=v*end;label(ax,pos[0]-.05*maxr,pos[1],f'{v:g}',fontsize=8)
    if phi0_deg is not None:
        q=np.deg2rad(phi0_deg);arrow(ax,(.28*maxr*np.cos(q),.28*maxr*np.sin(q)),(0,0),lw=1)
        ar=(.09 if num==10 else .14)*maxr
        t=np.linspace(0,q,100);ax.plot(ar*np.cos(t),ar*np.sin(t),'k',lw=.7)
        label(ax,.19*maxr*np.cos(q*.55),.19*maxr*np.sin(q*.55),r'$\varphi_0$',fontsize=9)
    # Compact sign key matches the original legends.
    lx=xmin+(xmax-xmin)*(legendloc[0]-.13);ly=ymin+(ymax-ymin)*legendloc[1]
    styles=[('-',r'$f^1<0$'),('--',r'$g^1<0$')]
    if num in [8,10]:styles.append(('-.',r'$g^1>0$'))
    for j,(ls,txt) in enumerate(styles):
        yy=ly-j*(ymax-ymin)*.065;ax.plot([lx,lx+.12*(xmax-xmin)],[yy,yy],'k',ls=ls,lw=1.5);label(ax,lx+.14*(xmax-xmin),yy,txt,ha='left',fontsize=9,bbox=dict(facecolor='white',edgecolor='none',pad=.4))
    # Angle labels in the original vary between caption and inset.
    txt=fr'$\alpha={alpha_deg}^\circ$'
    if phi0_deg is not None:txt=fr'$\varphi_0={phi0_deg}^\circ,\quad$'+txt
    if num==9:
        ax.text(.11,.19,txt,transform=ax.transAxes,ha='left',fontsize=9)
    else:ax.text(.67,.04 if num==8 else .08,txt,transform=ax.transAxes,ha='center',fontsize=9,bbox=dict(facecolor='white',edgecolor='none',pad=.5))
    save(fig,num,'Polar magnitude diagrams of the nonuniform-current diffraction coefficients',['4.07','4.08','4.09','4.10'],method='analytic',details={'alpha_degrees':alpha_deg,'incident_angle_degrees':phi0_deg,'monostatic':phi0_deg is None,'radius':'absolute coefficient; signs encoded by solid/dashed/dash-dot styles','singularities':'Removable cancellations avoided by offset sampling and finite-value interpolation only.'})

def fig14():
    fig,ax=drawing(14);o=(.25,.43)
    polygon(ax,[o,(.48,.85),(.93,.85),(.70,.43)],hatch='////')
    polygon(ax,[o,(.70,.43),(.70,.10)],hatch='||||')
    stroke(ax,[(.70,.10),(.94,.45)],lw=1.2)
    arrow(ax,o,(.80,.43));label(ax,.79,.39,r'$x$')
    arrow(ax,o,(.25,.97));label(ax,.28,.96,r'$y$')
    arrow(ax,o,(.04,.08));label(ax,.025,.06,r'$z$')
    stroke(ax,[(.10,.79),o,(.44,.06)],lw=1.4)
    arc(ax,o,.16,.23,220,309);label(ax,.26,.18,r'$\gamma$')
    label(ax,.22,.46,'O')
    save(fig,14,'Oblique plane-wave incidence on a conducting wedge; gamma measured to the edge')

def fig15():
    fig,ax=drawing(15);ap=(.45,.20);center=(.45,.76);rx=.35;ry=.105
    # Rays on a cone, shown by its projected elliptical cross-section.
    for t in np.linspace(0,2*np.pi,15,endpoint=False):
        q=np.array([center[0]+rx*np.cos(t),center[1]+ry*np.sin(t)])
        arrow(ax,ap,tuple(ap+1.12*(q-ap)),lw=.8)
    ax.add_patch(Ellipse(center,rx*2,ry*2,fill=False,edgecolor='black',lw=1.4))
    arrow(ax,(.45,.03),(.45,.98),lw=1.2);label(ax,.48,.975,r'$z$')
    stroke(ax,[(.32,.025),ap,(.80,.76)],lw=1.2)
    arc(ax,ap,.10,.11,243,270);label(ax,.395,.07,r'$\gamma$')
    q=(.80,.76);arrow(ax,q,(.96,.76));label(ax,.96,.79,r'$\mathbf{e}_r$')
    arrow(ax,q,(.93,.88));label(ax,.91,.91,r'$\mathbf{e}_\varphi$')
    arrow(ax,q,(.94,.68));label(ax,.95,.65,r'$\mathbf{e}_\gamma$')
    save(fig,15,'Cone of diffracted rays and local transverse basis',['5.15','5.16'])

def fig16():
    fig,ax=drawing(16);o=(.18,.39)
    arrow(ax,(.18,.06),(.18,.97),lw=1.1);label(ax,.145,.96,r'$y$')
    arrow(ax,o,(.95,.39));label(ax,.94,.35,r'$x$')
    stroke(ax,[(.18,.12),(.18,.83)],lw=2.6)
    dot(ax,(.18,.83),r'$a$',(-.05,0));dot(ax,(.18,.12),r'$-a$',(-.05,0))
    arrow(ax,o,(.82,.94));label(ax,.85,.94,r'$P$');label(ax,.53,.71,r'$r$')
    arrow(ax,o,(.80,.60));label(ax,.83,.60,r'$\mathbf{n}$')
    ray_arc(ax,o,(.95,.39),(.80,.60),.25,r'$\alpha$')
    ray_arc(ax,o,(.95,.39),(.82,.94),.18)
    label(ax,.36,.52,r'$\varphi$',bbox=dict(facecolor='white',edgecolor='none',pad=.3))
    save(fig,16,'Strip cross-section, incidence normal and observation coordinates')

def disk_base(ax,oblique=False):
    o=np.array([.23,.47]);ax.add_patch(Ellipse(o,.27,.81,facecolor='white',edgecolor='black',hatch='////',lw=1.2))
    arrow(ax,(.23,.04),(.23,.98));label(ax,.25,.975,r'$y$')
    arrow(ax,o,(.80,.47));label(ax,.82,.47,r'$z$')
    arrow(ax,o,(.55,.88));label(ax,.57,.90,r'$x$')
    q=np.array([.12,.64]);arrow(ax,o,q);label(ax,.12,.59,r'$\rho$')
    arc(ax,o,.09,.13,50,145);label(ax,.18,.61,r'$\psi$')
    return o,q

def fig17():
    fig,ax=drawing(17);o,q=disk_base(ax)
    p=(.94,.82);arrow(ax,o,p,lw=1.3);arrow(ax,q,p,lw=1.0)
    label(ax,.63,.65,r'$R$');label(ax,.62,.80,r'$r$');label(ax,.94,.86,r'$P(x,y,z)$',ha='right',fontsize=9)
    ray_arc(ax,o,(.80,.47),p,.22,r'$\vartheta$')
    save(fig,17,'Disk surface point and observation point geometry',['7.03','7.04','7.05'])

def fig18():
    fig,ax=drawing(18);ax.set_aspect('equal');o=(.43,.48);r=.33
    ax.add_patch(Ellipse(o,2*r,2*r,fill=False,lw=1.3,edgecolor='black'))
    arrow(ax,(.04,.48),(.96,.48));arrow(ax,(.43,.05),(.43,.95));label(ax,.96,.44,r'$x$');label(ax,.40,.95,r'$y$')
    for a in [20,62]:
        t=np.deg2rad(a);stroke(ax,[o,(o[0]+r*np.cos(t),o[1]+r*np.sin(t))],lw=1.1)
    t=np.deg2rad(41);arrow(ax,o,(o[0]+.41*np.cos(t),o[1]+.41*np.sin(t)))
    arc(ax,o,.13,.13,20,62);label(ax,.55,.60,r'$2\Phi_0$')
    arc(ax,o,.42,.42,0,41);label(ax,.82,.72,r'$\psi=\varphi$',rotation=32,fontsize=9)
    label(ax,.10,.445,r'$a$')
    save(fig,18,'Luminous disk sector bounded by the first Fresnel zone',['7.14','7.15','7.16'])

def aperture_base(ax):
    # Auxiliary tangent half-plane L, disk silhouette shown as a clear oval.
    plane=[(.10,.06),(.10,.71),(.64,.94),(.69,.25)]
    polygon(ax,plane,hatch='////')
    ax.add_patch(Ellipse((.38,.49),.27,.72,facecolor='white',edgecolor='black',lw=1.1))
    o=np.array([.38,.49])
    arrow(ax,(.38,.08),(.38,.98));label(ax,.40,.98,r'$y_1$')
    arrow(ax,o,(.90,.49));label(ax,.93,.49,r'$z$')
    arrow(ax,o,(.78,.91));label(ax,.81,.93,r'$x$')
    arrow(ax,(.18,.3692),(.86,.78));label(ax,.89,.79,r'$x_1$')
    arrow(ax,o,(.28,.95));label(ax,.25,.96,r'$y$')
    label(ax,.15,.70,r'$L$')
    return o

def fig19():
    fig,ax=drawing(19);o=aperture_base(ax)
    ray_arc(ax,o,(.78,.91),(.38,.98),.16,r'$\psi$')
    save(fig,19,'Disk and auxiliary half-plane tangent at y1=a, x1=0')

def fig22():
    fig,ax=drawing(22);o,q=disk_base(ax,True)
    p=(.95,.86);arrow(ax,o,p,lw=1.2);label(ax,.64,.72,r'$R$');label(ax,.96,.89,r'$P(x,y,z)$',ha='right',fontsize=9)
    arrow(ax,o,(.86,.62));label(ax,.89,.63,r'$\mathbf{n}$')
    ray_arc(ax,o,(.80,.47),(.86,.62),.34,r'$\gamma$')
    ray_arc(ax,o,(.80,.47),p,.23)
    label(ax,.50,.60,r'$\vartheta$',bbox=dict(facecolor='white',edgecolor='none',pad=.3))
    save(fig,22,'Obliquely incident plane wave and spherical disk observation geometry',['10.01'])

def fig23():
    fig,ax=drawing(23);o=aperture_base(ax)
    p=(.96,.77);q=(.76,.61);arrow(ax,o,p);stroke(ax,[q,p],ls='--',lw=.9);arrow(ax,o,q)
    label(ax,.76,.69,r'$R$');label(ax,.69,.565,r'$r_1$',bbox=dict(facecolor='white',edgecolor='none',pad=.3));label(ax,.98,.835,r'$P(x,y,z)$',ha='right',fontsize=9)
    label(ax,.80,.60,r'$p(y_1,z)$',ha='left',fontsize=9)
    ray_arc(ax,o,(.90,.49),q,.40,r'$\varphi_1$',text_scale=1.12)
    ray_arc(ax,o,(.90,.49),p,.31)
    label(ax,.715,.54,r'$\vartheta$',bbox=dict(facecolor='white',edgecolor='none',pad=.3))
    ray_arc(ax,o,(.78,.91),(.38,.98),.16,r'$\psi_1$')
    save(fig,23,'Auxiliary half-plane and projected observation coordinates for oblique incidence',['11.06','11.10','11.14'])

# Manual readings of the solid rigorous-theory curves in source Figs20/21.
# The mirrored half is fixed by source symmetry. Values are not exact data from[34].
RIGOROUS={
20:{'theta':[0,10,20,30,40,45,50,60,75,90],
    'magnitude':[1.0,.915,.685,.405,.185,.120,.092,.113,.125,.124],
    'phase':[3,5,9,18,43,65,96,141,164,168]},
21:{'theta':[0,10,20,30,35,40,45,50,60,75,90],
    'magnitude':[1.0,.910,.675,.350,.230,.170,.160,.154,.148,.145,.145],
    'phase':[1,4,10,18,32,56,82,106,124,132,134]},
}

def disk_comparison(num):
    stem=STEMS[num];fig=plt.figure(figsize=(6,6*aspect(stem)));ax=fig.add_axes([.12,.085,.76,.85]);ax2=ax.twinx()
    deg=np.linspace(.00001,179.99999,1801);t=np.deg2rad(deg);u=np.minimum(t,np.pi-t);ka=5.
    a=jv(1,ka*np.sin(t))/(ka*np.sin(u/2));b=jv(2,ka*np.sin(t))/(ka*np.cos(u/2))
    approximate=a+(-1j if num==20 else 1j)*b
    magnitude=np.abs(approximate);phase=np.abs(np.rad2deg(np.angle(approximate)))
    po=2*jv(1,ka*np.sin(t))/(ka*np.sin(t))
    if num==21:po*=np.cos(t)
    ax.plot(deg,np.abs(po),'k-.',lw=1.3,label='Physical optics: Eq.7.11')
    ax.plot(deg,magnitude,'k--',lw=1.4,label='Edge-wave approximation: Eqs.9.03/9.05')
    knots=RIGOROUS[num];fold=np.minimum(deg,180-deg)
    rigmag=PchipInterpolator(knots['theta'],knots['magnitude'])(fold)
    rigphase=PchipInterpolator(knots['theta'],knots['phase'])(fold)
    ax.plot(deg,rigmag,'k',lw=1.7,label='Published rigorous-theory magnitude: manually digitized')
    ax2.plot(deg,phase,'k--',lw=1.4,label='Approximate phase from Eqs.9.03/9.05')
    ax2.plot(deg,rigphase,'k',lw=1.7,label='Published rigorous-theory phase: manually digitized')
    ax.set_xlim(0,180);ax.set_ylim(0,1.2);ax.set_xticks(np.arange(0,181,30));ax.set_xticks(np.arange(0,181,10),minor=True)
    ax.set_yticks([0,.5,1.0]);ax.set_yticks(np.arange(0,1.201,.05),minor=True)
    ax.set_xticklabels([fr'${v}^\circ$' for v in range(0,181,30)])
    ax.grid(which='both',color='black',lw=.5,alpha=.65)
    # Printed right-hand phase scale has 0/90/180 at three aligned grid rows.
    ax2.set_ylim((230,-10) if num==20 else (-50,190));ax2.set_yticks([0,90,180]);ax2.set_yticklabels([r'$0^\circ$',r'$90^\circ$',r'$180^\circ$'])
    idx=1 if num==20 else 2
    ax.text(-.09,1.035,fr'$|V^{{({idx})}}(\vartheta)|$',transform=ax.transAxes,ha='left',fontsize=10)
    ax.text(.51,1.035,r'$ka=5$',transform=ax.transAxes,ha='center',fontsize=10)
    ax2.text(1.02,1.035,fr'$\arg V^{{({idx})}}(\vartheta)$',transform=ax.transAxes,ha='right',fontsize=9)
    ax.text(1.03,-.05,r'$\vartheta$',transform=ax.transAxes,ha='right',fontsize=11)
    ax.text(75,.17 if num==20 else .19,fr'$|V^{{({idx})}}(\vartheta)|$',fontsize=10,bbox=dict(facecolor='white',edgecolor='none',pad=1))
    ax2.text(71,150 if num==20 else 159,fr'$\arg V^{{({idx})}}(\vartheta)$',fontsize=10,bbox=dict(facecolor='white',edgecolor='none',pad=1))
    if num==21:ax2.text(118,176,r'$\arg V^{(2)}(\vartheta)+180^\circ$',fontsize=8,ha='center',bbox=dict(facecolor='white',edgecolor='none',pad=1))
    save(fig,num,'Disk diffraction magnitude/phase at ka=5: analytic physical optics and edge-wave approximation with manually digitized rigorous reference',['7.11','9.03','9.05','9.07'],method='mixed',details={'analytic_curves':['dash-dot physical-optics magnitude','dashed edge-wave magnitude and phase'],'digitized_curves':['solid rigorous-theory magnitude','solid rigorous-theory phase'],'digitized_control_points':knots,'digitization':'Manual visual readings of source grid, reflected about90 degrees and PCHIP-interpolated. Source does not supply numerical reference34 data; these solid curves are approximate reconstructions, not new exact computations.','phase_display':'Magnitude of phase; right-half V2 phase shown with180-degree branch adjustment as source labels.'})

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--figures',nargs='*',type=int);args=parser.parse_args()
    jobs={1:fig1,2:fig2,3:fig3,4:fig4,5:fig5,6:fig6,7:fig7,
    8:lambda:polar_figure(8,360,150),9:lambda:polar_figure(9,360),
    10:lambda:polar_figure(10,270,30),11:lambda:polar_figure(11,270,150),
    12:lambda:polar_figure(12,270),13:lambda:polar_figure(13,210),14:fig14,
    15:fig15,16:fig16,17:fig17,18:fig18,19:fig19,20:lambda:disk_comparison(20),
    21:lambda:disk_comparison(21),22:fig22,23:fig23}
    for n in args.figures or range(1,24):jobs[n]()

if __name__=='__main__':main()
