.PHONY: build
build:
	uv sync
	rm -r dist
	uv build
