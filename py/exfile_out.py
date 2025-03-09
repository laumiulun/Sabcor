
import os
import struct
from exafs import MAX_TIT, TIT_LEN

def exfile_out(filename, x, f1, f2, f3, nf, nx1, nx2, xi, dx, title, ntit):
    """
    Writes data to a binary file in the specified format.
    Returns:
        0 if successful,
        1 if an error occurred.
c	Input parameters (see exfile_in for ones not listed):
c	
c	nx1:	Index of first point
c	nx2:	Index of last point
c
c	WARNING!!!!
c	This subroutine writes out an xafs data file to filename
c	regardless of whether it exists or not!  Precede by a
c	call to outfilename!
c
c	Last modifies: 5/10/95 CB
c************************************************************************
    """
    # Check if file exists
    if os.path.exists(filename):
        # If file exists, check if we have write permissions
        if not os.access(filename, os.W_OK):
            print('Filename does not have write access!!!')
            return 1
    else:
        # If file does not exist, check if we have permissions to create it
        directory = os.path.dirname(filename) or '.'
        if not os.access(directory, os.W_OK):
            print('Cannot create file in the directory!!!')
            return 1

    nx = nx2 - nx1 + 1

    try:
        with open(filename, 'wb') as f:
            # Write ntit to the file as an integer
            f.write(struct.pack('i', ntit))

            # Print a warning if too many header lines
            if ntit > MAX_TIT:
                print('WARNING: too many header lines!')
                print(f'This file contains {ntit} header lines.')
                print(f'All lines after {MAX_TIT} will be ignored.')

            # Write the title lines
            if ntit <= MAX_TIT:
                for i in range(ntit):
                    line = title[i].ljust(TIT_LEN)[:TIT_LEN]
                    f.write(line.encode('utf-8'))
            else:
                for i in range(MAX_TIT):
                    line = title[i].ljust(TIT_LEN)[:TIT_LEN]
                    f.write(line.encode('utf-8'))
                for i in range(MAX_TIT, ntit):
                    tit_temp = title[i]
                    print(f'***HEADER LINE IGNORED {tit_temp}')

            # Write nf, nx, xi, dx
            f.write(struct.pack('i', nf))
            f.write(struct.pack('i', nx))
            f.write(struct.pack('f', xi))
            f.write(struct.pack('f', dx))

 
            start = nx1 - 1
            end = nx2

            # Write the data based on nf
            if nf == 11:
                for i in range(start, end):
                    f.write(struct.pack('ff', x[i], f1[i]))
            elif nf == 12:
                for i in range(start, end):
                    f.write(struct.pack('fff', x[i], f1[i], f2[i]))
            elif nf == 13:
                for i in range(start, end):
                    f.write(struct.pack('ffff', x[i], f1[i], f2[i], f3[i]))
            elif nf == 1:
                for i in range(start, end):
                    f.write(struct.pack('f', f1[i]))
            elif nf == 2:
                for i in range(start, end):
                    f.write(struct.pack('ff', f1[i], f2[i]))
            elif nf == 3:
                for i in range(start, end):
                    f.write(struct.pack('fff', f1[i], f2[i], f3[i]))
            else:
                print('ERROR: exfile_out()')
                print('Sorry! exfile_out not equipped to handle this format.')
                return 1

    except Exception as e:
        print(f'Error writing to file {filename}: {e}')
        return 1

    return 0
