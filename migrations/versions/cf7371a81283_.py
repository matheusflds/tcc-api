"""empty message

Revision ID: cf7371a81283
Revises: 8e3277268e47
Create Date: 2019-12-04 14:09:10.542168

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf7371a81283'
down_revision = '8e3277268e47'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('terms', 'anger', existing_type=sa.Integer(), type_=sa.Float())
    op.alter_column('terms', 'fear', existing_type=sa.Integer(), type_=sa.Float())
    op.alter_column('terms', 'joy', existing_type=sa.Integer(), type_=sa.Float())
    op.alter_column('terms', 'sadness', existing_type=sa.Integer(), type_=sa.Float())
    op.alter_column('terms', 'polarity', existing_type=sa.Integer(), type_=sa.Float())

def downgrade():
    op.alter_column('terms', 'anger', existing_type=sa.Float(), type_=sa.Integer())
    op.alter_column('terms', 'fear', existing_type=sa.Float(), type_=sa.Integer())
    op.alter_column('terms', 'joy', existing_type=sa.Float(), type_=sa.Integer())
    op.alter_column('terms', 'sadness', existing_type=sa.Float(), type_=sa.Integer())
    op.alter_column('terms', 'polarity', existing_type=sa.Float(), type_=sa.Integer())
