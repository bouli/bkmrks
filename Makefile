.PHONY: build, tests
buildd:
	uv sync
	rm -r dist
	uv build

testss:
	uv run --dev coverage run -m pytest -s

report:
	uv run --dev coverage report -m
