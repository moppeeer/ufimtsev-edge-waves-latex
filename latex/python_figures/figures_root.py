"""Figures73–80 and cover artwork, rebuilt as vector Matplotlib figures.

Theoretical wire curves are evaluated from the book, not fitted. Other authors'
comparison curves and the static-cylinder reference are approximate digitizations
of the printed plots. Anchors below are editable and exported in data JSON files.
"""
from common import *
from wire_model import normal_F, sigma_normalized, integral_normalized
from scipy.interpolate import PchipInterpolator
from matplotlib.patches import Arc, Polygon, PathPatch
from matplotlib.path import Path as MplPath
from matplotlib.ticker import MultipleLocator, LogLocator, NullFormatter
from skimage.measure import find_contours, approximate_polygon

STEMS={73:'r-0204-fig73',74:'r-0208-fig74',75:'r-0221-fig75',76:'r-0226-fig76',
       77:'r-0228-fig77',78:'r-0228-fig78',79:'r-0229-fig79',80:'r-0230-fig80'}

def grid(ax,minor=True):
    ax.grid(True,which='major',color='.55',lw=.65)
    if minor: ax.grid(True,which='minor',color='.80',lw=.4)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=9)

def digitized(ax,x,y,*,ls='-',label_=None,lw=1.4):
    xx=np.linspace(x[0],x[-1],1600)
    yy=PchipInterpolator(x,y)(xx)
    ax.plot(xx,yy,ls,color='black',lw=lw,label=label_)

def figures73_74():
    for n in [73,74]:
        stem=STEMS[n]
        fig,ax=canvas(stem)
        h=aspect(stem)
        y=h*.28
        ax.plot([.10,.70,.71,.70,.10],[y-.012,y-.012,y,y+.012,y+.012],color='black',lw=1.4)
        arrow(ax,(.02,y),(.93,y)); label(ax,.96,y,r'$z$')
        if n==73:
            start=np.array([.36,y]); tip=np.array([.62,h*.82])
            arrow(ax,tip,start,lw=1.3)
            ax.add_patch(Arc(start,.19,.19,theta1=0,theta2=51,lw=.8))
            label(ax,.49,y+.065,r'$\vartheta_0$')
            ax.plot([.1,.1],[y-.02,y-.09],color='black',lw=.7)
            ax.plot([.70,.70],[y-.02,y-.09],color='black',lw=.7)
            arrow(ax,(.1,y-.08),(.7,y-.08),style='<->',lw=.8)
            label(ax,.40,y-.095,r'$L$',bbox=dict(fc='white',ec='none',pad=1))
            label(ax,.10,y+.045,r'$z_1$'); label(ax,.70,y+.045,r'$z_2$')
            p=tip+np.array([-.005,.01]); e=p+np.array([.19,-.035])
            arrow(ax,p,e,lw=1.3); label(ax,e[0]-.02,e[1]+.055,r'$\mathbf{E}_0$')
            ax.plot([p[0],p[0]+.16,e[0]],[p[1],p[1]-.11,e[1]],'k--',lw=.8)
            label(ax,p[0]+.08,p[1]-.06,r'$\alpha$')
        else:
            p=np.array([.65,h*.79]); origin=np.array([.38,y])
            arrow(ax,origin,p,lw=1.2)
            label(ax,.48,y+.20,r'$R$')
            ax.add_patch(Arc(origin,.18,.18,theta1=0,theta2=52,lw=.8))
            label(ax,.48,y+.058,r'$\vartheta$')
            arrow(ax,p,p+np.array([-.075,.075]),lw=1.3)
            label(ax,p[0]-.10,p[1]+.075,r'$\mathbf{p}_1$'); label(ax,p[0]+.02,p[1],r'$1$')
            ax.add_patch(Arc((.27,y),.055,.11,theta1=45,theta2=320,ls='--',lw=.8))
            label(ax,.27,y+.075,r'$2$'); label(ax,.27,y-.08,r'$j^m_{2\varphi}$')
        finish(fig,stem,figure=n,method='geometric-redraw',description='Wire and electromagnetic excitation geometry redrawn with vector paths and mathematical labels.')

def fig75():
    stem=STEMS[75]; fig,ax=canvas(stem,plot=True)
    x=np.linspace(6,16,900)
    # Approximate points read from the solid curve in the printed Fig75.
    xd=[6,7,8,9,10,11,12,13,14,15,16]
    yd=[.330,.301,.276,.257,.242,.229,.219,.210,.203,.196,.190]
    digitized(ax,xd,yd,label_='1')
    ax.plot(x,1/(3*(np.log(4*x)-7/3)),'k--',label='2')
    ax.set(xlim=(6,16),ylim=(.15,.35),xlabel=r'$l$',ylabel=r'$D(l)$')
    ax.set_xticks([7,9,11,13,15]); ax.xaxis.set_minor_locator(MultipleLocator(.5))
    ax.set_yticks([.15,.20,.25,.30,.35]); ax.yaxis.set_minor_locator(MultipleLocator(.01)); grid(ax)
    finish(fig,stem,figure=75,method='mixed-formula-and-digitized',equations=['33.04'],
           description='Dashed curve evaluated from33.04; solid electrostatic-cylinder result of reference92 digitized from the printed curve.',
           details={'reference_anchors':{'l':xd,'D':yd},'digitization':'Visual control points; not original experimental or tabulated data.'})

