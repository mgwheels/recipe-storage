from os import environ
from importlib import reload

import app.core.config as config


def test_vars():
    # Test defaults
    assert config.DATABASE_URL == "sqlite:///recipes.db"

    # Test supplied vars
    environ["DATABASE_URL"] = "other val"
    reload(config)
    assert config.DATABASE_URL == "other val"
