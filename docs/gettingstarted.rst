********************************************************************************
Getting Started
********************************************************************************

Requirements
============

To use ``compas_fea2`` you have to make sure that at least one
of the supported backends is installed.

* Abaqus
* ANSYS
* SOFiSTiK
* OpenSEES


Installation
============

The recommended way to install ``compas_fea2``
is in in a dedicated ``conda`` environment.

.. code-block:: bash

    conda create -n fea2 compas
    conda activate fea2
    pip install compas_fea2

After the installation is complete, run the built-in tests
to verify that you have a functional setup with at least one working backend.

.. code-block:: bash

    python -m compas_fea2.test


First steps
===========

The tutorial and examples are a good place to start exploring.

* Tutorial
* Examples


Known issues
============

Currently none :)

If you do find problems, help us solving them by filing a bug report
on the `Issue Tracker <https://github.com/compas-dev/compas_fea2/issues>`_ of the repo.
