       subroutine umat(stress,statev,ddsdde,sse,spd,scd,
     &  rpl,ddsddt,drplde,drpldt,
     &  stran,dstran,time,dtime,temp,dtemp,predef,dpred,cmname,
     &  ndi,nshr,ntens,nstatv,props,nprops,coords,drot,pnewdt,
     &  celent,dfgrd0,dfgrd1,noel,npt,layer,kspt,kstep,kinc)
!---- Deklaration ABAQUS
       implicit none
       integer kstep,kspt,layer,npt,noel,nprops,nstatv,ntens,
     &  nshr,ndi,kinc
       double precision sse,spd,scd,rpl,drpldt,dtime,temp,dtemp,
     &  pnewdt,celent, dfgrd0(3,3),dfgrd1(3,3),time(2),stress(ntens),
     &  statev(nstatv),ddsdde(ntens,ntens),ddsddt(ntens),drplde(ntens),
     &  stran(ntens),dstran(ntens),predef(1),dpred(1),props(nprops),
     &  coords(3),drot(3,3)
       character*80 cmname
!---- Lokale Deklarationen
       integer i,j
       double precision c1111,c2222,c1122,c2233,c1212,c2323,eps(6),
     &  zero,one,two
!---- Nuetzliche Zahlen
       parameter(zero=0d0, one=1d0, two=2d0) 
       
!---- Dehnungstensor zum aktuellen Zeitpunkt
       eps = stran + dstran     
!---  Einlesen der Materialeingeschaften 
       c1111 = props(1)
       c2222 = props(2)
       c1122 = props(3)
       c2233 = props(4)
       c1212 = props(5)
!---  Berechnen der sechsten abhaengigen Konstante    
       c2323 = (one/two)*(c2222-c2233)
!---  Konstanten im Feld ddsdde speichern
       ddsdde(1,1:6) = [ c1111,c1122,c1122,zero ,zero ,zero ]
       ddsdde(2,1:6) = [ c1122,c2222,c2233,zero ,zero ,zero ]
       ddsdde(3,1:6) = [ c1122,c2233,c2222,zero ,zero ,zero ]
       ddsdde(4,1:6) = [ zero ,zero ,zero ,c1212,zero ,zero ]
       ddsdde(5,1:6) = [ zero, zero, zero ,zero ,c1212,zero ] 
       ddsdde(6,1:6) = [ zero, zero, zero, zero, zero, c2323]
!---  Spannung ausrechnen
       !stress = zero
       do i=1,6
         do j=1,6 
           stress(i)= stress(i) + ddsdde(i,j)*eps(j)
         end do
       end do

       end
