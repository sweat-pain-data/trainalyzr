.PHONY: lint

check: lint test

lint:
	flake8 cli.py trainalyzr

test: test-integration

test-integration:
	python -m pytest --cov-report term-missing --cov=trainalyzr tests/feature
