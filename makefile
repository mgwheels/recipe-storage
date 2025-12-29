help:
	echo "\nAvailable make commands:\n\ndeps\nlint\nrun\ntest"

deps:
	python -m pip install --upgrade pip
	pip install -r requirements/base.txt -r requirements/dev.txt

lint:
	ruff check --fix . && ruff format .

run:
	uvicorn app.main:app --reload

test:
	python -m pytest