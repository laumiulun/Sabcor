#include "exafs.hf"

!*****************************************************************************

      integer function read_feff_header(title, ntit,feff_ver,r_pair)

      character*TIT_LEN title(*),temp
      character feff_ver*1

      integer nleg, iver, i, it, ntit
      real r_pair,l
      logical feff_file

      rewind(11)
      !rewinds fileRef#11 back to the beginning
      read(11,'(a80)') title(1)
      !read fileRef#11 alpha-numeric with 80 characters (a80) into title(1),
      !the first position in the 'title' array

      iver=index(title(1),'Feff ')
	if(iver.eq.0) iver=index(title(1),'FEFF ')
      !find the position where 'Feff ' starts in title(1)

	if(iver.eq.0) then
		print *,'ERROR in read_feff_header'
		write(6,*)'Read in file generated by ',title(1)(iver:iver+11)
         	write(6,*)'WARNING: version not supported, check output...'
         	write(6,*)'Specifically, the phase may be defined differently.'
         	write(6,*)''
         	write(6,*)'Assuming Feff 5 or later version.'
!                feff_ver='3'
!                goto 2000
	else
      if(title(1)(iver:iver+5).ne.'Feff 5'.and.
     &   title(1)(iver:iver+11).ne.'Feff XXa6.10'.and.
     &   title(1)(iver:iver+9).ne.'Feff  7.00'.and.
     &   title(1)(iver:iver+9).ne.'Feff  7.01'.and.
     &   title(1)(iver:iver+9).ne.'Feff  7.02'.and.
     &   title(1)(iver:iver+8).ne.'Feff 8.10'.and.
     &   title(1)(iver:iver+9).ne.'FEFF 9.6.4'.and.
     &   title(1)(iver:iver+7).ne.'FEFF 10.'.and.
     &   title(1)(iver:iver+6).ne.'Feff  6') then
      !check the input file, feff3 ,feff5, feff6 feff7, feff7.01, feff7.02,
      !feff8.x16
         write(6,*)'Read in file generated by ',title(1)(iver:iver+11)
         write(6,*)'WARNING: version not supported, check output...'
         write(6,*)'Specifically, the phase may be defined differently.'
         write(6,*)''
         write(6,*)'Assuming Feff 5 or later version.'
!                feff_ver='3'
!                goto 2000
      endif
      endif
      !if input file version not found print error and assume Feff 5 or later

!     This is for version 5,6,6X, 7, 7.01, 7.02 8.x16,9.6.4,10.0.1
      feff_ver='5'

!     Read in the first potential lines
      read(11,'(a80)') title(2)
      read(11,'(a80)') title(3)

      !Find and read in the paths lines
      do while((index(temp,'file').eq.0.or.index(temp,'sig2').eq.0)
     &   .and.index(temp,'Path').eq.0)
         !test for two conditions , all must false to exit loop
            !(1)'temp' does not contain the word 'file' or 'sig2'
            !(2)'temp' does not contain the word 'Path'
         read(11,'(a80)') temp
         !read in next line from fileRef#11
      enddo

      !I don't understand the purpose of the above block YJH
      ! Answer: just reads in paths that are used for inclusion in the header
	! CHB

      title(4)=temp

      feff_file = .FALSE.
      !Assume we have chi.dat file

      if (index(temp,'Path').ne.0) then
         ntit = 4
         feff_file = .TRUE.
!		   goto 4000
      endif
      !If 'Path' found, then must be feffxxxx.dat file (rather than chi.dat)

      !This is for chi.dat files
      if (.not.feff_file) then
         read(11,'(a80)') temp
         read(temp(2:),*) temp1,temp2,temp3,temp4,temp5,r_pair
         title(5)=temp
         it=6
         read(11,'(a80)') temp

         do while(index(temp,'paths used').eq.0)
            title(it)=temp
            !save the header lines being looped through into the title array
            read(11,'(a80)') temp
            if(it.lt.40) then
               it=it+1
            endif
            !increment 'it' if the number of header lines is less than 40 (it
            !starts at 6)
         enddo
         !continue looping through header until you find a line with 'paths
         !used' on it. This is one line before '------' in chi.dat files
         if(it.eq.30) then
            ntit=it
         else
            ntit=it-1
         endif
      endif
      !The read position for fileRef#11 is now two lines above the start of data
      !in chi.dat type files


!2000    if (feff_ver.eq.'3') then
!! This is for version Feff3 and any other versions that are "undetectable"
!              ntit=5
!              write(6,*)'Read in chi.dat generated by ',title(1)(iver:iver+11)
!              write(6,*)'WARNING: version not supported, check output...'
!              do i=2,ntit
!              		read(11,'(a)')title(i)
!                       write(6,*)title(i)
!              enddo
!              read(11,'(a)')temp
!        endif

!       Wind off to the data
4000  do while(index(temp,'------').eq.0)
         read(11,'(a80)')temp
         !read next line of fileRef#11 and store in temp
         if (feff_file) then
            ntit=ntit+1
            title(ntit)=temp
         endif
         !if this is a Feffxxx.dat file then save the header lines being looped
         !through into the title array and increment 'ntit'
      end do
      !continue looping through header until you find a line '------'

      read(11,'(a80)')temp
      !read next line of fileRef#11 after the line '------'
      if (feff_file) then
         ntit=ntit+1
         title(ntit)=temp
      endif
      !if this is a Feffxxx.dat file then save the header lines being looped
      !through into the title array and increment 'ntit'

      nleg=0

      !Check if Feffxxxx.dat type file
      if (index(temp,'nleg').ne.0) then
      !Feff file found; read number of lines (atom coords) to skip
         backspace(11)
         !go up one row (back to the line that matched '------'
         read(11,*) nleg,l,r_pair
         !read the line again, but this time store the first three numbers into
         !variables:
            !nleg (number of legs used in the calculation)
            !l (degeneracy, or number of atoms around central atom)
            !r_pair (effective radius)

   !!		read(temp,*) nleg

         ntit=ntit+1
         read(11,'(a80)') title(ntit)
         !skip atom coordinates header
         do i=1,nleg
            ntit=ntit+1
            read(11,'(a80)') title(ntit)
         enddo
         !skip atom coordinates
         read(11,'(a80)') temp
         !skip data header - 1 more line
      endif

      !The read position is now at start of the data for fileRef#11
      read_feff_header=0
      !sets function value to 0 which indicates file was successfully opened
      return
      end
