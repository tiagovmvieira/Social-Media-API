"""add content column to posts table

Revision ID: ac9d4c7341ec
Revises: c7d609b44017
Create Date: 2022-04-28 22:42:25.787682

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac9d4c7341ec'
down_revision = 'c7d609b44017'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass

def downgrade():
    op.drop_column('posts', 'content')
    pass
