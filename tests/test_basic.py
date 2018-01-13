"""Basic tests."""
import os
import os.path
import sys

import docutils.core
from docutils.parsers.rst import directives

import chalicedoc


RST_DOC = '''
.. test:: sampleproject
'''
RST_DOC_CONTENT = '''
.. test::

    A simple example.
'''


def test_build():
    """Test a simple rst parse with the chalice directive."""
    cwd = os.getcwd()
    os.chdir(os.path.dirname(__file__))
    try:
        directives.register_directive('test', chalicedoc.ProjectDirective)
        result = docutils.core.publish_string(RST_DOC)
        efn = os.path.join(os.path.dirname(__file__), 'sampleproject.txt')
        # open(efn, 'wb').write(result)
        assert result.decode() == open(efn, 'rb').read().decode()
    finally:
        os.chdir(cwd)


def test_build_content():
    """Test rst parse with added content."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sampleproject'))
    try:
        directives.register_directive('test', chalicedoc.AppDirective)
        result = docutils.core.publish_string(RST_DOC_CONTENT)
        efn = os.path.join(os.path.dirname(__file__), 'sampleproject+content.txt')
        # open(efn, 'wb').write(result)
        assert result.decode() == open(efn, 'rb').read().decode()
    finally:
        sys.path.pop(0)
