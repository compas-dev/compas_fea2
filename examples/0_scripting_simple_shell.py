from compas_fea2.backends.abaqus import Model
from compas_fea2.backends.abaqus import Part
from compas_fea2.backends.abaqus import Node
from compas_fea2.backends.abaqus import ElasticIsotropic
from compas_fea2.backends.abaqus import ShellSection
from compas_fea2.backends.abaqus import ShellElement
from compas_fea2.backends.abaqus import Set

from compas_fea2.backends.abaqus import Problem
from compas_fea2.backends.abaqus import PinnedDisplacement
from compas_fea2.backends.abaqus import PointLoad
from compas_fea2.backends.abaqus import FieldOutput
from compas_fea2.backends.abaqus import GeneralStaticStep
from compas_fea2.backends.abaqus import Results

from compas_fea2.postprocessor.stresses import principal_stresses

import numpy as np
from math import atan2, degrees
import matplotlib.pyplot as plt


def create_points(minX, maxX, minY, maxY, dis):
    """Returns a grid of points for the shell.

    Parameters
    ----------
    minX : float
        lower bound for the x dimension.
    maxX : float
        upper bound for the x dimension.
    minY : float
        lower bound for the y dimension.
    maxY : float
        upper bound for the y dimension.
    dis : int
        number of elements to create alond each direction.

    Return
    ------
    X : array
        x corrdinate grid
    Y : array
        x corrdinate grid
    Z : array
        x corrdinate grid (all zeros)
    """
    x = np.linspace(minX, maxX, int((maxX-minX)*dis+1))
    y = np.linspace(minY, maxY,  int((maxY-minY)*dis+1))
    X, Y = np.meshgrid(x, y)
    X = X.reshape((np.prod(X.shape),))
    Y = Y.reshape((np.prod(Y.shape),))
    Z = np.zeros_like(X)

    return X, Y, Z


def plot_vectors(minX, maxX, minY, maxY, sp, stype, spr, e):
    # Plot the vectors
    x = np.linspace(minX, maxX, int((maxX-minX)*dis+1))
    y = np.linspace(minY, maxY,  int((maxY-minY)*dis+1))
    X, Y = np.meshgrid(x, y)
    x = X[:-1, :-1]+0.5
    y = Y[:-1, :-1]+0.5
    for stype in ['max', 'min']:
        color = 'r' if stype == 'max' else 'b'
        # z = spr[sp][stype]
        u = np.array(np.split(e[sp][stype][0]*spr['sp1'][stype]/2, 5))
        v = np.array(np.split(e[sp][stype][1]*spr['sp1'][stype]/2, 5))
        plt.quiver(x, y, u, v, color=color, width=1*10**-3)
        plt.quiver(x, y, -u, -v, color=color, width=1*10**-3)
    plt.axis('equal')
    plt.show()


##### ----------------------------- MODEL -------------------------------- #####
# Initialise the assembly object
model = Model(name='structural_model')

# Add a Part to the model
model.add_part(Part(name='part-1'))

minX, maxX, minY, maxY = 0., 1., 0., 1.
dis = 25

# Add nodes to the part
X, Y, Z = create_points(minX, maxX, minY, maxY, dis)
model.add_nodes([Node(xyz=node) for node in zip(X, Y, Z)], part='part-1')

# Define materials
model.add_material(ElasticIsotropic(name='mat_A', E=210000, v=0.2, p=7e-9))

# Define sections
model.add_section(ShellSection(name='section_A', material='mat_A', t=0.005))

# Define shell elements
for j in range(dis):
    for i in range(dis):
        # if not i % dis == 0:
        model.add_element(element=ShellElement(connectivity=[i+j*(dis+1), i+j*(dis+1)+1, i+j*(dis+1)+dis+2, i+j*(dis+1)+dis+1],
                                               section='section_A'),
                          part='part-1')

# Define sets for boundary conditions and loads
model.add_assembly_set(Set(name='pinned', selection=[0, dis, (dis+1)*(dis), (dis+1)**2-1],
                           stype='nset'), instance='part-1-1')
model.add_assembly_set(Set(name='pload', selection=[((dis+1)//2)*(dis+1)], stype='nset'), instance='part-1-1')

##### ----------------------------- PROBLEM ------------------------------ #####
folder = 'C:/temp/'
name = 'principal_stresses'

# Create the Problem object
problem = Problem(name='principal_stresses', model=model)

# Assign boundary conditions to the node stes
problem.add_bcs(bcs=[PinnedDisplacement(name='bc_roller', bset='pinned')])

# Assign a point load to the node set
problem.add_load(load=PointLoad(name='pload', lset='pload', z=-1000))

# Define the field outputs required
problem.add_field_output(fout=FieldOutput(name='fout'))

# Define the analysis step
problem.add_step(step=GeneralStaticStep(name='gstep', loads=['pload']))

# Solve the problem
problem.summary()
problem.analyse(path=folder)

##### --------------------- POSTPROCESS RESULTS -------------------------- #####
results = Results.from_problem(problem, fields=['s'])
spr, e = principal_stresses(results.element['gstep'])

sp = 'sp5'
stype = 'max'

# check the results for an element
id = 0
print(f'the {stype} principal stress for element {id} is: ', spr[sp][stype][id])
print('principal axes (basis):\n', e[sp][stype][:, id])
print('and its inclination w.r.t. World is: ', degrees(atan2(*e[sp][stype][:, id][::-1])))

# Plot the vectors
plot_vectors(minX, maxX, minY, maxY, sp, stype, spr, e)
