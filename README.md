# compas_fea2

2nd generation of compas_fea. Current Main changes:

- Imporoved API for in-parallel development
- Added User Material subroutines in Abaqus
- Added Parts, Instances and Assembly to Abaqus

## Package objectives

This package aims to create a bridge between the generation of structural geometries and thei analysis
using popular commercial FEA software. The geometry generation features of these software is usually 
limited, teduious and time-consuming.

### Users

- simplify finite element analysis with 'pre-made' recipes to help unexperienced users to get meaningful results
- better link with compas and its ecosystem
- unified (as much as possible) approach across multiple backends to help researchers to communicate with their industrial partners. (for example, a researcher develops a structural system for a pavilion using Abaqus, but the enginner of record uses sofistiks to check the results: the analysis model for both structures can be derived from the same script with few changes)
- increase the number of backend solvers supported

### Developers

- clearly separate frontend (geometry generation, problem definition and result displaying) and backend (fea analysis, result post-process) to enhance in-parallel development
- offer frontend and backend developers a framework to help the structuring of their modules and avoid code repetion
