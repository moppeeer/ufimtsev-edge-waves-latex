"""Regenerate and verify all83 vector assets, then optionally update LaTeX paths.

Usage: python python_figures/build_all.py [--verify-only] [--integrate]
Run from any directory. All inputs are local; no network calls are made.
"""
from __future__ import annotations
import argparse
import importlib.metadata
import json
import re
import runpy
import sys
from pathlib import Path
from common import PROJECT, ORIGINAL, OUTPUT, aspect
from pypdf import PdfReader

def category(method):
    method=method.lower()
    if 'tracing' in method:return 'vector-traced-artwork'
    if 'decorative' in method:return 'decorative-redraw'
    if 'mixed' in method:return 'calculated-and-digitized'
    if 'digit' in method:return 'digitized'
    if 'analytic' in method or 'formula' in method:return 'calculated'
    return 'geometric-redraw'

def main():
    p=argparse.ArgumentParser();p.add_argument('--verify-only',action='store_true');p.add_argument('--integrate',action='store_true');args=p.parse_args()
    here=Path(__file__).resolve().parent
    if not args.verify_only:
        original_argv=sys.argv[:]
        for script in ['figures_a.py','figures_b.py','figures_c.py','figures_root.py']:
            sys.argv=[str(here/script)]
            runpy.run_path(str(here/script),run_name='__main__')
        sys.argv=original_argv
    metadata=[];issues=[]
    originals=sorted(ORIGINAL.glob('*.png'))
    for source in originals:
        stem=source.stem
        for ext in ['pdf','svg','png','json']:
            if not (OUTPUT/f'{stem}.{ext}').exists():issues.append(f'Missing {stem}.{ext}')
        if issues and not (OUTPUT/f'{stem}.json').exists():continue
        meta=json.loads((OUTPUT/f'{stem}.json').read_text(encoding='utf-8'))
        pdf=PdfReader(OUTPUT/f'{stem}.pdf')
        if len(pdf.pages)!=1:issues.append(f'{stem}: expected one PDF page')
        page=pdf.pages[0]
        if len(page.images):issues.append(f'{stem}: PDF contains raster images')
        pdf_ratio=float(page.mediabox.height)/float(page.mediabox.width)
        if abs(pdf_ratio/aspect(stem)-1)>1e-4:issues.append(f'{stem}: changed canvas aspect ratio')
        svg=(OUTPUT/f'{stem}.svg').read_text(encoding='utf-8')
        if re.search(r'<(?:\w+:)?image\b',svg):issues.append(f'{stem}: SVG contains raster images')
        if meta.get('text_outside_canvas'):issues.append(f'{stem}: text outside canvas: {meta["text_outside_canvas"]}')
        meta['category']=category(meta['method'])
        meta['verification']={'one_pdf_page':len(pdf.pages)==1,'raster_objects':len(page.images),'aspect_relative_error':abs(pdf_ratio/aspect(stem)-1),'text_outside_canvas':meta.get('text_outside_canvas',[])}
        metadata.append(meta)
    ids=[m['figure'] for m in metadata if m.get('figure') is not None]
    if sorted(ids)!=list(range(1,81)):issues.append('Numbered figure coverage is not exactly1..80')
    if len(originals)!=83:issues.append(f'Expected83 original assets, got{len(originals)}')
    summary={}
    for m in metadata:summary[m['category']]=summary.get(m['category'],0)+1
    manifest={'total_assets':len(metadata),'numbered_figures':80,'source_aspect_preserved':True,
              'categories':summary,'issues':issues,'status':'pass' if not issues else 'fail',
              'runtime_versions':{name:importlib.metadata.version(name) for name in ['numpy','scipy','matplotlib','Pillow','scikit-image','pypdf']},'figures':metadata}
    (PROJECT/'figures-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in manifest.items() if k!='figures'},ensure_ascii=True,indent=2))
    if issues:raise SystemExit(1)
    if args.integrate:
        replaced=0
        for path in sorted((PROJECT/'transcription').glob('page-*.tex')):
            old=path.read_text(encoding='utf-8');new=old
            for source in originals:
                ref=f'images/{source.name}'
                replaced+=new.count(ref)
                new=new.replace(ref,f'images/recreated/{source.stem}.pdf')
            if new!=old:path.write_text(new,encoding='utf-8')
        print(f'Updated{replaced} LaTeX image references to vector PDFs.')

if __name__=='__main__':main()
