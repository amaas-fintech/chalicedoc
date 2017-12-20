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


def import_app(project_dir):
    """Import chalice app."""
    project_dir = os.path.realpath(project_dir)
    if project_dir not in sys.path:
        sys.path.insert(0, project_dir)

    module = importlib.import_module('app')
    app = module.app
    return module, app


def get_doc_content(obj, source):
    """Build a content block for parser consumption from an object docstring."""
    doc = inspect.getdoc(obj) or ''
    lines = statemachine.string2lines(doc)
    block = StringList(lines, source=source)
    return block


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
        module, app = import_app(self.arguments[0])
        source = inspect.getfile(module)
        # See RSTState.section for regular section creation logic.
        root = nodes.section()
        root['names'].append(nodes.fully_normalize_name(app.app_name))
        root += nodes.title(app.app_name, app.app_name.replace('_', ' ').title())
        self.state.document.note_implicit_target(root, root)
        # If content is given use that, otherwise use module docstring.
        if self.content:
            nodeutil.nested_parse_with_titles(self.state, self.content, root)
        else:
            content = get_doc_content(module, source)
            nodeutil.nested_parse_with_titles(self.state, content, root)
        for path in sorted(app.routes):
            section = nodes.section()
            section['names'].append(nodes.fully_normalize_name(path))
            section += nodes.title(path, path)
            self.state.document.note_implicit_target(section, section)
            routes = app.routes[path]
            for method in sorted(routes):
                # Maybe make this another section+title?
                section += nodes.subtitle(method, method)
                content = get_doc_content(routes[method].view_function, source=source)
                nodeutil.nested_parse_with_titles(self.state, content, section)

            root += section

        return [root]


def setup(app):
    """Sphinx extension setup."""
    app.add_directive('chalice', ChaliceDirective)
    return {'version': __version__}
