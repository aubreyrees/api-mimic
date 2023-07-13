python_version_full := $(wordlist 2,4,$(subst ., ,$(shell python --version 2>&1)))
python_version_major := $(word 1,${python_version_full})
python_version_minor := $(word 2,${python_version_full})
python_version_patch := $(word 3,${python_version_full})


help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "test - run `pytest` using `coverage`"
	@echo "coverage_report - generate a report for `coverage`. Run after `test`"
	@echo "lint - lint the project using `ruff`"
	@echo "lint_test - lint the tests using `ruff`"
	@echo "install - install the package using `build` frontend & `pip`"

clean: clean-test clean-build clean-pyc

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf .eggs/
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '*.egg' -exec rm -rf {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -rf .tox/
	coverage erase
	python -m ruff clean
	rm -rf .cache/
	rm -rf htmlcov/

coverage-report:
	coverage report --no-skip-covered -m
	coverage html

test:
	python -m pytest

install: clean
	python -m pip install .

lint:
	python -m ruff check src/api_mimic.py

lint-test:
	python -m ruff check tests/
