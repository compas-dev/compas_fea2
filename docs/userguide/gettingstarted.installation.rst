********************************************************************************
Installation
********************************************************************************

The recommended way to install ``compas_fea2``
is in a dedicated ``conda`` environment.

.. code-block:: bash

    conda create -n fea2 compas
    conda activate fea2
    pip install compas_fea2

After the installation is complete, run the built-in tests
to verify that you have a functional setup with at least one working backend.

.. code-block:: bash

    python -m compas_fea2.test
