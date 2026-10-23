"""Shared, reproducible Matplotlib export for the Ufimtsev figures.

PDF and SVG exports contain vector geometry and text. PNG files are previews.
The original crop is used only to match the canvas aspect ratio.
"""
from __future__ import annotations
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
WORKSPACE = PROJECT.parents[1]
LOCAL_DEPS = WORKSPACE / 'tmp' / 'figure-deps'
if LOCAL_DEPS.exists():
    sys.path.insert(0, str(LOCAL_DEPS))

import json
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.text import Text
from matplotlib.axis import Axis

ORIGINAL = PROJECT / 'images'
OUTPUT = ORIGINAL / 'recreated'
OUTPUT.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({
    'font.family': 'DejaVu Serif', 'font.size': 10,
    'mathtext.fontset': 'dejavuserif',
    'axes.linewidth': .7, 'lines.linewidth': 1.25,
    'xtick.direction':'in','ytick.direction':'in',
    'pdf.fonttype':42,'ps.fonttype':42,'svg.fonttype':'none',
    'savefig.facecolor':'white', 'figure.facecolor':'white',
})

def aspect(stem):
    with Image.open(ORIGINAL / (stem + '.png')) as im:
        return im.height / im.width

def canvas(stem, *, width=6., plot=False):
    ratio=aspect(stem)
    fig=plt.figure(figsize=(width,width*ratio))
    ax=fig.add_axes([.14,.15,.81,.78] if plot else [.03,.03,.94,.94])
    if not plot:
        ax.set_xlim(0,1)
        ax.set_ylim(0,ratio)
        ax.set_aspect('equal')
        ax.set_axis_off()
    return fig,ax

def arrow(ax,start,end,*,style='->',lw=1.1,ls='-',color='black',**kwargs):
    return ax.annotate('',xy=end,xytext=start,arrowprops=dict(arrowstyle=style,lw=lw,linestyle=ls,color=color,shrinkA=0,shrinkB=0,**kwargs))

def label(ax,x,y,text,**kwargs):
    return ax.text(x,y,text,ha=kwargs.pop('ha','center'),va=kwargs.pop('va','center'),**kwargs)

def finish(fig,stem,*,method,description,figure=None,equations=None,details=None):
    """Export exact canvas (not a changing tight crop) and provenance."""
    fig.canvas.draw()
    renderer=fig.canvas.get_renderer()
    width_px,height_px=fig.canvas.get_width_height()
    outside=[]
    offscale_labels=set()
    for axis in fig.findobj(match=Axis):
        lo,hi=sorted(axis.get_view_interval())
        for tick in axis.get_major_ticks()+axis.get_minor_ticks():
            if not lo-1e-10 <= tick.get_loc() <= hi+1e-10:
                offscale_labels.update([id(tick.label1),id(tick.label2)])
    for item in fig.findobj(match=Text):
        if id(item) not in offscale_labels and item.get_visible() and item.get_text().strip():
            box=item.get_window_extent(renderer)
            if box.x0 < -.5 or box.y0 < -.5 or box.x1 > width_px+.5 or box.y1 > height_px+.5:
                outside.append(item.get_text())
    meta={'asset':stem,'figure':figure,'method':method,'description':description,
          'equations':equations or [],'details':details or {},
          'source_crop':f'images/{stem}.png','vector_outputs':[f'images/recreated/{stem}.pdf',f'images/recreated/{stem}.svg'],
          'text_outside_canvas':outside}
    for ext in ['pdf','svg','png']:
        fig.savefig(OUTPUT/f'{stem}.{ext}',dpi=180,facecolor=fig.get_facecolor())
    (OUTPUT/f'{stem}.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
    data=[]
    for ai,ax in enumerate(fig.axes):
        for li,line in enumerate(ax.lines):
            x=np.asarray(line.get_xdata(),dtype=float)
            y=np.asarray(line.get_ydata(),dtype=float)
            if x.size>1:
                data.append({'axes':ai,'line':li,'label':line.get_label(),
                             'x':[float(v) if np.isfinite(v) else None for v in x],
                             'y':[float(v) if np.isfinite(v) else None for v in y]})
    if data:
        (OUTPUT/f'{stem}.data.json').write_text(json.dumps(data,ensure_ascii=False,allow_nan=False),encoding='utf-8')
    plt.close(fig)
    print(f'{stem}: {method}',flush=True)
    if outside:
        print('  LABELS OUTSIDE CANVAS: '+json.dumps(outside,ensure_ascii=True),flush=True)
    return meta
