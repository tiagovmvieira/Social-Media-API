"""add user table

Revision ID: 479cb0781529
Revises: ac9d4c7341ec
Create Date: 2022-04-28 22:50:36.792770

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '479cb0781529'
down_revision = 'ac9d4c7341ec'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable = False),
                    sa.Column('email', sa.String(), nullable = False),
                    sa.Column('password', sa.String(), nullable = False),
                    sa.Column('crated_at', sa.TIMESTAMP(timezone = True),
                            server_default = sa.text('now()'), nullable = False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email') #unique constraint 
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
