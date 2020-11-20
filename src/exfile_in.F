#include "exafs.hf"

!	This file contains:
!		function exfile_in
!		function infile_type
!		function aexfile_in NOTE: aexfile_in is in its own separate file
!		aexfile_in.F under rsxap/source/EXAFS
!		function bexfile_in
!		function cexfile_in
!		function fexfile_in
!
!
!	Last modified:	5/10/95 CB
!	Last modified:	9/27/04 LD
!		-- add function infile_type to determine file type
!		-- break reading files into fuctions based on file type:
!			bexfile_in - read standard binary data
!			aexfile_in - read gnuplot-type ascii data
!	Last modified:	10/07/04 LD
!			cexfile_in - read chi.dat file
!			fexfile_in - read feffxxxx.dat file
!


!*****************************************************************************

      integer function exfile_in(filename, x,f1,f2,f3,nf,nx,xi,dx,title,ntit)
!
!	Returns:
!
!		0	if filename is successfully loaded
!		1	if filename does not exist or can't be read
!		2	if some other fatal error occured
!		3	a non-fatal error occurs: filename was loaded
!
!	Input parameters:
!
!	filename 	character string containing full path of input file
!
!	x		real array with x-axis data IF AVAILABLE (see nf)
!			CHANGE 8/21/7: fill up x(i)
!
!	f1,f2,f3	y-axis data to plot
!
!	nf 	Code to determine number of columns and their meaning
!			nf < 10 means get x from x=xi+dx * (i-1)
!			where i is data point index
!

      character*TIT_LEN title(*)
      !TIT_LEN set in exafs.hf
      character*(*) filename
      real x(*),f1(*),f2(*),f3(*)
      real amp(MAX_NX),phase(MAX_NX)
      real dx,xi,r_pair
      integer nf,nx,ntit,ftype,ierr,n_pair
      integer access,aexfile_in,bexfile_in,cexfile_in,fexfile_in,infile_type


      ierr=access(filename,'r')
      !test if filename is accessable in read mode. Returns 0 if accessable,
      !otherwise it returns error and quits
      if(ierr.ne.0) then
         ierr=access(filename,' ') ! Test for existence
         if(ierr.ne.0) then ! used to be .eq.1 which worked in g77, but not
			    ! gfortran. Thanks Alison Pugmire!
                exfile_in=1 ! File does not exist
                print *,'ERROR in exfile_in:',filename,
     &                  ' does not exist!'
         else
                exfile_in=2 ! File exists, but doesn't have read permission
                print *,'ERROR in exfile_in: User does not have read '
     &                  //'permission for file ',filename,'!'
         endif
         !returns !=0 to the calling program. filename does not exist or can not
         !be read
         return
      endif
      !if filename not accessable set exfile_in to 1, print error and exit

!Call function to determine file type
      ierr=infile_type(filename, ftype)
      !input filename and get out ftype

!Read in the appropriate file type
      if (ftype.eq.0) then       !standard binary file
         ierr=bexfile_in(filename,x,f1,f2,f3,nf,nx,xi,dx,title,ntit)

      elseif (ftype.eq.1) then   !"gnu"-type ascii file
         ierr=aexfile_in(filename,x,f1,f2,f3,nf,nx,xi,dx,title,ntit)

      elseif (ftype.eq.2) then   !	chi.dat file
      !Chi.dat files not normalized n_pair = 1;  run chi2bin to set n_pair
         n_pair=1
         ierr=cexfile_in(filename,x,f1,f2,f3,amp,phase,
     &         n_pair,r_pair,nf,nx,xi,dx,title,ntit)

      elseif (ftype.eq.3) then      !	feffxxxx.dat file
         ierr=fexfile_in(filename,x,f1,f2,f3,nf,nx,xi,dx,title,ntit)
      endif

!Now fill x(i) if necessary
      if(nf.le.10) then
         do i=1,nx
            x(i)=xi+dx*float(i-1)
         enddo
      endif

      exfile_in=ierr
      return
      end
!*******************************************************************************

      integer function infile_type(filename, ftype)