def fig76():
    stem=STEMS[76];fig,ax=canvas(stem,plot=True)
    r=np.linspace(.16,3.,5000)
    for chi in [-.1,-.05]:
        ax.plot(r,integral_normalized(r,chi),'k:',lw=1.55,label='2' if chi==-.1 else None)
    # Leontovich/Levin comparison curves, read on the logarithmic printed axes.
    xr=[.2,.27,.34,.39,.43,.455,.48,.50,.53,.57,.65,.8,1.,1.2,1.35,1.42,1.47,1.50,1.55,1.65,1.8,2.,2.2,2.35,2.42,2.46,2.49,2.54,2.65,2.8,3.]
    upper=[.0013,.006,.027,.12,.55,1.55,2.05,1.75,.95,.50,.27,.13,.068,.055,.068,.11,.21,.205,.13,.065,.044,.035,.029,.033,.045,.058,.058,.035,.023,.018,.014]
    lower=[.0003,.0018,.008,.045,.25,.85,2.0,1.8,.52,.21,.079,.026,.014,.012,.014,.024,.14,.15,.040,.015,.010,.0084,.0073,.0085,.013,.038,.045,.014,.0085,.0065,.0054]
    for j,y in enumerate([upper,lower]):
        rr=np.linspace(xr[0],xr[-1],2400)
        ax.plot(rr,10**PchipInterpolator(xr,np.log10(y))(rr),'k-',lw=1.2,label='1' if j==0 else None)
    ax.set(xlim=(0,3),ylim=(1e-4,10),yscale='log',xlabel=r'$L/\lambda$',ylabel=r'$S/L^2$')
    ax.set_xticks(np.arange(0,3.1,.5));ax.yaxis.set_minor_formatter(NullFormatter());grid(ax,False)
    top=ax.secondary_xaxis('top',functions=(lambda r:np.pi*r,lambda x:x/np.pi))
    top.set_xticks(np.arange(1,7)*np.pi/2,labels=[r'$\pi/2$',r'$\pi$',r'$3\pi/2$',r'$2\pi$',r'$5\pi/2$',r'$3\pi$']);top.set_xlabel(r'$kL/2$')
    # Keep parameter labels in open space, clear of both the curves and peaks.
    ax.text(1.98,.050,r'$\chi=-0.1$',fontsize=9)
    ax.text(1.98,.0043,r'$\chi=-0.05$',fontsize=9)
    handles,labels_=ax.get_legend_handles_labels();ax.legend(handles[::-1],labels_[::-1],loc='upper center',frameon=False)
    finish(fig,stem,figure=76,method='mixed-formula-and-digitized',equations=['28.21','32.08','34.07'],
           description='Curve2 computed directly for chi=-0.1 and-0.05; curve1 reference85 reconstructed from visually digitized logarithmic plot anchors.',
           details={'comparison_x':xr,'comparison_y':[upper,lower],'comparison_uncertainty':'Approximate reading of a thick printed curve on logarithmic axes.'})

def lindroth_anchors():
    return ([0,.25,.31,.35,.39,.42,.45,.465,.477,.49,.51,.54,.59,.67,.78,.95,1.1,1.25,1.32,1.37,1.42,1.46,1.48,1.52,1.58,1.67,1.78,1.90,2.05,2.15,2.25,2.33,2.37,2.40,2.43,2.48,2.5],
            [0,.08,.3,1.2,4,10,24,37,39,30,15,7,4.7,3.8,3.7,3.9,3.9,3.7,4.3,7,23,32,32.5,28,23,21.5,21,21.6,21.5,20.7,18,16,19,30,51,65,65])

def vanvleck_anchors():
    return ([0,.25,.34,.4,.45,.48,.50,.52,.56,.64,.78,1,1.17,1.3,1.37,1.42,1.46,1.49,1.54,1.60,1.7,1.85,2,2.15,2.3,2.4,2.5],
            [0,.03,.2,1.5,5,22,45,20,8,4.6,3.9,4.1,3.8,2.5,2,5,27,40,27,23,21.5,22,24,26,28,32,45])

