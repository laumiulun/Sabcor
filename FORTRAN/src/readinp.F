#include "exafs.hf"
#define INP_FILENAME_LEN 20
#define MAX_SYMS 20
#define AVOGADRO 6.02252e23

c********************************************************************************
c********************************************************************************
	integer function readinp(inp_filename,d,phi,theta,formvol,formula,edge,
     &		fluor_energy,concentration)
c
c	Reads input directions from inp_filename.  Input is in the form of
c	"cards" with information following the cards.  Allowed cards are:
c
c		THICKNESS, PHI, ABC, FORMULA, EDGE, FLUOR_ENERGY,
c		CONCENTRATION
c
c	Formats:
c
c	THICKNESS d
c
c		d is the thickness of the sample in Angstroms.
c
c	PHI phi
c
c		phi is the angle of the face of the sample with respect to
c		the beam
c
c	THETA theta
c
c		theta is the angle of the face of the sample with respect to
c		the fluorescence
c
c	ABC a b c
c
c		a, b, and c are the lattice parameters.
c
c	VOLUME vol
c
c		a=vol**0.333, b=a,c=a
c
c	FORMULA formula_string
c
c		The string should look like YBa2Cu3O7.  Capital letters will be
c		taken as the first letter in a symbol.  Numbers seceding the symbol
c		should be immediately after the symbol.  The number for a symbol
c		should be the number of atoms of that type IN THE UNIT CELL.
c		For instance, in NiO, there are four formula units per unit
c		cell, so FORMULA Ni4O4 is correct.  These numbers must be integers!
c
c	EDGE edge_string
c
c		Something like Kr LIII.
c
c	CONVERSION conversion
c
c		use if the edge is from a substituted atom in the material.
c		"conversion" is the fraction of the material verses a single
c		atom in the unit cell.  For instance, if half the copper in YBCO
c		is replaced with Ni, then CONVERSION 1.5 would work, with a
c		FORMULA YBa2Cu3O7 and EDGE Ni K.
c
c********************************************************************************
	character*INP_FILENAME_LEN inp_filename
	character*FORMULA_LEN formula
	character*EDGE_LEN edge
	character*80 ascii_line
	real formvol,concentration,phi,theta,d,fluor_energy
	integer access,ierr
	logical check_edge_string

c	If no concentration is specified, then give negative concentration as a flag
c
	concentration=-1.0
c	Check that file exists
c
	ierr = access(inp_filename,'r')
	if(ierr.ne.0) then
		write(6,1000) inp_filename
1000		format('File does not exist: ',a15)
		goto 100
	endif

c	Open the file
c
	open(1,file=inp_filename,status='old')

c	Default is theta=90-phi, indicated by theta<-1000
	theta=-10000.0 ! So this is only altered if THETA card is included
c	Begin loop searching for cards
c
1	read(1,'(a80)',end=2) ascii_line
	if(ascii_line(1:10).eq.'THICKNESS ') then
		read(ascii_line(11:80),*) d
	elseif(ascii_line(1:4).eq.'PHI ') then
		read(ascii_line(5:80),*) phi
	elseif(ascii_line(1:6).eq.'THETA ') then
		read(ascii_line(7:80),*) theta
	elseif(ascii_line(1:4).eq.'ABC ') then
		read(ascii_line(5:80),*) a,b,c
	elseif(ascii_line(1:7).eq.'VOLUME ') then
		read(ascii_line(8:80),*) formvol
	elseif(ascii_line(1:8).eq.'FORMULA ') then
		read(ascii_line(9:80),*) formula
	elseif(ascii_line(1:5).eq.'EDGE ') then
		read(ascii_line(6:80),'(a7)') edge !fixed so it doesn't
	elseif(ascii_line(1:6).eq.'FLUOR ') then !cpip  LIII edges, DTO
		read(ascii_line(7:80),*) fluor_energy
	elseif(ascii_line(1:14).eq.'CONCENTRATION ') then
		read(ascii_line(15:80),*) concentration
	endif
	goto 1

2	close(1)
	if(check_edge_string(edge)) then
		continue
	else
		print *,'Trouble with edge string.'
		call exit(0)
	endif

100	readinp=ierr
	return
	end

