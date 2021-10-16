"""
This package consists of all pages used in the project, each page has its own module and class.
"""
from inspect import isclass
from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module

# This imports all page classes when using from game.pages import *
# iterate through the modules in the current package
package_dir = Path(__file__).resolve().parent
for (_, module_name, _) in iter_modules([package_dir]):

    # import the module and iterate through its attributes
    module = import_module(f"{__name__}.{module_name}")
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)

        if isclass(attribute):
            # Add the class to this package's variables
            globals()[attribute_name] = attribute
