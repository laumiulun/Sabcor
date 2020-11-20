#include "exafs.hf"
#include "sabcor.hf"

c*******************************************************************************
c*******************************************************************************
	subroutine fluor_corr(k,kchi_r,kchi_i,nf,nx,title,ntit,d,phi,theta,
     &			formvol,formula,edge,fluor_energy,concentration,
     &			io,option)
c
c	
c
c	io:	character='p' to print out statistics
c			  'f' to make a "sab_cor.dat" file with correction and 
c				information depth vs k
c			  'a' to output all (p and f)
c			  'n' where n is any character other that f and p
c				for no verbosity (is that a word?)
c	option:	character='u' to undo a self-absorption correction,
c				Otherwise do correction
c
c	last modified:
c		1/12/95 CB	added option to corr_chi to undo the
c				sab effect
c		3/24/3  CB	added k to corr_chi call for better
c				warnings
c		4/28/4	CB	header on sab_cor.dat
c*******************************************************************************

	integer nx,ntit,idat,nf
	integer Z,edge_code
	real d, phi,theta,formvol,temp
	real fluor_energy,concentration,e_not,phi_rad,theta_rad
	real tot_abs,fluor_abs
	real energy_at_1,tot_at_1
	real atomic_abs,energy,chi,corr_chi,correction
	real new_chi,g
	real info_depth
	character*FORMULA_LEN formula
	character*EDGE_LEN edge
c	character*INP_FILENAME_LEN inp_filename
	character*6 tempstring
	character io*1,option

	character*TIT_LEN title(MAX_TIT)
	real k(*),kchi_r(*),kchi_i(*)
	real info_at_5,corr_at_5
	logical isthick
        integer stringlen

c	Need Eo for calculating the energy
c
	call get_atomic(edge,Z,e_not,edge_code)
	
c	debugging...
!	print *,'Thickness=',d
!	print *,'e_not=',e_not
!	print *,'fluor_e=',fluor_energy
!	print *,'Density=',density('Cu3',formvol)
!	print *,'Phi=',phi
!	print *,'formula unit volume=',formvol
!	print *,'Formula=',formula
!	print *,'Edge=',edge

c	Convert angles to radians
c
	phi_rad=2.0*PI*phi/360.0
	if(theta.lt.-1000.0) then
		!print *,'Using default theta:',theta
		theta_rad=PI/2.0 - phi_rad
	else
		theta_rad=2.0*PI*theta/360.0
	endif
		
	g=sin(phi_rad)/sin(theta_rad)


c	Begin correction loop
c
c	Open up a stats file
c
	if(io.eq.'f'.or.io.eq.'a') then
		print 1111
1111		format('Outputting self-absorption correction to sab_cor.dat')
		open(3,file='sab_cor.dat')
		write(3,'(a)') '#	k	correction_coeff 	info_depth (Angstroms)'
	endif
	isthick=.false.	!Initialize
	do idat=1,nx
c
c		k() is the wavevector (real)
c

c		Need in terms of eV, since that is what the Victoreen
c		coefficients are in terms of...
c
c		trouble?
		if(k(idat).ge.0.0) then
		energy=e_not+(k(idat)/EV2INVANG)**2.0
		else
			print *,'Trouble in fluor_corr? k=',k(idat)
		endif
c	
c               Correction needs the total absorption
c
		call get_mus(tot_abs,fluor_abs,atomic_abs,formula,edge,energy,
     &			fluor_energy,concentration,formvol)

!	DEBUG
	!	alpha=tot_abs+fluor_abs*g
!		if(idat.eq.100) print *,'DEBUG: idat,k,tot_abs,fluor_abs,atomic_abs,alpha/mu_a=',idat,k(idat),tot_abs,fluor_abs,atomic_abs
!		if(idat.eq.100) print *,'DEBUG: alpha,g, alpha/atomic_abs=',alpha,g, alpha/atomic_abs

	
c		Separate out chi
c
		chi=kchi_r(idat)/k(idat)
		new_chi=corr_chi(k(idat),chi,tot_abs,atomic_abs,fluor_abs,
     &			d*1.0e-8,phi_rad,theta_rad,g,option,ierr)
		if(ierr.eq.0.and.isthick) then
