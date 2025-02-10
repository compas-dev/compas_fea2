from compas_fea2.model import Model
from compas_fea2.model.parts import BeamElement
from compas_fea2.model.materials import ElasticIsotropic
from compas_fea2.model.sections import RectangleSection
from compas_fea2.model.nodes import Node
from compas_fea2.model.elements import Element
from compas_fea2.model.bcs import FixedBC
from compas_fea2.model.loads import PointLoad
from compas_fea2.problem import Problem
from compas_fea2.results import Results
from compas_fea2.fea.calculix.calculix import CalculiX

# 1. Create the FEA model
model = Model(name="beam_model")

# 2. Define material properties (Steel)
steel = ElasticIsotropic(name="steel", E=210e9, v=0.3, p=7850)
model.add_material(steel)

# 3. Define a rectangular cross-section (100mm x 10mm)
section = RectangleSection(name="beam_section", b=0.1, h=0.01)
model.add_section(section)

# 4. Create nodes (simple cantilever beam: 1m long)
n1 = Node(0, 0, 0)
n2 = Node(1, 0, 0)
model.add_nodes([n1, n2])

# 5. Create a beam element connecting the two nodes
beam = BeamElement(nodes=[n1, n2], material=steel, section=section)
model.add_element(beam)

# 6. Apply boundary conditions (Fix left end)
bc_fixed = FixedBC(nodes=[n1])
model.add_boundary_conditions([bc_fixed])

# 7. Apply a downward point load at the free end (1000N)
load = PointLoad(nodes=[n2], z=-1000)
model.add_loads([load])

# 8. Create the analysis problem
problem = Problem(model=model, name="static_analysis")
solver = CalculiX(problem=problem)

# 9. Run the analysis
solver.solve()

# 10. Extract and display results
results = Results(problem)
displacements = results.get_nodal_displacements()
print("Nodal Displacements:", displacements)
