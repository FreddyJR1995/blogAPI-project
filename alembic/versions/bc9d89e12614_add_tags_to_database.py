"""Add Tags To DataBase

Revision ID: bc9d89e12614
Revises: 52ba7f14bb96
Create Date: 2024-08-16 23:22:02.312194

"""
from alembic import op
import sqlalchemy as sa
import requests


# revision identifiers, used by Alembic.
revision = 'bc9d89e12614'
down_revision = '52ba7f14bb96'
branch_labels = None
depends_on = None

def fetch_tags():
    url = 'https://api.stackexchange.com/2.3/tags'
    params = {
        'order': 'desc',
        'sort': 'popular',
        'site': 'stackoverflow'
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        tags = response.json().get('items', [])
        return [tag['name'] for tag in tags]
    else:
        print(f"Error: {response.json()}")
        return []

def upgrade():
    tags = fetch_tags()
    if tags:
        connection = op.get_bind()
        for tag in tags:
            connection.execute(
                sa.text("INSERT INTO labels (text) VALUES (:text) ON CONFLICT (text) DO NOTHING"),
                {"text": tag}
            )

def downgrade():
    pass