******************************************************************************
Problem
******************************************************************************

The `Problem` class in compas_fea2 is a central component for defining and managing finite element analysis problems. It encapsulates all the necessary information required to set up and solve an FEA problem, including the model, analysis type, boundary conditions, loads, and solver settings.

Key attributes and methods of the `Problem` class include:
- **Attributes**:
  - `model`: The finite element model to be analyzed.
  - `analysis_type`: The type of analysis to be performed (e.g., static, modal, dynamic).
  - `boundary_conditions`: A list of boundary conditions applied to the model.
  - `loads`: A list of loads applied to the model.
  - `solver_settings`: Configuration settings for the FEA solver.

- **Methods**:
  - `add_boundary_condition(bc)`: Adds a boundary condition to the problem.
  - `add_load(load)`: Adds a load to the problem.
  - `set_solver(solver)`: Sets the solver to be used for the analysis.
  - `solve()`: Executes the analysis using the specified solver and settings.

The `Problem` class provides a high-level interface for defining and managing FEA problems, making it easier for users to set up and run simulations without dealing with low-level details.

Example usage:
```python
from compas_fea2 import Problem

# Create a new Problem instance
problem = Problem(model=my_model, analysis_type='static')

# Add boundary conditions and loads
problem.add_boundary_condition(my_boundary_condition)
problem.add_load(my_load)

# Set the solver and solve the problem
problem.set_solver(my_solver)
problem.solve()
```

For more detailed information and examples, please refer to the official documentation and user guides.
