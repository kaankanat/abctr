"""Sync migration history

Revision ID: 91a595369bc4
Revises: 979491a2cef7
Create Date: 2023-08-25 19:29:05.161684

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91a595369bc4'
down_revision = '979491a2cef7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('company_info', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_company_info_user', 'user', ['user_id'], ['id'])

    with op.batch_alter_table('person', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_person_user', 'user', ['user_id'], ['id'])

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('company_info_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_user_company_info', 'company_info', ['company_info_id'], ['id'])
        batch_op.add_column(sa.Column('is_logged_in', sa.Boolean(), default=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint('fk_user_company_info', type_='foreignkey')
        batch_op.drop_column('company_info_id')

    with op.batch_alter_table('person', schema=None) as batch_op:
        batch_op.drop_constraint('fk_person_user', type_='foreignkey')
        batch_op.drop_column('user_id')

    with op.batch_alter_table('company_info', schema=None) as batch_op:
        batch_op.drop_constraint('fk_company_info_user', type_='foreignkey')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###