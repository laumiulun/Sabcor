#include "exafs.hf"
      integer function aexfile_out(outfile,x1,f1,f2,f3,
     &      nf,nx1,nx2,xi,dx,tit,ntit,type)

      integer ntit,iunit
      character tit(MAX_TIT)*TIT_LEN
      character outfile*FILENAME_LEN
      character type*2
      real x1(MAX_NX),f1(MAX_NX),f2(MAX_NX),f3(MAX_NX)

      iunit=11
      open(iunit,file=outfile)
      call tit2ascii(iunit,tit,ntit)
      !CORWIN: Where is tit2ascii?
      call fdata2ascii(iunit,x1,f1,f2,f3,nf,nx1,nx2,xi,dx,type)
      close(iunit)

      aexfile_out=0
      return
      end

c---------------------------------------------------------------------
c---------------------------------------------------------------------

	subroutine fdata2ascii(iunit,x1,f1,f2,f3,nf,nx1,nx2,xi,dx,type)

	integer iunit
        character tit(MAX_TIT)*TIT_LEN
        character infile*FILENAME_LEN
        character outfile*FILENAME_LEN
        character type*2
        real x1(MAX_NX),f1(MAX_NX),f2(MAX_NX),f3(MAX_NX)

	if((nf.gt.3.and.nf.lt.11).or.(nf.lt.1).or.(nf.gt.13)) then
		print *,'ERROR: unsupported file format in fdata2ascii.  nf=',nf
		stop
	endif

	if(nf.ne.2.and.type.eq.'rs') print *,'WARNING: r-space file may ',
     &	   'have extra data... nf=',nf
	do i=nx1,nx2
		if(nf.lt.10) then
			x=xi+float(i-1)*dx
			if(type.ne.'rs') then
				if(nf.eq.1) then
				  write(iunit,*) x,f1(i)
				elseif(nf.eq.2) then
				  write(iunit,*) x,f1(i),f2(i)
				elseif(nf.eq.3) then
				  write(iunit,*) x,f1(i),f2(i),f3(i)
				endif
			else
				amp=sqrt(f1(i)**2.0+f2(i)**2.0)
				write(iunit,*) x,amp,-amp,f1(i)
			endif
		else
			if(nf.eq.11) then
			  write(iunit,*) x1(i),f1(i)
			elseif(nf.eq.12) then
			  write(iunit,*) x1(i),f1(i),f2(i)
			elseif(nf.eq.13) then
			  write(iunit,*) x1(i),f1(i),f2(i),f3(i)
			endif
		endif
	enddo

	return
	end
