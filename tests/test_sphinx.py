"""Tests for Sphinx-specific functionality."""
import os
import re

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
    app.builder.build_all()

    result = app.outdir / 'contents.xml'
    expected = path(os.path.dirname(__file__)) / 'test_sphinx_build.xml'
    # expected.write_bytes(result.bytes())
    # strip top lines
    res_text = result.text()
    res_text = res_text[re.search(r'<document[^>]*>', res_text).end():]
    exp_text = expected.text()
    exp_text = exp_text[re.search(r'<document[^>]*>', exp_text).end():]
    assert res_text == exp_text

    assert warning.getvalue() == ''
