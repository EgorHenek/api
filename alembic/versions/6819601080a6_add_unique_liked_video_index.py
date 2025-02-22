"""Add unique liked video index

Revision ID: 6819601080a6
Revises: 3a33f90aae7c
Create Date: 2020-02-13 15:14:11.782833

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "6819601080a6"
down_revision = "3a33f90aae7c"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(
        "unique_liked_video",
        "liked_videos",
        ["user_id", "video_id"],
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("unique_liked_video", "liked_videos", type_="unique")
    # ### end Alembic commands ###
