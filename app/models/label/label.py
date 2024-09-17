from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models import Base
from app.models.article.article import article_label_association

class Label(Base):
    __tablename__ = 'labels'
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    text = Column(String, unique=True, index=True)
    articles = relationship("Article", secondary=article_label_association, back_populates="labels")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
