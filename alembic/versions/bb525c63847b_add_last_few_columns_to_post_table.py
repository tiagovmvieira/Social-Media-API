"""add last few columns to post table

Revision ID: bb525c63847b
Revises: 44da71abf95d
Create Date: 2022-05-11 19:41:58.392371

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb525c63847b'
down_revision = '44da71abf95d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable = False, server_default = 'TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone = True), nullable = False, server_default = sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
