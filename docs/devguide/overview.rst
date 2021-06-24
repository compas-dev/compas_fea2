********************************************************************************
Overview
********************************************************************************

Some light reading :)

https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging
https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes

https://git-scm.com/docs/git-pull
https://git-scm.com/docs/git-rebase


Fork the repo
=============

All contributions have to be made via pull requests from a fork of the repo.
To fork the ``compas_fea2`` repo, go to GitHub, click the "Fork" button
and select an account to host the fork.


Clone the fork
==============

.. code-block:: bash

    git clone https://github.com/<username>/compas_fea2.git


Create a dev environment
========================

The recommended way to set up a development environment is with ``conda``.
Make sure to activate the environment before using it...

.. code-block:: bash

    conda create -n fea2-dev python=3.8 --yes
    conda activate fea2


Install the requirements
========================

.. code-block:: bash

    pip install -r requirements-dev.txt

.. note::

    Note that this will also install ``compas`` and ``openseespy``,
    and add an editable install of your fork of ``compas_fea2`` to the environment.


Run all checks and tests
========================

Before starting to work on your contribution,
it is generally a good idea to run all tests and checks
to make sure you have a healthy clone of the repo.

.. code-block:: bash

    python -m compas_fea2.test

.. note::

    Note that the testing framework is currently not available yet.


Create a branch for your contribution
=====================================

Create and ``checkout`` a new branch on the forked repo.

.. code-block:: bash

    git branch my-awesome-contribution
    git checkout my-awesome-contribution


Start making changes
====================

This is all you!

Make sure to commit your changes regularly.
This makes it easier to undo if you change your mind about something...

Also push the commits regularly to your remote fork.
This way you have plenty of backups in case your computer blows up :)

.. code-block:: bash

    git commit -a -m "Some meaningful description of awesomeness"


Rebase on latest master/main
============================

Once you are done, the process of merging your contribution
into ``compas_fea2`` is much simpler if you rebase the contribution branch
of your fork onto the main branch of ``compas_fea2`` before submitting the PR.

.. note::

    This is a lot simpler using a Git GUI Client such as
    SourceTree, SmartGit or GitKraken than on the command line...


Run all checks and tests
========================

Before pushing your local fork branch to the remote fork repo
make sure all tests and check still pass
and make changes if necessary.

.. code-block:: bash

    python -m compas_fea2.test

.. note::

    Note that the testing framework is currently not available yet.


Push to remote fork
===================

Once all your changes have been commited,
the contribution bracnh is rebased onto the main branch of ``compaS_fea2``,
and all tests and checks pass,
push the local branch to the remote fork.

.. code-block:: bash

    git push
