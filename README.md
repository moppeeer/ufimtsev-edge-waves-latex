# Method of Edge Waves — an editable LaTeX reconstruction

> A tribute to a book whose mathematics helped change the shape of military aviation.

This repository preserves and reconstructs Pyotr Ya. Ufimtsev's *Method of Edge
Waves in the Physical Theory of Diffraction*. It contains the historical scan,
a fully editable 242-page LaTeX edition, a compiled PDF, and reproducible Python
code for all 80 numbered figures.

## Read the book

- [Original historical scan](original/ufimtsev-method-of-edge-waves-original-scan.pdf)
- [Reconstructed, searchable PDF](pdf/ufimtsev-method-of-edge-waves-reconstructed.pdf)
- [LaTeX source and figure-generation code](latex/)

## The book and the aircraft with the strange shape

Ufimtsev's monograph developed the Physical Theory of Diffraction: a practical
way to estimate electromagnetic scattering from edges and surface
discontinuities. That is precisely the difficult part of predicting how an
object will appear to radar.

In the 1970s, Lockheed Skunk Works engineer Denys Overholser recognized that
Ufimtsev's published method could be turned into a computer calculation of
radar cross section. The resulting **ECHO I** program could evaluate shapes made
from flat panels. With the computers available at the time, that computational
constraint encouraged the extraordinary faceted geometry nicknamed the
**Hopeless Diamond**. The idea became the **Have Blue** demonstrator and then
the Lockheed **F-117 Nighthawk**, the first operational aircraft designed around
stealth technology.

The monograph did not create the F-117 by itself: the aircraft also depended on
materials, flight controls, propulsion, manufacturing, testing, and the work of
large engineering teams. But Ufimtsev's diffraction theory supplied a crucial
mathematical foundation that allowed engineers to predict—and therefore design
for—a very small radar return. The angular silhouette that once looked almost
impossibly strange was mathematics made visible.

This connection is documented by the
[U.S. Air Force Research Laboratory](https://www.afrl.af.mil/News/Article-Display/Article/3495849/afwerx-reaches-out-to-academia-for-new-technologies/),
the [Air Force Office of Scientific Research](https://www.afrl.af.mil/Portals/90/Documents/AFOSR/AFOSR%2060th%20Monograph.pdf?ver=2020-08-24-144422-047),
[Lockheed Martin's account of ECHO I](https://www.lockheedmartin.com/en-us/news/features/2022/Now-Thats-a-Milestone-Worth-Celebrating-1000-Stealth-Air.html),
and the U.S. Air Force histories of
[Have Blue](https://www.holloman.af.mil/News/Display/Article/317620/december-1st-is-an-historic-day-for-stealth-fighters/)
and the [F-117](https://www.airmanmagazine.af.mil/Features/Display/Article/2604078/airframe-the-f-117-nighthawk/).

## What was reconstructed

- All 242 scan leaves, preserving the original page boundaries and labels,
  including inserted page 116a.
- Editable text, equations, equation numbers, captions, and references.
- 620 numbered-equation occurrences checked against page images.
- All 80 numbered figures recreated as vector PDF and SVG assets with Python.
- The cover motif redrawn and the two historical emblems vector-traced.
- Per-figure provenance recording formulas, parameters, approximations, and
  digitized comparison curves.

This is a carefully typeset reconstruction, not a pixel facsimile. Theoretical
curves are evaluated from equations in the book wherever possible. Curves from
external experiments or rigorous solutions for which the book provides no
tables are explicitly marked as approximate digitizations of the printed graph;
they are not presented as raw experimental data.

## Repository layout

```text
original/   source scan as obtained from the Internet Archive
pdf/        compiled reconstructed edition
latex/      complete LaTeX project
  transcription/       one editable .tex file per scan leaf
  python_figures/      reproducible Matplotlib/SciPy figure code
  images/recreated/    vector PDF/SVG, previews, data, and provenance
  figures-manifest.json
  page-manifest.json
  verification.json
```

## Build

The generated vector assets are already included. To compile the book:

```bash
cd latex
tectonic -X compile main.tex
```

XeLaTeX can be used instead. To regenerate and verify every illustration first:

```bash
cd latex
python -m pip install -r python_figures/requirements.txt
python python_figures/build_all.py --integrate
tectonic -X compile main.tex
```

The final audit checks page count and dimensions, editable text, object bounds,
missing glyphs, uncertain transcription markers, and raster-image embedding.
The supplied edition passes with 242 pages, no missing glyphs, no overfull boxes,
and no embedded raster images in the compiled book.

## Integrity

| File | SHA-256 |
|---|---|
| Original scan | `acb527297d5555afa14def4a0df13e772d25eb2d8b5ed49b8d6c4c5084b8420d` |
| Reconstructed PDF | `355a7743ed9325ce624ef473960324ad263040542f1b63247d7f6ef552b76a23` |

## Archival sources and rights

The page-order source is the
[Internet Archive copy](https://archive.org/details/ufintsev-method-of-edge-waves-in-the-physical-theory-of-diffraction).
Clearer scans from the National Security Archive were used to resolve damaged
printing. The U.S. Air Force document-control page identifies report
**FTD-HC-23-259-71** as unclassified and states: “Approved for public release;
distribution unlimited.” See [RIGHTS_AND_ATTRIBUTION.md](RIGHTS_AND_ATTRIBUTION.md)
for the intentionally cautious distinction between public-release status and a
copyright license.

Python reconstruction code is available under the MIT License in
[LICENSE-CODE](LICENSE-CODE). That license does not purport to relicense the
historical report, its translation, or the underlying monograph.

## Acknowledgment

This edition is offered in admiration of Ufimtsev's work and of the engineers
who recognized that an abstract diffraction theory could become a practical
design tool. It is also a reminder that foundational research can travel across
languages, institutions, and decades before its full consequence becomes clear.

