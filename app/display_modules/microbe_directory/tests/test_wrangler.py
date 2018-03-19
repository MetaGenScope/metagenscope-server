"""Test suite for Microbe Directory Wrangler."""

from app import db
from app.display_modules.microbe_directory.wrangler import MicrobeDirectoryWrangler
from app.samples.sample_models import Sample
from app.tool_results.microbe_directory.tests.factory import create_microbe_directory

from tests.base import BaseTestCase
from tests.utils import add_sample_group


class TestMicrobeDirectoryWrangler(BaseTestCase):
    """Test suite for Microbe Directory Wrangler."""

    def test_run_microbe_directory_sample_group(self):  # pylint: disable=invalid-name
        """Ensure run_sample_group produces correct results."""

        def create_sample(i):
            """Create unique sample for index i."""
            metadata = {'foobar': f'baz{i}'}
            data = create_microbe_directory()
            return Sample(name=f'Sample{i}',
                          metadata=metadata,
                          microbe_directory_annotate=data).save()

        sample_group = add_sample_group(name='SampleGroup01')
        sample_group.samples = [create_sample(i) for i in range(6)]
        db.session.commit()
        MicrobeDirectoryWrangler.run_sample_group(sample_group.id).get()
        analysis_result = sample_group.analysis_result
        self.assertIn('microbe_directory', analysis_result)
        microbe_directory = analysis_result.microbe_directory
        self.assertEqual(microbe_directory.status, 'S')