!			print *,'WARNING: wasn''t thick, now is, k=',k(idat)
			continue
		elseif(ierr.eq.1.and.(.not.isthick)) then
			isthick=.true.
!			if(io.ne.'n')
!     &			  print *,'WARNING:  Using ''thick limit'' equation.'
		endif
!		if(idat.eq.100) print *,'DEBUG: chi,new_chi,isthick,d,phi_rad,g,option=',chi,new_chi,isthick,d,phi_rad,g,option
		correction=new_chi/chi
		kchi_r(idat)=new_chi*k(idat)

c		Do imaginary part, if it is there!
		if(nf.eq.2.or.nf.eq.12) kchi_i(idat)=correction*kchi_i(idat)
		

		temp =1.0e8*info_depth(tot_abs,fluor_abs,phi_rad,theta_rad,g)
		if(k(idat).le.5.0) then
			corr_at_5=correction
			info_at_5=temp
		endif

		if(io.eq.'f'.or.io.eq.'a') write(3,*) k(idat),correction,temp
	enddo

c	Close the stats file
	if(io.eq.'f'.or.io.eq.'a') close(3)

c	Fix up header
c
	write(tempstring,'(f6.3)') corr_at_5
	if(ntit.lt.MAX_TIT) ntit=ntit+1
	title(ntit) = 'Self-absorption corrected with '//VERSION//
     &		', corr at 5 inv ang= '//tempstring
	if(ntit.lt.MAX_TIT) then
                ntit=ntit+1
                ifl=stringlen(formula)
                write(tempstring,'(f6.0)') d
                title(ntit) = 'using formula='//formula(1:ifl)//
     &                  ' and thickness='//tempstring//' Angstroms.'
        endif

c	debugging...
!	print *,'DEBUGGING again...'
!	print *,'Thickness=',d
!	print *,'e_not=',e_not
!	print *,'fluor_e=',fluor_energy
!	print *,'Density=',density('Cu3',formvol)
!	print *,'Phi=',phi
!	print *,'formula unit volume=',formvol
!	print *,'Formula=',formula
!	print *,'Edge=',edge


	if(io.eq.'p'.or.io.eq.'a') then
	print *
	print *,'Self-Absorption correction statistics: '
	print *
	print 1010,info_at_5
1010	format('info depth at 5 inv ang:                  ',f8.1,' Angstroms')
	print 1011,corr_at_5
1011	format('correction chi_true/chi_exp at 5 inv ang: ',f6.2)
c	print *,'Thickness=',d
c	print *,'e_not=',e_not
c	print *,'Density=',density('Cu3',formvol)
c	print *,'Phi=',phi
c	print *,'formula unit volume=',formvol
c	print *,'Formula=',formula
c	print *,'Edge=',edge
	print *
	endif



	return
	end

c*******************************************************************************
c*******************************************************************************
	real function get_tot_abs(formula,energy,edge,formvol)
c
c	Returns absorption in inverse cm.
c
c*******************************************************************************
	character*(*) formula
	character*EDGE_LEN edge
	character*2 symbol(MAX_SYMS),tempsym
	real energy,temp,lam_e,conversion
	real e_nots(9),density
	real xsec(11),fly(4)
	real formvol,mu_Z,cross_section
	real num_sym(MAX_SYMS)
	integer isym,ier
	integer Z,tot_syms,sym2Z
	logical erf
	data erf/.false./

c	Function defs
c

c	Begin...
c

	temp=0.0
	ier=0
	lam_e=EV2ANG/energy


	call form2sym(formula,symbol,num_sym,tot_syms)

c	Got the symbol list.  Now we need to figure out which edge coefficients
c	we need to use from the Victoreen formula
c
	cross_section=0.0
	do isym=1,tot_syms
		Z=sym2Z(symbol(isym))
	
