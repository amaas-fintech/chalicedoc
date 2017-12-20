.PHONY: test docs clean

test:
	pipenv install
	pipenv check --style chalicedoc.py
	pipenv run python -m pytest

docs:
	pipenv install
	pipenv run sphinx-build docs docs/_build

clean:
	rm -r docs/_build
