#include "exafs.hf"
#define MAX_Z 100
#define MAX_SYMS 20
c*****************************************************************************

	integer function sym2Z(sym)
c
c	given two chacacter sym, returns Z (atomic number).  Only has first
c	100 elements of periodic table.
c
c	Returns -1 if element not found
c
c	Last modified by Corwin Booth 2/24/93
c
c*****************************************************************************

	character*2 sym
	character*2 periodic_table(MAX_Z)
	data periodic_table/'H ','He','Li','Be','B ','C ','N ',
     &			'O ','F ','Ne','Na','Mg','Al','Si','P ','S ','Cl',
     &			'Ar','K ','Ca','Sc','Ti','V ','Cr','Mn','Fe','Co',
     &			'Ni','Cu','Zn','Ga','Ge','As','Se','Br','Kr','Rb',
     &			'Sr','Y ','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag',
     &			'Cd','In','Sn','Sb','Te','I ','Xe','Cs','Ba','La',
     &			'Ce','Pr','Nd','Pm','Sm','Eu','Gd','Tb','Dy','Ho',
     &			'Er','Tm','Yb','Lu','Hf','Ta','W ','Re','Os','Ir',
     &			'Pt','Au','Hg','Tl','Pb','Bi','Po','At','Rn','Fr',
     &			'Ra','Ac','Th','Pa','U ','Np','Pu','Am','Cm','Bk',
     &			'Cf','Es','Fm' /


	i=0
1	i=i+1
	if (i.lt.101) then
                if(sym.ne.periodic_table(i)) goto 1
        else
	        i=-1
        endif
	sym2Z=i

	return
	end

c*****************************************************************************

	character*2 function Z2sym(Z)
c
c	given two chacacter sym, returns Z (atomic number).  Only has first
c	100 elements of periodic table.
c
c	Returns -1 if element not found
c
c	Last modified by Corwin Booth 2/24/93
c
c*****************************************************************************

	integer Z
	character*2 sym
	character*2 periodic_table(MAX_Z)
	data periodic_table/'H ','He','Li','Be','B ','C ','N ',
     &			'O ','F ','Ne','Na','Mg','Al','Si','P ','S ','Cl',
     &			'Ar','K ','Ca','Sc','Ti','V ','Cr','Mn','Fe','Co',
     &			'Ni','Cu','Zn','Ga','Ge','As','Se','Br','Kr','Rb',
     &			'Sr','Y ','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag',
     &			'Cd','In','Sn','Sb','Te','I ','Xe','Cs','Ba','La',
     &			'Ce','Pr','Nd','Pm','Sm','Eu','Gd','Tb','Dy','Ho',
     &			'Er','Tm','Yb','Lu','Hf','Ta','W ','Re','Os','Ir',
     &			'Pt','Au','Hg','Tl','Pb','Bi','Po','At','Rn','Fr',
     &			'Ra','Ac','Th','Pa','U ','Np','Pu','Am','Cm','Bk',
     &			'Cf','Es','Fm' /



	if(i.gt.100) then
		sym='EE'
	else
		sym=periodic_table(Z)
	endif
	Z2sym=sym

	return
	end

c*******************************************************************************
c*******************************************************************************
        real function atomic_weight(Z)
