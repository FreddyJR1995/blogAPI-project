from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.models import Base

article_label_association = Table(
    'article_label', Base.metadata,
    Column('article_id', Integer, ForeignKey('articles.id')),
    Column('label_id', Integer, ForeignKey('labels.id'))
)

class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship("User", back_populates="articles")
    labels = relationship("Label", secondary=article_label_association, back_populates="articles")
