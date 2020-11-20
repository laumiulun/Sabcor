#include "exafs.hf"
#define MAXASCII 3000

      integer function aexfile_in(filename,x,f1,f2,f3,nf,nx,xi,dx,title,ntit)
!
!  Reads a gnuplot-like ascii data file in, mimicking exfile_in.
!  Returns:
!
!		0	if filename is opened and read in successfully
!		1	if filename does not exist
!		2	some other error occured
!
!	Last modified:
!		8/26/99 CB
!		5/26/00 CB	Made some improvements to reading out headers
!		6/30/03 CB	ported from amultichan_in to be more
!				"exfile_in"-like
!		8/21/08 CB	minor bug, filename needs to be declared *(*)
!*****************************************************************************

      character title(MAX_TIT)*TIT_LEN,tit_temp*TIT_LEN
      character filename*(*)
      character char2*2
      character ascii_line*MAXASCII
	   real x(*),f1(*),f2(*),f3(*)
	   real dx,xi
      integer nf,nx,ntit,field_nums
      integer ierr, access

      ierr=access(filename,'r')
      !Check if file exists.  If not, return with error code=1
      if(ierr.ne.0) then
	 print *,'File no moa in aexfile_in ierr=', ierr,filename
         aexfile_in=1
         return
      endif
      !tests to see if ierr !=0, if so then aexfile_in returns 1 which notifies
      !the calling program that an error occured in reading the file

      open(11,file=filename,status='old')
      !open filename

      !Read in number of header lines.
      ntit=0
      !initiate number of title lines 'ntit' to 0
      read(11,1002,err=666,end=666)ascii_line
1002  format(a MAXASCII)
      !read from FileRef#11 and put the data into 'ascii_line. If there is an
      !error then abort to line 666
      char2=ascii_line(1:2)
      !char2 is '# ' for gnu files, ending the header with '# -'
      do while (char2(1:1).eq.'#')
      !while the first character of the line is a hash continue to loop
         ntit=ntit+1
         !increment number of title lines
         title(ntit)=ascii_line(3:TIT_LEN)
         !remove the hash mark and put the line into the title() array
         read(11,1002,err=666,end=666)ascii_line
         !read the next line of the file into the variable 'ascii_line'
         char2=ascii_line(1:2)
         !redefine char2 to be the first two characters of the new 'ascii_line'

         !title(ntit)=ascii_line(3:TIT_LEN)
         !print *,ascii_line(1:70)
         !print *,char2,title(ntit)
      enddo

      if(ntit.lt.0) then	! This should never happen
         print *,'ERROR in aexfile_in:  Header is not of proper format!!'
         print *,'Header lines must be at the beginning of the file and'
         print *,'be preceeded by a ''#''.  Data then must follow in'
         print *,'Tab or space delimited columns, x, y1, y2, y3, etc.'

         aexfile_in=2
         return
      endif

      if (ntit.gt.MAX_TIT) then
         print *,'WARNING: too many header lines!'
         print *,' '
         print *,'This file contains ',ntit,' header lines.'
         print *,'All lines after MAX_TIT will be ignored.'
	ntit=MAX_TIT
      endif
      !Print a warning if too many header lines

!	Read in data.  Afterwords, set the file info:
!		NF:	Code to determine number of columns and their meaning
!		NX:	Number of data lines
!		XI:	x of first data point
!		DX:	Difference in x of each data point

!	Determine number of columns

      field_nums=num_fields(ascii_line)
      nf=10+field_nums-1
      !HAYES AND BOYCE: SCREW YOU AND YOUR nf CODES!

      !Get first data point from ascii_line
      index=1
      if(field_nums.eq.2) then
         read(ascii_line,*,err=666) x(index),f1(index)
      elseif(field_nums.eq.3) then
         read(ascii_line,*,err=666) x(index),f1(index),f2(index)
      elseif(field_nums.eq.4) then
         read(ascii_line,*,err=666) x(index),f1(index),f2(index),f3(index)
      else
	 print *,'WARNING: more than 4 columns of data.  5th column and'
         print *,'beyond are ignored!! field_nums=',field_nums
         read(ascii_line,*,err=666) x(index),f1(index),f2(index),f3(index)
      endif

      !Read in the rest of the data!
1     index=index+1
      if(field_nums.eq.2) then
         read(11,*,end=2) x(index),f1(index)
      elseif(field_nums.eq.3) then
         read(11,*,end=2) x(index),f1(index),f2(index)
      elseif(field_nums.eq.4) then
         read(11,*,end=2) x(index),f1(index),f2(index),f3(index)
      else
         !print *,'WARNING: more than 4 columns of data.  5th column and'
         !print *,'beyond are ignored!! field_nums=',field_nums
         read(11,*,end=2) x(index),f1(index),f2(index),f3(index)
      endif
      goto 1

2     nx=index-1
      !the final value for nx overcounts by 1
      xi=0.0	! set to zero for cleanliness
      dx=0.0

      !Close up shop!
      close(11)

      aexfile_in=0
      !sets aexfile_in to 0 which informs the calling program that the data was
      !properly read in
	!print *,'DEBUG in aexfile_in: gettin out!',nf
      return

666   print *,'ERROR in aexfile_in: reading file... is file binary?'
      aexfile_in=2
      !sets aexfile_in to 2 which informs the calling program that an error
      !occured when attempting to read in data
      return
      end
