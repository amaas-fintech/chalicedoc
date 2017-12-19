"""Basic tests."""
import os.path

import docutils.core
from docutils.parsers.rst import directives
import chalice

import chalicedoc


RST_DOC = '''
.. chalice:: sampleproject

    A simple example.

'''
EXPECTED_OUTPUT = b'''<document source="<string>" title="Testing">
    <title>
        Testing
    <paragraph>
        A simple example.
    <section>
        <title>
            /
        <subtitle>
            GET
        <paragraph>
            Return {'hello': 'world'}.
        <paragraph>
            The view function above will return ''' b'''
            <literal>
                {"hello": "world"}
            ''' b'''
            whenever you make an HTTP GET request to '/'.
    <section>
        <title>
            /hello/{name}
        <subtitle>
            GET
        <paragraph>
            <literal>
                '/hello/james' -> {"hello": "james"}
            .
        <section dupnames="returns" ids="returns">
            <title>
                Returns
            <paragraph>
                <literal>
                    {'hello': name}
    <section>
        <title>
            /users
        <subtitle>
            POST
        <paragraph>
            Create user.
        <paragraph>
            This is the JSON body the user sent in their POST request.
        <literal_block xml:space="preserve">
            user_as_json = app.current_request.json_body
        <paragraph>
            We'll echo the json body back to the user in a 'user' key.
        <section dupnames="returns" ids="id1">
            <title>
                Returns
            <paragraph>
                <literal>
                    {'user': user_as_json}
'''


def test_import_app():
    """Test import_app function."""
    project_dir = os.path.join(os.path.dirname(__file__), 'sampleproject')
    app = chalicedoc.import_app(project_dir)
    assert isinstance(app, chalice.Chalice)


def test_build():
    """Test a simple rst parse with the chalice directive."""
    directives.register_directive('chalice', chalicedoc.ChaliceDirective)
    result = docutils.core.publish_string(RST_DOC)
    assert result == EXPECTED_OUTPUT
