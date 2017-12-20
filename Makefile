
.PHONY: test

test:
	pipenv install
	pipenv run python -m pytest
