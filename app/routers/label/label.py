from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.label.label import get_all_labels
from app.schemas.label.label import Label
from typing import List
from app.utils.db import get_db


router = APIRouter()

@router.get("/labels/", response_model=List[Label])
def get_labels(db: Session = Depends(get_db)):
    return get_all_labels(db)