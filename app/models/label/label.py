from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models import Base
from app.models.article.article import article_label_association

class Label(Base):
    __tablename__ = 'labels'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, unique=True, index=True)
    articles = relationship("Article", secondary=article_label_association, back_populates="labels")
