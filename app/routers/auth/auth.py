from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.services.user import user as user_service
from app.models import SessionLocal
from app.schemas.token import token as token_schema
from app.schemas.auth import auth as auth_schema
from app.core.config.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.security.security import create_access_token
from app.utils.db import get_db

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")

@router.post("/login", response_model=token_schema.Token)
def login(form_data: auth_schema.LoginForm, db: Session = Depends(get_db)):
    result = user_service.authenticate_user(db, form_data.email, form_data.password)
    
    if "error" in result:
        if result["error"] == "User not registered":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not registered",
                headers={"WWW-Authenticate": "Bearer"},
            )
        elif result["error"] == "Incorrect password":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    user = result["user"]
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "user": user}
