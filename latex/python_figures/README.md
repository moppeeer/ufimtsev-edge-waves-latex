# Figure reconstruction

All 80 numbered figures and the 3 front-matter artwork assets are generated
with Python. The PDF/SVG files are vector files; PNGs are review previews.
The original crops remain in `../images/` for comparison and canvas sizing,
but are not embedded in the reconstructed figure PDFs or SVGs.

## Regenerate

```text
python -m pip install -r python_figures/requirements.txt
python python_figures/build_all.py --integrate
tectonic -X compile main.tex
```

The scripts are independent of the current working directory. Once dependencies
are installed, generation is offline. Generated assets are in `images/recreated/`.
Each scientific curve is also exported as numerical line coordinates in a
`.data.json` file; null values mark intentional discontinuities.

## What was calculated and what was digitized

`figures-manifest.json` is the per-figure provenance record. It identifies the
equations, parameters, approximations, comparison control points, and any
source-caption discrepancy. The original book captions remain unchanged.

- Geometric diagrams use independently drawn vector primitives and labels.
- Calculated curves evaluate equations from the book with NumPy/SciPy.
- Curves from external rigorous solutions or experiments without numerical
  tables in the book are approximate digitizations of the printed graphs.
  These control points are not newly computed exact solutions or raw
  experimental observations. Shape-preserving interpolation is documented.
- The cover graph is a decorative reconstruction, not a calibrated data plot.
- The two historical emblems retain their artwork through contour vectorization.

Important numerical choices are explicit in the scripts and manifest. For
example, some disk curves require the near-axis approximation recommended by
the text; the join is documented rather than hidden. The wire model is used in
the displayed graph ranges. Its direct resummed approximation must not be
extrapolated to arbitrarily small kL; `static_F` implements the separate
electrostatic asymptote from 33.18 for that regime.

The regeneration check requires all 83 assets, exactly figures 1..80, one page
per vector PDF, unchanged canvas aspect ratios, no raster objects in the
PDF/SVG outputs, and no labels outside the canvas.
