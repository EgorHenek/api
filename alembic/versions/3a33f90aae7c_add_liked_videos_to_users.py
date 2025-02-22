"""Add liked videos to users

Revision ID: 3a33f90aae7c
Revises: 35ebe639c258
Create Date: 2020-02-13 14:30:39.226632

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "3a33f90aae7c"
down_revision = "35ebe639c258"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "liked_videos",
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("video_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.ForeignKeyConstraint(
            ["video_id"],
            ["videos.id"],
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("liked_videos")
    # ### end Alembic commands ###
