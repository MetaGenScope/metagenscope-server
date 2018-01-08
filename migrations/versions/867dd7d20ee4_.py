"""Added many-to-many relationship between organizations and users

Revision ID: 867dd7d20ee4
Revises: f01f18259e54
Create Date: 2018-01-05 18:00:16.452900

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '867dd7d20ee4'
down_revision = 'f01f18259e54'
branch_labels = None
depends_on = None


def upgrade():
    # Create link table
    op.create_table('users_organizations',
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('organization_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('role', sa.String(length=128), default="member", nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )


def downgrade():
    op.drop_table('users_organizations')
