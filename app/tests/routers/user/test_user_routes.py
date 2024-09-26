from unittest.mock import patch, MagicMock, ANY
import pytest
from sqlalchemy.orm import Session
from app.routers.user import user as user_router
from app.schemas.user import user as user_schema
from app.services.user import user as user_service
from app.utils.db import get_db
from app.core.security.security import verify_token
from fastapi import HTTPException, status
import uuid 

user_data = {
    "email": "testuser@example.com",
    "password": "testpassword",
    "name": "Test",
    "last_name": "User",
    "id": uuid.uuid4(),
}


@pytest.fixture
def mock_get_db():
    return MagicMock(Session)


@patch("app.services.user.user.create_user")
def test_create_user(mock_create_user, mock_get_db):
    user_create = user_schema.UserCreate(**user_data)
    mock_create_user.return_value = user_schema.User(**user_data)

    response = user_router.create_user(user_create, db=mock_get_db)

    assert response == user_schema.User(**user_data)
    mock_create_user.assert_called_once_with(mock_get_db, user_create)


@patch("app.routers.user.user.verify_token")
@patch("app.services.user.user.get_user_by_email")
def test_get_current_user(mock_get_user_by_email, mock_verify_token, mock_get_db):
    token = "mock_token"
    user = user_schema.User(**user_data)

    mock_verify_token.return_value = MagicMock(username=user.email)
    mock_get_user_by_email.return_value = user

    response = user_router.get_current_user(token=token, db=mock_get_db)
    print(response)

    assert response == user
    mock_verify_token.assert_called_once_with(token, ANY)
    mock_get_user_by_email.assert_called_once_with(mock_get_db, email=user.email)


@patch("app.routers.user.user.verify_token")
@patch("app.services.user.user.get_user_by_email")
def test_read_users_me(mock_get_user_by_email, mock_verify_token, mock_get_db):
    token = "mock_token"
    user = user_schema.User(**user_data)
    
    mock_verify_token.return_value = MagicMock(username=user.email)
    mock_get_user_by_email.return_value = user
    
    def override_get_current_user():
        return user
    
    response = user_router.read_users_me(current_user=override_get_current_user())
    
    assert response == user

@patch("app.routers.user.user.verify_token")
@patch("app.services.user.user.get_user_by_email")
def test_get_current_user_user_not_found(mock_get_user_by_email, mock_verify_token, mock_get_db):
    token = "mock_token"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    mock_verify_token.return_value = MagicMock(username="non_existent_user")
    mock_get_user_by_email.return_value = None
    
    with pytest.raises(HTTPException) as excinfo:
        user_router.get_current_user(token=token, db=mock_get_db)
    
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Could not validate credentials"
    mock_verify_token.assert_called_once_with(token, ANY)
    mock_get_user_by_email.assert_called_once_with(mock_get_db, email="non_existent_user")