!
!	Returns:
!		0	if filename is successfully loaded
!		1	if filename does not exist or can''t be read
!		2	if some other fatal error occured
!		3	a non-fatal error occurs: filename was loaded
!
!	Values for ftype:
!		0	if filename is binary format
!		1	if filename is "gnu"-type ascii format
!		2	if filename is chi.dat format
!		3	if filename is Feffxxxx.dat format
!
!

      character*(*) filename
      !automatically sets variable filename to length of string passed to
      !infile_type function
      character testchar,testline*TIT_LEN
      !TIT_LEN set in exafs.hf
      integer ierr, ftype, read_feff_header

      !These variables needed for read_feff_header; they are NOT used here.
      character*TIT_LEN title(MAX_TIT)
      character feff_ver*1
      integer ntit
      real r_pair

      ierr=0
      !initiates error code returned by infile_type function to 'successfully
      !loaded'

      open(11,file=filename,form='formatted',status='old')
      !uses open to set file 'filename' to fileRef#11. The file is opened as if
      !it was formatted (ASCII, not binary) and assumed to exist (old)

      read(11,'(a)',err=666,end=666) testline	! err likely due to binary file
      !from fileRef#11 read first line and store in 'testline'
666   testchar = testline(1:1)
      !read first character from 'testline'

!Start tests for various file types
!*******************************************************************************

      !Does the first line contain "Feff"? Is the first character legal (4/25/6)
      if ( (index(testline,'Feff').ne.0.or.index(testline,'FEFF').ne.0)
     &	    .and.ichar(testchar).ge.32.and.
     &      ichar(testchar).ne.127) then
      !test for three conditions, all must be true:
         !(1)'Feff' found within 'testline'. NOTE index() will return 0 if
         !'Feff' is not within 'testline'
         !(2)the first character has an ascii code >= 32 not control codes
         !(spaces, alpha-numeric and other text characters). NOTE ichar()
         !returns the ascii code for a specific character
         !(3)the first character is not the ascii code for DEL (also an ascii
         !control code)

         ierr=read_feff_header(title,ntit,feff_ver,r_pair)
         !calls function read_feff_header() to check if it is a chi.dat file or
         !a Feffxxx.dat file

         backspace(11)
         !back-up 1 line
         read(11,'(a)') testline

         if (index(testline,'chi').ne.0) then
            ftype=2
            !if 'chi' found on line, then chi.dat
         else
            ftype=3
            !else feff.dat
         endif
      !*************************************************************************

      elseif (testchar.eq.'#') then
      !test for a "gnu"-type text file
         ftype=1
         !ftype=1 if filename is "gnu"-type ascii format
      !*************************************************************************

      else
         ftype=0
         !Assume it is binary
      endif

      infile_type=ierr
      !assigns infile_type to ierr since this subroutine calls
      !read_feff_header() and read_feff_header() might fail at opening the file.
      !This allows the calling subroutine to know and return an error code to
      !the program which is calling it
      close(11)
      !closes FileRef#11
      return
      end

!beginning of various filetype reading subroutines/functions
!*****************************************************************************
      integer function bexfile_in(filename,x,f1,f2,f3,nf,nx,xi,dx,title,ntit)

!	This function reads in a standard binary data file.
!
!	Returns:
!
!		0	if filename is successfully loaded
!		1	if filename does not exist or can''t be read
!		2	if some other fatal error occured
!		3	a non-fatal error occurs: filename was loaded
!
!	Output parameters:
!
!	filename 	character string with full path
!	x		real array with x-axis data IF AVAILABLE (see nf)
!	f1,f2,f3	y-axis data to plot
!	nf 		Code to determine number of columns and their meaning
!			nf < 10 means get x from x=xi+dx * (i-1)
!
!	Last modified:  9/27/04 LD
!		-- moved to separate function from exfile_in


      character*TIT_LEN title(*),tit_temp
      character*(*) filename
      character testchar
   	real x(*),f1(*),f2(*),f3(*), rjunk(20)
   	real dx,xi
      integer nf,nx,ntit,ierr

      ierr=0
      !initiates error code returned by bexfile_in function to 'successfully
      !loaded'

      open(11,file=filename,form='unformatted',status='old')
      !open filename and give it FileRef#11 assuming that it is 'unformatted'
      !i.e. a binary file

      read(11) ntit
      !Read in number of header lines

      if (ntit.gt.MAX_TIT) then
         print *,'WARNING: too many header lines!'
         print *,' '
         print *,'This file contains ',ntit,' header lines.'
         print *,'All lines after MAX_TIT will be ignored.'
         ierr=3
      endif
      !Print a warning if too many header lines

      !Read in those lines and spit them to the screen
      if (ntit.le.MAX_TIT) then
         read(11) (title(itit),itit=1,ntit)
         !write(6,*) (title(itit),itit=1,ntit)
      else
         read(11) (title(itit),itit=1,MAX_TIT)
         write(6,*) (title(itit),itit=1,MAX_TIT)
         !writing to 6 cooresponds ot standard-out (terminal screen)
         read(11) (tit_temp,itit=MAX_TIT+1, ntit)
         write(6,*) ('***LINE IGNORED ',tit_temp,itit=MAX_TIT+1,ntit)
         !writing to 6 cooresponds ot standard-out (terminal screen)
      endif

