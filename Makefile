.PHONY: lint
lint:
	mypy --install-types --non-interactive .
	flake8 .

.PHONY: style
style:
	black . --check --diff
	isort . -c --diff

.PHONY: test
test: style lint
	pytest .

.PHONY: format
format:
	black .
	isort .

.PHONY: migration
migration:
	alembic revision --autogenerate

.PHONY: dev
dev:
	python -m lxdapi dev

.PHONY: run
run:
	python -m lxdapi run

.PHONY: prepare
prepare:
	python -m lxdapi db migrate
