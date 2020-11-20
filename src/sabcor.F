#include "exafs.hf"
#include "sabcor.hf"

	program sab_cor

!	Program to correct for the self-absorption effect in fluorescence
!	XAFS data.  The program requires the following input to work (see
!	sab.inp for an example):
!
!		d:		sample thickness (angstroms)
!		phi:		angle of sample w.r.t. beam (degrees)
!		theta:		angle of sample w.r.t. fluorescence (degrees)
!		formvol:	volume occupied by a formula unit (angstroms^3)
!		formula:	chemical formula (eg. YBa2Cu3O7)
!		edge:		the edge atom and edge type (eg. Kr LIII)
!
!	Correction uses formulae from Booth & Bridges, 
!	http://xxx.lanl.gov/cond-mat/0306252, Physica Scripta T115, 202 (2005).
!	YOU MUST cite this article, or its in-print version from 
!	XAFS XII (in press) if you use this correction.
!
!
!	9/13/94	Corwin Booth, inception
!	6/30/3		Restored this stand-alone version, including reading
!			ascii files, repairing a bug in corr_chi, changing
!			input to require FORMVOL instead of ABC, other stuff
!	7/7/3	1.01	finalized prep for 1st release
!	4/28/4	1.02	added header to sab_cor.dat
!	10/13/5	1.03	removed approximation in fluor_corr that is mentioned 
!			in the paper above
!       9/6/7   CB      Imported into svn
!	8/5/13	1.04	No change to the main code except in the libraries. 
!			mucal_mod in particular had a BIG bug that gave bad
!			corrections for L3 edges.
!	8/15/13	1.05	Added sabcor.hf so definitions could be properly shared.
!			This fixed a bug in a bad version reported in the
!			corrected output.
!	12/11/17 1.06	Added theta
!	12/13/17 1.07	Fixed some minor bugs
!------------------------------------------------------------------------------

	integer nf,nx,ntit,ierr,in_len,idat
	integer readinp,Z,edge_code, access,exfile_in,exfile_out
	integer aexfile_in,aexfile_out
	real d, phi,theta,formvol
	real fluor_energy,concentration,e_not,phi_rad,theta_rad
	real tot_abs,fluor_abs
	real atomic_abs,energy,chi,corr_chi,correction
	real info_depth
	character*FILENAME_LEN in_datafile, out_datafile
	character*2 file_type
	character*FORMULA_LEN formula
	character*EDGE_LEN edge
	character*INP_FILENAME_LEN inp_filename
	character*6 tempstring

	character*TIT_LEN title(MAX_TIT)
	real k(MAX_NX),kchi_r(MAX_NX),kchi_i(MAX_NX)
	real dummy(MAX_NX)
	real dx,xi

	logical file_ascii, format_ascii


	print *,'Welcome to '//VERSION//'.'

c	First lets read in an input file that gives the above information
c	and spit out the total absorption coefficient at the edge of interest.
c
	inp_filename='sab.inp'
	ierr=readinp(inp_filename,d,phi,theta,formvol,formula,edge,fluor_energy,
     &		concentration)
	if(ierr.gt.0) then
		print *,'ERROR: sab_cor reports error from readinp.  ierr=',ierr
		call exit(0)
	endif

c	Get filename and read in the data file
c
1	call getexfilename(in_datafile,file_type)

c	If file_type is r-space,e-space, or d-sapce, assume is not ks and bail
c
	if (file_type.eq.'ds'.or.file_type.eq.'es'.or.file_type.eq.'rs') then
		print *,'ERROR in sab_cor: Unsupported filetype ',file_type
		stop
	endif
	file_type='ks'

c	Read in file after determining file format
	format_ascii=file_ascii(30,in_datafile)	! unit=30

	if(format_ascii) then
		ierr=aexfile_in(in_datafile,k,kchi_r,kchi_i,dummy,
     &			nf,nx,xi,dx,title,ntit)
	else
		ierr=exfile_in(in_datafile,k,kchi_r,kchi_i,dummy,
     &			nf,nx,xi,dx,title,ntit)
	endif

c	print *,'Got the inputfile...'
c	Now build the output filename
c
	in_len=index(in_datafile,' ')
c	is there an extension?
	idot=in_len
	do while((in_datafile(idot:idot).ne.'.').and.idot.ge.1)
		idot=idot-1
	enddo
	if(idot.eq.0) then
		out_datafile=in_datafile(1:in_len-1)//'_sac'
	else
		out_datafile=in_datafile(1:idot-1)//'_sac'
     &			//in_datafile(idot:in_len-1)
	endif

c	make the correction!
c	write(6,*) 'calling fluor_corr...'
	call fluor_corr(k,kchi_r,kchi_i,nf,nx,title,ntit,
     &			d,phi,theta,formvol,formula,edge,fluor_energy,
     &			concentration,
     &			'a',' ')
		
	write(6,'(a)') 'writing out file '//out_datafile(1:62)
	if(format_ascii) then
		ierr=aexfile_out(out_datafile,k,kchi_r,kchi_i,dummy,
     &			nf,1,nx,xi,dx,title,ntit,file_type)
	else
		ierr=exfile_out(out_datafile,k,kchi_r,kchi_i,dummy,
     &			nf,1,nx,xi,dx,title,ntit)
	endif

	end


