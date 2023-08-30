"""Add is_logged_in column

Revision ID: dcd50e62c56b
Revises: 91a595369bc4
Create Date: 2023-08-26 12:11:13.128809

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dcd50e62c56b'
down_revision = '91a595369bc4'
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('is_logged_in')

    # ### end Alembic commands ###
