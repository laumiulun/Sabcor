import sys
import os
from exafs import MAX_NX, MAX_TIT, VERSION
from aexfile_in import aexfile_in
from aexfile_out import aexfile_out
from exfile_in import exfile_in
from exfile_out import exfile_out
from sab_sub import fluor_corr
from read_inp import readinp
from file_ascii import file_ascii
from elements_data import elements

def main():
    print(f'Welcome to {VERSION}.')

    # Check command-line arguments
    if len(sys.argv) < 2:
        print("Usage: sabcor <datafile> [inputfile]")
        sys.exit(1)

    # Get the data file and input file
    in_datafile = sys.argv[1]
    inp_filename = sys.argv[2] if len(sys.argv) > 2 else "sab.inp"

    # Verify that the data file exists
    if not os.path.isfile(in_datafile):
        print(f'ERROR: The data file "{in_datafile}" does not exist.')
        sys.exit(1)

    # Verify that the input file exists
    if not os.path.isfile(inp_filename):
        print(f'ERROR: The input file "{inp_filename}" does not exist.')
        sys.exit(1)

    ierr = 0

    # Read the input file
    params = readinp(inp_filename)
    d = params['d']
    phi = params['phi']
    theta = params['theta']
    formvol = params['formvol']
    formula = params['formula']
    edge = params['edge']
    fluor_energy = params['fluor_energy']
    concentration = params['concentration']
    if ierr > 0:
        print(f'ERROR: sab_cor reports error from readinp. ierr={ierr}')
        sys.exit(1)

    # Determine the file format of the data file
    format_ascii = file_ascii(in_datafile)

    # Read the data file
    if format_ascii:
        ierr, x, f1, f2, f3, nf, nx, xi, dx, title, ntit = aexfile_in(in_datafile)
    else:
        ierr, x, f1, f2, f3, nf, nx, xi, dx, title, ntit = exfile_in(in_datafile)

    if ierr != 0:
        print(f'Error reading input file {in_datafile}')
        sys.exit(1)

    # Map variables
    k = x
    kchi_r = f1
    kchi_i = f2
    dummy = f3

    # Construct the output filename
    idot = in_datafile.rfind('.')
    if idot == -1:
        out_datafile = in_datafile + '_sac'
    else:
        out_datafile = in_datafile[:idot] + '_sac' + in_datafile[idot:]

    # Perform the correction
    kchi_r, title_string = fluor_corr(k, kchi_r, kchi_i, nf, nx, title, ntit,
           d, phi, theta, formvol, formula, edge, fluor_energy,
           concentration, 'a', ' ', elements)


    # Write the output file
    print(f'writing out file {out_datafile[:62]}')
    if format_ascii:
        ierr = aexfile_out(out_datafile, k, kchi_r, kchi_i, dummy,
                           nf, 1, nx, xi, dx, title, ntit, 'ks', title_string)
    else:
        ierr = exfile_out(out_datafile, k, kchi_r, kchi_i, dummy,
                          nf, 1, nx, xi, dx, title, ntit)

    if ierr != 0:
        print(f'Error writing output file {out_datafile}')
        sys.exit(1)

if __name__ == "__main__":
    main()
