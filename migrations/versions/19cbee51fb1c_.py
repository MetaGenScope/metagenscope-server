"""Add theme and description to Sample Group

Revision ID: 19cbee51fb1c
Revises: f50f4895f74d
Create Date: 2018-04-18 15:09:44.025628

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19cbee51fb1c'
down_revision = 'f50f4895f74d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('sample_groups', sa.Column('description', sa.String(length=300), nullable=False))
    op.add_column('sample_groups', sa.Column('theme', sa.String(length=16), nullable=False))


def downgrade():
    op.drop_column('sample_groups', 'theme')
    op.drop_column('sample_groups', 'description')
