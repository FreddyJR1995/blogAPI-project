from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import SessionLocal
from app.schemas.user import user as user_schema
from app.services.user import user as user_service
from app.routers.auth.auth import oauth2_scheme
from fastapi.security import OAuth2PasswordBearer
from app.core.security.security import verify_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_token(token, credentials_exception)
    user = user_service.get_user_by_email(db, email=token_data.username)
    if user is None:
        raise credentials_exception
    return user

@router.post("/register/", response_model=user_schema.User)
def create_user(user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user_create)

@router.get("/users/me", response_model=user_schema.User)
def read_users_me(current_user: user_schema.User = Depends(get_current_user)):
    return current_user