c		Now weve got the proper edge to work with, get the proper coefficients
c		and add up the absorption
c
	
c		Convert to inverse cm
c

c		using McMaster tables
c
		tempsym='  '
		call mucal(energy/1000.0,tempsym,
     &				Z,'B',xsec,e_nots,fly,erf,ier)
		temp=xsec(4)

c		Try Using Henke Tables
c

c		temp=cross(energy,Z)

		conversion=1.0
		conversion=conversion*num_sym(isym)
		conversion=conversion*density(symbol(isym),formvol)

c		Put mu_Z into inverse cm
		mu_Z=conversion*temp

		cross_section=cross_section+mu_Z 
		
		if(ier.gt.0.and.ier.ne.5.and.ier.ne.6) then
			print *,'energy=',energy
			print *,'ier,symbol,numer ',ier,symbol(isym),
     &				num_sym(isym)
			print *,'Z,cross_section,mu_Z',Z,cross_section,mu_Z
			print *,'E_nots:',e_nots
		endif

666	enddo


	temp=cross_section

	get_tot_abs=temp
	return
	end

c*******************************************************************************
c*******************************************************************************
	real function get_noedge_abs(formula,energy,edge,formvol)
c
c	Returns absorption in inverse cm, MINUS the current absorption edge.
c	Nearly a copy of get_tot_abs.
c
c*******************************************************************************
	character*(*) formula
	character*EDGE_LEN edge
	character*2 symbol(MAX_SYMS),tempsym
	real energy,temp,lam_e,conversion
	real e_nots(9),density
	real xsec(11),fly(4)
	real formvol,mu_Z,cross_section
	real num_sym(MAX_SYMS)
	integer isym,ier
	integer Z,tot_syms,sym2Z
	logical erf
	data erf/.false./

c	Function defs
c

c	Begin...
c

	temp=0.0
	ier=0
	lam_e=EV2ANG/energy


	call form2sym(formula,symbol,num_sym,tot_syms)

c	Got the symbol list.  Now we need to figure out which edge coefficients
c	we need to use from the Victoreen formula
c
	cross_section=0.0
	do isym=1,tot_syms
		Z=sym2Z(symbol(isym))
	
c		Now weve got the proper edge to work with, get the proper coefficients
c		and add up the absorption
c
	
c		Convert to inverse cm
c

c		using McMaster tables
c
		tempsym='  '
		call mucal(energy/1000.0,tempsym,
     &				Z,'B',xsec,e_nots,fly,erf,ier)
		temp=xsec(11)
c		print *,'DEBUG: energy,xsec(1),xsec(11)=',energy,xsec(1),xsec(11)

c		Try Using Henke Tables
c

c		temp=cross(energy,Z)

		conversion=1.0
		conversion=conversion*num_sym(isym)
		conversion=conversion*density(symbol(isym),formvol)

c		Put mu_Z into inverse cm
		mu_Z=conversion*temp

		cross_section=cross_section+mu_Z 
		
		if(ier.gt.0.and.ier.ne.5.and.ier.ne.6) then
			print *,'energy=',energy
			print *,'ier,symbol,numer ',ier,symbol(isym),
     &				num_sym(isym)
			print *,'Z,cross_section,mu_Z',Z,cross_section,mu_Z
			print *,'E_nots:',e_nots
		endif

666	enddo


	temp=cross_section

	get_noedge_abs=temp
	return
	end

c*******************************************************************************
c*******************************************************************************
	logical function lowercase(x)
c*******************************************************************************
	character*1 x,lower_alpha(26)
	integer i
	logical temp

	data lower_alpha/'a','b','c','d','e','f','g','h','i','j','k','l','m',
     &		'n','o','p','q','r','s','t','u','v','w','x','y','z'/

	temp=.false.

	do i=1,26
		if(x.eq.lower_alpha(i)) temp=.true.
	enddo

	lowercase=temp
	return
	end

