"""empty message

Revision ID: 414bedf5f008
Revises: 2511c836e170
Create Date: 2021-03-10 13:20:32.063703

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '414bedf5f008'
down_revision = '2511c836e170'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contact',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('message', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('contact')
    # ### end Alembic commands ###
