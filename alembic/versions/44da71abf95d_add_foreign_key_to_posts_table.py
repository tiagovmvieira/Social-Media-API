"""add foreign key to posts table

Revision ID: 44da71abf95d
Revises: aaa28e898802
Create Date: 2022-05-11 19:34:38.322103

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44da71abf95d'
down_revision = 'aaa28e898802'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable = False))
    op.create_foreign_key('posts_users_fk', source_table = 'posts',
                        referent_table = 'users', local_cols = ['owner_id'], remote_cols = ['user_id'], ondelete = 'CASCADE')
    pass

def downgrade():
    op.drop_constraint('post_users_fk', table_name = 'posts')
    op.drop_column('posts', 'owner_id')
    pass