c********************************************************************************
c********************************************************************************
	logical function uppercase(x)
c********************************************************************************
	character*1 x,upper_alpha(26)
	integer i
	logical temp

	data upper_alpha/'A','B','C','D','E','F','G','H','I','J','K','L','M',
     &          'N','O','P','Q','R','S','T','U','V','W','X','Y','Z'/
 
        temp=.false.
        
        do i=1,26
                if(x.eq.upper_alpha(i)) temp=.true.
        enddo
        
        uppercase=temp
        return
        end

c********************************************************************************
c********************************************************************************
        logical function a_number(x)
c********************************************************************************
        character*1 x,numbers(11)
	integer i
        logical temp
 
        data numbers/'0','1','2','3','4','5','6','7','8','9','.'/
 
        temp=.false.
 
        do i=1,11
                if(x.eq.numbers(i)) temp=.true.
        enddo
 
        a_number=temp
        return
        end
 
c*******************************************************************************
c*******************************************************************************
	real function density(formula,formvol)
c
c	Returns the density in units of (atoms) per (barn cm), which is the same
c	as atoms per cubic angstrom.

c*******************************************************************************
	character*(*) formula
	character*2 symbol(MAX_SYMS)
	integer tot_syms,i
	real num_sym(MAX_SYMS)
	real formvol,volume
	real temp

	call form2sym(formula,symbol,num_sym,tot_syms)

	temp=0.0
	do i=1,tot_syms
		temp=temp+num_sym(i)/formvol
	enddo
	density=temp
	return
	end

c*******************************************************************************
c*******************************************************************************
	real function corr_chi(k,chi_exp,mu_t,mu_a,mu_f,d_given,phi,theta,g,
     &		option,ierr)
c
c	k:		real k vector (just for WARNINGS, and DEBUG)
c	chi_exp:	real experimental measurement of XAFS chi
c	mu_t:		real total absorption coefficient of material
c	mu_a:		real absorbing atom''s total absorption contribution to mu_t
c	mu_f:		real total absorption at the fluorescence energy
c	d_given:	real thickness of material in cm.
c	phi:		real angle of incident beam wrt sample surface in rads.
c	g:		sin(phi)/sin(theta), where theta is the angle of the
c			exit beam wrt the sampe surface.
c	option:		character='u' to undo the correction, otherwise make
c			correction.  In this case, chi_exp is really chi
c	ierr:		Error code =0 ok, =1 used thick limit
c
c	This should work even in the thin limit
c
c	Last modified:
c		1/12/95 CB	added option 'u'
c		10/13/5 CB	Now use the approximation in the paper as a 	c				seed value to solve "exactly"!
c********************************************************************************
	real k,chi_exp,mu_t,mu_a,mu_f,d,phi,theta
	real d_given,g
	real reality,approx,error
	double precision alpha,beta,gamma,chi
	double precision thick
	double precision crit1,crit2
	character option

!	print *,'DEBUG in corr_chi: k,chi_exp,mu_t,mu_a,mu_f,d_given,phi,g,option=',k,chi_exp,mu_t,mu_a,mu_f,d_given,phi,g,option,chi
c	Initialize ierr
	ierr=0

c	Set a maximum limit on thickness
c	Why? Deal with this below CB 2/14/13
!	if(d_given.gt.0.01) then
!		d=0.01
!	else 
		d=d_given
!	endif

	alpha=mu_t+mu_f*dble(g)
	beta=alpha*mu_a*d*dexp(-alpha*d/sin(phi))/sin(phi)
	gamma=1.0-dexp(-alpha*d/sin(phi))


c

c	Thick limit is more accurate than Troger et al because it includes the
c	XAFS oscillations
c
	if(option.eq.'u') then
		thick = chi_exp*(alpha-mu_a)/(alpha+chi_exp*mu_a)
	else
		thick = chi_exp/(1.0-mu_a*(1.0+chi_exp)/alpha)
