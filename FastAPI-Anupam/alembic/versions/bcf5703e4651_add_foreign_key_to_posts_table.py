"""add foreign-key to posts table

Revision ID: bcf5703e4651
Revises: 1e232f8b035e
Create Date: 2024-04-03 15:07:28.100838

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bcf5703e4651'
down_revision = '1e232f8b035e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('post_users_fk',source_table='posts',referent_table="users",
                          local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk',table_name="posts")
    op.drop_column('posts','owner_id')
    pass
