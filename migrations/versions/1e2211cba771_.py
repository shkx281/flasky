"""empty message

Revision ID: 1e2211cba771
Revises: 0c9844eae4f9
Create Date: 2022-05-10 22:39:36.645274

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e2211cba771'
down_revision = '0c9844eae4f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('driver',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('team', sa.String(), nullable=True),
    sa.Column('country', sa.String(), nullable=True),
    sa.Column('handsome', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('driver')
    # ### end Alembic commands ###
