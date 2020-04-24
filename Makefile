.PHONY: test install clean

all: venv

venv:
	python3 -m venv venv --prompt meta

install: venv requirements.txt
	venv/bin/python3 -m pip install -U pip
	venv/bin/python3 -m pip install -r requirements.txt

test:
	venv/bin/pytest --cov=meta/ --mypy meta/**/*.py tests/test_*.py

clean:
	rm -rf venv/
