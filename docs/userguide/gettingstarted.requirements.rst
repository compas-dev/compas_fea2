********************************************************************************
Requirements
********************************************************************************

COMPAS FEA2 is a high-level modelling language for finite element analysis.
It uses COMPAS data structures and geometry to define analysis models and related analysis problem definitions.
The actual analysis is handed off to open source solvers, such as OpenSEES or commercial analysis software, such as Abaqus.

Currently the following solvers or "backends" are supported:

* Abaqus
* ANSYS
* SOFiSTiK
* OpenSEES

In order to run an analysis, you need to have one of these solvers installed on your system.
See :doc:`backends/index` for more information.
