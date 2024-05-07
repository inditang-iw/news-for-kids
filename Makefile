.PHONY: lint

lint:
	@pylint *.py

run:
	@python3 rewrite_news.py