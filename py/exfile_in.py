import os
import numpy as np
from exafs import MAX_NX, TIT_LEN, MAX_TIT, FILENAME_LEN

from spline import spline
from splint import splint

from aexfile_in import aexfile_in
from read_feff_header import read_feff_header

# !	This file contains:
# !		function exfile_in
# !		function infile_type
# !		function aexfile_in  (in its own separate file)
# !		function bexfile_in
# !		function cexfile_in
# !		function fexfile_in
# !
# !	Last modified: 1/09/25 Levi Recla
# !         Translation from Fortran to Python
# !         Updated to remove scipy spline usage and use custom spline/splint.

def exfile_in(filename):
    """
    Reads data from a file, automatically determining its type and format.
    Returns x, f1, f2, f3, nf, nx, xi, dx, title, ntit, and an error code ierr.
    """
    ierr = 0
    x = []
    f1 = []
    f2 = []
    f3 = []
    title = []
    ntit = 0
    xi = 0.0
    dx = 0.0
    nf = 0
    nx = 0

    # Check if file exists and is readable
    if not os.path.isfile(filename):
        print(f'ERROR in exfile_in: {filename} does not exist!')
        return 1, x, f1, f2, f3, nf, nx, xi, dx, title, ntit
    if not os.access(filename, os.R_OK):
        print(f'ERROR in exfile_in: User does not have read permission for file {filename}!')
        return 2, x, f1, f2, f3, nf, nx, xi, dx, title, ntit

    # Determine file type
    ierr, ftype = infile_type(filename)
    if ierr != 0:
        return ierr, x, f1, f2, f3, nf, nx, xi, dx, title, ntit

    # Read in the appropriate file type
    if ftype == 0:  # Standard binary file
        ierr, x, f1, f2, f3, nf, nx, xi, dx, title, ntit = bexfile_in(filename)
    elif ftype == 1:  # "gnu"-type ASCII file
        ierr, x, f1, f2, f3, nf, nx, xi, dx, title, ntit = aexfile_in(filename)
    elif ftype == 2:  # chi.dat file
        n_pair = 1  # Chi.dat files not normalized; run chi2bin to set n_pair
        ierr, x, f1, f2, f3, nf, nx, xi, dx, title, ntit = cexfile_in(filename, n_pair)
    elif ftype == 3:  # feffxxxx.dat file
        ierr, x, f1, f2, f3, nf, nx, xi, dx, title, ntit = fexfile_in(filename)
    else:
        print('ERROR in exfile_in: Unsupported file type.')
        return 2, x, f1, f2, f3, nf, nx, xi, dx, title, ntit

    # If nf <= 10, fill x(i) with a uniform grid
    if nf <= 10:
        x = [xi + dx * float(i) for i in range(nx)]

    return ierr, x, f1, f2, f3, nf, nx, xi, dx, title, ntit

def infile_type(filename):
    """
    Determines the type of the input file.
    Returns an error code ierr and ftype:
        ierr = 0 if successful
        ftype values:
            0 - standard binary format
            1 - "gnu"-type ASCII format
            2 - chi.dat format
            3 - feffxxxx.dat format
    """
    ierr = 0
    ftype = None

    try:
        with open(filename, 'r') as f:
            first_line = f.readline()
    except Exception:
        # Assume binary file
        ftype = 0
        return ierr, ftype

    testchar = first_line[:1]
    # Check for Feff file
    if ('Feff' in first_line or 'FEFF' in first_line) and 32 <= ord(testchar) != 127:
        # Read feff header to check for chi.dat or feffxxxx.dat
        ierr, title, ntit, feff_ver, r_pair = read_feff_header(filename)
        if ierr != 0:
            return ierr, ftype
        if any('chi' in line.lower() for line in title):
            ftype = 2  # chi.dat file
        else:
            ftype = 3  # feffxxxx.dat file
    elif testchar == '#':
        ftype = 1  # "gnu"-type ASCII file
    else:
        ftype = 0  # Assume binary file

    return ierr, ftype

