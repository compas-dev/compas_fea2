********************************************************************************
Units in compas_fea2
********************************************************************************

Most of FEA programs are unit-independent: the user does not directly specify the
units of the input quantities. Even though this could seem a more straightforward
approach, it delegates a big responsability to the user, who has to keep track of
the consistency of all the quantities involved. For example, if the leghts have been
specified in `mm` and the forces in `N`, then any pressure/stress quantity must be
given in `MPa` otherwise it would be inconsistent.

Below there are common consistent units specifications (also included, comparative
values and gravitational acceleration):

.. csv-table:: SI consistent units
   :file: units_consistent.csv
   :header-rows: 1

Engineers are usually trained to keep track of the consistency of their units, but
errors are quite likely to happen, especially for inesperienced users or when dealing
with different units systems, such `SI` or `imperial`.

For these reasons, in ``compas_fea2`` the user *can* specify the units to be used
when instanciating a ``Model`` by providing either the 'base units' or the 'standard'.

The follwoing table describes the SI base units:

.. csv-table:: SI base units
   :file: units_base.csv
   :widths: 50, 50, 50, 50
   :header-rows: 1



If the user decides to do so, before launching the analysis, ``compas_fea2`` checks
if the units in the model are conistent by comparing the order of magnitude of the
input quantities with conventional references: if the comparions produces unexpected
results, a ``WARNING`` is provided in the log.