c
c       returns atomic weight in Z in g/mol. Got these from mucal
c*******************************************************************************
        integer Z
        real weight(MAX_Z),temp

        data weight /1.008,  4.003,  6.940,  9.012, 10.811, 12.010, 14.008, 
     &		16.000, 19.000, 20.183, 22.997, 24.320, 26.970, 28.086, 30.975, 
     &		32.066, 35.457, 35.457, 39.102, 40.080, 44.960, 47.900, 50.942, 
     &		51.996, 54.940, 55.850, 58.933, 58.690, 63.540, 65.380, 69.720, 
     &		72.590, 74.920, 78.960, 79.920, 83.800, 85.480, 87.620, 88.905, 
     &		91.220, 92.906, 95.950, 99.000,101.070,102.910,106.400,107.880,
     &		112.410,114.820,118.690,121.760,127.600,126.910,131.300,132.910,
     &		137.360,138.920,140.130,140.920,144.270,147.000,150.350,152.000,
     &		157.260,158.930,162.510,164.940,167.270,168.940,173.040,174.990,
     &		178.500,180.950,183.920,186.200,190.200,192.200,195.090,197.200,
     &		200.610,204.390,207.210,209.000,209.000,210.000,222.000,223.000,
     &		226.000,227.000,232.038,231.036,238.029,237.000,239.100,243.000,
     &		247.000,247.000,251.000,252.000,257.000/


	if(Z.gt.MAX_Z) then
                print *,'Z>100 in atomic_weight, Z=',Z
                print *,'reset to Z=100'
                Z=100
        elseif(Z.lt.1)then
                print *,'Element not found, Z=',Z
                temp=0.0
        else
                temp=weight(Z)
        endif

        atomic_weight=temp
        return
        end

c*******************************************************************************
c*******************************************************************************
        real function tot_weight(formula)
c
c               formula:        character string with chemical formula
c
c*******************************************************************************
        character formula*(*)
        character*2 symbol(MAX_SYMS)
        integer tot_syms,isym
        integer sym2Z,Z
        real num_sym(MAX_SYMS)
        real weight,atomic_weight

        call form2sym(formula,symbol,num_sym,tot_syms)

        weight=0.0
        do isym=1,tot_syms
                Z=sym2Z(symbol(isym))
                weight=weight+atomic_weight(Z)*num_sym(isym)
        enddo

        tot_weight=weight
        return
        end

c*******************************************************************************
c*******************************************************************************
        subroutine form2sym(formula,symbol,num_sym,tot_syms)
c
c       Convert formula into a pair of arrays:
c
c               GIVEN:

c               formula: character string such as Ni2O4
c                        or YBa2Fe0.31Cu2.69O7
c
c               RETURNED:
c               symbol: character string array with the atoms in the formula
c               num_sym: real array with number (occupancy) of symbols
c               tot_syms: integer number of symbols in formula
c
c       Last modified:  2/29/96 CB      add fractional num_sym
c*******************************************************************************

        character formula*(*)
        character*2 symbol(*)
        integer tot_syms,i,isym,form_len
        real num_sym(*)

        logical lowercase,uppercase,a_number,testlogic

        form_len=len(formula)

        i=1
	j=0
        isym=0


c       Build symbol
c
1       if(i.le.form_len) then
         if(uppercase(formula(i:i))) then
                isym=isym+1
                if(i+j+1.le.form_len)testlogic=lowercase(formula(i+1:i+1))
                if((i+1.le.form_len).and.testlogic) then
                        symbol(isym)=formula(i:i+1)
                        i=i+2
                else
                        symbol(isym)=formula(i:i)//' '
                        i=i+1
                endif

c               What is the subscript?

                num_sym(isym)=1
                if(i.le.form_len) then
		 if(a_number(formula(i:i))) then
                        j=0
2                       if(i+j+1.le.form_len)
     &                          testlogic=a_number(formula(i+j+1:i+j+1))
                        if((i+j+1.le.form_len).and.testlogic) then
                                j=j+1
                                goto 2
                        else
                                read(formula(i:i+j),*) num_sym(isym)
                                i=i+j+1
                        endif
                 endif
                endif

c               print *,symbol(isym),num_sym(isym)
                goto 1
         endif
        endif

        tot_syms=isym
        return
        end

c**********************************************************************
c**********************************************************************

	subroutine get_atomic(in_string,Z,e_not,edge_code)
