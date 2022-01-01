"""add content col to posts

Revision ID: d79928e7fe04
Revises: 58fff261c93a
Create Date: 2021-12-31 01:31:18.920581

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd79928e7fe04'
down_revision = '58fff261c93a'
branch_labels = None
depends_on = None


def upgrade():
    # op.add_column(
    #     "posts",
    #     sa.Column("content", sa.String(), nullable=False)
    # )
    pass


def downgrade():
    # op.drop_column("posts", "content")
    pass
