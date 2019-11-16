"""empty message

Revision ID: 1f71c7a81451
Revises: 
Create Date: 2019-11-16 16:04:13.008679

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1f71c7a81451'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('terms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=64), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('topics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('term_id', sa.Integer(), nullable=True),
    sa.Column('words', postgresql.ARRAY(sa.String(length=32)), nullable=True),
    sa.Column('polarity', sa.Float(), nullable=True),
    sa.Column('anger_percentage', sa.Float(), nullable=True),
    sa.Column('fear_percentage', sa.Float(), nullable=True),
    sa.Column('joy_percentage', sa.Float(), nullable=True),
    sa.Column('sad_percentage', sa.Float(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['term_id'], ['terms.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('topics')
    op.drop_table('terms')
    # ### end Alembic commands ###