c
c	given character*EDGE_LEN in_string, returns Z and edge_code.
c
c	Uses: get_e_not
c
c	Last Modified: 3/5/93 CB
c***********************************************************************

	character*EDGE_LEN in_string
	character*2 Zsym
	character*4 edge_sym
	real e_not,get_e_not
	integer Z,edge_code,sym2Z

	Zsym=in_string(1:2)
	if(in_string(3:3).eq.' ') then
		edge_sym=in_string(4:7)
	else
		edge_sym=in_string(3:6)
	endif
	Z=sym2Z(Zsym)
	if(edge_sym.eq.'K   ') then
		edge_code=0
	elseif(edge_sym.eq.'LI  '.or.edge_sym.eq.'L1  ') then
		edge_code=1
	elseif(edge_sym.eq.'LII '.or.edge_sym.eq.'L2  ') then
		edge_code=2
	elseif(edge_sym.eq.'LIII'.or.edge_sym.eq.'L3  ') then
		edge_code=3
	else
		print *,'ERROR:get_atomic. symbol bad: ',Zsym,',',edge_sym
	endif

	e_not=get_e_not(Z,edge_code)

	return
	end

c************************************************************************
c************************************************************************

	real function get_e_not(Z,edge_code)

c	Given Z and edge, returns Eo.  Values for K and L3 edges are from
c	mucal.  Other
c	edges are from the X-Ray Data Book.
c
c	Last Modified: 3/5/93 CB
c	12/3/6 CB	put mucal data in
c************************************************************************

	integer Z,edge_code
	real K_e_not(MAX_Z), LI_e_not(MAX_Z), LII_e_not(MAX_Z),LIII_e_not(MAX_Z)
c	data K_e_not /13.6,25,55,112,192,283,399,531,687,867,1072,
c	Adjusted Oxygen(?)
	data K_e_not /13.6,25.00,55.00,112.00,188.00,284.00,402.00,537.00,
     &		686.00,867.00,1072.00,1305.00,1560.00,1839.00,2149.00,2472.00,
     &		2822.00,2822.00,3607.00,4038.00,4493.00,4965.00,5465.00,5989.00,
     &		6540.00,7112.00,7709.00,8333.00,8979.00,9659.00,10367.00,
     &		11104.00,11868.00,12658.00,13474.00,14322.00,15200.00,16105.00,
     &		17080.00,17998.00,18986.00,19999.00,21045.00,22117.00,23220.00,
     &		24350.00,25514.00,26711.00,27940.00,29200.00,30491.00,31813.00,
     &		33169.00,34582.00,35985.00,37441.00,38925.00,40444.00,41991.00,
     &		43569.00,45184.00,46835.00,48520.00,50240.00,51996.00,53789.00,
     &		55618.00,57486.00,59390.00,61332.00,63314.00,65351.00,67414.00,
     &		69524.00,71676.00,73872.00,76112.00,78395.00,80723.00,83103.00,
     &		85528.00,88006.00,90527.00,90527.00,90527.00,98417.00,98417.00,
     &		98417.00,98417.00,109649.00,109649.00,115603.00,115603.00,
     &		121760.00,121760.00,121760.00,121760.00,121760.00,121760.00,
     &		121760.00/

	data LI_e_not /0,0,0,0,0,0,37.3,41.6,0,48.5,63.5,88.6,117.8,
     &			149.7,189,2309,270,326.3,378.6,438.4,498.0,
     &			560.9,626.7,695.7,769.1,844.6,925.1,1008.6,
     &			1096.7,1196.2,1299.0,1414.6,1527.0,1652.0,
     &			1782,1921,2065,2216,2373,2532,2698,2866,3043,
     &			3224,3412,3604,3806,4018,4238,4465,4698,4939,
     &			5188,5453,5714,5989,6266,6548,6835,7126,7428,
     &			7737,8052,7376,7808,9046,9394,9751,10116,
     &			10486,10870,11271,11682,12100,12527,12968,13419,
     &			13880,14353,14839,15347,15861,16388,16939,17493,
     &			18049,18639,19237,19840,20472,21105,21757,22427.0,
     &			23104.0,23808.0,
     &			24526.0,25256.0,26010.0,0,0/

	data LII_e_not /0,0,0,0,0,0,0,0,0,21.7,30.4,49.6,72.9,99.8,136,
     &			163.6,202,250.6,297.6,349.7,403.6,461.2,519.8,
     &			583.8,649.9,719.9,793.3,870.0,952.3,1044.9,1143.2,
     &			1248.1,1359.1,1474.3,1596,1730.9,1864,2007,2156,
     &			2307,2465,2625,2793,2967,3146,3330,3524,3727,3938,
     &			4156,4380,4612,4852,5104,5359,5624,5891,6164,6440,
     &			6722,7013,7312,7617,7930,8252,8581,8918,9264,9617,
     &			9978,10349,10739,11136,11544,11959,12385,12824,
     &			13273,13734,14209,14698,15200,15711,16244,16785,
     &			17337,17907,18484,19083,19693,20314,20948,21600,22266.,
     &			22952.0,23651.0,24371.0,25108.0,0,0/

	data LIII_e_not /0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,
     &		49.20,72.50,99.20,135.00,162.50,200.00,200.00,294.60,346.20,
     &		398.70,453.80,512.10,574.10,638.70,706.80,778.10,855.00,932.00,
     &		1021.00,1115.00,1218.00,1325.00,1436.00,1550.00,1675.00,1805.00,
     &		1940.00,2080.00,2223.00,2371.00,2520.00,2677.00,2838.00,3003.00,
     &		3173.00,3351.00,3537.00,3730.00,3929.00,4132.00,4341.00,4557.00,
     &		4781.00,5012.00,5247.00,5483.00,5724.00,5965.00,6208.00,6460.00,
     &		6717.00,6977.00,7243.00,7515.00,7790.00,8071.00,8358.00,8648.00,
     &		8943.00,9244.00,9561.00,9881.00,10204.00,10534.00,10871.00,
     &		11215.00,11564.00,11918.00,12284.00,12657.00,13035.00,13418.00,
     &		13418.00,13418.00,14612.00,14612.00,14612.00,14612.00,16300.00,
     &		16300.00,17166.00,17610.00,18057.00,18510.0,18970.0,19435.0,
     &		19907.0,0,0/

	if(Z.le.MAX_Z) then
		if(edge_code.eq.0) then
			e_not=K_e_not(Z)
		elseif(edge_code.eq.1) then
			e_not=LI_e_not(Z)
		elseif(edge_code.eq.2) then
			e_not=LII_e_not(Z)
		elseif(edge_code.eq.3) then
			e_not=LIII_e_not(Z)
		else
			stop'ERROR in get_e_not: Edge not supported.'
		endif
	else
		stop'ERROR: get_e_not.'
	endif

	get_e_not=e_not

	return
	end

