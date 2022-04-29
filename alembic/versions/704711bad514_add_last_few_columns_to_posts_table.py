"""add last few columns to posts table

Revision ID: 704711bad514
Revises: 9da797af34b8
Create Date: 2022-04-28 23:23:45.062455

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '704711bad514'
down_revision = '9da797af34b8'
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
