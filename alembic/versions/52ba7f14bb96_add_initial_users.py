"""Add initial users

Revision ID: 52ba7f14bb96
Revises: None
Create Date: 2024-08-17 22:59:55.575638

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from app.schemas.user.user import UserCreate
from app.services.user.user import create_user


# revision identifiers, used by Alembic.
revision = '52ba7f14bb96'
down_revision = None
branch_labels = None
depends_on = None

Session = sessionmaker()

def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    users = [
        UserCreate(name="John", last_name="Doe", email="john.doe@example.com", password="password123"),
        UserCreate(name="Jane", last_name="Smith", email="jane.smith@example.com", password="securepassword"),
    ]

    for user in users:
        create_user(session, user)
    
    session.commit()


def downgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    session.execute(
        sa.text(
            "DELETE FROM users WHERE email IN ('john.doe@example.com', 'jane.smith@example.com')"
        )
    )
    
    session.commit()
