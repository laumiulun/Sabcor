# Sabcor

Self Adsoprtions code from [http://lise.lbl.gov/RSXAP/](http://lise.lbl.gov/RSXAP/).

## Requirements
The only requirement is any version of gfortran. The version that was tested version
9.30. To know what version of gfortran:

    gfortran --version

## Compile
To compile sabcor, type `make` and it should compile the object files in `obj/` and
executable in `bin/`

## Test
To run a simple test, type:

    sabcor example.dat

this looks for a sab.inp in the current directory, but one can also specify a input file by

    sabcor <data_file> <sabcor_input>

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
    [chbooth@hahn stand_alone]$ sabcor example.dat
     Welcome to SAB_COR 1.05.

    Outputting self-absorption correction to sab_cor.dat

     Self-Absorption correction statistics:

    info depth at 5 inv ang:                   24885.0 Angstroms
    correction chi_true/chi_exp at 5 inv ang:   1.93

    writing out file example_sac.dat
    [chbooth@hahn stand_alone]$
    ---------------------
