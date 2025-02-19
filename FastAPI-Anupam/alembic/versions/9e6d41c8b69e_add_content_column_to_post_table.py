"""add content column to post table

Revision ID: 9e6d41c8b69e
Revises: c866e2527a62
Create Date: 2024-04-03 14:07:55.580150

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e6d41c8b69e'
down_revision = 'c866e2527a62'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable= False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
