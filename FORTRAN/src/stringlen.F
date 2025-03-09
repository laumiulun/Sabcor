	integer function stringlen(string)
c
c	Returns actual length of string, assuming the end is padded
c	with spaces.

	character*(*) string

	length=len(string)


1	if(string(length:length).eq.' ') then
		length=length-1
		if(length.gt.0)	goto 1
	endif

	stringlen=length
	return
	end
