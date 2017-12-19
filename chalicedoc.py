"""Chalicedoc provides a chalice directive for reStructuredText parsing of Chalice apps."""
__version__ = '0.1'

import importlib
import inspect
import os.path
import sys

from docutils import nodes, statemachine
from docutils.parsers.rst import Directive
from docutils.statemachine import StringList
import sphinx.util.nodes as nodeutil


DEBUG = False


def import_app(project_dir):
    """Import chalice app."""
    project_dir = os.path.realpath(project_dir)
    try:
        from chalice.cli import CLIFactory
    except ImportError:
        if project_dir not in sys.path:
            sys.path.insert(0, project_dir)

        appmodule = importlib.import_module('app')
        app = appmodule.app
    else:
        app = CLIFactory(project_dir, debug=DEBUG).load_chalice_app()
    return app


class ChaliceDirective(Directive):
    """
    chalice directive class.

    The chalice directive searches a chalice app for routes and extracts
    docstring documentation for each of them.
    """

    required_arguments = 1
    has_content = True

    def run(self):
        """Parse chalice app docstrings."""
        root = nodes.section()
        app = import_app(self.arguments[0])
        root += nodes.title(app.app_name, app.app_name.replace('_', ' ').title())
        nodeutil.nested_parse_with_titles(self.state, self.content, root)
        for path, routes in app.routes.items():
            section = nodes.section()
            section += nodes.title(path, path)
            for method, route in routes.items():
                section += nodes.subtitle(method, method)
                doc = inspect.getdoc(route.view_function) or ''
                lines = statemachine.string2lines(doc)
                block = StringList(lines, source='<chalice:{}>'.format(app.app_name))
                nodeutil.nested_parse_with_titles(self.state, block, section)

            root += section

        return [root]


def setup(app):
    """Sphinx extension setup."""
    app.add_directive('chalice', ChaliceDirective)
    return {'version': __version__}
