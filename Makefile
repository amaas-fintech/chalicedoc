
.PHONY: test docs clean

test:
	pipenv install
	pipenv run python -m pytest

docs:
	pipenv install --dev
	pipenv run sphinx-build docs docs/_build

clean:
	rm -r docs/_build
