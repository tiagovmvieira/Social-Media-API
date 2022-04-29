"""create posts table

Revision ID: c7d609b44017
Revises: 
Create Date: 2022-04-28 22:26:56.233585

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7d609b44017'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable= False))
    pass


def downgrade():
    op.drop_table('posts')
