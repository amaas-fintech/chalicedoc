"""Tests for Sphinx-specific functionality."""
import os
import pickle

import pytest
from sphinx.testing.path import path


pytest_plugins = 'sphinx.testing.fixtures'


@pytest.fixture()
def rootdir():
    """Location of sphinx test projects."""
    return path(os.path.dirname(__file__))


ALL_TEXT = '''Testing

Sample chalice app with docstrings.

GET /

Return {‘hello’: ‘world’}.

The view function above will return {"hello": "world"}
whenever you make an HTTP GET request to ‘/’.

GET POST /hello/{name}

'/hello/james' -> {"hello": "james"}.

Returns

{'hello': name}

GET /minimal

GET /refs

Cross-reference example.

This docstring contains a cross-reference to GET /.

You can also use the
:any:
functionality: GET /.

POST /users

Create user.

This is the JSON body the user sent in their POST request.

user_as_json = app.current_request.json_body

We’ll echo the json body back to the user in a ‘user’ key.

Returns

{'user': user_as_json}'''


@pytest.mark.sphinx('xml', testroot='project')
def test_build(app, warning):
    """Test sphinx build of chalicedoc."""
    app.builder.build_all()

    result = app.outdir / 'contents.xml'
    expected = path(os.path.dirname(__file__)) / 'test_sphinx_build.xml'
    # expected.write_bytes(result.bytes())
    assert result.text() == expected.text()

    assert warning.getvalue() == ''
