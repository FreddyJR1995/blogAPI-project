import pytest
from unittest.mock import patch, MagicMock
from app.services.user.user import get_user, get_user_by_email, create_user, authenticate_user
from app.models.user.user import User
from app.schemas.user.user import UserCreate
from sqlalchemy.orm import Session

mock_user_data = {
    "id": 1,
    "name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "password": "hashed_password"
}

class MockUser:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

@pytest.fixture
def mock_session():
    return MagicMock(spec=Session)

def test_get_user_found(mock_session):
    mock_user = MockUser(**mock_user_data)
    mock_session.query().filter().first.return_value = mock_user
    user = get_user(mock_session, 1)
    assert user.id == 1
    assert user.email == "john.doe@example.com"

def test_get_user_not_found(mock_session):
    mock_session.query().filter().first.return_value = None
    user = get_user(mock_session, 1)
    assert user is None

def test_get_user_by_email_found(mock_session):
    mock_user = MockUser(**mock_user_data)
    mock_session.query().filter().first.return_value = mock_user
    user = get_user_by_email(mock_session, "john.doe@example.com")
    assert user.email == "john.doe@example.com"
    assert user.id == 1

def test_get_user_by_email_not_found(mock_session):
    mock_session.query().filter().first.return_value = None
    user = get_user_by_email(mock_session, "john.doe@example.com")
    assert user is None

@patch("bcrypt.hashpw")
@patch("bcrypt.gensalt")
def test_create_user(mock_gensalt, mock_hashpw, mock_session):
    mock_gensalt.return_value = b'salt'
    mock_hashpw.return_value = b'hashed_password'
    
    user_data = UserCreate(
        name="John",
        last_name="Doe",
        email="john.doe@example.com",
        password="password"
    )
    mock_user = MockUser(**mock_user_data)
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = mock_user
    
    user = create_user(mock_session, user_data)
    
    assert user.email == "john.doe@example.com"
    assert user.password == "hashed_password"

@patch("bcrypt.checkpw")
def test_authenticate_user_success(mock_checkpw, mock_session):
    mock_user = MockUser(**mock_user_data)
    mock_session.query().filter().first.return_value = mock_user
    mock_checkpw.return_value = True

    response = authenticate_user(mock_session, "john.doe@example.com", "password")
    
    assert "user" in response
    assert response["user"].email == "john.doe@example.com"

def test_authenticate_user_not_found(mock_session):
    mock_session.query().filter().first.return_value = None

    response = authenticate_user(mock_session, "john.doe@example.com", "password")
    
    assert "error" in response
    assert response["error"] == "User not registered"

@patch("bcrypt.checkpw")
def test_authenticate_user_incorrect_password(mock_checkpw, mock_session):
    mock_user = MockUser(**mock_user_data)
    mock_session.query().filter().first.return_value = mock_user
    mock_checkpw.return_value = False

    response = authenticate_user(mock_session, "john.doe@example.com", "password")
    
    assert "error" in response
    assert response["error"] == "Incorrect password"
