"""Rename adminEmail --> admin_email

Revision ID: 67bde1501dde
Revises: 4b6145b431fe
Create Date: 2018-01-19 11:42:40.990548

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67bde1501dde'
down_revision = '4b6145b431fe'
branch_labels = None
depends_on = None


def upgrade():
    # Rename adminEmail --> admin_email
    op.alter_column('organizations', 'adminEmail', new_column_name='admin_email')


def downgrade():
    op.alter_column('organizations', 'admin_email', new_column_name='adminEmail')
