# Sabcor

Self Adsoprtions code from [http://lise.lbl.gov/RSXAP/](http://lise.lbl.gov/RSXAP/).

## Requirements
The only requirement is any version of python. The version that was tested version 
3.12.2. To know what version of python:

    python --version

## Compile
To compile and run sabcor, simply change into the 'py' directory type 
`python sabcor.py [file.dat]` and it will execute sabcor with the resulting files in the 'py' directory.

## Test
To run a simple test, type:

    python sabcor.py example.dat

this looks for a sab.inp in the current directory, but one can also specify a input file by

    sabcor <data_file> <sabcor_input>

## Sabcor Module
The Sabcor module can be imported into a project by calling:

    from sabcor import Sabcor

Once the module has been imported, you can instantiate a Sabcor object by passing in the data file and input files as parameters:

    sabcor_processor = Sabcor("example.dat", "sab.inp")

You can then call the process() function which will run the Sabcor program and place resulting files in working director.

    output_filename = sabcor_processor.process()



## Sab.inp format

    PHI 49.4
    VOLUME 47.22
    THICKNESS 46000
    FORMULA Hf
    EDGE Hf K
    FLUOR 8047


The outputs should be
    The output onto the screen should look like:
    ---------------------
    $ python sabcor.py example.dat
     Welcome to SAB_COR 1.07.

    Outputting self-absorption correction to sab_cor.dat

     Self-Absorption correction statistics:

    info depth at 5 inv ang:                   99540.1 Angstroms
    correction chi_true/chi_exp at 5 inv ang:   1.19

    writing out file example_sac.dat
    ---------------------

## Sabcor Inp file

The following is the format for sabcor input file `sab.inp`:

    THICKNESS:  sample thickness (angstroms)
    PHI:        angle of sample w.r.t. beam (degrees)
    THETA:      (optional) angle of sample w.r.t. fluorescence (degrees)
    VOLUME:    volume occupied by a formula unit (angstroms^3)
    ABC:       a b c lattice parameters (angstroms)
    FORMULA:    chemical formula (eg. YBa2Cu3O7)
    EDGE:       the edge atom and edge type (eg. Kr LIII)
    CONVERSION: (optional) use if the edge is from a substituted atom in the material.

Example `sab.inp`:

    PHI 49.4
    VOLUME 47.22
    THICKNESS 46000
    FORMULA Cu
    EDGE Cu K
    FLUOR 8047


## Comparing Fortran and Python Results

To compare the results of the Fortran and Python implementations, run the following script:

```bash
python py/testing/generate_comparison.py <FORTRAN_example_sac.dat> <PYTHON_example_sac.dat>
```

This script will:
- Parse the Fortran and Python output data from the .dat files.
- Convert the parsed data into CSV format for easier processing.
- Generate an overlay plot comparing the results, saving it as comparison_plot.png

By default, the script assumes that the data files are formatted with the following names:
- FORTRAN_example_sac.dat
- PYTHON_example_sac.dat

However, you can specify different input data files by passing their names as arguments:
```bash
python py/testing/generate_comparison.py <fortran_result_data.dat> <python_result_data.dat>
```
