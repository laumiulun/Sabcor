import os
import sys
from exafs import MAX_NX, MAX_TIT, VERSION
from aexfile_in import aexfile_in
from aexfile_out import aexfile_out
from exfile_in import exfile_in
from exfile_out import exfile_out
from sab_sub import fluor_corr
from read_inp import readinp
from file_ascii import file_ascii
from elements_data import elements


class Sabcor:
    def __init__(self, datafile: str, inputfile: str = "sab.inp"):
        """
        Initialize the Sabcor processing class.

        :param datafile: Path to the input data file.
        :param inputfile: Path to the input parameters file (default: 'sab.inp').
        """
        self.datafile = datafile
        self.inputfile = inputfile
        self.params = {}
        self.k = None
        self.kchi_r = None
        self.kchi_i = None
        self.dummy = None
        self.nf = None
        self.nx = None
        self.xi = None
        self.dx = None
        self.title = None
        self.ntit = None
        self.format_ascii = None

    def validate_files(self):
        """Ensure the required input files exist before processing."""
        if not os.path.isfile(self.datafile):
            raise FileNotFoundError(f'ERROR: The data file "{self.datafile}" does not exist.')

        if not os.path.isfile(self.inputfile):
            raise FileNotFoundError(f'ERROR: The input file "{self.inputfile}" does not exist.')

    def read_input_file(self):
        """Read the input file parameters."""
        self.params = readinp(self.inputfile)

    def read_data_file(self):
        """Determine the format and read the data file."""
        self.format_ascii = file_ascii(self.datafile)

        if self.format_ascii:
            ierr, self.k, self.kchi_r, self.kchi_i, self.dummy, self.nf, self.nx, self.xi, self.dx, self.title, self.ntit = aexfile_in(self.datafile)
        else:
            ierr, self.k, self.kchi_r, self.kchi_i, self.dummy, self.nf, self.nx, self.xi, self.dx, self.title, self.ntit = exfile_in(self.datafile)

        if ierr != 0:
            raise RuntimeError(f'Error reading input file {self.datafile}')

    def process_correction(self):
        """Perform the fluorescence correction."""
        d = self.params['d']
        phi = self.params['phi']
        theta = self.params['theta']
        formvol = self.params['formvol']
        formula = self.params['formula']
        edge = self.params['edge']
        fluor_energy = self.params['fluor_energy']
        concentration = self.params['concentration']

        self.kchi_r, title_string = fluor_corr(
            self.k, self.kchi_r, self.kchi_i, self.nf, self.nx, self.title, self.ntit,
            d, phi, theta, formvol, formula, edge, fluor_energy,
            concentration, 'a', ' ', elements
        )

        return title_string

    def write_output_file(self):
        """Generate and save the output file."""
        idot = self.datafile.rfind('.')
        out_datafile = self.datafile[:idot] + '_sac' + self.datafile[idot:] if idot != -1 else self.datafile + '_sac'

        print(f'Writing output file {out_datafile[:62]}')

        if self.format_ascii:
            ierr = aexfile_out(out_datafile, self.k, self.kchi_r, self.kchi_i, self.dummy,
                               self.nf, 1, self.nx, self.xi, self.dx, self.title, self.ntit, 'ks', "")
        else:
            ierr = exfile_out(out_datafile, self.k, self.kchi_r, self.kchi_i, self.dummy,
                              self.nf, 1, self.nx, self.xi, self.dx, self.title, self.ntit)

        if ierr != 0:
            raise RuntimeError(f'Error writing output file {out_datafile}')

        return out_datafile

    def process(self):
        """Complete processing pipeline from reading input to writing output."""
        print(f'Processing {self.datafile} using Sabcor {VERSION}')
        self.validate_files()
        self.read_input_file()
        self.read_data_file()
        self.process_correction()
        output_file = self.write_output_file()
        print(f'Processing complete. Output saved to {output_file}')
        return output_file


# COMMAND-LINE SUPPORT
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <datafile> [inputfile]")
        sys.exit(1)

    datafile = sys.argv[1]
    inputfile = sys.argv[2] if len(sys.argv) > 2 else "sab.inp"

    try:
        sabcor_processor = Sabcor(datafile, inputfile)
        output_filename = sabcor_processor.process()
        print(f"Output file generated: {output_filename}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
