#include "exafs.hf"

	integer function exfile_out(filename,x,f1,f2,f3,
     &				nf,nx1,nx2,xi,dx,title,ntit)
c
c	Returns:
c
c		0	If filename is successfully output
c		1	If filename could not be output
c
c	Input parameters (see exfile_in for ones not listed):
c	
c	nx1:	Index of first point
c	nx2:	Index of last point
c
c	WARNING!!!!
c	This subroutine writes out an xafs data file to filename
c	regardless of whether it exists or not!  Precede by a
c	call to outfilename!
c
c	Last modifies: 5/10/95 CB
c************************************************************************

	character*TIT_LEN title(MAX_TIT),tit_temp
	character filename*(*)
	real x(MAX_NX),f1(MAX_NX),f2(MAX_NX),f3(MAX_NX)
	real dx,xi
	integer nf,nx,nx1,nx2,ntit,access

c	Does file exist?  If so, 
c	Does file have write permission?
	ierr=access(filename,' ')
	if(ierr.eq.0) then
		ierr=access(filename,'w')
		if(ierr.ne.0) then
			print *,'Filename does not have write access!!!'
			exfile_out=1
			return
		endif
	endif

	nx=nx2-nx1+1
c	open filename
	open(11,file=filename,form='unformatted',status='unknown')

c	Write out number of header lines
	write(11) ntit

c	Print a warning if too many header lines
	if (ntit.gt.MAX_TIT) then
		print *,'WARNING: too many header lines!'
		print *,' '
		print *,'This file contains ',ntit,' header lines.'
		print *,'All lines after MAX_TIT will be ignored.'
	endif

c	Read in those lines and spit them to the screen, or not spit
	if (itit.le.MAX_TIT) then
		write(11) (title(itit),itit=1,ntit)
c		write(6,*) (title(itit),itit=1,ntit)
	else
		write(11) (title(itit),itit=1,MAX_TIT)
c		write(6,*) (title(itit),itit=1,MAX_TIT)
		write(11) (tit_temp,itit=MAX_TIT+1, ntit)
		write(6,*) ('***HEADER LINE IGNORED ',tit_temp,itit=MAX_TIT+1,ntit)
	endif

c	Read in file info:
c		NF:	Code to determine number of columns and their meaning
c		NX:	Number of data lines
c		XI:	x of first data point
c		DX:	Difference in x of each data point

	write(11) nf,nx,xi,dx
c	print *,'NF,NX,XI,DX=',nf,nx,xi,dx
c	print *,' '

	if (nf.eq.11) then
		write(11) (x(i),f1(i),i=nx1,nx2)
	elseif (nf.eq.12) then
		write(11) (x(i),f1(i),f2(i),i=nx1,nx2)
	elseif (nf.eq.13) then
		write(13) (x(i),f1(i),f2(i),f3(i),i=nx1,nx2)
	elseif(nf.eq.1) then
		write(11) (f1(i),i=nx1,nx2)
	elseif(nf.eq.2) then
		write(11) (f1(i),f2(i),i=nx1,nx2)
	elseif(nf.eq.3) then
		write(11) (f1(i),f2(i),f3(i),i=nx1,nx2)
	else
		print *,'ERROR: exfile_out() EXAFS.a'
		stop'Sorry! exfile_in not equiped to handle this format.'
	endif

c	Close up shop!
	close(11)

	exfile_out=0
	return
	end
