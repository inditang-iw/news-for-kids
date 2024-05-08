.PHONY: lint

lint:
	@pylint src/*.py

run:
	@python3 src/rewrite_news.py