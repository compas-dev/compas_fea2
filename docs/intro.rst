********************************************************************************
Introduction
********************************************************************************

.. rst-class:: lead


Workflow
========

The image below describes a general FEA workflow:

.. figure:: /_images/workflow_1.png
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
