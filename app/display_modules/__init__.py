"""Modules for converting analysis tool output to front-end display data."""

import importlib
import inspect
import pkgutil
import sys


def find_all_display_packages():
    """Find all Display Modules."""
    package = sys.modules[__name__]
    all_modules = pkgutil.iter_modules(package.__path__)
    blacklist = ['display_module']
    display_module_names = [modname for importer, modname, ispkg in all_modules
                            if modname not in blacklist]
    display_packages = [importlib.import_module(f'app.display_modules.{name}')
                        for name in display_module_names]
    return display_packages


def find_all_display_modules():
    """Find all display models."""
    display_packages = find_all_display_packages()

    def get_display_model(display_module):
        """Inspect DisplayModule and return its module class."""
        classmembers = inspect.getmembers(display_module, inspect.isclass)
        modules = [classmember for name, classmember in classmembers
                   if name.endswith('Module') and name != 'DisplayModule']
        if not modules:
            return None
        return modules[0]

    results = [get_display_model(module) for module in display_packages]
    results = [result for result in results if result is not None]

    return results


all_display_modules = find_all_display_modules()  # pylint: disable=invalid-name
