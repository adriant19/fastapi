"""add last few cols

Revision ID: 03fb462a0275
Revises: 50071ae2a9fa
Create Date: 2021-12-31 11:39:40.273970

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03fb462a0275'
down_revision = '50071ae2a9fa'
branch_labels = None
depends_on = None


def upgrade():

    with op.batch_alter_table("posts_testing") as batch_op:
        batch_op.add_column(
            # "posts_testing",
            sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE")
        )

        batch_op.add_column(
            # "posts_setting",
            sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("current_timestamp"))
        )
    pass


def downgrade():
    with op.batch_alter_table("posts_testing") as batch_op:
        batch_op.drop_column(
            # "posts_setting",
            "published"
        )

        batch_op.drop_column(
            # "posts_setting",
            "created_at"
        )
    pass
