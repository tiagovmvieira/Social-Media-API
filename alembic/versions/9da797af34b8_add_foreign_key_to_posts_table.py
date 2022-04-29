"""add foreign-key to posts table

Revision ID: 9da797af34b8
Revises: 479cb0781529
Create Date: 2022-04-28 23:04:46.807389

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9da797af34b8'
down_revision = '479cb0781529'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable = False))
    op.create_foreign_key('posts_users_fk', source_table = 'posts', referent_table = 'users',
    local_cols = ['owner_id'], remote_cols=['id'], ondelete = 'CASCADE')
    pass

def downgrade():
    op.drop_constraint('post_users_fk', table_name = 'posts')
    op.drom_column('posts', 'owner_id')
    pass
