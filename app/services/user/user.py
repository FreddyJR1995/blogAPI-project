from sqlalchemy.orm import Session
from app.models.user.user import User
from app.schemas.user.user import UserCreate
import bcrypt

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = User(name=user.name, last_name=user.last_name, email=user.email, password=hashed_password.decode('utf-8'))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return {"error": "User not registered"}
    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return {"error": "Incorrect password"}
    return {"user": user}
