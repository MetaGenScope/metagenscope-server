"""Add analysis_result_uuid column to Sample Groups.

Revision ID: f50f4895f74d
Revises: 2638a3e8aaf7
Create Date: 2018-03-15 16:00:18.189121

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f50f4895f74d'
down_revision = '2638a3e8aaf7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('sample_groups', sa.Column('analysis_result_uuid', postgresql.UUID(as_uuid=True), nullable=False))


def downgrade():
    op.drop_column('sample_groups', 'analysis_result_uuid')