!	Read in file info:
!		NF:	Code to determine number of columns and their meaning
!		NX:	Number of data lines
!		XI:	x of first data point
!		DX:	Difference in x of each data point

      read(11) nf,nx,xi,dx
      !the next line after the header contains these four parameters which
      !define how the data is stored

      !print *,'NF,NX,XI,DX=',nf,nx,xi,dx
      !print *,' '

      if (nf.eq.11) then
         read(11) (x(i),f1(i),i=1,nx)
         !if nf=11 then the data is stored as:
         !x-values, yvalues
      elseif (nf.eq.12) then
         read(11) (x(i),f1(i),f2(i),i=1,nx)
         !if nf=12 then the data is stored as:
         !x-values, y1-values, y2-values
      elseif (nf.eq.13) then
         read(11) (x(i),f1(i),f2(i),f3(i),i=1,nx)
         !if nf=13 then the data is stored as:
         !x-values, y1-values, y2-values, y3-values
      elseif(nf.eq.1) then
         read(11) (f1(i),i=1,nx)
         !if nf=1 then the data is stored as:
         !y-values
      elseif(nf.eq.2) then
         read(11) (f1(i),f2(i),i=1,nx)
         !if nf=2 then the data is stored as:
         !y1-values, y2-values
      elseif(nf.eq.3) then
         read(11) (f1(i),f2(i),f3(i),i=1,nx)
         !if nf=3 then the data is stored as:
         !y1-values, y2-values, y3-values
      else
         print *,'ERROR: bexfile_in() EXAFS.a'
         print *,'Sorry! bexfile_in not equiped to handle this format.'
         bexfile_in=2
         close(11)
         return
         !print error, set bexfile_in to 2 (notifying the calling program that
         !an error occured in attempting to read the data) and exit
      endif
      close(11)
      !Close up shop!

      bexfile_in=ierr
      !sets bexfile_in to an error code unless everything opens correctly (then
      !it stays as initiated to 0). This notifies the calling program whether or
      !not an error has occured
      return
      end

!*****************************************************************************

      integer function cexfile_in(filename, k,f1,f2,f3,amp,phase,
     &      n_pair,r_pair,nf,nx,xi,dx,title,ntit)

!	This function reads in a chi.dat file, and outputs:
!		k  - the x-axis data,
!		f1 - the real part of chi,
!		f2 - the imaginary part of chi,
!		amp, phase - for plotting in program chi2bin
!
!	Returns:
!
!		0	if filename is successfully loaded
!		1	if filename does not exist or can''t be read
!		2	if some other fatal error occured
!		3	a non-fatal error occurs: filename was loaded
!
!	Output parameters:
!
!	filename 	character string with full path
!	k     		real array with x-axis data IF AVAILABLE (see nf)
!	f1,f2,f3 	y-axis data to plot
!	nf 	   	Code to determine number of columns and their meaning
!		      	nf < 10 means get x from x=xi+dx * (i-1)
!	n_pair		normalization factor
!

      character*TIT_LEN title(*),tit_temp
      character*(*) filename
      character feff_ver*1
      real k(*),f1(*),f2(*),f3(*)
      real chi(MAX_NX),amp(*),phase(*)
      real dx,xi,r_pair
      integer nf,nx,ntit,ierr,n_pair,read_feff_header

      ierr=0
      !initiates error code returned by bexfile_in function to 'successfully
      !loaded'

      open(11,file=filename,form='formatted',status='old')
      !open filename as a formatted file (i.e. ascii file)

      ierr=read_feff_header(title,ntit,feff_ver,r_pair)
      !calls read_feff_header() which is located in the file read_feff_header.F
      !to read all the header lines from the feff file and stop at the point
      !when the data starts. read_feff_header() returns an error code if there
      !is a problem with reading the file

      i=1
      !initiate counter to 1 for first line
