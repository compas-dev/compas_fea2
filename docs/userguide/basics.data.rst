******************************************************************************
Data
******************************************************************************

An analysis with COMPAS FEA2 is defined by a "model" (:class:`compas_fea2.model.Model`)
and a "problem" (:class:`compas_fea2.problem.Problem`), with each many different sub-components.

All these components, and the model and problem themselves, are COMPAS data objects,
and derive from a base FEA2 data class (:class:`compas_fea2.base.FEAData`).

.. code-block:: None

    compas.data.Data
    |_ compas_fea2.base.FEAData
        |_ compas_fea2.model.Model
        |_ compas_fea2.model.Node
        |_ compas_fea2.model.Element
            |_ ...
        |_ compas_fea2.model.Part
            |_ ...
        |_ compas_fea2.model.Material
            |_ ...
        |_ compas_fea2.model.Section
            |_ ...
        |_ compas_fea2.model.Constraint
            |_ ...
        |_ compas_fea2.model.Group
            |_ ...
        |_ compas_fea2.model.BoundaryCondition
            |_ ...
        |_ compas_fea2.model.InitialCondition 
            |_ ...


.. code-block:: None

    compas.data.Data
    |_ compas_fea2.base.FEAData
        |_ compas_fea2.problem.Problem
        |_ compas_fea2.problem.Step
            |_ ...
        |_ compas_fea2.problem.Load
            |_ ...
        |_ compas_fea2.problem.Displacement
            |_ ...


This means that all these components have the same base data infrastructure as all other COMPAS objects.
They have a guid, a name, and general attributes.

>>> from compas_fea2.model import Node
>>> node = Node(xyz=(0., 0., 0.), name='node')
>>> node.name
'node'

