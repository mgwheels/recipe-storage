help:
	echo "\nAvailable make commands:\n\ndeps\nlint\nrun\ntest\ndocker-run\ndocker-stop"

deps:
	python -m pip install --upgrade pip
	pip install -r requirements.txt -r dev-requirements.txt

lint:
	ruff check --fix . && ruff format .

run:
	uvicorn app.main:app --reload

test:
	python -m pytest

# TODO: remove sudo after updating docker permissions
docker-run:
	sudo docker build -t recipe-storage .
	sudo docker run -d --rm --name recipe-storage recipe-storage

# TODO: remove sudo after updating docker permissions
docker-stop:
	sudo docker stop recipe-storage