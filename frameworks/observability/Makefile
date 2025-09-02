PY=.venv/bin/python
PIP=.venv/bin/pip

.PHONY: venv install lint validate package verify digest fmt

venv:
	python3 -m venv .venv || python3.13 -m venv .venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

install:
	make venv

lint: venv
	$(PY) -m ruff check tools || true
	$(PY) -m mypy tools || true

validate: venv
	$(PY) -m tools.validators.schema_lint artifacts schemas && \
	$(PY) -m tools.validators.cross_stream_consistency artifacts && \
	$(PY) -m tools.validators.parity_coverage artifacts

package: venv
	$(PY) -m tools.manifest.seal_manifest artifacts schemas

verify: venv
	$(PY) -m tools.manifest.verify_manifest artifacts

digest: venv
	$(PY) -m tools.digest.generate_digest artifacts digests

fmt: venv
	$(PY) -m ruff format tools
