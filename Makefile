#* development variables
LOCAL_PORT="8000"

#* read version from pyproject.toml version = "x.x.x" using bash
VERSION="$(shell cat pyproject.toml | grep version | head -n 1 | cut -d '"' -f 2)"


test: ## [Local development] Run all Python tests with pytest.
	poetry run pytest --cov-report=html --cov=embedbase_internet_search;poetry run coverage-badge -o assets/images/coverage.svg -f
	@echo "Done testing"

release: ## [Local development] Release a new version of the API.
	@echo "Releasing version ${VERSION}"; \
	read -p "Commit content:" COMMIT; \
	git add .; \
	echo "Committing '${VERSION}: $$COMMIT'"; \
	git commit -m "Release ${VERSION} $$COMMIT"; \
	git push origin main
	@echo "Done, check '\033[0;31mhttps://github.com/different-ai/embedbase-internet-search/actions\033[0m'"

#* Poetry
.PHONY: poetry-download
poetry-download:
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python3 -

.PHONY: poetry-remove
poetry-remove:
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python3 - --uninstall

#* Installation
.PHONY: install
install:
	poetry lock -n
	poetry install -n

#* Formatters
.PHONY: codestyle
codestyle:
	poetry run pyupgrade --exit-zero-even-if-changed --py38-plus **/*.py
	poetry run isort --settings-path pyproject.toml ./
	poetry run black --config pyproject.toml ./

.PHONY: formatting
formatting: codestyle

.PHONY: check-codestyle
check-codestyle:
	poetry run isort --diff --check-only --settings-path pyproject.toml ./
	poetry run black --diff --check --config pyproject.toml ./
	poetry run darglint --verbosity 2 embedbase tests

.PHONY: mypy
mypy:
	poetry run mypy --config-file pyproject.toml ./

.PHONY: lint
lint: test check-codestyle mypy check-safety

.PHONY: help

help: # Run `make help` to get help on the make commands
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
