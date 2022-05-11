"""create user table

Revision ID: aaa28e898802
Revises: 301d094ab22d
Create Date: 2022-05-11 19:27:52.828023

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aaa28e898802'
down_revision = '301d094ab22d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable = False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone = True),
                            server_default = sa.text('now()'), nullable = False),
                    sa.PrimaryKeyConstraint('user_id'),
                    sa.UniqueConstraint('email')
    )
    pass

def downgrade():
    op.drop_table('users')
    pass
