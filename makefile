help:
	echo "\nAvailable make commands:\n\ndeps\nlint\nrun\ntest"

deps:
	pip install -r requirements.txt
	pip install -r dev-requirements.txt

lint:
	ruff check --fix . && ruff format .

run:
	uvicorn app.main:app --reload

test:
	python -m pytest