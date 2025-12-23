from unittest.mock import MagicMock, patch

import app.dependencies as dependencies


@patch("app.dependencies.SessionLocal")
def test_get_db_yields_session(mock_session_local):
    mock_session = MagicMock()
    mock_session_local.return_value = mock_session

    generator = dependencies.get_db()
    db = next(generator)
    assert db == mock_session


@patch("app.dependencies.SessionLocal")
def test_get_db_closes_session(mock_session_local):
    mock_session = MagicMock()
    mock_session_local.return_value = mock_session

    generator = dependencies.get_db()
    next(generator)  # Advance the generator to yield the session
    try:
        next(generator)  # Attempt to advance the generator again
    except StopIteration:
        pass
    mock_session.close.assert_called_once()
