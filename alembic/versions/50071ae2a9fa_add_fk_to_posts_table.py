"""add fk to posts table

Revision ID: 50071ae2a9fa
Revises: c4535454cb4f
Create Date: 2021-12-31 01:32:22.287770

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50071ae2a9fa'
down_revision = 'c4535454cb4f'
branch_labels = None
depends_on = None


# https://alembic.sqlalchemy.org/en/latest/batch.html

def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False)),

    with op.batch_alter_table("posts") as batch_op:
        batch_op.create_foreign_key(
            "post_users_fk",
            # source_table="posts_testing",
            referent_table="users",  # target table
            local_cols=["owner_id"],  # source table
            remote_cols=["id"],  # target table
            ondelete="cascade"
        )

    pass


def downgrade():
    with op.batch_alter_table("posts") as batch_op:  # remove constraint first
        batch_op.drop_constraint(
            "post_users_fk",
            # table_name="posts_testing"
        )

    op.drop_column("posts", "owner_id")

    pass
