# recipe-storage

Python app designed to locally manage various recipes. Built with FastAPI and SQLAlchemy

## Development

### Running DB

In root directory, run `make run`. Alternatively if don't have make installed, can run `uvicorn app.main:app --reload`

Naviage to URL `127.0.0.1:8000/docs` to test available endpoints