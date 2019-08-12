.PHONY: help clean clean-pyc clean-build list test test-dbg test-cov test-all coverage docs release sdist install install-dev tag

project-name = docstamp

version-var := "__version__ = "
version-string := $(shell grep $(version-var) $(project-name)/version.py)
version := $(subst __version__ = ,,$(version-string))

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-cov - run tests with the default Python and report coverage"
	@echo "test-dbg - run tests and debug with ipdb"
	@echo "testall - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "sdist - package"
	@echo "install - install"
	@echo "install-dev - install in development mode"
	@echo "tag - create a git tag with current version"

install:
	python -m pip install .

install-ci:
	python -m pip install pipenv
	pipenv install --dev
	python -m pip install -e .

install-dev: install-ci
	pre-commit install

clean: clean-build clean-pyc clean-caches

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	rm -fr *.egg-info
	rm -fr *.spec

clean-pyc:
	pyclean $(project-name)
	find . -name '*~' -exec rm -f {} +
	find . -name __pycache__ -exec rm -rf {} +
	find . -name '*.log*' -delete
	find . -name '*_cache' -exec rm -rf {} +
	find . -name '*.egg-info' -exec rm -rf {} +

clean-caches:
	rm -rf .tox
	rm -rf .pytest_cache

lint:
	tox -e lint

test:
	tox -e tests

mypy:
	tox -e mypy

isort-check:
	tox -e isort

isort:
	isort -rc $(project-name)/

test-cov:
	py.test --cov-report term-missing --cov=$(project-name)

test-dbg:
	py.test --ipdb

test-all:
	tox

tag: clean
	@echo "Creating git tag v$(version)"
	git tag v$(version)
	git push --tags

release: clean
	python setup.py sdist
	twine upload dist/*
