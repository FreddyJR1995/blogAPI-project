from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models import Base

article_label_association = Table(
    'article_label', Base.metadata,
    Column('article_id', UUID(as_uuid=True), ForeignKey('articles.id')),
    Column('label_id', UUID(as_uuid=True), ForeignKey('labels.id'))
)

class Article(Base):
    __tablename__ = 'articles'
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    title = Column(String, index=True)
    content = Column(Text)
    author_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    author = relationship("User", back_populates="articles")
    labels = relationship("Label", secondary=article_label_association, back_populates="articles")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    comments = relationship("Comment", back_populates="article")
