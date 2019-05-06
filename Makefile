.PHONY: lint

TEST_COMMAND:=@python -m pytest --cov-report term-missing --cov=trainalyzr

check: lint test

lint:
	flake8 cli.py trainalyzr

test:
	$(TEST_COMMAND)

test-integration:
	$(TEST_COMMAND) tests/feature

test-unit:
	$(TEST_COMMAND) tests/unit
