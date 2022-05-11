"""add content column to posts table

Revision ID: 301d094ab22d
Revises: 244b32129e2c
Create Date: 2022-05-11 19:25:19.410625

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '301d094ab22d'
down_revision = '244b32129e2c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable = False))
    pass

def downgrade():
    op.drop_column('posts', 'content')
    pass
