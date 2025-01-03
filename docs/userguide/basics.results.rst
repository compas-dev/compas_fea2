******************************************************************************
Results
******************************************************************************

In compas_fea2, the results of a finite element analysis are organized in a structured manner to facilitate easy access and post-processing. The results are typically stored in a `Results` object, which contains various types of data depending on the analysis performed.

Key components of the `Results` object include:
- **Nodal Results**: Displacements, velocities, accelerations, and reaction forces at the nodes.
- **Element Results**: Stresses, strains, and internal forces within the elements.
- **Global Results**: Overall quantities such as total reaction forces and energy values.

To access the results, you can use the following methods provided by the `Results` object:
- `get_nodal_displacements()`: Returns the displacements at the nodes.
- `get_nodal_reactions()`: Returns the reaction forces at the nodes.
- `get_element_stresses()`: Returns the stresses within the elements.
- `get_element_strains()`: Returns the strains within the elements.

Example usage:
```python
# Assuming 'results' is an instance of the Results class
nodal_displacements = results.get_nodal_displacements()
nodal_reactions = results.get_nodal_reactions()
element_stresses = results.get_element_stresses()
element_strains = results.get_element_strains()

# Process or visualize the results as needed
```

The `Results` object provides a convenient interface for accessing and manipulating the analysis results, enabling users to perform further analysis, visualization, or reporting.

For more detailed information and examples, please refer to the official documentation and user guides.
