.PHONY: test docs clean release

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

release: test dist
	pipenv run twine upload dist/*

clean:
	rm -rf build chalicedoc.egg-info dist
	rm -rf docs/_build
