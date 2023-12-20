.PHONY: coverage tests wheel

tests:
	python -m pytest

coverage:
	coverage run --source=src -m pytest
	coverage html
	coverage report

wheel:
	pip wheel --no-deps .