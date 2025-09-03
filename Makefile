PY=python
PIP=pip
VENV=.venv

.PHONY: venv install data-pipelines users events transactions clean test ci

venv:
	python3 -m venv $(VENV)
	. $(VENV)/bin/activate; $(PIP) install -r data/pipelines/requirements.txt

install: venv
	. $(VENV)/bin/activate; $(PIP) install -r requirements-dev.txt

data-pipelines:
	$(PY) data/pipelines/pipeline.py --dataset users --input data/pipelines/samples/users.csv --output data/pipelines/out
	$(PY) data/pipelines/pipeline.py --dataset session_events --input data/pipelines/samples/session_events.csv --output data/pipelines/out
	$(PY) data/pipelines/pipeline.py --dataset transactions --input data/pipelines/samples/transactions.csv --output data/pipelines/out

users:
	$(PY) data/pipelines/pipeline.py --dataset users --input data/pipelines/samples/users.csv --output data/pipelines/out

events:
	$(PY) data/pipelines/pipeline.py --dataset session_events --input data/pipelines/samples/session_events.csv --output data/pipelines/out

transactions:
	$(PY) data/pipelines/pipeline.py --dataset transactions --input data/pipelines/samples/transactions.csv --output data/pipelines/out

clean:
	rm -rf data/pipelines/out

test:
	. $(VENV)/bin/activate; pytest -q

ci:
	bash ci/run_ci.sh | cat