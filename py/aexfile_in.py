import os
import header
# !
# !  Reads a gnuplot-like ascii data file in, mimicking exfile_in.
# !  Returns:
# !
# !		0	if filename is opened and read in successfully
# !		1	if filename does not exist
# !		2	some other error occured
# !
# !	Last modified:
# !		8/26/99 CB
# !		5/26/00 CB	Made some improvements to reading out headers
# !		6/30/03 CB	ported from amultichan_in to be more
# !				"exfile_in"-like
# !		8/21/08 CB	minor bug, filename needs to be declared *(*)
# !		1/9/2025 Levi Recla translation from Fortran to Python
# !*****************************************************************************
def num_fields(line):
    return len(line.strip().split())

def aexfile_in(filename):
    #Initialize variables
    ierr = 0
    nf = 0
    nx = 0
    xi = 0.0
    dx = 0.0
    title = []
    ntit = 0
    x = []
    f1 = []
    f2 = []
    f3 = []

    # Check if file exists
    if not os.path.isfile(filename):
        print(f'File not found in aexfile_in ierr= 1 {filename}')
        ierr = 1
        return ierr, x, f1, f2, f3, nf, nx, xi, dx, title, ntit

    #open the file and read
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except Exception as e:
        print('ERROR in aexfile_in: reading file... is file binary?')
        ierr = 2
        return ierr, x, f1, f2, f3, nf, nx, xi, dx, title, ntit

    index = 0
    ntit = 0

    while index < len(lines):
        ascii_line = lines[index].rstrip('\n')
        if not ascii_line:
            index += 1
            continue
        char2 = ascii_line[:2]
        if char2.startswith('#'):
            ntit += 1
            #Remove the hash
            title_line = ascii_line[2:].strip()
            title.append(title_line)
            index += 1
        else:
            break
    if ntit < 0:
        print('ERROR in aexfile_in: Header is not of proper format!!')
        print('Header lines must be at the beginning of the file and')
        print('be preceded by a \'#\'.  Data then must follow in')
        print('Tab or space delimited columns, x, y1, y2, y3, etc.')
        ierr = 2
        return ierr, x, f1, f2, f3, nf, nx, xi, dx, title, ntit

    if ntit > header.MAX_TIT:
        print('WARNING: too many header lines!')
        print(' ')
        print(f'This file contains {ntit} header lines.')
        print(f'All lines after {header.MAX_TIT} will be ignored.')
        ntit = header.MAX_TIT
        title = title[:header.MAX_TIT]

    #index points to the first data line
    if index >= len(lines):
        print('ERROR in aexfile_in: No data lines found after header.')
        ierr = 2
        return ierr, x, f1, f2, f3, nf, nx, xi, dx, title, ntit

    #Determine number of columns
    ascii_line = lines[index].strip()
    field_nums = num_fields(ascii_line)
    nf = 10 + field_nums - 1
    # HAYES AND BOYCE: SCREW YOU AND YOUR nf CODES!

    # Get first data point from ascii_line
    index_data = 0
    index_line = index

    while index_line < len(lines):
        line = lines[index_line].strip()
        if not line or line.startswith('#'):
            index_line += 1
            continue
        values = line.split()
        if len(values) < 2:
            index_line += 1
            continue

        try:
            values = list(map(float, values))
            x.append(values[0])
            f1.append(values[1])
            f2.append(values[2] if len(values) > 2 else 0.0)
            f3.append(values[3] if len(values) > 3 else 0.0)
        except Exception as e:
            print('ERROR in aexfile_in: reading data line.')
            ierr = 2
            return ierr, x, f1, f2, f3, nf, nx, xi, dx, title, ntit

        index_data += 1
        index_line += 1

    nx = index_data
    xi = x[0] if nx > 0 else 0.0
    dx = x[1] - x[0] if nx > 1 else 0.0

    ierr = 0
    return ierr, x, f1, f2, f3, nf, nx, xi, dx, title, ntit