c**************************************************************************
c**************************************************************************

	logical function check_edge_string(string)

c	Checks syntax of string as an edge string 
c
c	Last Modified: 3/5/93 CB
c**************************************************************************

	character*EDGE_LEN string
	integer sym2Z
	logical todo

1	ierror=0
	iZ=sym2Z(string(1:2))
	if (iZ.lt.1) ierror=1

	if (string(3:3).ne.' ') then
		if (string(2:2).ne.' ') ierror=1
c		Try to fix
c
		string(7:7)=string(6:6)
		string(6:6)=string(5:5)
		string(5:5)=string(4:4)
		string(4:4)=string(3:3)
		string(3:3)=' '
*		print *,'Attempting to fix symbol: ',string
	endif
	if ((string(4:7).ne.'K   ').and.(string(4:7).ne.'LI  ').and.
     &		(string(4:7).ne.'LII ').and.(string(4:7).ne.'LIII').and.
     &		(string(4:7).ne.'L1  ').and.(string(4:7).ne.'L2  ').and.
     &		(string(4:7).ne.'L3  '))
     &		then ierror=1


	if (ierror.gt.0) then
		write(6,1000)
1000		format('Syntax error in edge description.'/
     &              'Please input edge in format AA_EEEE,'/
     &              'where AA are the characters of the atomic',/
     &              'symbol, _ is a space, and EEEE are the edge-'/
     &              'type.  Blank means pre-edge by hand.'/
     &              '  e.g. ''Cu K'' : ',$)
		read(5,'(a8)') string
		if (string.eq.'        ') then
			todo=.false.
		else
			goto 1
		endif
	else
		todo=.true.
	endif

	check_edge_string=todo

	return
	end

