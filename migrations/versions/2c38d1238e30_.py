"""empty message

Revision ID: 2c38d1238e30
Revises: 335941381ad7
Create Date: 2019-12-07 22:27:09.715154

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '2c38d1238e30'
down_revision = '335941381ad7'
branch_labels = None
depends_on = None

def upgrade():
  op.alter_column('topics', 'words', existing_type=postgresql.ARRAY(sa.String(length=32)), type_=postgresql.ARRAY(sa.String(length=64)))

def downgrade():
  op.alter_column('topics', 'words', existing_type=postgresql.ARRAY(sa.String(length=64)), type_=postgresql.ARRAY(sa.String(length=32)))
