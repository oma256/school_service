"""empty message

Revision ID: 2a34ebf22397
Revises: 45bdd50bf137
Create Date: 2024-06-18 20:33:00.752232

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a34ebf22397'
down_revision = '45bdd50bf137'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('t_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=128), nullable=True),
    sa.Column('last_name', sa.String(length=128), nullable=True),
    sa.Column('email', sa.String(length=256), nullable=True),
    sa.Column('phone_number', sa.String(length=32), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('t_user')
    # ### end Alembic commands ###