def bexfile_in(filename):
    """
    Reads a standard binary data file.
    Returns ierr and data arrays.
    """
    ierr = 0
    x = []
    f1 = []
    f2 = []
    f3 = []
    title = []
    ntit = 0
    xi = 0.0
    dx = 0.0
    nf = 0
    nx = 0

    try:
        with open(filename, 'rb') as f:
            # Read ntit
            ntit_bytes = f.read(4)
            ntit = int.from_bytes(ntit_bytes, byteorder='little')
            if ntit > MAX_TIT:
                print('WARNING: too many header lines!')
                print(f'This file contains {ntit} header lines.')
                print(f'All lines after {MAX_TIT} will be ignored.')
                ntit = MAX_TIT  # Limit to MAX_TIT

            # Read titles
            for _ in range(ntit):
                title_line = f.read(TIT_LEN).decode('utf-8').strip()
                title.append(title_line)

            # Read nf, nx, xi, dx
            nf_bytes = f.read(4)
            nf = int.from_bytes(nf_bytes, byteorder='little')
            nx_bytes = f.read(4)
            nx = int.from_bytes(nx_bytes, byteorder='little')
            xi_bytes = f.read(4)
            xi = float.fromhex(f'{int.from_bytes(xi_bytes, byteorder="little"):08x}')
            dx_bytes = f.read(4)
            dx = float.fromhex(f'{int.from_bytes(dx_bytes, byteorder="little"):08x}')

            # Read data based on nf
            if nf == 11:
                for _ in range(nx):
                    x_value = np.frombuffer(f.read(4), dtype=np.float32)[0]
                    f1_value = np.frombuffer(f.read(4), dtype=np.float32)[0]
                    x.append(x_value)
                    f1.append(f1_value)
            elif nf == 12:
                for _ in range(nx):
                    x_value = np.frombuffer(f.read(4), dtype=np.float32)[0]
                    f1_value = np.frombuffer(f.read(4), dtype=np.float32)[0]
                    f2_value = np.frombuffer(f.read(4), dtype=np.float32)[0]
                    x.append(x_value)
                    f1.append(f1_value)
                    f2.append(f2_value)
            elif nf == 13:
                for _ in range(nx):
                    x_value = np.frombuffer(f.read(4), dtype=np.float32)[0]
                    f1_value = np.frombuffer(f.read(4), dtype=np.float32)[0]
                    f2_value = np.frombuffer(f.read(4), dtype=np.float32)[0]
                    f3_value = np.frombuffer(f.read(4), dtype=np.float32)[0]
                    x.append(x_value)
                    f1.append(f1_value)
                    f2.append(f2_value)
                    f3.append(f3_value)
            elif nf == 1:
                for _ in range(nx):
                    f1_value = np.frombuffer(f.read(4), dtype=np.float32)[0]
                    f1.append(f1_value)
            elif nf == 2:
                for _ in range(nx):
                    f1_value = np.frombuffer(f.read(4), dtype=np.float32)[0]
                    f2_value = np.frombuffer(f.read(4), dtype=np.float32)[0]
                    f1.append(f1_value)
                    f2.append(f2_value)
            elif nf == 3:
                for _ in range(nx):
                    f1_value = np.frombuffer(f.read(4), dtype=np.float32)[0]
                    f2_value = np.frombuffer(f.read(4), dtype=np.float32)[0]
                    f3_value = np.frombuffer(f.read(4), dtype=np.float32)[0]
                    f1.append(f1_value)
                    f2.append(f2_value)
                    f3.append(f3_value)
            else:
                print('ERROR: bexfile_in()')
                print('Sorry! bexfile_in not equipped to handle this format.')
                return 2, x, f1, f2, f3, nf, nx, xi, dx, title, ntit

    except Exception as e:
        print(f'Error reading binary file {filename}: {e}')
        return 2, x, f1, f2, f3, nf, nx, xi, dx, title, ntit

    return ierr, x, f1, f2, f3, nf, nx, xi, dx, title, ntit

def cexfile_in(filename, n_pair):
    """
    Reads a chi.dat file.
    Returns ierr and data arrays.
    """
    ierr = 0
    x = []
    f1 = []
    f2 = []
    f3 = []
    amp = []
    phase = []
    title = []
    ntit = 0
    xi = 0.0
    dx = 0.0
    nf = 0
    nx = 0

    # Read the header using read_feff_header
    ierr, title, ntit, feff_ver, r_pair = read_feff_header(filename)
    if ierr != 0:
        return ierr, x, f1, f2, f3, nf, nx, xi, dx, title, ntit

    # Read the data
    try:
        with open(filename, 'r') as f:
            # Skip header lines
            for _ in range(ntit):
                f.readline()
            # Read data
            for line in f:
                if not line.strip():
                    continue
                values = list(map(float, line.strip().split()))
                if len(values) >= 4:
                    k_value, chi_value, amp_value, phase_value = values[:4]
                    x.append(k_value)
                    f1.append(k_value * chi_value / n_pair)
                    f2.append(-k_value * amp_value / n_pair * np.cos(phase_value))
                    # (Optional) storing amplitude or phase if you need them
                    amp.append(k_value * amp_value * r_pair ** 2 / n_pair)
                    phase.append(phase_value - 2.0 * k_value * r_pair)
                else:
                    continue

            nx = len(x)
            xi = x[0] if nx > 0 else 0.0
            if nx > 5:
                dx = x[5] - x[4]
                dx2 = abs((x[-1] - x[-2]) - dx)
                if dx2 > 0.00001:
                    print('Error: cexfile_in -- check dx of chi.dat-formatted file:', filename)
                    return 2, x, f1, f2, f3, nf, nx, xi, dx, title, ntit
            nf = 2

    except Exception as e:
        print(f'Error reading chi.dat file {filename}: {e}')
        return 2, x, f1, f2, f3, nf, nx, xi, dx, title, ntit

    return ierr, x, f1, f2, f3, nf, nx, xi, dx, title, ntit

