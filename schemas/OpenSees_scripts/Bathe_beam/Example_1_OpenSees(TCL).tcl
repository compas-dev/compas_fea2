wipe all;

model BasicBuilder -ndm 2 -ndf 3;

node    1       0.0     0.0;
node    2       20.0    0.0;

fix     1       1       1       1;

set LinearTransf 1;
geomTransf Linear $LinearTransf;


set eleTag  1;
set A       [expr 0.1*1];
set E       200000.0;
set Iz      [expr 0.1*1/12.0];
element elasticBeamColumn $eleTag 1 2 $A $E $Iz $LinearTransf


pattern Plain 101 Constant {

	load    2   0.0  -0.1    0.0;

}



recorder Node       -file Reaction.out    -node 1 -dof 1     2   3 reaction;
recorder Node       -file Disp.out        -node 2 -dof 1     2   3 disp;
recorder Element    -file Ele_Force.out   -ele  1                  force;

set Tol 1.0e-6;							# convergence tolerance for test
constraints Plain;						# how it handles boundary conditions
numberer RCM;							# renumber dof's to minimize band-width (optimization)
system BandGeneral;						# how to store and solve the system of equations in the analysis (large model: try UmfPack)
test NormDispIncr $Tol 6;				# determine if convergence has been achieved at the end of an iteration step
algorithm Newton;						# use Newton's solution algorithm: updates tangent stiffness at every iteration
set LoadStep 10;					    # apply gravity in 10 steps
set Increment [expr 1.0/$LoadStep];	    # load increment
integrator LoadControl $Increment;		# determine the next time step for an analysis
analysis Static;						# define type of analysis static or transient
analyze $LoadStep;					    # apply gravity

loadConst -time 0.0