def fig77():
    stem=STEMS[77];fig,ax=canvas(stem,plot=True)
    x1,y1=lindroth_anchors();x2,y2=vanvleck_anchors()
    digitized(ax,x1,y1,label_='1');digitized(ax,x2,y2,ls='-.',label_='2')
    r=np.linspace(.08,2.5,6000);x=2*np.pi*r;b=2*x*np.exp(-7.5)
    ax.plot(r,100*3/(8*np.pi)*np.abs(normal_F(x,b))**2,'k:',label='3',lw=1.65)
    ax.set(xlim=(0,2.5),ylim=(0,50),xlabel=r'$L/\lambda$',ylabel=r'$100\,\overline{\sigma}/\lambda^2$')
    ax.xaxis.set_major_locator(MultipleLocator(.5));ax.xaxis.set_minor_locator(MultipleLocator(.125))
    ax.yaxis.set_major_locator(MultipleLocator(10));ax.yaxis.set_minor_locator(MultipleLocator(2));grid(ax)
    top=ax.secondary_xaxis('top',functions=(lambda r:np.pi*r,lambda x:x/np.pi));top.set_xticks([1,3,5,7]);top.set_xlabel(r'$kL/2$')
    ax.legend(frameon=True,facecolor='white',edgecolor='none',loc='upper center')
    finish(fig,stem,figure=77,method='mixed-formula-and-digitized',equations=['28.21','32.08','34.12'],
           description='Curve3 computed with Omega_p=15. Comparison1(Lindroth79) and2(VanVleck86) digitized from the original plot; plotted ordinate is100sigma/lambda².',
           details={'Omega_p':15,'comparison_1':{'x':x1,'y':y1},'comparison_2':{'x':x2,'y':y2},'digitization':'Shape-preserving interpolation of manually read control points, including the separated second/third resonance branches.'})

def fig78():
    stem=STEMS[78];fig,ax=canvas(stem,plot=True)
    f=np.linspace(1800,12000,6000);r=f/6000.;x=2*np.pi*r
    wave_cm=30000/f
    ax.plot(f,3/(8*np.pi)*np.abs(normal_F(x,2*x*np.exp(-7.5)))**2*wave_cm**2,'k:',lw=1.65,label='2')
    # Directly digitized reference79 curve from Fig78, in MHz and cm².
    xf=[1800,2200,2450,2600,2700,2800,2850,2900,3000,3150,3350,3600,4000,5000,6000,7000,8000,8500,8750,9000,9300,9600,10000,11000,12000]
    yf=[.6,2,5,12,26,37,35,26,14,7,4,3,2.3,1.7,1.4,1.15,.95,1.1,2.3,4.0,3.4,2.7,2.2,1.6,1.4]
    digitized(ax,xf,yf,label_='1',lw=1.4)
    ax.set(xlim=(0,12000),ylim=(0,50),xlabel=r'$f\;(\mathrm{MHz})$',ylabel=r'$\overline{\sigma}\;(\mathrm{cm}^2)$')
    ax.xaxis.set_major_locator(MultipleLocator(2000));ax.xaxis.set_minor_locator(MultipleLocator(2000/3))
    ax.yaxis.set_major_locator(MultipleLocator(10));ax.yaxis.set_minor_locator(MultipleLocator(10/3));grid(ax)
    ax.text(6500,44,r'$L=5\,\mathrm{cm}$'+'\n'+r'$2\ln(2L/a)=15$',bbox=dict(fc='white',ec='none',pad=3),ha='center')
    finish(fig,stem,figure=78,method='mixed-formula-and-digitized',equations=['28.21','32.08','34.12'],
           description='Dotted curve calculated for L=5cm, Omega_p=15, with frequency converted fromMHz. Solid reference79 trace digitized separately.',
           details={'length_cm':5,'Omega_p':15,'comparison_MHz':xf,'comparison_cm2':yf})

def symmetric_curve(ax,angle,values,style,label_):
    aa=np.r_[angle,180-np.asarray(angle[-2::-1])]
    vv=np.r_[values,np.asarray(values[-2::-1])]
    digitized(ax,aa.tolist(),vv.tolist(),ls=style,label_=label_)

