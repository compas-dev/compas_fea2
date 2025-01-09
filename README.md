# compas_fea2

2nd generation of compas_fea. Current main changes:

* Plug-in architecture
* Improved API for in-parallel development
* Extended functionalities

## Package Objectives

This package aims to create a bridge between the generation of structural geometries and their analysis using popular commercial FEA software. The geometry generation features of these software are usually limited, tedious, and time-consuming.

### Users

* Simplify finite element analysis with 'pre-made' recipes to help inexperienced users get meaningful results
* Better link with compas and its ecosystem
* Provide a unified (as much as possible) approach across multiple backends to help researchers communicate with their industrial partners. For example, a researcher develops a structural system for a pavilion using Abaqus, but the engineer of record uses Sofistik to check the results: the analysis model for both structures can be derived from the same script with few changes
* Increase the number of backend solvers supported

### Developers

* Clearly separate frontend (geometry generation, problem definition, and result displaying) and backend (FEA analysis, result post-process) to enhance in-parallel development
* Offer frontend and backend developers a framework to help the structuring of their modules and avoid code repetition
* Provide comprehensive documentation and examples to facilitate the development and integration of new features
* Ensure modularity and extensibility to allow easy addition of new functionalities and support for additional FEA software

## Installation

To install compas_fea2, use the following command:

```bash
pip install compas_fea2
```

## Usage

Here is a basic example of how to use compas_fea2:

```python
# Import the compas_fea2 library
import compas_fea2
from compas_fea2.model import Model, Part, Node, Element, Material, Section
from compas_fea2.problem import Problem, Step, BoundaryCondition, Pattern, Load, FieldOutput

# Define a Model and its parts
mdl = Model()
prt_1 = Part()
prt_2 = Part()
# Assign the parts to the model
mdl.add_parts([prt_1, prt_2])

# Define sections and materials
mat = Material(E=..., v=..., density=...)
sec = Section(t=..., material=mat)

# Define the geometry of the structure
# Specify nodes
nodes_1 = [Node(xyz=...), Node(xyz=...), ...]
nodes_2 = [Node(xyz=...), Node(xyz=...), ...]
# Assign the nodes to a part
prt_1.add_nodes(nodes_1)
prt_2.add_nodes(nodes_2)

# Specify elements
elements_1 = [Element(nodes=[...], section=sec), Element(nodes=[...], section=sec), ...]
elements_2 = [Element(nodes=[...], section=sec), Element(nodes=[...], section=sec), ...]
# Assign the elements to a part
prt_1.add_elements(elements_1)
prt_2.add_elements(elements_2)

# Define boundary conditions
# Apply constraints and loads to the structure
bcs = [BoundaryCondition(nodes=[...], ...), BoundaryCondition(nodes=[...], ...)]
mdl.add_bcs(bcs)

# Define a Problem to analyze
prb = Problem()
# Add the problem to the model
mdl.add_problem(prb)

# Define the steps of the analysis
stp_1 = Step(...)
stp_2 = Step(...)
# Add the steps to the problem (note: this is the sequence in which they are applied)
prb.add_steps([stp_1, stp_2])

# Define the load patterns
pattern_1 = Pattern(nodes=[...], load=Load(...))
pattern_2 = Pattern(nodes=[...], load=Load(...))
# Add the pattern to the step
stp_1.add_pattern(pattern_1)
stp_2.add_pattern(pattern_2)

# Define the outputs to save
output = FieldOutput(...)
stp_1.add_output(output)
stp_2.add_output(output)

# Run the analysis
# Execute the finite element analysis
prb.analyze_and_extract(...)

# Post-process the results
# Extract and visualize the results
results = prb.results

# View the results
prb.show()
```

For more detailed examples and documentation, please refer to the official documentation.

## Contributing

We welcome contributions from the community. If you would like to contribute, please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature-branch`)
6. Create a new Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
