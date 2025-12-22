# recipe-storage

Python app designed to locally manage various recipes. Built with FastAPI and SQLAlchemy

## Development

### Project Structure

The project structure is as follows:

```
recipe-storage
├── .gitignore
├── LICENSE
├── makefile
├── README.md
├── requirements.txt
├── dev-requirements.txt
├── app
│   ├── __init__.py
│   ├── dependencies.py
│   ├── main.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── config.py
│   ├── db
│   │   ├── __init__.py
│   │   ├── database.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── recipes.py
│   ├── routers
│   │   ├── __init__.py
│   │   ├── recipes.py
│   ├── schemas
│   │   ├── __init__.py
│   │   ├── recipes.py
│   ├── services
│       ├── __init__.py
│       ├── receipes_service.py
├── tests
│   ├── test-main.py
```

### Running DB

In root directory, run `make run`. Alternatively if don't have make installed, can run `uvicorn app.main:app --reload`

Naviage to URL `127.0.0.1:8000/docs` to test available endpoints

## Resources

For getting started there is a helpful tutorial for FastAPI & SQLAlchemy available here: [Link](https://www.youtube.com/watch?v=xq1Snezb1rs)

For modular project structure there is documentation available here: [Link](https://dev.to/mohammad222pr/structuring-a-fastapi-project-best-practices-53l6)