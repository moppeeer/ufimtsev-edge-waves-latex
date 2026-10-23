# Ufimtsev: editable LaTeX transcription

This edition transcribes all 242 leaves of the supplied Internet Archive scan.
Text, equations, equation numbers, captions, and references are editable LaTeX.
All 80 numbered illustrations have been recreated as Python-generated vector
figures. Theoretical curves are evaluated from the book where possible;
unavailable external comparison data are explicitly identified as digitizations.
The cover motif is redrawn, and the historical emblems are vector-traced.
Each original scan leaf has its
own source file and produces one output page, including the inserted page
numbered 116a. Original page labels and page boundaries are retained.

The typography and line wrapping are newly set; this is not a pixel replica.
The earlier image-only facsimile is a separate artifact and is not needed to
compile this project.

## Build

From this directory:

```text
tectonic -X compile main.tex
```

Alternatively, compile `main.tex` with XeLaTeX. The required packages are
standard TeX Live/MiKTeX packages. Latin Modern is supplied by the TeX system;
the DejaVu Serif fonts used for the original Cyrillic references are included
with their license in `fonts/`.

`pages.tex` includes the 242 files in `transcription/` in scan order. Images
are in `images/recreated/`; original crops in `images/` are comparison inputs
only. See `python_figures/README.md` to regenerate every illustration, and
`figures-manifest.json` for formulas, parameters, and data provenance.
`page-manifest.json` records the scan leaf, physical PDF
page, original printed label, and equation tags for each page.

## Reading and review

The first transcription used the supplied page images. All displayed equations
then received a second visual comparison against the clearer National Security
Archive scan. Context and repeated formulas were used to interpret damaged
printing; several initially uncertain readings could subsequently be confirmed
in that second scan. Review notes and preserved source misprints are recorded
in `notes/`. Any residual uncertain token uses `\unclear{...}` in the source
and prints in amber, so it can be located without changing the page count.

Primary page-order source:
https://archive.org/details/ufintsev-method-of-edge-waves-in-the-physical-theory-of-diffraction

Supplementary scan used to resolve damaged printing:
- https://nsarchive2.gwu.edu/NSAEBB/NSAEBB443/docs/area51_10a.PDF
- https://nsarchive2.gwu.edu/NSAEBB/NSAEBB443/docs/area51_10b.PDF
- https://nsarchive2.gwu.edu/NSAEBB/NSAEBB443/docs/area51_10c.PDF

The supplementary PDFs have their own irregular scan order. They were used
for reading, not as the pagination template.
