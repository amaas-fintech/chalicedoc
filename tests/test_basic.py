"""Basic tests."""
import os.path

import docutils.core
from docutils.parsers.rst import directives
import chalice

import chalicedoc


RST_DOC = '''
.. chalice:: sampleproject
'''
RST_DOC_CONTENT = RST_DOC + '''
    A simple example.
'''


def test_import_app():
    """Test import_app function."""
    project_dir = os.path.join(os.path.dirname(__file__), 'sampleproject')
    module, app = chalicedoc.import_app(project_dir)
    assert isinstance(app, chalice.Chalice)


def test_build():
    """Test a simple rst parse with the chalice directive."""
    directives.register_directive('chalice', chalicedoc.ChaliceDirective)
    result = docutils.core.publish_string(RST_DOC)
    efn = os.path.join(os.path.dirname(__file__), 'sampleproject.txt')
    # open(efn, 'wb').write(result)
    assert result == open(efn, 'rb').read()


def test_build_content():
    """Test rst parse with added content."""
    directives.register_directive('chalice', chalicedoc.ChaliceDirective)
    result = docutils.core.publish_string(RST_DOC_CONTENT)
    efn = os.path.join(os.path.dirname(__file__), 'sampleproject+content.txt')
    # open(efn, 'wb').write(result)
    assert result == open(efn, 'rb').read()
