import os
import importlib
import pytest
from unittest.mock import patch, MagicMock

@patch("sqlalchemy.create_engine")
@patch("sqlalchemy.orm.sessionmaker")
@patch("sqlalchemy.ext.declarative.declarative_base")
@patch("dotenv.load_dotenv")
@patch.dict(os.environ, {
    "DATABASE_HOST": "localhost",
    "DATABASE_USER": "test_user",
    "DATABASE_NAME": "test_db",
    "DATABASE_PASSWORD": "test_password"
})
def test_db_initialization(mock_load_dotenv, mock_declarative_base, mock_sessionmaker, mock_create_engine):
    importlib.reload(importlib.import_module("app.models"))

    from app.models import DATABASE_URL, engine, SessionLocal, Base

    assert os.environ["DATABASE_HOST"] == "localhost"
    assert os.environ["DATABASE_USER"] == "test_user"
    assert os.environ["DATABASE_NAME"] == "test_db"
    assert os.environ["DATABASE_PASSWORD"] == "test_password"

    expected_database_url = "postgresql://test_user:test_password@localhost:5432/test_db"
    assert DATABASE_URL == expected_database_url

    mock_create_engine.assert_called_once_with(DATABASE_URL)
    mock_sessionmaker.assert_called_once_with(autocommit=False, autoflush=False, bind=mock_create_engine.return_value)

    mock_declarative_base.assert_called_once()
    assert Base == mock_declarative_base.return_value

    with patch.object(mock_declarative_base.return_value.metadata, "create_all") as mock_create_all:
        from app.models import init_db
        init_db()
        mock_create_all.assert_called_once_with(bind=mock_create_engine.return_value)
