"""Chalicedoc provides a chalice directive for reStructuredText parsing of Chalice apps."""
__version__ = '0.2'

import importlib
import inspect
import os.path
import sys

from docutils import nodes, statemachine
from docutils.parsers.rst import Directive
from docutils.statemachine import StringList
import sphinx.util.nodes as nodeutil
from sphinx.domains import Domain, ObjType
from sphinx.roles import XRefRole


def get_doc_content(obj, source):
    """Build a content block for parser consumption from an object docstring."""
    doc = inspect.getdoc(obj) or ''
    lines = statemachine.string2lines(doc)
    block = StringList(lines, source=source)
    return block


class ChaliceBaseDirective(Directive):
    """Chalice directive baseclass."""

    def build_doc(self, module, app=None, source=None):
        """Build full docs for Chalice app."""
        if not app:
            # Standard Chalice location
            app = module.app
        if not source:
            source = inspect.getfile(module)

        root = self.build_app_doc(module, app, source)
        for path in sorted(app.routes):
            routes = app.routes[path]
            # Group routes with multiple methods
            inverted_routes = {}
            for method in routes:
                view_function = routes[method].view_function
                inverted_routes.setdefault(view_function, set()).add(method)

            for view_function in sorted(inverted_routes, key=lambda f: f.__name__):
                methods = inverted_routes[view_function]
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
        # Add cross-reference
        self.add_xref('app', app.app_name, root['ids'][0])
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
        section['names'].extend([
            nodes.fully_normalize_name(path),
            view_function.__name__,
        ])
        self.state.document.note_implicit_target(section, section)
        sid = section['ids'][0]
        # Add title
        title_src = ' '.join(methods + [path])
        title = nodes.title(title_src)
        for method in methods:
            title += [nodes.strong(method, method), nodes.Text(' ')]
            # ...add cross-reference
            self.add_xref('route', '{} {}'.format(method, path), sid)

        title += nodes.Text(path)
        section += title
        # Add content
        content = get_doc_content(view_function, source=source)
        nodeutil.nested_parse_with_titles(self.state, content, section)
        return section

    def add_xref(self, objtyp, target, targetid):
        """Add cross-reference record for an element."""
        try:
            env = self.state.document.settings.env
        except AttributeError:
            # We're in regular docutils, not sphinx, so skip.
            return

        refs = env.domaindata['chalice']['route']
        if target in refs:
            msg = 'Duplicate {} reference {!r}, other instance in {}'
            src = env.doc2path(refs[target][0])
            self.state_machine.reporter.warning(
                msg.format(objtyp, target, src),
                line=self.lineno,
            )

        docname = env.docname
        refs[target] = (docname, targetid)


def project_rel_validate(value):
    """Validate rel option on project directive."""
    choices = {'cwd', 'src'}
    if not value:
        # default value
        return 'cwd'

    try:
        if value.strip().lower() not in choices:
            raise ValueError('rel must be one of {}'.format('|'.join(choices)))
    except AttributeError:
        raise TypeError('rel must be a string')

    return value


class ProjectDirective(ChaliceBaseDirective):
    """
    Chalice project directive.

    The project directive imports a Chalice app from a Chalice project
    directory, collects the app routes and extracts docstring documentation for
    each of them.
    """

    required_arguments = 1
    option_spec = {
        'rel': project_rel_validate,
    }
    has_content = True

    def run(self):
        """Parse chalice project docstrings."""
        if self.options.get('rel') == 'src':
            source_dir = os.path.dirname(self.state.document.attributes['source'])
            project_dir = os.path.realpath(os.path.join(source_dir, self.arguments[0]))
        else:
            project_dir = os.path.realpath(self.arguments[0])

        if project_dir not in sys.path:
            sys.path.insert(0, project_dir)

        # Clear old import if there already
        sys.modules.pop('app', None)
        sys_modules = set(sys.modules.keys())
        try:
            module = importlib.import_module('app')
            return self.build_doc(module)
        finally:
            # Remove any modules added
            to_remove = set(sys.modules.keys()) - sys_modules
            for key in to_remove:
                del sys.modules[key]