def fexfile_in(filename):
    """
    Reads a feffxxxx.dat file.
    Returns ierr and data arrays.
    """
    ierr = 0
    x = []
    f1 = []
    f2 = []
    f3 = []
    amp = []
    phase_new = []
    title = []
    ntit = 0
    xi = 0.0
    dx = 0.0
    nf = 0
    nx = 0

    # Read the header using read_feff_header
    ierr, title, ntit, feff_ver, r_pair = read_feff_header(filename)
    if ierr != 0:
        return ierr, x, f1, f2, f3, nf, nx, xi, dx, title, ntit

    # Read the data
    kx = []
    phic = []
    mag = []
    phase = []
    redfact = []
    lambda_ = []
    realp = []

    try:
        with open(filename, 'r') as f:
            # Skip header lines
            for _ in range(ntit):
                f.readline()
            for line in f:
                if not line.strip():
                    continue
                values = list(map(float, line.strip().split()))
                # The feffxxxx.dat typically has 7 columns: k, phc, mag, phase, redfact, lambda, re(...)
                if len(values) >= 7:
                    kx_value, phic_value, mag_value, phase_value, \
                        redfact_value, lambda_value, realp_value = values[:7]
                    kx.append(kx_value)
                    phic.append(phic_value)
                    mag.append(mag_value)
                    phase.append(phase_value)
                    redfact.append(redfact_value)
                    lambda_.append(lambda_value)
                    realp.append(realp_value)
                else:
                    continue

            nx = len(kx)
            if nx == 0:
                print(f"Error in fexfile_in: no data read from {filename}")
                return 2, x, f1, f2, f3, nf, nx, xi, dx, title, ntit

            xi = kx[0]
            xmax = kx[-1]

            # Typical spacing
            dx = 0.04999
            new_nx = int((xmax - xi) / dx + 0.5) + 1

            # ----------------------------------------------------------------
            # 1) Compute second derivatives for each array using spline()
            #    Using natural boundary condition => yp1=1e30, ypn=1e30
            # ----------------------------------------------------------------
            phic_y2    = spline(kx, phic, 1.0e30, 1.0e30)
            mag_y2     = spline(kx, mag, 1.0e30, 1.0e30)
            phase_y2   = spline(kx, phase, 1.0e30, 1.0e30)
            redfact_y2 = spline(kx, redfact, 1.0e30, 1.0e30)
            lambda_y2  = spline(kx, lambda_, 1.0e30, 1.0e30)

            # ----------------------------------------------------------------
            # 2) Evaluate splines at evenly spaced k-values using splint()
            # ----------------------------------------------------------------
            for i in range(new_nx):
                k_value = xi + i * dx

                # Interpolate each quantity
                phic_interp    = splint(kx, phic,    phic_y2,    k_value)
                mag_interp     = splint(kx, mag,     mag_y2,     k_value)
                phase_interp   = splint(kx, phase,   phase_y2,   k_value)
                redfact_interp = splint(kx, redfact, redfact_y2, k_value)
                lambda_interp  = splint(kx, lambda_, lambda_y2,  k_value)

                # Combine phases and apply shift
                phase_new_value = phase_interp + phic_interp + 2.0 * k_value * r_pair
                phase_new.append(phase_new_value)

                # Compute amplitude
                if k_value != 0.0:
                    amp_value = (mag_interp * (1.0 / (k_value * r_pair**2)) *
                                 redfact_interp * np.exp(-2.0 * r_pair / lambda_interp))
                else:
                    amp_value = 0.0
                amp.append(amp_value)

                # Construct the chi
                chi_value = amp_value * np.sin(phase_new_value)
                # Store outputs for plotting
                x.append(k_value)
                f1.append(k_value * chi_value)
                f2.append(-k_value * amp_value * np.cos(phase_new_value))

            nx = new_nx
            nf = 12

    except Exception as e:
        print(f'Error reading feffxxxx.dat file {filename}: {e}')
        return 2, x, f1, f2, f3, nf, nx, xi, dx, title, ntit

    return ierr, x, f1, f2, f3, nf, nx, xi, dx, title, ntit
