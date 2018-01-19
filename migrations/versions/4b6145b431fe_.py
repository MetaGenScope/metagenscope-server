"""Add Sample Group table

Revision ID: 4b6145b431fe
Revises: 867dd7d20ee4
Create Date: 2018-01-17 15:31:44.478602

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4b6145b431fe'
down_revision = '867dd7d20ee4'
branch_labels = None
depends_on = None


def upgrade():
    # Create Sample Groups table
    op.create_table('sample_groups',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('access_scheme', sa.String(length=128), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )


def downgrade():
    op.drop_table('sample_groups')
