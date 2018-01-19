"""Test suite for Sample Group model."""

from sqlalchemy.exc import IntegrityError

from app import db
from app.sample_groups.sample_group_models import SampleGroup
from tests.base import BaseTestCase
from tests.utils import add_sample_group


class TestUserModel(BaseTestCase):
    """Test suite for User model."""

    def test_add_sample_group(self):
        """Ensure sample group model is created correctly."""
        group = add_sample_group('Sample Group One', 'public')
        self.assertTrue(group.id)
        self.assertEqual(group.name, 'Sample Group One')
        self.assertEqual(group.access_scheme, 'public')
        self.assertTrue(group.created_at)

    def test_add_user_duplicate_name(self):
        """Ensure duplicate group names are not allowed."""
        add_sample_group('Sample Group One', 'public')
        duplicate_group = SampleGroup(
            name='Sample Group One',
            access_scheme='public',
        )
        db.session.add(duplicate_group)
        self.assertRaises(IntegrityError, db.session.commit)
