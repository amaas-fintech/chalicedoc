"""Tests for Sphinx-specific functionality."""
import os.path
from string import Template
import shutil

import pytest
from sphinx.testing.path import path


pytest_plugins = 'sphinx.testing.fixtures'


@pytest.fixture()
def rootdir():
    """Location of sphinx test projects."""
    return path(os.path.dirname(__file__))


@pytest.mark.sphinx('xml', testroot='project')
def test_build(app, warning):
    """Test sphinx build of chalicedoc."""
    try:
        app.builder.build_all()

        result = app.outdir / 'contents.xml'
        expected = path(os.path.dirname(__file__)) / 'test_sphinx_build.xml'
        # expected.write_bytes(result.bytes())
        exp_text = Template(expected.text()).substitute(
            SOURCEFILE=app.srcdir / 'contents.rst'
        )
        assert result.text() == exp_text

        assert warning.getvalue() == ''
    finally:
        shutil.rmtree(app.srcdir)


@pytest.mark.sphinx('xml', testroot='two')
def test_two(app, warning):
    """Test sphinx build of multiple chalice projects."""
    try:
        app.builder.build_all()

        result = app.outdir / 'contents.xml'
        expected = path(os.path.dirname(__file__)) / 'test_sphinx_two.xml'
        # expected.write_bytes(result.bytes())
        exp_text = Template(expected.text()).substitute(
            SOURCEFILE=app.srcdir / 'contents.rst'
        )
        assert result.text() == exp_text

        assert warning.getvalue() == ''
    finally:
        shutil.rmtree(app.srcdir)
