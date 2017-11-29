"""Common utility methods for use in testing."""

import datetime


from app import db
from app.api.v1.models import User, Organization


def add_user(username, email, password, created_at=datetime.datetime.utcnow()):
    """Wrap functionality for adding user."""
    user = User(
        username=username,
        email=email,
        password=password,
        created_at=created_at)
    db.session.add(user)
    db.session.commit()
    return user


def add_organization(name, admin_email, created_at=datetime.datetime.utcnow()):
    """Wrap functionality for adding organization."""
    organization = Organization(name=name, adminEmail=admin_email, created_at=created_at)
    db.session.add(organization)
    db.session.commit()
    return organization
