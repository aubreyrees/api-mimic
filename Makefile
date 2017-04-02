python_version_full := $(wordlist 2,4,$(subst ., ,$(shell python --version 2>&1)))
python_version_major := $(word 1,${python_version_full})
python_version_minor := $(word 2,${python_version_full})
python_version_patch := $(word 3,${python_version_full})


help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "test - run tests with the active Python binary"
	@echo "coverage - check code coverage with the active Python binary"
	@echo "lint - generate a full report on the state of the code"
	@echo "lint-bare - a bare bones sanity check of the code to ensure there are no major problems"
	@echo "install - install the package to the active Python's site-packages"

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
	rm -f .coverage
	rm -rf .cache/
	rm -rf htmlcov/

coverage:
	coverage erase --rcfile ./coverage.${python_version_major}.rc
	coverage run --rcfile ./coverage.${python_version_major}.rc setup.py test
	coverage report --rcfile ./coverage.${python_version_major}.rc
	coverage html --rcfile ./coverage.${python_version_major}.rc

test:
	python setup.py test --pytest-args="--cov=api_mimic --cov-config coverage.${python_version_major}.rc"

install: clean
	python setup.py install

lint:
	pylint --rcfile=pylint.rc api_mimic

lint-bare:
	pylint --rcfile=pylint.rc --disable C,R --persistent=n --reports=n api_mimic
