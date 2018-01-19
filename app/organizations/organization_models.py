"""Organization model definitions."""

import datetime

from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from marshmallow import fields

from app.base import BaseSchema
from app.extensions import db
from app.users.user_models import users_organizations


# pylint: disable=too-few-public-methods
class Organization(db.Model):
    """MetaGenScope Organization model."""

    __tablename__ = 'organizations'

    # pylint: disable=invalid-name
    id = db.Column(UUID(as_uuid=True),
                   primary_key=True,
                   server_default=db.text('uuid_generate_v4()'))
    name = db.Column(db.String(128), unique=True, nullable=False)
    admin_email = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    users = relationship(
        'User',
        secondary=users_organizations,
        back_populates='organizations')

    def __init__(self, name, admin_email, created_at=datetime.datetime.utcnow()):
        """Initialize MetaGenScope Organization model."""
        self.name = name
        self.admin_email = admin_email
        self.created_at = created_at


class OrganizationSchema(BaseSchema):
    """Serializer for Organization model."""

    __envelope__ = {
        'single': 'organization',
        'many': 'organizations',
    }
    __model__ = Organization

    slug = fields.Str()
    name = fields.Str()
    admin_email = fields.Str()
    created_at = fields.Date()


organization_schema = OrganizationSchema()   # pylint: disable=invalid-name
