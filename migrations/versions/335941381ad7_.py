"""empty message

Revision ID: 335941381ad7
Revises: cf7371a81283
Create Date: 2019-12-07 22:12:16.273962

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '335941381ad7'
down_revision = 'cf7371a81283'
branch_labels = None
depends_on = None


def upgrade():
  op.alter_column('terms', 'description', existing_type=sa.String(length=128), type_=sa.String(length=256))

def downgrade():
  op.alter_column('terms', 'description', existing_type=sa.String(length=256), type_=sa.String(length=128))