2     read(11,*,end=3) k(i),chi(i),amp(i),phase(i)
      if(k(i).ge.0.0) i=i+1
      goto 2
      !loops through all the data placing values in the proper column array.

!		NF:	Code to determine number of columns and their meaning
!		NX:	Number of data lines
!		XI:	x of first data point
!		DX:	Difference in x of each data point

3     nf=2
      !if nf=2 then the data is stored as:
      !y1-values, y2-values
      nx=i-1
      !total number of data lines (we overcount by one in loop 2 above)
      xi=k(1)
      !the first x-value data point

      dx=k(6)-k(5)
      dx2=k(nx)-k(nx-1)
      dx2=abs(dx2-dx)
      if(dx2.gt.0.00001)then
		print *,'Error: cexfile_in -- check dx of chi.dat-formatted'
		print *,'file: ',filename(1:70)
		stop
      endif
      !takes the difference between the 5th and 6th x-values and compairs it to
      !the difference between second to last and last data values. Tests for
      !difference in the dx step greater than 0.00001 and if found prints an
      !error

      !This is for version Feff3 and any other versions that are "undetectable"
      !(Now assumes Feff 5 or later version for "undetectable")
      if (feff_ver.eq.'3') then
         read(title(4)(6:17),*)r_pair
         do i=1,nx
            phase(i)=phase(i)+2.0*k(i)*r_pair
         enddo
      endif

      do i=1,nx
         f1(i)=k(i)*chi(i)/float(n_pair)
         !data in f1() is printed as k*chi
         f2(i)=-k(i)*amp(i)/float(n_pair)*cos(phase(i))
         !data in f2() is printed as k*amp/cos(phase)
         amp(i)=k(i)*amp(i)*r_pair**2.0/real(n_pair)
         !data in amp() is printed as k*amp*r_pair^2
         phase(i)=phase(i)-2.0*k(i)*r_pair	! Isolate phi in the EXAFS eq
      enddo

      !Close up shop!
      close(11)

      cexfile_in=ierr
      !sets cexfile_in to an error code unless everything opens correctly (then
      !it stays as initiated to 0). This notifies the calling program whether or
      !not an error has occured
      return
      end

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!Clean up to here YJH
!*****************************************************************************

      integer function fexfile_in(filename,k,f1,f2,f3,nf,nx,xi,dx,title,ntit)

!This function reads in a feffxxxx.dat file, and outputs:
!		k  - the x-axis data,
!		f1 - the real part of chi (calculated),
!		f2 - the imaginary part of chi (caluclated),

!	WARNING: May not work with Feff versions older than 5,  phase may be
!		defined differently - check output

