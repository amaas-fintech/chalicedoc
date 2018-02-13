"""A first app."""

from chalice import Chalice

app = Chalice(app_name='first')


@app.route('/a')
def index():
    """Project A."""
