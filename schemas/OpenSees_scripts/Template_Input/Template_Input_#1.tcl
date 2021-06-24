# ******This template corresponds to Beam Bathe Example 1*******

# Heading
wipe

# The following command is used to define spatial dimension of model and number of degrees-of-freedom at nodes. 
model basic -ndm 3 -ndf 6


# ------------------------------------------------------------------
# Nodes
# ------------------------------------------------------------------
node $nodeTag	$GlobalX	$GlobalXY	$GlobalZ; 	# $nodeTag is an input integer given by user to assign a unique tag to the node


# ------------------------------------------------------------------
# Boundary conditions
# ------------------------------------------------------------------
# The following command is used to construct single-point homogeneous boundary constraints.
fix $nodeTag	 1	1	1	1	1	1; # this command calls the previously defined node, and, "1" corresponds to fully constrained (or fully fixed) 


# -----------------------------------------------------------------
# Materials
# -----------------------------------------------------------------
# The following command is used to construct an elastic uniaxial material object.
uniaxialMaterial Elastic $matTag $E; # $matTag is an input integer given by user to assign a unique tag to the material, $E is the Young's modulus


# -----------------------------------------------------------------
# Elements
# -----------------------------------------------------------------
#Before defining an element, local coordinate system of the element should be defined first. This command builds the geometrical transformation method. Diffrrent options exist, Linear, PDelta, and Corotational.
# We generally use Linear transformation. The following command is used to construct a linear coordinate transformation (LinearCrdTransf) object.
# The Linear transformation performs a linear geometric transformation of beam stiffness and resisting force from the basic system to the global-coordinate system.
	
geomTransf Linear $transfTag $vecxzX $vecxzY $vecxzZ; # $transfTag is an input integer given by user to assign a unique tag to the geometrical transformation method, ALSO:
													  # $vecxzX $vecxzY $vecxzZ are specified in the global-coordinate system X,Y,Z and define a vector that is in a plane parallel to the x-z plane of the local-coordinate system.


# The following command is used to construct an elasticBeamColumn element object.
element elasticBeamColumn $eleTag $iNode $jNode $A $E $G $J $Iy $Iz $transfTag; # $eleTag is an input integer given by user to assign a unique tag to the Element. $iNode and $jNode are the ending nodes, ALSO:
																				# $E is the Young's Modulus, $G is the	Shear Modulus, $J is the torsional moment of inertia of cross section,
																				# $Iz is the second moment of area about the local z-axis, $Iy is the second moment of area about the local y-axis, and
																				# $transfTag is	identifier for previously-defined coordinate-transformation (CrdTransf) object

#------------------------------------------------------------------
# Steps
#------------------------------------------------------------------
timeSeries Linear $tag; # This command is used to construct a TimeSeries object in which the load factor applied is linearly proportional to the time in the domain. 
						# $tag is an input integer given by user to assign a unique tag to the timeSeries.


# The following commnand allows the user to construct a LoadPattern object. Each plain load pattern is associated with a TimeSeries object and can contain multiple NodalLoads, ElementalLoads and SP_Constraint objects.
# The command to generate LoadPattern object contains in { } the commands to generate all the loads and the single-point constraints in the pattern.					
pattern Plain  $patternTag $tsTag {   ;# Note: $patternTag is a	unique tag among load patterns, and $tsTag	is the tag of the time series to be used in the load pattern

load $nodeTag $LoadValue_GlobalX	$LoadValue_GlobalY		$LoadValue_GlobalZ		$LoadValue_GlobalX_rotation		$LoadValue_GlobalY_rotation			$LoadValue_GlobalZ_rotation	

}


# -----------------------------------------------------------------
# Node recorders
# -----------------------------------------------------------------
# The Node recorder type records the response of a number of nodes at every converged step.
recorder Node -file $fileName -time -node $node1 $node2 ...  -dof $dof1 $dof2 ... $respType; # $fileName is the name of file to which output is sent. File output is either in xml format (-xml option), textual (-file option) or binary (-binary option)
																							 # -time: using this option places domain time in first entry of each data line.
																							 # $node1 $node2 ... are the tags of nodes whose response is being recorded.
																							 # $dof1 $dof2 ... are the specified dof at the nodes whose response is requested.
																							 # $respType is a string indicating response required. Response types are: "disp" or "reaction"





# Element recorders
# The Element recorder type records the response of a number of elements at every converged step. The response recorded is element-dependent and also depends on the arguments which are passed to the setResponse() element method.
recorder Element -file $fileName -time -ele $ele1 $ele2 ... $arg; # $fileName is the name of file to which output is sent. 
																  # $ele1 $ele2 ... are the tags of elements whose response is being recorded -- selected elements in domain
																  # $arg is the argument which is passed to the setResponse() element method.
																  # for elasticBeamColumn, the $arg is "force"