!	Returns:
!
!		0	if filename is successfully loaded
!		1	if filename does not exist or can''t be read
!		2	if some other fatal error occured
!		3	a non-fatal error occurs: filename was loaded
!
!	Output parameters:
!
!	filename 	character string with full path
!	x     		real array with x-axis data IF AVAILABLE (see nf)
!	f1,f2,f3	   y-axis data to plot
!	nf 		   Code to determine number of columns and their meaning
!			      nf < 10 means get x from x=xi+dx * (i-1)
!

      character*TIT_LEN title(*),tit_temp
      character*(*) filename
      character feff_ver*1
      character*FILENAME_LEN outfile
      real k(*),f1(*),f2(*),f3(*)
      !data arrays to be read from file
      real kx(MAX_NX),phic(MAX_NX),mag(MAX_NX),phase(MAX_NX),redfact(MAX_NX)
   	real lambda(MAX_NX),realp(MAX_NX),chi(MAX_NX),amp(MAX_NX)
      real dx,xi,r_pair,xmax,phase_new(MAX_NX)
      !second derivatives for spline routine
   	real y2phic(MAX_NX),y2mag(MAX_NX),y2phase(MAX_NX)
   	real y2redfact(MAX_NX),y2lambda(MAX_NX)
      !interpolated values
   	real phic_interp,mag_interp,phase_interp,redfact_interp,lambda_interp
      integer nf,nx,new_nx,ntit,ierr,n_pair,read_feff_header

      ierr=0
      open(11,file=filename,form='formatted',status='old')
      !open filename

      ierr=read_feff_header(title,ntit,feff_ver,r_pair)
      !calls read_feff_header() which is located in the file read_feff_header.F
      !to read all the header lines from the feff file and stop at the point
      !when the data starts. read_feff_header() returns an error code if there
      !is a problem with reading the file

      i=1
2     read(11,*,end=3) kx(i),phic(i),mag(i),phase(i),redfact(i),
     &      lambda(i),realp(i)
      !if(k(i).ge.0.0) i=i+1
      i=i+1
      goto 2
      !loops through all the data placing values in the proper column array.

3     nf=12
      !if nf=12 then the data is stored as:
      !x-values, y1-values, y2-values
      nx=i-1
      !total number of data lines (we overcount by one in loop 2 above)
      xi=kx(1)
      !the first x-value data point
      xmax=kx(nx)
      !the last x-value data point
      dx=0.04999
      new_nx=int((xmax-xi)/dx+0.5)+1
      !calculating a new number of data lines to be one more than the previous
      !nx value. Is this right? and if so why didn't you just leave 
      !nx = 1 above? Also WHY are you doing this?

! This is for version Feff3 and any other versions that are "undetectable"

!!        if (feff_ver.eq.'3') then
!!                read(title(4)(6:17),*)r_pair
!!                do i=1,nx
!!                        phase(i)=phase(i)+2.0*k(i)*r_pair
!!                enddo
!!        endif


!	N_pair set to 1, data in feffxxxx.dat files may already be normalized,
! 	   need to check for same output from feffxxxx.dat and chi.dat files
      n_pair=1

      !Spline the data
      call spline(kx,phic,nx,0.0,0.0,y2phic)
      call spline(kx,mag,nx,0.0,0.0,y2mag)
      call spline(kx,phase,nx,0.0,0.0,y2phase)
      call spline(kx,redfact,nx,0.0,0.0,y2redfact)
      call spline(kx,lambda,nx,0.0,0.0,y2lambda)

      do i=1,new_nx
         k(i)=xi+(i-1)*dx
         !Spline interpolate
         call splint(kx,phic,y2phic,nx,k(i),phic_interp)
         call splint(kx,mag,y2mag,nx,k(i),mag_interp)
         call splint(kx,phase,y2phase,nx,k(i),phase_interp)
         call splint(kx,redfact,y2redfact,nx,k(i),redfact_interp)
         call splint(kx,lambda,y2lambda,nx,k(i),lambda_interp)

         phase_new(i)=phase_interp+phic_interp+2*k(i)*r_pair

         if (k(i).ne.0.0) then
            amp(i) = (mag_interp*float(n_pair)/(k(i)*r_pair**2))*
     &            redfact_interp*exp(-2*r_pair/lambda_interp)
         else
            amp(i) = 0.0
         endif

         chi(i) = amp(i)*sin(phase_new(i))

         f1(i)=k(i)*chi(i)/float(n_pair)
         f2(i)=-k(i)*amp(i)/float(n_pair)*cos(phase_new(i))

         !amp(i)=k(i)*amp(i)*r_pair**2.0/real(n_pair)
         !phase_new(i)=phase_new(i)-2.0*k(i)*r_pair
      enddo

      nx=new_nx
      !Close up shop!
      close(11)

      fexfile_in=ierr
      !sets fexfile_in to an error code unless everything opens correctly (then
      !it stays as initiated to 0). This notifies the calling program whether or
      !not an error has occured
      return
      end
