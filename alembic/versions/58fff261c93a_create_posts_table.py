"""create posts table

Revision ID: 58fff261c93a
Revises: 
Create Date: 2021-12-31 01:23:38.195044

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58fff261c93a'
down_revision = None
branch_labels = None
depends_on = None


# https://alembic.sqlalchemy.org/en/latest/api/ddl.html

def upgrade():
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False)
    )
    pass


def downgrade():
    op.drop_table("posts")
    pass
