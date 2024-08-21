from app.models.label.label import Label
from sqlalchemy.orm import Session

def get_all_labels(db: Session):
    return db.query(Label)
