from datetime import datetime, timedelta
from app.core.security import verify_password, get_password_hash, create_access_token, verify_token
from app.schemas.token.token import TokenData
from jose import JWTError, jwt
from fastapi import HTTPException, status
from unittest.mock import patch, MagicMock
import pytest

SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"

def test_verify_password_should_validate_hashed_password_when_it_is_correct():
    hashed_password = get_password_hash("mysecretpassword")
    assert verify_password("mysecretpassword", hashed_password)

def test_verify_password_should_validate_hashed_password_when_it_is_incorrect():
    hashed_password = get_password_hash("mysecretpassword")
    assert not verify_password("wrongpassword", hashed_password)

def test_get_password_hash_should_return_a_valid_password():
    password = "mysecretpassword"
    hashed_password = get_password_hash(password)
    assert hashed_password != password
    assert verify_password(password, hashed_password)

@patch('jose.jwt.encode')
@patch('datetime.datetime')
def test_create_access_token_without_expiry(mock_datetime, mock_jwt_encode):
    mock_datetime.utcnow.return_value = datetime(2023, 1, 1)
    mock_jwt_encode.return_value = "mocked_token"

    data = {"sub": "testuser"}
    token = create_access_token(data)
    
    assert token == "mocked_token"

@patch('jose.jwt.encode')
@patch('datetime.datetime')
def test_create_access_token_with_expiry(mock_datetime, mock_jwt_encode):
    mock_datetime.utcnow.return_value = datetime(2023, 1, 1)
    mock_jwt_encode.return_value = "mocked_token"

    data = {"sub": "testuser"}
    expires_delta = timedelta(minutes=30)
    token = create_access_token(data, expires_delta)
    
    assert token == "mocked_token"

@patch('jose.jwt.decode')
@patch('app.schemas.token.token.TokenData')
def test_verify_token_valid(mock_token_data, mock_jwt_decode):
    mock_jwt_decode.return_value = {"sub": "testuser"}
    mock_token_data.return_value = TokenData(username="testuser")

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = "valid_token"
    token_data = verify_token(token, credentials_exception)
    assert token_data.username == "testuser"
    mock_jwt_decode.assert_called_once_with(token, SECRET_KEY, algorithms=[ALGORITHM])
    
@patch('jose.jwt.decode')
def test_verify_token_invalid_token(mock_jwt_decode):
    mock_jwt_decode.side_effect = JWTError()
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = "invalid_token"
    with pytest.raises(HTTPException) as excinfo:
        verify_token(token, credentials_exception)
    assert excinfo.value == credentials_exception
    mock_jwt_decode.assert_called_once_with(token, SECRET_KEY, algorithms=[ALGORITHM])

@patch('jose.jwt.decode')
def test_verify_token_no_username(mock_jwt_decode):
    mock_jwt_decode.return_value = {"sub": None}
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = "token_without_username"
    with pytest.raises(HTTPException) as excinfo:
        verify_token(token, credentials_exception)
    assert excinfo.value == credentials_exception
    mock_jwt_decode.assert_called_once_with(token, SECRET_KEY, algorithms=[ALGORITHM])
