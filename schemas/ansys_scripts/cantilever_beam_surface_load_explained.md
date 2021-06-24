# Ansys input files

## Structure

### File start (physical)

```
/batch                           ! Set the program in batch mode 
/config,noeldb,1                 ! off writing results to database
*get,_wallstrt,active,,time,wall ! Start a timer (get retrieves a value and store it
! ANSYS input file written by Workbench version 2020 R2
! File used for geometry attach: C:\Users\robin\AppData\Local\Temp\WB_DESKTOP-6I1E0KC_robin_10284_8\unsaved_project_files\dp0\SYS\DM\SYS.agdb
/title,cantilever_simple--Static Structural (A5)
! Create an array with its dimensions
*DIM,_wb_ProjectScratch_dir,string,248  
_wb_ProjectScratch_dir(1) = 'C:\Users\robin\Documents\cantilever_simple_files\dp0\SYS\MECH\'
*DIM,_wb_SolverFiles_dir,string,248
_wb_SolverFiles_dir(1) = 'C:\Users\robin\Documents\cantilever_simple_files\dp0\SYS\MECH\'
*DIM,_wb_userfiles_dir,string,248
_wb_userfiles_dir(1) = 'C:\Users\robin\Documents\cantilever_simple_files\user_files\'
/com,--- Data in consistent MKS units. See Solving Units in the help system for more information.
```

### File start tag

```
/units,MKS                  ! Annotate the database with system of units used 
/nopr                       ! Issuing this command with no arguments suppresses the interpreted data input print out.    
/wb,file,start              ! signify a WB generated input file
/prep7                      ! These commands are used to create and set up the model
SHPP,OFF,,NOWARN            ! --> Turn off shape checking because checks already performed inside WB mesher.
/nolist                     ! Issue the command with no arguments to suppress the data input listing. Suppress til /golist used
etcon,set                   ! allow ANSYS to choose best KEYOP's for 180x elements
```

### Nodes

357 nodes in real, why 392 for the dimension instead of 357?


```
nblock, 3, 392, ! node block, NUM_FIELDS
(1i9,3e20.9e3)  ! formatters
        1    -1.250000000E-01     1.000000000E-01     2.000000000E-01
        2    -2.500000000E-01     1.000000000E-01     2.000000000E-01
        3    -3.750000000E-01     1.000000000E-01     2.000000000E-01
        4    -5.000000000E-01     1.000000000E-01     2.000000000E-01
        5    -6.250000000E-01     1.000000000E-01     2.000000000E-01
        6    -7.500000000E-01     1.000000000E-01     2.000000000E-01
        7    -8.750000000E-01     1.000000000E-01     2.000000000E-01
        8    -1.250000000E-01     1.000000000E-01     1.000000000E-01
        9    -2.500000000E-01     1.000000000E-01     1.000000000E-01
       10    -3.750000000E-01     1.000000000E-01     1.000000000E-01
...
      353    -3.125000000E-01    -3.827021247E-17     0.000000000E+00
      354    -4.375000000E-01    -5.357829746E-17     0.000000000E+00
      355    -5.625000000E-01    -6.888638245E-17     0.000000000E+00
      356    -6.875000000E-01    -8.419446744E-17     0.000000000E+00
      357    -8.125000000E-01    -9.950255243E-17     0.000000000E+00
-1
```

The final line of the block will be a -1 in field 1.

### Elements

186 elements
```
\wb, elem, start
et,1,186
keyo,1,2,1          ! set full integration on SOLID186
eblock,19,solid,,48 ! Block of elements, NUM_NODES (number of nodes to be read in the first line of an element def), solid=part of a solid model. 48 is the element type number.
(19i9)
        1        1        1        1        0        0        0        0       20        0        1        1       73       80       81       28       75       79       88
        113      308      319      114      209      312      318      210      111      307      317      321
...
-1
\wb, elem, end
```

#### Details on fields

