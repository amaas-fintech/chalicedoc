"""A second app."""

from chalice import Chalice

app = Chalice(app_name='second')


@app.route('/b')
def index():
    """Project B."""
