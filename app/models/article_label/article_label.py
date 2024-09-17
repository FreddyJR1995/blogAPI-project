from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models import Base

article_label_association = Table(
    'article_label', Base.metadata,
    Column('article_id', UUID(as_uuid=True), ForeignKey('articles.id')),
    Column('label_id', UUID(as_uuid=True), ForeignKey('labels.id'))
)