- Field 1 - The material number.
- Field 2 - The element type number.
- Field 3 - The real constant number.
- Field 4 - The section ID attribute (beam section) number.
- Field 5 - The element coordinate system number.
- Field 6 - The birth/death flag.
- Field 7 - The solid model reference number.
- Field 8 - The element shape flag.
- Field 9 - The number of nodes defining this element if Solkey = SOLID; otherwise, Field 9 = 0.
- Field 10 - Not used.
- Field 11 - The element number.
- Field 12-xx The node numbers

The final line of the block will be a -1 in field 1.

### Coordinate system

```
/com,*********** Send User Defined Coordinate System(s) ***********
csys,0          ! Cartesian
```

### Temperature 

```
toffst,273.15,  ! Temperature offset from absolute zero
/com,*********** Set Reference Temperature ***********
tref,22.        ! Reference temp
```

### Material

```
/wb,mat,start   !  starting to send materials
/com,*********** Send Materials ***********
Temperature = 'TEMP' ! Temperature
MP,DENS,1,7850,	        ! density kg m^-3
MP,ALPX,1,1.2e-05,	! secant coefficients of thermal expansion C^-1
MP,C,1,434,	        ! specific heat J kg^-1 C^-1
MP,KXX,1,60.5,	        ! thermal conductivity W m^-1 C^-1
MP,RSVX,1,1.7e-07,	! kg m^3 A^-2 s^-3
MP,EX,1,200000000000,	! Pa Elastic modulus
MP,NUXY,1,0.3,          ! Minor Poisson's ratios 
MP,MURX,1,10000,        ! Magnetic relative permeabilities

/wb,mat,end                !  done sending materials
```

### Model

#### Bounding box

```
! get the diagonal of the bounding box. Needed later for other things
*get,_xmin,node,,mnloc,x
*get,_ymin,node,,mnloc,y
*get,_zmin,node,,mnloc,z
*get,_xmax,node,,mxloc,x
*get,_ymax,node,,mxloc,y
*get,_zmax,node,,mxloc,z
_ASMDIAG=(_xmax-_xmin)*(_xmax-_xmin)+(_ymax-_ymin)*(_ymax-_ymin)+(_zmax-_zmin)*(_zmax-_zmin)
_ASMDIAG=SQRT(_ASMDIAG)
```

#### Contacts

```
/wb,contact,start          !  starting to send contact
/wb,contact,end            !  done creating contacts
```

#### 

```
\golist                    ! Cancel \nolist written at the beginning of the input file
```

#### Loads

```
/wb,load,start                          !  Starting to send loads
/com,*********** Fixed Supports ***********
CMBLOCK,_FIXEDSU,NODE,       29         !  Defines the entities contained in a node or element component
(8i10)
        61        62        63        64        65        66        67        68
        69        70        71        72       285       286       287       288
       289       290       291       292       293       294       295       296
       297       298       299       300       303
cmsel,s,_FIXEDSU                        !  Selects a subset of components and assemblies.
d,all,all
nsel,all
/com,*********** Define Force Using Surface Effect Elements ***********
local,12,0,0.,0.,0.,0.,0.,0.
csys,0
et,2,154
eblock,10,,,16
(15i9)
      141        2        2        2       12       78       95       43       57      316      250      249      279
      142        2        2        2       12       77      102       95       78      315      340      316      314
      143        2        2        2       12       95       96       44       43      339      252      248      250
      144        2        2        2       12      102      103       96       95      352      342      339      340
      145        2        2        2       12       96       97       45       44      341      254      251      252
      146        2        2        2       12      103      104       97       96      353      344      341      342
      147        2        2        2       12       97       98       46       45      343      256      253      254
      148        2        2        2       12      104      105       98       97      354      346      343      344
      149        2        2        2       12       98       99       47       46      345      258      255      256
      150        2        2        2       12      105      106       99       98      355      348      345      346
      151        2        2        2       12       99      100       48       47      347      260      257      258
      152        2        2        2       12      106      107      100       99      356      350      347      348
      153        2        2        2       12      100      101       49       48      349      262      259      260
      154        2        2        2       12      107      108      101      100      357      351      349      350
      155        2        2        2       12      101       69       61       49      301      286      261      262
      156        2        2        2       12      108       70       69      101      302      300      301      351
-1
esel,s,type,,2
keyop,2,2,1                ! Apply load in local coordinate system
keyop,2,7,1                ! Use original area so load is constant in large deformation
keyop,2,11,2               ! Use real and not project area
esel,all
/gst,on,on
fini
*get,_numnode,node,0,count
*get,_numelem,elem,0,count
*get, _MAXELEMNUM, elem, 0, NUM, MAX
*get, _MAXNODENUM, node, 0, NUM, MAX
*get, _MAXELEMTYPE, etyp, 0, NUM, MAX
*get, _MAXREALCONST, real, 0, NUM, MAX
/go
/wb,load,end               !  done creating loads
```

