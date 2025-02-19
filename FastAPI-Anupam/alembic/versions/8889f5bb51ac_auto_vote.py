"""auto-vote

Revision ID: 8889f5bb51ac
Revises: 4c4464310886
Create Date: 2024-04-03 21:06:36.526105

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8889f5bb51ac'
down_revision = '4c4464310886'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
    sa.Column('user_id',sa.Integer(),nullable=False),
    sa.Column('post_id',sa.Integer(),nullable=False),
    sa.ForeignKeyConstraint(['post_id'],['posts.id'],ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'],['users.id'],ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id','post_id'))
    # ### end Alembic commands ###


def downgrade():
    op.drop_table('votes')
    # ### commands auto generated by Alembic - please adjust! ###
    # op.create_table('users',
    # sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('users_id_seq'::regclass)"), autoincrement=True, nullable=False),
    # sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
    # sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=False),
    # sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    # sa.PrimaryKeyConstraint('id', name='users_pkey'),
    # sa.UniqueConstraint('email', name='users_email_key'),
    # postgresql_ignore_search_path=False
    # )
    # op.create_table('posts',
    # sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    # sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False),
    # sa.Column('content', sa.VARCHAR(), autoincrement=False, nullable=False),
    # sa.Column('owner_id', sa.INTEGER(), autoincrement=False, nullable=False),
    # sa.Column('published', sa.BOOLEAN(), server_default=sa.text('true'), autoincrement=False, nullable=False),
    # sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    # sa.ForeignKeyConstraint(['owner_id'], ['users.id'], name='post_users_fk', ondelete='CASCADE'),
    # sa.PrimaryKeyConstraint('id', name='posts_pkey')
    # )
    # ### end Alembic commands ###
