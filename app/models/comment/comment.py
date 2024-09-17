from sqlalchemy import Column, Text, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models import Base

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    author_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    article_id = Column(UUID(as_uuid=True), ForeignKey('articles.id'), nullable=False)

    author = relationship("User", back_populates="comments")
    article = relationship("Article", back_populates="comments")
