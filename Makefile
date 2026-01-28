.PHONY: build, tests
build:
	uv sync
	rm -r dist
	uv build

tests:
	uv run --dev pytest -s
