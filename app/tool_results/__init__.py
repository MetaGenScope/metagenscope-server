"""Modules for genomic analysis tool outputs."""

import importlib
import inspect
import pkgutil
import sys

# Re-export modules
from app.tool_results.tool_module import ToolResult, ToolResultModule


def find_all_tool_modules():
    """Find all Tool Result modules."""
    package = sys.modules[__name__]
    all_modules = pkgutil.iter_modules(package.__path__)
    blacklist = ['register', 'tool_module', 'food_pet']
    tool_module_names = [modname for importer, modname, ispkg in all_modules
                         if modname not in blacklist]
    tool_modules = [importlib.import_module(f'app.tool_results.{name}')
                    for name in tool_module_names]

    def get_tool_module(tool_module):
        """Inspect ToolResult module and return its Module class."""
        classmembers = inspect.getmembers(tool_module, inspect.isclass)
        modules = [classmember for name, classmember in classmembers
                   if name.endswith('ResultModule') and name != 'ToolResultModule']
        if not modules:
            return None
        return modules[0]

    results = [get_tool_module(module) for module in tool_modules]
    results = [result for result in results if result is not None]
    return results


all_tool_result_modules = find_all_tool_modules()  # pylint: disable=invalid-name
