c********************************************************************
        integer function num_fields(ascii_line)
c
c	Determines the number of separate fields in an ascii line.
c	line_len is no longer used, and was left into the call
c	for compatability with
c	older codes, but has been removed. Hopefully I found all the other 
c	spots it has been called from in the codes!
c 
        character ascii_line*(*)
	character*1 tab
        logical new
 
        itemp=0
        new=.true.
	tab=char(9)
 
        do index=1,len(ascii_line) 
                if(ascii_line(index:index).eq.' '.or.
     &             ascii_line(index:index).eq.','.or.
     &             ascii_line(index:index).eq.tab) then
                        new=.true.
                else
                        if(new) itemp=itemp+1
                        new=.false.
                endif
 
        enddo
 
        num_fields=itemp
        return
        end
