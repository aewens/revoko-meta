.PHONY: test install clean

all: venv

venv:
	python3 -m venv venv --prompt meta

install: venv requirements.txt
	venv/bin/python3 -m pip install -U pip
	venv/bin/python3 -m pip install -r requirements.txt

clean:
	rm -rf venv/

check:
	venv/bin/pytest --showlocals --cov=meta/ meta/**/*.py tests/test_*.py

types:
	venv/bin/pytest --mypy --mypy-ignore-missing-imports meta/**/*.py tests/test_*.py

test: check types
