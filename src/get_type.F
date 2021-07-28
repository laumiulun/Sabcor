#include "exafs.hf"
c******************************************************************************
c******************************************************************************

      subroutine get_type(filename,file_type)

!  7/23/2004  CB	Fixed bug for cwd''s with es,ks,rs,ds else where in
!                 their name than the type
c******************************************************************************

      integer type_pos
      character filename*(*), file_type*2
      character string*FILENAME_LEN

      string=filename
      !First search filename

      type_pos=index(string,'/ds/')
      if(type_pos.eq.0) type_pos=index(string,'/es/')
      if(type_pos.eq.0) type_pos=index(string,'/ks/')
      if(type_pos.eq.0) type_pos=index(string,'/rs/')
      if(type_pos.eq.0) then
         call getcwd(string)
         islen=index(string,' ')-1
         type_pos=index(string(islen-2:islen),'/ds')
         if(type_pos.eq.0) type_pos=index(string(islen-2:islen),'/es')
         if(type_pos.eq.0) type_pos=index(string(islen-2:islen),'/ks')
         if(type_pos.eq.0) type_pos=index(string(islen-2:islen),'/rs')
         if(type_pos.ne.0) type_pos=type_pos+islen-3
      endif

      if(type_pos.ne.0) file_type=string(type_pos+1:type_pos+2)
      return
      end
