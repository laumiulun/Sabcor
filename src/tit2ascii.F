#include "exafs.hf"
!---------------------------------------------------------------------
!---------------------------------------------------------------------

      subroutine tit2ascii(iunit,tit,ntit)

      integer ntit,iunit
      character tit(MAX_TIT)*TIT_LEN

      do i=1,ntit
         write(iunit,1000) tit(i)
      enddo
1000  format('# ',a80)
      write(iunit,1001)
1001  format('# ----------------------------------------------------')

      return
      end
