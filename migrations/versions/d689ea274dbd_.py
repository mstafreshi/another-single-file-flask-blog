"""empty message

Revision ID: d689ea274dbd
Revises: 76bed5892913
Create Date: 2023-05-09 21:08:26.670258

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd689ea274dbd'
down_revision = '76bed5892913'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('linkdump_categories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('integrated_with_template', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('linkdump_categories', schema=None) as batch_op:
        batch_op.drop_column('integrated_with_template')

    # ### end Alembic commands ###
