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
        root = self.build_app_doc(module, app, source)
        for path in sorted(app.routes):
            routes = app.routes[path]
            # Group routes with multiple methods
            reversed_routes = {}
            for method in routes:
                view_function = routes[method].view_function
                reversed_routes.setdefault(view_function, set()).add(method)

            for view_function in sorted(reversed_routes):
                methods = reversed_routes[view_function]
                section = self.build_route_doc(sorted(methods), path, view_function, source)
                root += section

        return [root]

    def build_app_doc(self, module, app, source):
        """
        Build overall Chalice app documentation.

        Heading comes from app name.
        Body comes from directive content or module docstring.
        """
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

        return root

    def build_route_doc(self, methods, path, view_function, source):
        """Build documentation for an individual route from view_function docstring."""
        section = nodes.section()
        section['names'].append(nodes.fully_normalize_name(path))
        # Add title
        title_src = ' '.join(methods + [path])
        title = nodes.title(title_src)
        for method in methods:
            title += [nodes.strong(method, method), nodes.Text(' ')]

        title += nodes.Text(path)
        section += title
        # Add content
        self.state.document.note_implicit_target(section, section)
        content = get_doc_content(view_function, source=source)
        nodeutil.nested_parse_with_titles(self.state, content, section)
        return section



def setup(app):
    """Sphinx extension setup."""
    app.add_directive('chalice', ChaliceDirective)
    return {'version': __version__}
