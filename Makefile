.PHONY: coverage tests wheel rm_deps

tests:
	python -m pytest

coverage:
	coverage run --source=src -m pytest
	coverage html
	coverage report

wheel:
	poetry build

upload:
	twine upload -r testpypi test_pypi_upload_with_wheel-0.0.1-py3-none-any.whl

rm_deps:
	pip freeze | xargs pip uninstall -y

poetry_install_all:
	poetry install --no-root -with=test,dev