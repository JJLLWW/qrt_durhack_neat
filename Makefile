.PHONY: coverage tests wheel

tests:
	python -m pytest

coverage:
	coverage run --source=src -m pytest
	coverage html
	coverage report

wheel:
	pip wheel --no-deps .

upload:
	twine upload -r testpypi test_pypi_upload_with_wheel-0.0.1-py3-none-any.whl