"""users table

Revision ID: ca613cd445a4
Revises: 
Create Date: 2020-09-13 15:39:03.355294

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca613cd445a4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('board_model',
    sa.Column('id', sa.String(length=128), nullable=False),
    sa.Column('body', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('board_model')
    # ### end Alembic commands ###