def figs79_80():
    for n,r in [(79,.5),(80,2.)]:
        stem=STEMS[n];fig,ax=canvas(stem,plot=True)
        theta=np.linspace(0,np.pi,3601);x=2*np.pi*r;b=x/900
        analytic=sigma_normalized(theta,x,b)
        if n==79:
            aa=[0,10,20,30,40,50,60,70,80,90]
            y1=[0,.0003,.003,.011,.032,.072,.124,.182,.224,.238]
            y3=[0,.0004,.004,.017,.052,.108,.187,.264,.309,.320]
            y4=[0,.0004,.006,.022,.070,.145,.245,.330,.371,.380]
            ymax=.38;major=.1;minor=.02
        else:
            aa=[0,10,15,20,25,30,34,36,40,45,50,55,60,65,70,75,80,85,90]
            y1=[0,.01,.035,.10,.25,.45,.565,.57,.47,.25,.075,.025,.016,.025,.045,.053,.035,.10,.21]
            y3=[0,.012,.04,.14,.34,.60,.72,.735,.60,.35,.11,.025,.006,.04,.12,.14,.12,.17,.22]
            y4=[0,.018,.06,.20,.50,.96,1.08,1.04,.72,.30,.055,.004,.01,.03,.14,.14,.14,.19,.24]
            ymax=1.1;major=.1;minor=.05
        symmetric_curve(ax,aa,y1,'-','1')
        ax.plot(np.degrees(theta),analytic,'k:',lw=1.7,label='2')
        symmetric_curve(ax,aa,y3,'-.','3');symmetric_curve(ax,aa,y4,'--','4')
        ax.set(xlim=(0,180),ylim=(0,ymax),xlabel=r'$\vartheta\;(\mathrm{deg})$',ylabel=r'$\overline{\sigma}(\vartheta)/\lambda^2$')
        ax.xaxis.set_major_locator(MultipleLocator(30));ax.xaxis.set_minor_locator(MultipleLocator(10 if n==79 else 15))
        ax.yaxis.set_major_locator(MultipleLocator(major));ax.yaxis.set_minor_locator(MultipleLocator(minor));grid(ax)
        ax.legend(loc='upper left',frameon=False,ncol=2)
        finish(fig,stem,figure=n,method='mixed-formula-and-digitized',equations=['28.21','32.08','32.09','34.12'],
               description='Curve2 computed from the book. Published comparison curves1(Tai),3(induced emf),4(VanVleck) are symmetric digitizations from the printed figure.',
               details={'L_over_lambda':r,'L_over_a':900,'reference_angles_deg':aa,'curve_1':y1,'curve_3':y3,'curve_4':y4,'calculated_peak':float(analytic.max())})

def cover():
    stem='a-0000-cover-graph';fig,ax=canvas(stem)
    h=aspect(stem)
    fig.patch.set_facecolor('#0958c5');ax.set_facecolor('#0958c5')
    for xx in np.linspace(.02,.98,9):ax.plot([xx,xx],[.02*h,.98*h],color='white',lw=1.5)
    for yy in np.linspace(.02*h,.98*h,7):ax.plot([.02,.98],[yy,yy],color='white',lw=1.5)
    x=np.linspace(.026,.976,6000);u=(x-.026)/.95
    base=PchipInterpolator([0,.02,.08,.15,.25,.4,.6,1],[.08,.40,.53,.63,.73,.81,.88,.94])(u)
    ax.plot(x,h*(base+.012*np.sin(40*np.pi*u)),'w-',lw=2.5)
    lower=base-.22+.19*np.log(np.maximum(np.abs(np.sin(20*np.pi*u)),1e-9))
    lower=np.where(lower>.02,lower,np.nan)
    ax.plot(x,h*lower,color='white',lw=1.9,ls=(0,(6,3)))
    finish(fig,stem,method='decorative-geometric-redraw',description='Unlabelled cover motif recreated parametrically as a blue field, white grid, rising oscillatory curve and dashed lobes. Decorative reconstruction, not a scientific data plot.')

def emblems():
    for stem in ['a-0001-emblem1','a-0001-emblem2']:
        with Image.open(ORIGINAL/(stem+'.png')) as im:
            pixels=np.asarray(im.convert('L'));hh,ww=pixels.shape
        mask=np.pad(pixels<150,1)
        contours=find_contours(mask.astype(float),.5,fully_connected='high',positive_orientation='low')
        fig,ax=canvas(stem)
        paths=[]
        for contour in contours:
            if len(contour)<12:continue
            area=abs(np.sum(contour[:,0]*np.roll(contour[:,1],1)-contour[:,1]*np.roll(contour[:,0],1)))/2
            if area<8:continue
            c=approximate_polygon(contour,tolerance=.65)
            xy=np.c_[(c[:,1]-1)/ww,(hh-(c[:,0]-1))/ww]
            codes=np.full(len(xy),MplPath.LINETO);codes[0]=MplPath.MOVETO;codes[-1]=MplPath.CLOSEPOLY
            paths.append(MplPath(xy,codes))
        ax.add_patch(PathPatch(MplPath.make_compound_path(*paths),facecolor='black',edgecolor='none'))
        finish(fig,stem,method='artwork-vector-tracing',description='Historical organizational emblem converted into simplified closed vector contours, preserving the original artwork and lettering; no raster is embedded in the PDF/SVG.',details={'threshold':150,'polygon_tolerance_px':.65,'paths':len(paths)})

def main():
    figures73_74();fig75();fig76();fig77();fig78();figs79_80();cover();emblems()

if __name__=='__main__':main()
