.PHONY: test docs clean

test:
	pipenv install
	pipenv check --style chalicedoc.py
	pipenv run python setup.py check -smr
	pipenv run python -m pytest

docs:
	pipenv install
	pipenv run sphinx-build docs docs/_build

dist:
	pipenv install --dev
	pipenv run python setup.py sdist bdist_wheel

clean:
	rm -rf build chalicedoc.egg-info dist
	rm -rf docs/_build
