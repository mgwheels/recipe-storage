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
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── routers.py
│   │   ├── schemas.py
│   │   ├── utils.py
├── tests
│   ├── test-main.py
│   ├── core
│   │   ├── test_config.py
│   │   ├── test_database.py
├── requirements
│   ├── base.txt
│   ├── dev.txt
```

### Running DB

In root directory, run `make deps` and `make run`.

Naviage to URL `127.0.0.1:8000/docs` to test available endpoints

## Resources

For getting started there is a helpful tutorial for FastAPI & SQLAlchemy available here: [Link](https://www.youtube.com/watch?v=xq1Snezb1rs)

For modular project structure there is documentation available here: [Link](https://dev.to/mohammad222pr/structuring-a-fastapi-project-best-practices-53l6)