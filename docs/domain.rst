Chalice Domain
==============


Directives
----------
The chalice domain contains two directives, both of which build Chalice app
route documentation, but provide different methods for referring to the app.

Project
~~~~~~~
::

   .. chalice:project:: <project_dir>
      :rel: "cwd" / "src"
      :basepath: str

Build documentation for Chalice app located in ``project_dir``. Standard chalice
project layout *project_dir/app.py* is expected.

The **rel** option specifies the nature of the ``project_dir`` path:

cwd (default)
  states path is relative to current working directory when sphinx-build is
  executed.
src
  states path is relative to the directory containing the .rst source file.

The **basepath** option is a string that specifies a path that will be
prepended to every path in the app.

App
~~~
::

   .. chalice:app:: <module_name>
      :basepath: str

Build documentation for chalice app, importable at ``module_name``. This assumes
that the chalice module is already on your system path and can be directly
imported.

The **basepath** option is the same as for ``chalice:project`` above.


Roles
-----
There are two roles in the chalice domain, which can be used for referencing
within your documentation.

App
~~~
The ``chalice:app`` role refers to the chalice application as a whole. The name
used for the reference will be the app_name as specified when defining the
Chalice app.

E.g. a chalice app defined in your *app.py* as:

.. code-block:: python3

   app = Chalice(app_name='example')

could be referenced using::

   :chalice:app:`example`

Route
~~~~~
The ``chalice:route`` role refers to individual routes within the application.
Routes are referred to by their method in caps, followed by the path.

E.g. a routes defined in your *app.py* as:

.. code-block:: python3

   @app.route('/example', methods=['GET'])

could be referenced using::

   :chalice:route:`GET /example`

.. note::
   If a basepath has been specified on the ``chalice`` directive, then it must
   be included in the route reference.
