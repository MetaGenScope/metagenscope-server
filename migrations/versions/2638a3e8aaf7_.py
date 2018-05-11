"""Add Sample Placeholder table

Revision ID: 2638a3e8aaf7
Revises: 5b58785f1c3c
Create Date: 2018-03-06 15:47:47.311799

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2638a3e8aaf7'
down_revision = '5b58785f1c3c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('sample_placeholder',
    sa.Column('sample_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('sample_group_id', postgresql.UUID(as_uuid=True), nullable=False),
              sa.ForeignKeyConstraint(['sample_group_id'], ['sample_groups.id'], ),
              sa.PrimaryKeyConstraint('sample_id', 'sample_group_id'))



def downgrade():
    op.drop_table('sample_placeholder')
