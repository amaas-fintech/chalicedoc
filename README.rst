==========
Chalicedoc
==========

Chalicedoc makes documenting Chalice applications easier.

This module adds a "chalice" domain for reStructuredText, which can be
used by Sphinx/docutils to autogenerate documentation of your chalice routes
using the docstrings in your Chalice app.

Usage (Sphinx)
==============

Usage is simple. First, you must include the ``chalicedoc`` module in your
extensions list in *conf.py*::

  extensions = [
      ...,
      'chalicedoc',
  ]

Next, within your .rst source, use the "chalice:project" directive to scan your
app for docstrings::

  .. chalice:project:: path/to/chalice/project

This will product output as follows:

1. The title will be adapted from the chalice ``app_name``
2. The docstring of your module will be included as a summary
3. For each route:

  a. The path will be added as a section title
  b. The method will be added as a section subtitle
  c. The docstring of the corresponding function will be used as the section
     content
