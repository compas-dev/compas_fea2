********************************************************************************
Introduction
********************************************************************************

Plug-in architecture
====================

``compas_fea2`` implements a plug-in architecture. The ``compas_fea2`` main
package only defines the general API for a Finite Element Analysis, while the
actual implementation in the a specific backend is done in the corresponding
plug-in, whcih is registered and the beginning of the analysis. Once the analysis
is complente, the results are recorded in a SQL database and can be accessed by
the user through the SQL wrapper provided by ``compas_fea2``, by his/her own
SQL statements or through an external interface.

.. figure:: /_images/registration.jpg
     :figclass: figure
     :class: figure-img img-fluid


Workflow
========

The image below describes a general FEA workflow:

.. figure:: /_images/basic_workflow.png
     :figclass: figure
     :class: figure-img img-fluid


Collaboration Workflow
======================

The aim of ``compas_fea2`` is to create a common platform for FEA that can be shared
across disciplines and software. This is achieved by standardizing the API for
the creation and analysis of an FE model, and by serializing `models`, `problems`
and `results` in a common database that can be easly shared.

The two images below show the general collaboration workflow and a specific example
of a structural engineer using rhino and abaqus collaborating with an acoustic
engineer using blender and ansys:


.. figure:: /_images/CollaborationWorkflow.jpg
     :figclass: figure
     :class: figure-img img-fluid


.. figure:: /_images/CollaborationWorkflow_example.jpg
     :figclass: figure
     :class: figure-img img-fluid


Units
=====

Before starting any model, you need to decide which system of
units you will use. ``compas_fea2`` has no built-in system of units.

.. warning:: Units consistency

    All input data must be specified in consistent units.
    Do not include unit names or labels when entering data in ``compas_fea2``.


Some common systems of consistent units are shown in the table below:


.. csv-table:: Consistent Units
   :file: ../data/units_consistent.csv
   :header-rows: 1

In case you do not want to follow a predefined system, you need to be consistent with
your units assignemnts. Below there are some exmple of correct choices of units:

.. csv-table:: Consistent Units
   :file: ../data/units_consistent_2.csv
   :header-rows: 1

The order of magnitude expected for different properties is shown below:

.. csv-table:: Magnitude
   :file: ../data/units_magnitude.csv
   :header-rows: 1
