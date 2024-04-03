"""add last few columns to post table

Revision ID: 4c4464310886
Revises: bcf5703e4651
Create Date: 2024-04-03 20:35:35.253559

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c4464310886'
down_revision = 'bcf5703e4651'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('published',sa.Boolean(),nullable=False,server_default = 'TRUE'),)
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')

    pass