!		print *,'DEBUG: chi_exp,mu_a,alpha,thick=',chi_exp,mu_a,alpha,thick,mu_a/alpha
	endif

c	Criteria are for checking if roundoff error is starting to be a 
c	problem
	crit1=(4.0*beta*alpha*gamma*chi_exp)/
     &		(gamma*(alpha-mu_a*(chi_exp+1.0))+beta)
	crit2=beta

!	Max d for non-thick is 1 cm
	if(abs(crit1).gt.1.0e-7.and.abs(crit2).gt.1.0e-7.and.d.le.0.01) then
c	
c	Otherwise use the "nearly exact" expression 
! Now used as a starting value below
c
		if(option.eq.'u') then

c		This is exact...
c		chi=(1.0-dexp(-(alpha+chi_exp*mu_a)*d/sin(phi)))
c		chi=chi*(chi_exp+1)*alpha/(gamma*(alpha+chi_exp*mu_a))
c		chi=chi-1.0

c		This is from the same approx used in the else...
		F=gamma*mu_a/(2.0*beta)
		E=-(gamma*(alpha-mu_a)+beta)/(2.0*beta)
		H=alpha*gamma/beta
		chi=(chi_exp*(chi_exp-2.0*E))/(2.0*F*chi_exp+H)

		else
	
		chi=-(gamma*(alpha-mu_a*(chi_exp+1.0))+beta)
		chi=chi+dsqrt(chi*chi+4.0*beta*alpha*gamma*chi_exp)
		chi=chi/(2.0*beta)

		endif
!		print *,'WARNING:  NOT Using ''thick limit'' equation.',k,thick,d
	else
c
c	If roundoff potentially bad, goto the thick limit
c
		chi=thick
		ierr=1
!		print *,'WARNING:  Using ''thick limit'' equation.',k,thick,d,chi_exp
	endif

c	Check the main approx ! Don't need to anymore? Solved exactly below
c
c	Playing with some improvements 10/14/5 CB to get around the 
c	"approximation" in the paper
	jj=0
	old_chi=chi
	do while (abs((chi_exp-chi_exp_trial)).gt.1E-7.and.jj.lt.200)
		jj=jj+1

		chi_exp_trial=(1-exp(-(alpha+chi*mu_a)*d/sin(phi)))
		chi_exp_trial=chi_exp_trial/(1-exp(-alpha*d/sin(phi)))
		chi_exp_trial=chi_exp_trial*(alpha*(chi+1))/(alpha+chi*mu_a)
		chi_exp_trial=chi_exp_trial-1
		del_chi=(chi_exp-chi_exp_trial)
		chi=chi+del_chi
	enddo
	error=abs(chi_exp-chi_exp_trial)
	if(error.gt.1E-6) print *,'DEBUG: k,error,jj=',k,error,jj
	error=(chi-old_chi)/chi
	corr_fact=chi/chi_exp
!	Print a warning if this procedure improved things by more than 5%
!	Not anymore!
c	if(error.gt.0.05) print 667,k,old_chi/chi_exp,corr_fact,100.0*error,jj
667	format('DEBUG:k,chi/chi_exp,old_chi/chi_exp,%improv,jj=',f5.2,1x,f4.2,1x,f4.2,1x,f6.2,'%',1x,i3)


!	print *,'DEBUG2 in corr_chi: k,chi_exp,mu_t,mu_a,mu_f,d_given,phi,g,option=',k,chi_exp,mu_t,mu_a,mu_f,d_given,phi,g,option,chi
	corr_chi=real(chi)
	return
	end
c********************************************************************************
c********************************************************************************
	real function thick_chi(chi_exp,mu_t,mu_a,mu_f,phi,theta)

