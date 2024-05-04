.PHONY: lint

lint:
	@pylint *.py

run:
	. ./env-setup.sh && \
	python3 rewrite_news.py