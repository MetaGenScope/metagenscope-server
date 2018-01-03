"""Organization model definitions."""


import datetime

from sqlalchemy.dialects.postgresql import UUID

from app.extensions import db


# pylint: disable=too-few-public-methods
class Organization(db.Model):
    """MetaGenScope Organization model."""

    __tablename__ = "organizations"

    # pylint: disable=invalid-name
    id = db.Column(UUID(as_uuid=True),
                   primary_key=True,
                   server_default=db.text("uuid_generate_v4()"))
    name = db.Column(db.String(128), unique=True, nullable=False)
    adminEmail = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, name, adminEmail, created_at=datetime.datetime.utcnow()):
        """Initialize MetaGenScope Organization model."""
        self.name = name
        self.adminEmail = adminEmail
        self.created_at = created_at
