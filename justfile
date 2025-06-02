project-name := "docstamp"

# Show available recipes
default:
  @just --list

# Show the version of the project
version:
  hatch version

# Install the dependencies necessary for CI and development
install:
  uv sync

# Install the dependencies needed for a production installation
install-prod:
  uv sync --no-default-groups

# Upgrade the dependencies to the latest accepted versions
upgrade:
  uv lock --upgrade

# Delete all intermediate files
clean-temp: clean-build clean-pyc

# Delete all intermediate files and caches
clean-all: clean-temp clean-caches

# Delete the Python build files and folders
clean-build:
  rm -fr build/
  rm -fr dist/
  rm -fr .eggs/
  rm -fr *.egg-info
  rm -fr *.spec

# Remove Python file artifacts
clean-pyc:
    pyclean {{project-name}}
    find . -name '*~' -exec rm -f {} +
    find . -name __pycache__ -exec rm -rf {} +
    find . -name '*.log*' -delete
    find . -name '*_cache' -exec rm -rf {} +
    find . -name '*.egg-info' -exec rm -rf {} +

# Remove cache directories
clean-caches:
    rm -rf .mypy_cache
    rm -rf .ruff_cache
    rm -rf .pytest_cache

# Remove all build, Python, and cache artifacts
clean: clean-build clean-pyc clean-caches

##@ Code check
# Format your code with ruff
format-ruff:
  ruff format .

# Format your code
format: format-ruff

# Run mypy check
lint-mypy:
  mypy .

# Run ruff lint check
lint-ruff:
  ruff check --fix .

# Run all code checks
lint: lint-mypy lint-ruff

# Run tests with coverage
test args="":
  pytest --cov -vvv {{args}}

# Run tests in debug mode
test-dbg args="":
  pytest --pdb --ff {{args}}

# Run format, linting, then tests
check: format lint test

build:
  uv build

release:
  uv release