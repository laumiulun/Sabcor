import math

def aexfile_out(outfile, x1, f1, f2, f3, nf, nx1, nx2, xi, dx, tit, ntit, file_type, correction_string=None):
    """
    Writes data to an ASCII file 
    """
    try:
        with open(outfile, 'w') as f:
            tit2ascii(f, tit, ntit, correction_string)
            fdata2ascii(f, x1, f1, f2, f3, nf, nx1, nx2, xi, dx, file_type)
        ierr = 0
    except Exception as e:
        print(f'Error writing output file in aexfile_out: {e}')
        ierr = 1
    return ierr

def tit2ascii(file_handle, tit, ntit, correction_string=None):
    """
    Writes title lines to the ASCII file
    """
    # Write standard titles
    for i in range(ntit):
        line = tit[i]
        if not line.startswith('#'):
            line = '# ' + line
        file_handle.write(f'{line}\n')
    
    # Write the correction string if provided
    if correction_string:
        file_handle.write(correction_string)
        file_handle.write("\n")

def fdata2ascii(file_handle, x1, f1, f2, f3, nf, nx1, nx2, xi, dx, file_type):
    """
    Writes data arrays to the ASCII file, handling different formats based on 'nf'.
    """
    if ((nf > 3 and nf < 11) or (nf < 1) or (nf > 13)):
        print(f'ERROR: unsupported file format in fdata2ascii. nf={nf}')
        raise ValueError('Unsupported file format in fdata2ascii.')

    if nf != 2 and file_type == 'rs':
        print(f'WARNING: r-space file may have extra data... nf={nf}')

    for i in range(nx1 - 1, nx2):
        if nf < 10:
            x = xi + float(i) * dx
            if file_type != 'rs':
                if nf == 1:
                    file_handle.write(f'{x} {f1[i]}\n')
                elif nf == 2:
                    file_handle.write(f'{x} {f1[i]} {f2[i]}\n')
                elif nf == 3:
                    file_handle.write(f'{x} {f1[i]} {f2[i]} {f3[i]}\n')
            else:
                amp = math.sqrt(f1[i] ** 2 + f2[i] ** 2)
                file_handle.write(f'{x} {amp} {-amp} {f1[i]}\n')
        else:
            if nf == 11:
                file_handle.write(f'{x1[i]} {f1[i]}\n')
            elif nf == 12:
                file_handle.write(f'{x1[i]} {f1[i]} {f2[i]}\n')
            elif nf == 13:
                file_handle.write(f'{x1[i]} {f1[i]} {f2[i]} {f3[i]}\n')