# -----------------------------------------------------------------
# Solver
# -----------------------------------------------------------------

# ----------- set up analysis parameters
# CONSTRAINTS handler -- Determines how the constraint equations are enforced in the analysis (http://opensees.berkeley.edu/OpenSees/manuals/usermanual/617.htm)
#          Plain Constraints -- Removes constrained degrees of freedom from the system of equations (only for homogeneous equations)
#          Lagrange Multipliers -- Uses the method of Lagrange multipliers to enforce constraints 
#          Penalty Method -- Uses penalty numbers to enforce constraints --good for static analysis with non-homogeneous eqns (rigidDiaphragm)
#          Transformation Method -- Performs a condensation of constrained degrees of freedom 
constraints Transformation



# DOF NUMBERER (number the degrees of freedom in the domain): (http://opensees.berkeley.edu/OpenSees/manuals/usermanual/366.htm)
#   determines the mapping between equation numbers and degrees-of-freedom
#          Plain -- Uses the numbering provided by the user 
#          RCM -- Renumbers the DOF to minimize the matrix band-width using the Reverse Cuthill-McKee algorithm 
numberer RCM



# SYSTEM (http://opensees.berkeley.edu/OpenSees/manuals/usermanual/371.htm)
#   Linear Equation Solvers (how to store and solve the system of equations in the analysis)
#   -- provide the solution of the linear system of equations Ku = P. Each solver is tailored to a specific matrix topology. 
#          ProfileSPD -- Direct profile solver for symmetric positive definite matrices 
#          BandGeneral -- Direct solver for banded unsymmetric matrices 
#          BandSPD -- Direct solver for banded symmetric positive definite matrices 
#          SparseGeneral -- Direct solver for unsymmetric sparse matrices 
#          SparseSPD -- Direct solver for symmetric sparse matrices 
#          UmfPack -- Direct UmfPack solver for unsymmetric matrices 
system ProfileSPD



# TEST: # convergence test to 
# Convergence TEST (http://opensees.berkeley.edu/OpenSees/manuals/usermanual/360.htm)
#   -- Accept the current state of the domain as being on the converged solution path 
#   -- determine if convergence has been achieved at the end of an iteration step
#          NormUnbalance -- Specifies a tolerance on the norm of the unbalanced load at the current iteration 
#          NormDispIncr -- Specifies a tolerance on the norm of the displacement increments at the current iteration 
#          EnergyIncr-- Specifies a tolerance on the inner product of the unbalanced load and displacement increments at the current iteration 
test NormUnbalance 0.01 100 5



# Solution ALGORITHM: -- Iterate from the last time step to the current (http://opensees.berkeley.edu/OpenSees/manuals/usermanual/682.htm)
#          Linear -- Uses the solution at the first iteration and continues 
#          Newton -- Uses the tangent at the current iteration to iterate to convergence 
#          ModifiedNewton -- Uses the tangent at the first iteration to iterate to convergence 
lgorithm NewtonLineSearch



# Static INTEGRATOR: -- determine the next time step for an analysis  (http://opensees.berkeley.edu/OpenSees/manuals/usermanual/689.htm)
#          LoadControl -- Specifies the incremental load factor to be applied to the loads in the domain 
#          DisplacementControl -- Specifies the incremental displacement at a specified DOF in the domain 
#          Minimum Unbalanced Displacement Norm -- Specifies the incremental load factor such that the residual displacement norm in minimized 
#          Arc Length -- Specifies the incremental arc-length of the load-displacement path 
# Transient INTEGRATOR: -- determine the next time step for an analysis including inertial effects 
#          Newmark -- The two parameter time-stepping method developed by Newmark 
#          HHT -- The three parameter Hilbert-Hughes-Taylor time-stepping method 
#          Central Difference -- Approximates velocity and acceleration by centered finite differences of displacement 
integrator LoadControl 0.01




# ANALYSIS  -- defines what type of analysis is to be performed (http://opensees.berkeley.edu/OpenSees/manuals/usermanual/324.htm)
#          Static Analysis -- solves the KU=R problem, without the mass or damping matrices. 
#          Transient Analysis -- solves the time-dependent analysis. The time step in this type of analysis is constant. The time step in the output is also constant. 
#          variableTransient Analysis -- performs the same analysis type as the Transient Analysis object. The time step, however, is variable. This method is used when 
#                 there are convergence problems with the Transient Analysis object at a peak or when the time step is too small. The time step in the output is also variable.
analysis Static


analyze 100
