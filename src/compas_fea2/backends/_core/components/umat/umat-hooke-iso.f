       subroutine umat(stress,statev,ddsdde,sse,spd,scd,       
     & rpl,ddsddt,drplde,drpldt,
     & stran,dstran,time,dtime,temp,dtemp,predef,dpred,cmname,
     & ndi,nshr,ntens,nstatv,props,nprops,coords,drot,pnewdt,
     & celent,dfgrd0,dfgrd1,noel,npt,layer,kspt,kstep,kinc)
!---- Deklaration ABAQUS
       implicit none
       integer kstep,kspt,layer,npt,noel,nprops,nstatv,ntens,
     & nshr,ndi,kinc
      double precision sse,spd,scd,rpl,drpldt,dtime,temp,dtemp,
     & pnewdt,celent, dfgrd0(3,3),dfgrd1(3,3),time(2),stress(ntens),
     & statev(nstatv),ddsdde(ntens,ntens),ddsddt(ntens),drplde(ntens),
     & stran(ntens),dstran(ntens),predef(1),dpred(1),props(nprops),
     & coords(3),drot(3,3)
       character*80 cmname
!---- Lokale Deklarationen
       integer i
       double precision E,G,lambda,nu,spEps,eps(6),zero,one,two
!---- Nuetzliche Zahlen
       parameter(zero=0d0, one=1d0, two=2d0)     

!---- Elastische Konstanten
       E      = PROPS(1)           ! E-Modul
       nu     = PROPS(2)           ! Querkontraktionszahl
       G      = (one/two)*E/(one+nu)     ! 2. Lame Konstante (Schubmodul)
       lambda = two*G*nu/(one-two*nu)    ! 1. Lame Konstante
!---- Dehnungstensor zum aktuellen Zeitpunkt
       eps = stran + dstran
!---- Spur des Dehnungstensors      
       spEps = sum(eps(1:3))
!---- Spannungstensor fuer isotropes elastisches Gesetz in ABAQUS-Notation      
       stress(1:3) = lambda*spEps + 2*G*eps(1:3)
       stress(4:6) = G*eps(4:6)
!---- Steifigkeitsmatrix in ABAQUS-Notation
!       ddsdde = ...schon definiert? => ddsdde(ntens,ntens)
!       ddsdde = zero
       ddsdde(1:3,1:3) = lambda
       do i = 1,3
         ddsdde(i,i) = ddsdde(i,i) + 2*G
       end do
       do i = 4,6
         ddsdde(i,i) = G
       end do      

       end
