# Tables

Run python analysis/generate_tables.py to rebuild all six LaTeX fragments in
generated.

Tables I, IV, V, and VI are generated from CSV data. Tables II and III compose
the circuit schematic PNGs in assets. Their editable drawings are retained
under figures/source.

The fragments assume the parent LaTeX document loads graphicx and supports
rotatebox. Asset paths are written relative to the repository root.

To smoke-test all fragments from the repository root, run:

~~~bash
pdflatex -interaction=nonstopmode -halt-on-error \
  -output-directory=/tmp tables/preview.tex
~~~
