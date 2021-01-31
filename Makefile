.PHONY: all build install typing lint test

all: black build install typing lint test

black:
	black -l 99 maps tests
	isort --atomic .

#build:
#	python3 -m pip install -r requirements.txt

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +
	rm -rf docs/source/_build/

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage*
	rm -fr htmlcov/
	rm -fr .mypy_cache
	rm -fr .pytest_cache
	find . -name '.ipynb_checkpoints' -exec rm -fr {} +

install:
	python3 -m pip install -e .

#typing:
#	pytest -v -s --mypy maps

lint:
	isort --check --diff maps tests
	flake8 -v --statistics --count .
	black -l 99 --diff --check maps tests

test:
	pytest -vv -s --durations=10 --cov=maps tests
	coverage html
