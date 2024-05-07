.PHONY: lint

lint:
	@pylint *.py

run:
	@python3 src/rewrite_news.py