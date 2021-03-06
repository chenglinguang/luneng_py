"""follow_part

Revision ID: dbfd9a30962c
Revises: 0d077e2d00dc
Create Date: 2016-08-03 11:39:09.705877

"""

# revision identifiers, used by Alembic.
revision = 'dbfd9a30962c'
down_revision = '0d077e2d00dc'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('follows',
    sa.Column('follower_id', sa.Integer(), nullable=False),
    sa.Column('followed_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('follower_id', 'followed_id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('follows')
    ### end Alembic commands ###
