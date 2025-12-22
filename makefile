deps:
	pip install -r requirements.txt
	pip install -r dev-requirements.txt

run:
	uvicorn app.main:app --reload

test:
	python -m pytest