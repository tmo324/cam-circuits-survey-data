# Third-Party Notices

The root `LICENSE` applies to original project code. Data, editable Draw.io
sources, and author-created figure assets are covered separately by
`LICENSE-DATA.md`. This repository does not vendor the source code of its Python
dependencies.

## Runtime Dependencies

| Dependency | License | Project |
|---|---|---|
| NumPy | BSD-3-Clause | https://numpy.org/ |
| pandas | BSD-3-Clause | https://pandas.pydata.org/ |
| Matplotlib | PSF-based Matplotlib License | https://matplotlib.org/ |
| openpyxl | MIT | https://openpyxl.readthedocs.io/ |

The exact dependency constraints are defined in `pyproject.toml` and mirrored in
`requirements.txt` for simple script-based installation.

## Workflow Tooling

GitHub Actions downloads its actions at workflow runtime. Those actions are not
redistributed as part of this repository and retain their upstream terms. The
workflows use GitHub's `actions/checkout`, `actions/setup-python`, and the
Gitleaks secret-scanning action.

## Bibliographic and Paper Material

Bibliographic metadata, paper titles, citations, and identifiers remain subject
to their original records and rights. The associated IEEE article PDF and
third-party paper contents are not distributed in this repository.
