"""The Conductor module orchestrates Display module generation based on changing data."""

from app.display_modules import all_display_modules
from app.samples.sample_models import Sample
from app.sample_groups.sample_group_models import SampleGroup


class DisplayModuleConductor:
    """The Conductor module orchestrates Display module generation based on ToolResult changes."""

    def __init__(self, sample_id, tool_result_cls):
        """
        Initialize the Conductor.

        Parameters
        ----------
        sample_id : str
            The ID of the Sample that had a ToolResult change event.
        tool_result_cls: ToolResultModule
            The class of the ToolResult that was changed.

        """
        self.sample_id = sample_id
        self.tool_result_cls = tool_result_cls
        self.downstream_modules = [module for module in all_display_modules
                                   if module.is_dependent_on_tool(self.tool_result_cls)]

    def direct_sample(self):
        """Kick off computation for the affected sample's relevant DisplayModules."""
        sample = Sample.objects.get(uuid=self.sample_id)
        tools_present = set(sample.tool_result_names)

        # Determine which dispaly modules can actually be computed based on tool results present
        valid_modules = []
        for module in self.downstream_modules:
            dependencies = set([tool.name() for tool in module.required_tool_results()])
            if dependencies <= tools_present:
                valid_modules.append(module)

        for module in valid_modules:
            # Pass off middleware execution to Wrangler
            module.get_wrangler().run_sample(sample_id=self.sample_id)

    def direct_sample_group(self, sample_group):
        """Kick off computation for a sample group's relevant DisplayModules."""
        tools_present_in_all = set(sample_group.tools_present)

        # Validate each module
        valid_modules = []
        for module in self.downstream_modules:
            dependencies = set([tool.name() for tool in module.required_tool_results()])
            if dependencies <= tools_present_in_all:
                valid_modules.append(module)

        for module in valid_modules:
            # Pass off middleware execution to Wrangler
            module.get_wrangler().run_sample_group(sample_group_id=sample_group.id)

    def direct_sample_groups(self):
        """Kick off computation for affected sample groups' relevant DisplayModules."""
        query_filter = SampleGroup.sample_ids.any(sample_id=self.sample_id)
        sample_groups = SampleGroup.query.filter(query_filter)
        for sample_group in sample_groups:
            self.direct_sample_group(sample_group)

    def shake_that_baton(self):
        """Begin the orchestration of middleware tasks."""
        self.direct_sample()
        self.direct_sample_groups()
