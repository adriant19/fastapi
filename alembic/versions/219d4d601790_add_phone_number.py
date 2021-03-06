"""add phone number

Revision ID: 219d4d601790
Revises: fccb33765770
Create Date: 2021-12-31 16:31:51.769894

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '219d4d601790'
down_revision = 'fccb33765770'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('phone_number', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('phone_number')
    # ### end Alembic commands ###
