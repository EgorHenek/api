"""Add comments table

Revision ID: c56146eaf110
Revises: ee29f266ee74
Create Date: 2019-12-23 15:27:42.917219

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'c56146eaf110'
down_revision = 'ee29f266ee74'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'comments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('published_at', sa.DateTime(), nullable=False),
        sa.Column('deleted', sa.Boolean(), nullable=True),
        sa.Column('video_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(
            ['video_id'],
            ['videos.id'],
            ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comments')
    # ### end Alembic commands ###
