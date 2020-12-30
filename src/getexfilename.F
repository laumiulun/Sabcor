#include "exafs.hf"
c******************************************************************************
c******************************************************************************
	subroutine getexfilename(filename,file_type)

	character*FILENAME_LEN filename
	character*FILENAME_LEN sub_dir
	character*FILENAME_LEN data_dir
	character file_type*2
	character*1 ans
	character*FILENAME_LEN string
	integer sublen, system, access, ierr
	integer num_fields, field_num, getcwd
	logical first

	data first/.true./
	data field_num/1/

	common /io/sub_dir

	!print *,' '
c	First check command line.  If a filename exists
c	there, use that.
c
	if(first)then
		num_fields=iargc()
		if(num_fields.ge.field_num) then
			call getarg(field_num,filename)
			ierr=access(filename,' ')
			if(ierr.ne.0) then
				write(6,1239) filename
1239				format('File does not exist:',a100)
				call exit(0)
			endif
			field_num=field_num+1
c			write(6,1005) filename
c
c			Try to determine file''s type
c
			call get_type(filename,file_type)
c
			return
		elseif(num_fields.gt.0) then
			call exit(0)
		endif

		sub_dir='            '

	else
5		write(6,1238) sub_dir
1238		format('Current sub-directory is ',a50)
		write(6,1237)
1237		format('Change directory? [RET=n,q=quit] ',$)
		read(5,'(a1)') ans
		if(ans.eq.'q') then
			print *,'Good-day!'
			call exit(0)
		endif
		if(ans.ne.'y') goto 8
	endif


c	Next get directory

c	Use environment variable to get data directory
	call getenv('EXDATA_DIR',data_dir)
	idd=index(data_dir,' ')-1

9	write(6,1000)
1000	format('Input exdata subdirectory: [RET=cwd, ?=list] ',$)
	read(5,'(a12)') sub_dir

	if(sub_dir(1:1).eq.'?') then
		if(idd.gt.0) then
			string='ls '//data_dir(1:idd)
		else
			string='ls '//DATA_DIR
		endif
		istatus=system(string)
		goto 9
	endif

	sublen=index(sub_dir,' ')-1

	if(sub_dir(1:12).ne.'            ') then
		if(sublen.eq.0) then
			write(6,1003)
1003			format('Please start data directory with a ',$)
			write(6,1004)
1004			format('valid character.')
			goto 9
		endif
		if(idd.gt.0) then
			sub_dir=data_dir(1:idd)//'/'//sub_dir(1:sublen)
		else
			sub_dir=DATA_DIR//'/'//sub_dir(1:sublen)
		endif
		ierr = access(sub_dir,' ')
		if(ierr.ne.0) then
			write(6,1234) sub_dir
1234			format(a20,' directory does not exist.')
			goto 9
		endif

10		write(6,1001)
1001		format('Input file type: (ds,es,ks,rs,!) ',$)
		read(5,'(a2)') file_type

		if (((file_type.ne.'ds').and.(file_type.ne.'es'))
     &		.and.((file_type.ne.'ks').and.(file_type.ne.'rs')))
     &		then
			if(file_type(1:1).eq.'!') goto 9
			write(6,1002) file_type
1002			format(a2,' is not understood.')
			goto 10
		endif
		sublen=index(sub_dir,' ')-1
		sub_dir=sub_dir(1:sublen)//'/'//file_type
 		ierr = access(sub_dir,'r')
		if(ierr.ne.0) then
			write(6,1234) sub_dir
			goto 10
		endif
	else
		ierr=getcwd(sub_dir)
		if(ierr.ne.0) then
			stop'Trouble with CWD in get_exfilename...'
		endif
	endif

8	write(6,1006)
1006	format('Name of file (?=dir,!): ',$)
	read(5,'(a50)') filename

	sublen=index(sub_dir,' ')-1

	if (filename(1:1).eq.'?') then
		write(6,1246)
1246		format('Wild Card: [RET=*] ',$)
		read(5,'(a)') string
		string='ls '//sub_dir(1:sublen)//'/'//string
		ierr=system(string)
		goto 8
	elseif(filename(1:1).eq.'!') then
		goto 9
	endif

	if(filename(1:1).eq.' ') then
		write(6,1007)
1007		format('Please start name with legal character.')
		goto 8
	endif

	if((sublen.ne.0).and.(sub_dir(1:sublen).ne.'.')) 
     &		filename=sub_dir(1:sublen)//'/'//filename
	call get_type(filename,file_type)
	ierr = access(filename,'r')
	if(ierr.ne.0) then
		write(6,1239) filename
		goto 8
	endif

c	Don't print out file name.  Leave that to "outheader'
c	print *,' '
c	write(6,1005) filename
1005	format('file: ',a50)

	first=.false.
	return
	end

