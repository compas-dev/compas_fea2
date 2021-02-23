#------------------------------------------------------------------
# Heading
#------------------------------------------------------------------
#
wipe
model basic -ndm 3 -ndf 6
#
#
#------------------------------------------------------------------
# Nodes
#------------------------------------------------------------------
#
node 1 0.000 0.000 0.000
node 2 20.000 0.000 0.000
#
#
#
#------------------------------------------------------------------
# Boundary conditions
#------------------------------------------------------------------
#
# disp_fixed
#-----------
#
fix 1 1 1 1 1 1 1
#
#
#
#------------------------------------------------------------------
# Materials
#------------------------------------------------------------------
#
# mat_elastic
#------------
#
uniaxialMaterial Elastic 1 200000
#
#
#
#------------------------------------------------------------------
# Elements
#------------------------------------------------------------------
#
# ep_beam
#--------
#
geomTransf Linear 1 0.0 -1.0 0.0;
element elasticBeamColumn 1 1 2 0.1 200000 76923.0769231 0.000312330175 8.33333333333e-05 0.00833333333333 1
#
#
#
#------------------------------------------------------------------
# Steps
#------------------------------------------------------------------
#
# step_load
#----------
#
timeSeries Linear 1
pattern Plain 1 1 {
#
# load_point
#-----------
#
load 2 0.0 0.0 -0.1 0.0 0.0 0.0
#
#
#
# Output
#-------
#
}
#
# Node recorders
#---------------
#
recorder Node -file C:/TEMP/step_load_u.out -time -nodeRange 1 2 -dof 1 2 3 disp
#
recorder Node -file C:/TEMP/step_load_rf.out -time -nodeRange 1 2 -dof 1 2 3 reaction
#
#
# Element recorders
#------------------
#
recorder Element -file C:/TEMP/step_load_sf_beam.out -time -ele 1  localForce
#
# Solver
#-------
#
#
constraints Transformation
numberer RCM
system ProfileSPD
test NormUnbalance 0.01 100 5
algorithm NewtonLineSearch
integrator LoadControl 0.01
analysis Static
analyze 100
