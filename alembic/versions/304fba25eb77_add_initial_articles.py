"""Add initial articles

Revision ID: 304fba25eb77
Revises: bc9d89e12614
Create Date: 2024-08-17 23:46:19.252872

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from app.models.article.article import Article
from app.models.user.user import User
from app.models.label.label import Label



# revision identifiers, used by Alembic.
revision = '304fba25eb77'
down_revision = 'bc9d89e12614'
branch_labels = None
depends_on = None

Session = sessionmaker()

def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    author = session.query(User).filter(User.email == "john.doe@example.com").first()

    if not author:
        raise ValueError("Author not found, make sure the user is created")

    markdown_content = """# Heading 1

This is a paragraph with some **bold text**, *italic text*, and a [link](http://example.com).

## Subheading

Another paragraph with a list:
- Item 1
- Item 2
- Item 3

### Subheading 2

_Finally, a paragraph with some underlined text and **bold text** together_.
"""

    for i in range(10):
        article = Article(
            title=f"Sample Article {i + 1}",
            content=markdown_content,
            author_id=author.id
        )
        session.add(article)

        labels = session.query(Label).limit(3).all()
        
        article.labels.extend(labels)

    session.commit()


def downgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    session.execute(
        sa.text(
            "DELETE FROM articles WHERE title IN ('Article 1', 'Article 2', 'Article 3', 'Article 4', 'Article 5', 'Article 6', 'Article 7', 'Article 8', 'Article 9', 'Article 10')"
        )
    )
    
    session.commit()