### Solution

I haven't worked on this yet. ANSYS works like ABAQUS. You need to specifically ask for solutions
for Von-Mises, deformation etc... If you want to add something to study, you need to reload the
calculations. 

```
*get,_wallbsol,active,,time,wall
/com,****************************************************************************
/com,*************************    SOLUTION       ********************************
/com,****************************************************************************
/solu
antype,0                        ! static analysis
_thickRatio=  0                 ! Ratio of thick parts in the model
eqsl,sparse,,,,,1
cntr,print,1                    ! print out contact info and also make no initial contact an error
dmpoption,emat,no               ! Don't combine emat file for DANSYS
dmpoption,esav,no               ! Don't combine esav file for DANSYS
nldiag,cont,iter                ! print out contact info each equilibrium iteration
rescontrol,,none                ! Do not keep any restart files
/com,****************************************************
/com,******************* SOLVE FOR LS 1 OF 1 ****************
esel,s,type,,2
nsle
sfe,all,1,pres,1,0.
sfe,all,2,pres,1,0.
sfe,all,3,pres,1,-50000.0000000037
nsel,all
esel,all
/nopr
/gopr
nsub,1,1,1
time,1.
outres,erase
outres,all,none
outres,nsol,all,
outres,rsol,all
outres,eangl,all
outres,etmp,all
outres,veng,all
outres,strs,all,
outres,epel,all,
outres,eppl,all,
outres,cont,all,
! *********** WB SOLVE COMMAND ***********
! check interactive state
*get,ANSINTER_,active,,int
*if,ANSINTER_,ne,0,then
/eof
*endif
solve
/com *************** Write FE CONNECTORS ********* 
CEWRITE,file,ce,,INTE
/com,****************************************************
/com,*************** FINISHED SOLVE FOR LS 1 *************
*get,_wallasol,active,,time,wall
/nopr
*get,_numnode,node,0,count
*get,_numelem,elem,0,count
*get, _MAXELEMNUM, elem, 0, NUM, MAX
*get, _MAXNODENUM, node, 0, NUM, MAX,,,INTERNAL
*get, _MAXELEMTYPE, etyp, 0, NUM, MAX
*get, _MAXREALCONST, real, 0, NUM, MAX
/gopr
/post1
xmlo,ENCODING,ISO-8859-1
xmlo,parm
/xml,parm,xml
fini
/gopr
*get,_walldone,active,,time,wall
_preptime=(_wallbsol-_wallstrt)*3600
_solvtime=(_wallasol-_wallbsol)*3600
_posttime=(_walldone-_wallasol)*3600
_totaltim=(_walldone-_wallstrt)*3600
*get,_dlbratio,active,0,solu,dlbr
*get,_combtime,active,0,solu,comb
/com,--- Total number of nodes = %_numnode%
/com,--- Total number of elements = %_numelem%
/com,--- Element load balance ratio = %_dlbratio%
/com,--- Time to combine distributed files = %_combtime%
/wb,file,end               ! done with WB generated input
```

  
