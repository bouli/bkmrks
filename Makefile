.PHONY: build, tests
build:
	uv sync
	rm -r dist
	uv build

tests:
	uv run --dev coverage run -m pytest -s

report:
	uv run --dev coverage report -m
