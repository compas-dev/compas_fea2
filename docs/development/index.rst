********************************************************************************
Development
********************************************************************************

.. toctree::
    :maxdepth: 2
    :titlesonly:


Getting started with this project
=================================

Setup code editor
-----------------

1. Open project folder in VS Code
2. Select python environment for the project

    All terminal commands in the following sections can be run from the VS Code integrated terminal. 

First steps with git
--------------------

1. Go to the ``Source control`` tab
2. Make an initial commit with all newly created files

First steps with code
---------------------

1. Install the newly created project 

    .. code-block:: bash

        pip install -e .

2. Install it on Rhino

    .. code-block:: bash

        python -m compas_rhino.install

Code conventions
----------------

Code convention follows `PEP8 <https://pep8.org/>`_ style guidelines and line length of 120 characters.

1. Check adherence to style guidelines

    .. code-block:: bash

        invoke lint

2. Format code automatically

    .. code-block:: bash

        invoke format

Documentation
-------------

Documentation is generated automatically out of docstrings and `RST <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_ files in this repository

1. Generate the docs

    .. code-block:: bash

        invoke docs

2. Check links in docs are valid

    .. code-block:: bash

        invoke linkcheck

3. Open docs in your browser (file explorer -> ``dist/docs/index.html``)

Testing
-------

Tests are written using the `pytest <https://docs.pytest.org/>`_ framework

1. Run all tests from terminal

    .. code-block:: bash

        invoke test

2. Or run them from VS Code from the ``Testing`` tab

Developing Grasshopper components
---------------------------------

We use `Grasshopper Componentizer <https://github.com/compas-dev/compas-actions.ghpython_components>`_ to develop Python components that can be stored and edited on git.

1. Build components

    .. code-block:: bash

        invoke build-ghuser-components

2. Install components on Rhino

    .. code-block:: bash

        python -m compas_rhino.install

Publish release
---------------

Releases follow the `semver <https://semver.org/spec/v2.0.0.html>`_ versioning convention.

1. Create a new release

    .. code-block:: bash

        invoke release major
