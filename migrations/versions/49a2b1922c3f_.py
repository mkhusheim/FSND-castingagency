"""empty message

Revision ID: 49a2b1922c3f
Revises: 
Create Date: 2020-08-25 01:25:12.935646

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49a2b1922c3f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('actors', 'age',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('actors', 'age',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###