class AppDirective(ChaliceBaseDirective):
    """
    Chalice app directive.

    The app directive collects a Chalice app routes and extracts docstring
    documentation for each of them. The directive assumes that the app referred
    to is already in the global namespace or importable from the current system
    path.
    """

    optional_arguments = 1
    has_content = True

    def run(self):
        """Parse chalice app docstrings."""
        name = self.arguments[0] if len(self.arguments) > 0 else 'app'
        # Clear old import if there already
        sys.modules.pop(name, None)
        sys_modules = set(sys.modules.keys())
        try:
            module = importlib.import_module(name)
            return self.build_doc(module)
        finally:
            # Remove any modules added
            to_remove = set(sys.modules.keys()) - sys_modules
            for key in to_remove:
                del sys.modules[key]


class ChaliceDomain(Domain):
    """Chalice domain."""

    name = 'chalice'
    label = 'Chalice'
    object_types = {
        'app': ObjType('app', 'app'),
        'route': ObjType('route', 'route'),
    }
    directives = {
        'project': ProjectDirective,
        'app': AppDirective,
    }
    roles = {
        'app': XRefRole(),
        'route': XRefRole(),
    }

    initial_data = {
        'app': {},
        'route': {},
    }

    def clear_doc(self, docname):
        # type: (unicode) -> None
        """Remove traces of a document in the domain-specific inventories."""
        for typ in ('app', 'route'):
            entry = self.data[typ]
            for target, (doc, _) in list(entry.items()):
                if doc == docname:
                    del entry[target]

    def merge_domaindata(self, docnames, otherdata):
        # type: (List[unicode], Dict) -> None
        """Merge in data regarding *docnames* from *otherdata*."""
        for typ in ('app', 'route'):
            entry = otherdata[typ]
            for target, (doc, tid) in entry.items():
                if doc in docnames:
                    self.data[typ][target] = (doc, tid)

    # def process_doc(self, env, docname, document):
    #     # type: (BuildEnvironment, unicode, nodes.Node) -> None
    #     """Process a document after it is read by the environment."""
    #     pass
    #
    # def check_consistency(self):
    #     # type: () -> None
    #     """Do consistency checks (**experimental**)."""
    #     pass
    #
    # def process_field_xref(self, pnode):
    #     # type: (nodes.Node) -> None
    #     """Process a pending xref created in a doc field.
    #     For example, attach information about the current scope.
    #     """
    #     pass

    def resolve_xref(self, env, fromdocname, builder,
                     typ, target, node, contnode):
        # type: (BuildEnvironment, unicode, Builder, unicode, unicode, nodes.Node, nodes.Node) -> nodes.Node  # NOQA
        """
        Resolve the pending_xref *node* with the given *typ* and *target*.

        :param typ: == roles key
        :param target: == target text e.g. ``GET /path``
        """
        for objtyp in self.objtypes_for_role(typ):
            try:
                todocname, targetid = self.data[objtyp][target]
            except KeyError:
                pass
            else:
                return nodeutil.make_refnode(
                    builder, fromdocname, todocname, targetid, contnode,
                )

    def resolve_any_xref(self, env, fromdocname, builder, target, node, contnode):
        # type: (BuildEnvironment, unicode, Builder, unicode, nodes.Node, nodes.Node) -> List[Tuple[unicode, nodes.Node]]  # NOQA
        """Resolve the pending_xref *node* with the given *target*."""
        results = []
        for objtyp in self.object_types:
            try:
                todocname, targetid = self.data[objtyp][target]
            except KeyError:
                pass
            else:
                results.append((
                    '{}:{}'.format(self.name, self.role_for_objtype(objtyp)),
                    nodeutil.make_refnode(
                        builder, fromdocname, todocname, targetid, contnode,
                    )
                ))

        return results

    def get_objects(self):
        # type: () -> Iterable[Tuple[unicode, unicode, unicode, unicode, unicode, int]]
        """Return an iterable of "object descriptions"."""
        for typ in ('app', 'route'):
            entry = self.data[typ]
            for target, (doc, tid) in entry.items():
                pri = self.object_types[typ].attrs['searchprio']
                yield target, target, typ, doc, tid, pri

    # def get_type_name(self, type, primary=False):
    #     # type: (ObjType, bool) -> unicode
    #     """Return full name for given ObjType."""
    #     if primary:
    #         return type.lname
    #     return _('%s %s') % (self.label, type.lname)
    #
    # def get_full_qualified_name(self, node):
    #     # type: (nodes.Node) -> unicode
    #     """Return full qualified name for given node."""
    #     return None


def setup(app):
    """Sphinx extension setup."""
    app.add_domain(ChaliceDomain)
    return {'version': __version__}
