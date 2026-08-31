.PHONY: all data figures tables check clean

PYTHON ?= python3

all:
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

check:
	$(PYTHON) analysis/validate_artifacts.py

clean:
	$(PYTHON) analysis/clean_generated.py
