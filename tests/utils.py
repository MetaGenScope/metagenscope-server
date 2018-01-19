"""Common utility methods for use in testing."""

import datetime
import json

from functools import wraps

from app import db
from app.users.user_models import User
from app.organizations.organization_models import Organization
from app.sample_groups.sample_group_models import SampleGroup


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
    organization = Organization(name=name, admin_email=admin_email, created_at=created_at)
    db.session.add(organization)
    db.session.commit()
    return organization

def add_sample_group(name, access_scheme='public', created_at=datetime.datetime.utcnow()):
    """Wrap functionality for adding sample group."""
    group = SampleGroup(name=name, access_scheme=access_scheme, created_at=created_at)
    db.session.add(group)
    db.session.commit()
    return group

# pylint: disable=invalid-name
def with_user(f):
    """Decorate API route calls requiring authentication."""
    @wraps(f)
    def decorated_function(self, *args, **kwargs):
        """Wrap function f."""
        login_user = add_user('test', 'test@test.com', 'test')
        with self.client:
            resp_login = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )
            auth_headers = dict(
                Authorization='Bearer ' + json.loads(
                    resp_login.data.decode()
                )['auth_token']
            )

        return f(self, auth_headers, login_user, *args, **kwargs)
    return decorated_function
