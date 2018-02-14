"""Basic tests."""
import copy
import os
import os.path
from string import Template
import sys

import docutils.core
from docutils.parsers.rst import directives

import chalicedoc


SOURCEFILE = os.path.join(os.path.dirname(__file__), 'test-project', 'sample', 'app.py')

RST_DOC = '''
.. test:: test-project/sample
'''
RST_DOC_REL = '''
.. test:: test-project/sample
   :rel: src

'''
RST_DOC_CONTENT = '''
.. test::

   A simple example.
'''


def test_build():
    """Test a simple rst parse with the project directive."""
    cwd = os.getcwd()
    os.chdir(os.path.dirname(__file__))
    try:
        directives.register_directive('test', chalicedoc.ProjectDirective)
        result = docutils.core.publish_string(RST_DOC)
        efn = os.path.join(os.path.dirname(__file__), 'test_basic_build.txt')
        # open(efn, 'wb').write(result)
        tpl = Template(open(efn, 'rb').read().decode())
        assert result.decode() == tpl.substitute(SOURCEFILE=SOURCEFILE)
    finally:
        os.chdir(cwd)


def test_build_rel():
    """Test a simple rst parse using rel option on project directive."""
    cwd = os.getcwd()
    csp = copy.copy(sys.path)
    # remove top dir so test fails if option isn't working
    sys.path.pop(0)
    parent_dir, here = os.path.split(os.path.dirname(__file__))
    os.chdir(parent_dir)
    try:
        directives.register_directive('test', chalicedoc.ProjectDirective)
        test_path = os.path.join(here, 'test.rst')
        result = docutils.core.publish_string(RST_DOC_REL, source_path=test_path)
        efn = os.path.join(os.path.dirname(__file__), 'test_basic_rel.txt')
        # open(efn, 'wb').write(result)
        tpl = Template(open(efn, 'rb').read().decode())
        assert result.decode() == tpl.substitute(SOURCEFILE=SOURCEFILE)
    finally:
        sys.path[:] = csp
        os.chdir(cwd)


def test_build_content():
    """Test rst parse with added content on app directive."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'test-project', 'sample'))
    try:
        directives.register_directive('test', chalicedoc.AppDirective)
        result = docutils.core.publish_string(RST_DOC_CONTENT)
        efn = os.path.join(os.path.dirname(__file__), 'test_basic_content.txt')
        # open(efn, 'wb').write(result)
        tpl = Template(open(efn, 'rb').read().decode())
        assert result.decode() == tpl.substitute(SOURCEFILE=SOURCEFILE)
    finally:
        sys.path.pop(0)
