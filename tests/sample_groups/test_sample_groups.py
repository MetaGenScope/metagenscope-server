"""Test suite for Sample Group model."""

from sqlalchemy.exc import IntegrityError

from app import db
from app.analysis_results.analysis_result_models import AnalysisResultMeta
from app.samples.sample_models import Sample
from app.sample_groups.sample_group_models import SampleGroup
from tests.base import BaseTestCase
from tests.utils import add_sample_group


class TestSampleGroupModel(BaseTestCase):
    """Test suite for SampleGroup model."""

    def test_add_sample_group(self):
        """Ensure sample group model is created correctly."""
        group = add_sample_group('Sample Group One', access_scheme='public')
        self.assertTrue(group.id)
        self.assertEqual(group.name, 'Sample Group One')
        self.assertEqual(group.access_scheme, 'public')
        self.assertTrue(group.created_at)

    def test_add_user_duplicate_name(self):
        """Ensure duplicate group names are not allowed."""
        add_sample_group('Sample Group One', access_scheme='public')
        duplicate_group = SampleGroup(
            name='Sample Group One',
            analysis_result=AnalysisResultMeta().save(),
            access_scheme='public',
        )
        db.session.add(duplicate_group)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_sample_group_analysis_result(self):  # pylint: disable=invalid-name
        """Ensure sample group's analysis result can be accessed."""
        analysis_result = AnalysisResultMeta().save()
        sample_group = add_sample_group('Sample Group One', analysis_result=analysis_result)
        self.assertEqual(sample_group.analysis_result, analysis_result)

    def test_add_samples(self):
        """Ensure that samples can be added to SampleGroup."""
        sample_group = add_sample_group('Sample Group One', access_scheme='public')
        sample_one = Sample(name='SMPL_01', metadata={'subject_group': 1}).save()
        sample_two = Sample(name='SMPL_02', metadata={'subject_group': 4}).save()
        sample_group.samples = [sample_one, sample_two]
        db.session.commit()
        self.assertEqual(len(sample_group.sample_ids), 2)
        self.assertIn(sample_one.uuid, sample_group.sample_ids)
        self.assertIn(sample_two.uuid, sample_group.sample_ids)
        samples = sample_group.samples
        self.assertEqual(len(samples), 2)
        self.assertIn(sample_one, samples)
        self.assertIn(sample_two, samples)