c	In the thick approximation ala L. Troger and K. Baberschke et al,
c	PRB 46, 3283 (1992).
c********************************************************************************
	real chi_exp,mu_t,mu_a,mu_f,phi,theta
	real g,alpha,chi
	logical first
	data first/.true./

	if(phi.ne.old_phi) first=.true.
	if(first) g=sin(phi)/sin(theta)
	old_phi=phi
	alpha=mu_t+mu_f*g

	chi=chi_exp/(1.0-mu_a/alpha)

	first=.false.
	thick_chi=chi
	return
	end

c********************************************************************************
c********************************************************************************
	real function info_depth(tot_abs,fluor_abs,phi,theta,g)

	real tot_abs,fluor_abs,phi,g,tcrazy

c	From Troger and Baberschke
c
	tcrazy=sin(phi)/(tot_abs+fluor_abs*g)
	if (tcrazy.lt.0.0) print *,phi,g,tot_abs,fluor_abs

	info_depth=tcrazy
	return
	end
c********************************************************************************
c********************************************************************************
	subroutine get_mus(tot_abs,fluor_abs,atomic_abs,formula,edge,energy,
     &			fluor_energy,concentration,formvol)
	
c	Last modified: 2/29/96 CB	cleaned up fractional units in formula
c		3/31/00 CB	activate old_fluor_energy to change from "first"
c********************************************************************************
	integer i,j
	real formvol,concentration,tot_abs,fluor_abs,atomic_abs
	real energy,fluor_energy,old_fluor_energy
	character*FORMULA_LEN atomic_sym
	character*FORMULA_LEN formula, old_formula
	character*EDGE_LEN edge, old_edge
	logical a_number

c	Functions def
	real get_tot_abs
	real get_noedge_abs

	logical first
	data first/.true./

c	If anything changes, then this call should not be treated as "first."
	if (old_formula.ne.formula.or.old_edge.ne.edge
     &		.or.old_fluor_energy.ne.fluor_energy
     &		.or.old_formvol.ne.formvol) first=.true.

	if(first) then
		k=0
		if(concentration.lt.0.0) then

			atomic_sym='   '

c			Isolate the atom from the kind of edge
			i=index(edge,' ')

c			Find position of edge atom in formula
			j=index(formula,edge(1:i-1))
                        if(j.eq.0) then
                                print *,'ERROR in sab_sub:'
                                        print *,'  absorbing atom needs to be in formula...'
                                print *,'  edge=',edge
                                print *,'  formula=',formula
                                stop
                        endif

c			Make sure the number of atoms stay in atomic_sym
1			if(a_number(formula(j+i+k-1:j+i+k-1))) then
				k=k+1
				goto 1
c				atomic_sym(1:i)=formula(j:j+i-1)
			else
				atomic_sym(1:i+k-1)=formula(j:j+i+k-2)
			endif
		else
       	         atomic_sym=edge(1:2)
	        endif

c		Clean up end of atomic_sym with blanks
		if(k.ne.0) then
			do j=i+k,FORMULA_LEN
				atomic_sym(j:j)=' '
			enddo
		else
			do j=3,FORMULA_LEN
				atomic_sym(j:j)=' '
			enddo
		endif

		fluor_abs=get_tot_abs(formula,fluor_energy,edge,formvol)

		old_formula=formula
		old_edge=edge
		old_fluor_energy=fluor_energy
		old_formvol=formvol
	endif

	
c	Correction needs the total absorption
	
	tot_abs=get_tot_abs(formula,energy,edge,formvol)
	r1=get_tot_abs(atomic_sym,energy,edge,formvol)
        r2=get_noedge_abs(atomic_sym,energy,edge,formvol)
	if(concentration.lt.0.0)then
		atomic_abs=r1-r2
	else
		atomic_abs=concentration*(r1-r2)
	endif

c	diagnostic check
        r3=get_tot_abs(atomic_sym,fluor_energy,edge,formvol)
	if((r3-r1)/r1.gt.0.03) then
		print *,'BIG TROUBLE, see sab_sub.F...'
		print *,'DIAG: energy,r1,r2,r3=',energy,r1,r2,r3
c		stop
	endif

	first=.false.
	return

	end
c********************************************************************************

