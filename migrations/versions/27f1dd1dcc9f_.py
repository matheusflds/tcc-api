"""empty message

Revision ID: 27f1dd1dcc9f
Revises: 37859257bce7
Create Date: 2019-11-22 21:53:46.041331

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '27f1dd1dcc9f'
down_revision = '37859257bce7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('topics', sa.Column('words_probability', postgresql.ARRAY(sa.Integer()), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('topics', 'words_probability')
    # ### end Alembic commands ###
