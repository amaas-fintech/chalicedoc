"""Sample chalice app with docstrings."""

from chalice import Chalice

app = Chalice(app_name='testing')


@app.route('/')
def index():
    """
    Return {'hello': 'world'}.

    The view function above will return ``{"hello": "world"}``
    whenever you make an HTTP GET request to '/'.
    """


@app.route('/hello/{name}', methods=['GET', 'POST'])
def hello_name(name):
    """
    ``'/hello/james' -> {"hello": "james"}``.

    Returns
    -------
    ``{'hello': name}``

    """


@app.route('/users', methods=['POST'])
def create_user():
    """
    Create user.

    This is the JSON body the user sent in their POST request::

        user_as_json = app.current_request.json_body

    We'll echo the json body back to the user in a 'user' key.

    Returns
    -------
    ``{'user': user_as_json}``

    """


@app.route('/users',  # split to test get_content
           methods=['GET'])
def get_user():
    """
    Get user.

    Return user information as sent in query parameters::

        user_as_json = app.current_request.query_params

    Returns
    -------
    ``{'user': user_as_json}``

    """


@app.route('/minimal')
def no_doc():  # NoQA

    pass


@app.route('/refs')
def xref():
    """Cross-reference example.

    This docstring contains a cross-reference to :chalice:route:`GET /`.

    You can also use the
    `:any: <http://www.sphinx-doc.org/en/stable/markup/inline.html#role-any>`_
    functionality: :any:`GET /hello/{name}`.
    """
