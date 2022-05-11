"""create posts table

Revision ID: 244b32129e2c
Revises: 
Create Date: 2022-05-11 19:22:09.802100

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '244b32129e2c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,
                    primary_key = True), sa.Column('title', sa.String(), nullable =  False))
    pass

def downgrade():
    op.drop_table('posts')
    pass
