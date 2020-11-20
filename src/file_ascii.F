#include "exafs.hf"
	logical function file_ascii(iunit,filename)
c
c	determines whether file is in the RSXAP binary format, or the so-called
c	"gnu" ascii format.  Uses IUNIT for opening and cloasing the file.

	character*FILENAME_LEN filename
        character testchar
	integer iunit
	logical temp_log

c       Is this a "gnu"-type ascii file?
c
c       open filename
        open(iunit,file=filename)
c       Read in number of header lines
        read(iunit,'(a)') testchar
        if(testchar.eq.'#') then
		temp_log=.true.
	else
		temp_log=.false.
        endif
        close(iunit)

	file_ascii=temp_log
	return
	end

	
