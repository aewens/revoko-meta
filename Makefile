.PHONY: test install clean

all: venv

venv:
	python3 -m venv venv --prompt meta

install: venv requirements.txt
	venv/bin/python3 -m pip install -U pip
	venv/bin/python3 -m pip install -r requirements.txt

clean:
	rm -rf venv/

types:
	venv/bin/pytest --mypy --mypy-ignore-missing-imports meta/**/*.py tests/test_*.py

check:
	venv/bin/pytest --showlocals --exitfirst --verbose --tb=long --cov-report term-missing --cov=meta/ meta/**/*.py tests/test_*.py

test:
	venv/bin/pytest --showlocals --exitfirst --verbose --tb=long --cov-report term-missing --cov=meta/ --mypy --mypy-ignore-missing-imports meta/**/*.py tests/test_*.py
