help:
	@echo "clean          run \`clean-build\`, \`clean-pyc\` & \`clean-test\` targets"
	@echo "clean-build    remove build artifacts"
	@echo "clean-pyc      remove Python file artifacts"
	@echo "clean-test     remove test and coverage artifacts"
	@echo "clean-venv     remove the dev tools virtual enviroment"
	@echo "test           run \`pytest\` on the project"
	@echo "tox            run \`tox\` on the project"
	@echo "coverage       run \`coverage\` and generate a report"
	@echo "lint           lint the project using \`ruff\`"
	@echo "lint-test      lint the tests using \`ruff\`"
	@echo "install        install the package locally"
	@echo "install-build  install the package & its extra build dependencies"
	@echo "install-dev    install the package & its extra dev dependencies"
	@echo "build-only     build the package"
	@echo "build          run \`install-build\`, \`tox\` & \`build-only\` targets"
	@echo "im             starts Python in interactive mode; uses \`ipython\`"
	@echo "help           print this messsage"

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
	scripts/safe_bin.sh coverage erase
	scripts/safe_bin.sh python -m ruff clean
	rm -rf .cache/
	rm -rf htmlcov/

clean-venv:
	rm -rf api_mimic_build_venv

coverage:
	scripts/safe_bin.sh coverage -m pytest
	scripts/safe_bin.sh coverage report --no-skip-covered
	scripts/safe_bin.sh coverage html

test:
	scripts/safe_bin.sh python -m pytest

tox:
	scripts/safe_bin.sh python -m tox

lint:
	scripts/safe_bin.sh python -m ruff check src/api_mimic.py

lint-test:
	scripts/safe_bin.sh python -m ruff check tests/

install-dev:
	scripts/safe_bin.sh python -m pip install .[dev]

install:
	scripts/safe_bin.sh python -m pip install .

install-build:
	scripts/safe_bin.sh python -m pip install .[build]

build: install-build tox build-only

build-only:
	scripts/safe_bin.sh python -m build

im:
	scripts/safe_bin.sh ipython
