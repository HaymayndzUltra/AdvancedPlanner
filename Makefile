.PHONY: qa-install qa-validate qa-manifest qa-digest

qa-install:
	python3 -m venv .venv && . .venv/bin/activate && pip install -r frameworks/qa-test/tools/requirements.txt

qa-validate:
	. .venv/bin/activate && python frameworks/qa-test/tools/qa_cli.py schema_lint

qa-manifest:
	. .venv/bin/activate && python frameworks/qa-test/tools/qa_cli.py generate_manifest --snapshot_rev git:abcdef1234 --rulebook_hash sha256:rulebookhashhere --signed_by qa-bot@local

qa-digest:
	. .venv/bin/activate && python frameworks/qa-test/tools/qa_cli.py digest
