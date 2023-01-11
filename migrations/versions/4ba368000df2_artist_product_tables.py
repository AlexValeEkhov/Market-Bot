"""+ Artist, Product tables

Revision ID: 4ba368000df2
Revises: 60bf7a65beef
Create Date: 2023-01-11 12:54:22.184627

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ba368000df2'
down_revision = '60bf7a65beef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('artist', schema=None) as batch_op:
        batch_op.drop_column('pop')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('artist', schema=None) as batch_op:
        batch_op.add_column(sa.Column('pop', sa.VARCHAR(), nullable=True))

    # ### end Alembic commands ###
