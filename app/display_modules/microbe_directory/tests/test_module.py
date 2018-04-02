"""Test suite for Microbe Directory diplay module."""
from app.display_modules.display_module_base_test import BaseDisplayModuleTest
from app.display_modules.microbe_directory.wrangler import MicrobeDirectoryWrangler
from app.samples.sample_models import Sample
from app.display_modules.microbe_directory.models import MicrobeDirectoryResult
from app.display_modules.microbe_directory.constants import MODULE_NAME
from app.display_modules.microbe_directory.tests.factory import MicrobeDirectoryFactory
from app.tool_results.microbe_directory.tests.factory import (
    create_values,
    create_microbe_directory
)



class TestMethylsModule(BaseDisplayModuleTest):
    """Test suite for Microbe Directory diplay module."""

    def test_get_microbe_directory(self):
        """Ensure getting a single Methyl behaves correctly."""
        methyls = MicrobeDirectoryFactory()
        self.generic_getter_test(methyls, 'microbe_directory')

    def test_add_microbe_directory(self):
        """Ensure Methyl model is created correctly."""
        samples = create_values()
        microbe_directory_result = MicrobeDirectoryResult(samples=samples)
        self.generic_adder_test(microbe_directory_result, 'microbe_directory')

    def test_run_mixcrobe_directory_sample_group(self):  # pylint: disable=invalid-name
        """Ensure microbe directory run_sample_group produces correct results."""

        def create_sample(i):
            """Create unique sample for index i."""
            data = create_microbe_directory()
            return Sample(name=f'Sample{i}',
                          metadata={'foobar': f'baz{i}'},
                          microbe_directory_annotate=data).save()

        self.generic_run_group_test(create_sample,
                                    MicrobeDirectoryWrangler,
                                    MODULE_NAME)
