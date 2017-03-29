help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "test - run tests with the active Python binary"
	@echo "coverage - check code coverage with the active Python binary"
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

coverage2:
	coverage report erase
	coverage run --rcfile coveragerc2 --branch --source api_mimic setup.py test
	coverage report -m
	coverage html

coverage3:
	coverage erase --rcfile ./coverage.3.rc
	coverage run --rcfile ./coverage.3.rc setup.py test
	coverage report --rcfile ./coverage.3.rc
	coverage html --rcfile ./coverage.3.rc

test2:
	python setup.py test --pytest-args="--cov=api_mimic --cov-config coverage.2.rc"

test3:
	python setup.py test --pytest-args="--cov=api_mimic --cov-config coverage.3.rc"

install: clean
	python setup.py install

lint3:
	pylint --rcfile=pylint.3.rc api_mimic

lint3-bare:
	pylint --rcfile=pylint.3.rc --disable C,R --persistent=n --reports=n api_mimic
