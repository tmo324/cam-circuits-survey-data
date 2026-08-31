.PHONY: install install-test test check all paper data figures tables clean

PYTHON ?= python3
MPLCONFIGDIR ?= $(CURDIR)/.matplotlib
MPLBACKEND ?= Agg

export MPLCONFIGDIR MPLBACKEND

install:
	$(PYTHON) -m pip install -e .

install-test:
	$(PYTHON) -m pip install -e ".[test]"

test:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m unittest discover -s tests -v

check:
	$(PYTHON) -m compileall -q analysis tests
	$(MAKE) PYTHON=$(PYTHON) test
	$(PYTHON) analysis/validate_artifacts.py

all: paper

paper:
	$(PYTHON) analysis/generate_all.py

data:
	$(PYTHON) analysis/prepare_data.py

figures: data
	$(PYTHON) analysis/sync_manual_figures.py
	$(PYTHON) analysis/plot_cell_area.py
	$(PYTHON) analysis/plot_information_density.py
	$(PYTHON) analysis/plot_search_energy.py

tables:
	$(PYTHON) analysis/generate_tables.py

clean:
	$(PYTHON) analysis/clean_generated.py
