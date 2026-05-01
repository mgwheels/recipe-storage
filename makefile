help:
	echo "\nAvailable make commands:\n\ndeps\nlint\nrun\ntest\ndocker-run\ndocker-stop"

deps:
	uv sync

lint:
	uv run ruff check --fix . && uv run ruff format .

run:
	uv run uvicorn app.main:app --reload

test:
	uv run python -m pytest

# TODO: remove sudo after updating docker permissions
docker-run:
	sudo docker build -t recipe-storage .
	sudo docker run -d --rm --name recipe-storage -p 8000:8000 recipe-storage

# TODO: remove sudo after updating docker permissions
docker-stop:
	sudo docker stop recipe-storage
