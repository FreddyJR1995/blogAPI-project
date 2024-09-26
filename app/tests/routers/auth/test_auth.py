from datetime import timedelta
from unittest.mock import patch, MagicMock
import pytest

from app.routers.auth import auth
from app.schemas.auth import auth as auth_schema
from app.schemas.token import token as token_schema
from app.core.config.config import ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import HTTPException
from app.utils.db import get_db

@pytest.fixture
def mock_get_db():
    db = MagicMock(Session)
    return db

@patch("app.routers.auth.auth.create_access_token")
@patch("app.services.user.user.authenticate_user")
@patch("app.utils.db")
def test_login_should_return_token_when_credentials_are_correct(mock_get_db, mock_authenticate_user, mock_create_access_token):
    mock_get_db.return_value = MagicMock()
    mock_authenticate_user.return_value = {"user": MagicMock(email="user@example.com")}
    mock_create_access_token.return_value = "mocked_token"
    
    form_data = auth_schema.LoginForm(email="user@example.com", password="correct_password")
    response = auth.login(form_data=form_data, db=mock_get_db())
    expected_user = mock_authenticate_user.return_value["user"]
    

    assert response == {
        "access_token": "mocked_token",
        "token_type": "bearer",
        "user": expected_user
    }
    mock_authenticate_user.assert_called_once_with(mock_get_db(), "user@example.com", "correct_password")
    mock_create_access_token.assert_called_once_with(
        data={"sub": "user@example.com"},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

@patch("app.routers.auth.auth.create_access_token")
@patch("app.services.user.user.authenticate_user")
@patch("app.utils.db")
def test_login_should_raise_an_exception_when_user_not_registered(mock_get_db, mock_authenticate_user, mock_create_access_token):
    mock_get_db.return_value = MagicMock()
    mock_authenticate_user.return_value = {"error": "User not registered"}
    
    form_data = auth_schema.LoginForm(email="not_registered@example.com", password="some_password")
    
    with pytest.raises(HTTPException) as exc_info:
        auth.login(form_data=form_data, db=mock_get_db())
    
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not registered"
    mock_authenticate_user.assert_called_once_with(mock_get_db(), "not_registered@example.com", "some_password")
    mock_create_access_token.assert_not_called()

@patch("app.routers.auth.auth.create_access_token")
@patch("app.services.user.user.authenticate_user")
@patch("app.utils.db")
def test_login_should_raise_an_exception_when_password_is_incorrect(mock_get_db, mock_authenticate_user, mock_create_access_token):
    mock_get_db.return_value = MagicMock()
    mock_authenticate_user.return_value = {"error": "Incorrect password"}
    
    form_data = auth_schema.LoginForm(email="user@example.com", password="incorrect_password")
    
    with pytest.raises(HTTPException) as exc_info:
        auth.login(form_data=form_data, db=mock_get_db())
    
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Incorrect password"
    mock_authenticate_user.assert_called_once_with(mock_get_db(), "user@example.com", "incorrect_password")
    mock_create_access_token.assert_not_called()