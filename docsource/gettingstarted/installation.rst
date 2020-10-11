********************************************************************************
compas_fea2 installation
********************************************************************************

The next steps show how to install ``compas_fea2`` package using the
Terminal (Mac) or the Anaconda Prompt (Windows).


1. Create a virtual environment
-------------------------------

First, create a fresh virtual environment with ``conda``.

.. code-block:: bash

	$ conda create -n fea2 python=3.7 compas
	$ conda activate fea2


2. Get the ``compas_fea2`` repo
-------------------------------

Navigate to the folder in which you want to store ``compas_fea2``,
and clone the github repository there. For example, if you want to put it in a pre-existing ``C:/code/compas`` folder:

.. code-block:: bash

	(fea2) $ cd C:/code/compas
	(fea2) $ git clone https://github.com/BlockResearchGroup/compas_fea2.git


3. Install ``compas_fea2``
--------------------------

Move into the folder you just created and generate an editable ``compas_fea2`` installation using ``pip``.

.. code-block:: bash

	(fea2) $ cd compas_fea2
	(fea2) $ pip install -e .

.. note::

	Make sure that you are in the ``fea2`` virtual environment.


4. Install dependencies [WIP]
-----------------------------

The required dependencies are:

- ...


5. Check your installation
--------------------------

Launch an interactive Python interpreter by typing ``python`` on the command line.
To make sure that ``compas``, ``fea2`` and all its dependencias are installed, after launching a ``python`` interpreter from the command line, let's type:

.. code-block:: bash

	>>> import compas
	>>> import compas_fea2

If no errors arise, congratulations! You have a working installation of ``compas_fea2``.


6. Install ``compas_fea2`` for Rhino
------------------------------------

[WIP]
