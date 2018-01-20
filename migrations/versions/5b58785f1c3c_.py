"""Add one-to-many relationship between organizations and sample groups

Revision ID: 5b58785f1c3c
Revises: 67bde1501dde
Create Date: 2018-01-20 16:48:26.624371

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5b58785f1c3c'
down_revision = '67bde1501dde'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('sample_groups', sa.Column('organization_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key('fk_organization_sample_group', 'sample_groups', 'organizations', ['organization_id'], ['id'])


def downgrade():
    op.drop_constraint('fk_organization_sample_group', 'sample_groups', type_='foreignkey')
    op.drop_column('sample_groups', 'organization_id')
