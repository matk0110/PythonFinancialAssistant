# Simple cross-platform targets (Windows users: use `make` via mingw or treat as docs)
PYTHON?=python
VENV=.venv
REQ=requirements.txt

.PHONY: venv install dev test run streamlit lint clean

venv:
	$(PYTHON) -m venv $(VENV)

install: venv
	$(VENV)/Scripts/python -m pip install -r $(REQ)

# Dev installs test/lint extras
dev: install
	$(VENV)/Scripts/pip install -r requirements.dev.txt

test:
	$(VENV)/Scripts/pytest -q

run:
	$(VENV)/Scripts/python main.py

streamlit:
	$(VENV)/Scripts/streamlit run streamlit_app.py

clean:
	rm -rf $(VENV) .pytest_cache __pycache__ data
