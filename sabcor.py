# sabcor Wrapper files
import pathlib
import os
import argparse
import subprocess
import shutil
import re
import numpy as np

def get_args():
    """Command line args for sabcor

    Returns:
        args : args for sabcor
    """

    parser = argparse.ArgumentParser()
    # parser.add_argument('-i', action='store_true')
    # parser.add_argument('-a', action='store_true')
    parser.add_argument('file',type=str)
    # parser.add_argument('output_file',type=str)
    parser.add_argument('sabcor_inp_file',nargs='?',type=str,default='sab.inp')

    args = parser.parse_args()

    return args

def check_executable(paths=None):
    """Check if the sabcor executable exists

    Args:
        paths (str, optional): Path locations for sabcor. Defaults to None.

    Returns:
       str: excutable path for sabcor
    """

    if paths == None:
        excut_paths = pathlib.Path.cwd() / 'bin/sabcor'
    else:
        excut_paths = paths
    exists = excut_paths.is_file()
    # Compile sabcor
    if exists == False:
        subprocess.run(['make'])

    return excut_paths

def if_params(full_params,params_name,params):
    """Check if the params is in the sabcor input file

    Args:
        full_params (_type_): _description_
        params_name (_type_): _description_
        params (_type_): _description_

    Returns:
        _type_: _description_
    """
    if params[0] == params_name:
        full_params[params_name] = params[1]

    return full_params

def checkParams(params,params_name,default):
    if params[params_name] == default:
        print('Missing ' + params_name + ' !')
        exit()

def read_sab(file):
    """Read sabcor input file

    Args:
        file (str): file name for sabcor input file

    Returns:
        dicts : dict of params for sabcor input file
    """
    full_sab_path = pathlib.Path.cwd() / file

    params = {
        'PHI' : 0,
        'VOLUME': 0,
        'THICKNESS' : 0,
        'FORMULA' : 'NA',
        'EDGE': 'NA',
        'FLUOR' : 0
    }

    with open(file,'r',encoding='utf-8') as f:
        lines = f.readlines()
        for i in lines:
            result = i.strip().split(' ')
            params = if_params(params,'PHI',result)
            params = if_params(params,'VOLUME',result)
            params = if_params(params,'THICKNESS',result)
            params = if_params(params,'FORMULA',result)
            params = if_params(params,'FLUOR',result)
            if result[0] == 'EDGE':
                params['EDGE'] = ' '.join(result[1::])

    # Check params to make sure it got replaced
    checkParams(params,'PHI',0)
    checkParams(params,'VOLUME',0)
    checkParams(params,'THICKNESS',0)
    checkParams(params,'FORMULA','NA')
    checkParams(params,'EDGE','NA')
    checkParams(params,'FLUOR',0)
    return params

def write_sab(params,paths=None):
    """Write sabc.inp file

    Sabcor params file contains the require parameters:
    PHI, VOLUME, THICKNESS, FORMULA, EDGE, FLUOR

    Args:
        params (dicts): params for sabcor input file
        paths (str, optional): file path for sabcor.inp. Defaults to None.
    """
    # Write the file
    if paths == None:
        paths = pathlib.Path.cwd() / 'sab.inp'

    print(paths)
    with open(paths, 'w', encoding='utf-8') as f:
        f.write('PHI ' + str(params['PHI']) + '\n')
        f.write('VOLUME ' + str(params['VOLUME']) + '\n')
        f.write('THICKNESS ' + str(params['THICKNESS']) + '\n')
        f.write('FORMULA ' + str(params['FORMULA']) + '\n')
        f.write('EDGE ' + str(params['EDGE']) + '\n')
        f.write('FLUOR ' + str(params['FLUOR']) + '\n')

def call_executable(excut_paths,sac_file):
    # Call the subprocess
    subprocess.run([excut_paths,str(sac_file)])

def calculate_header(file_loc,return_lines=False):
    i = 0
    with open(file_loc) as file:
        for line in file:
            # print(line)
            if line.rstrip()[0] == "#":
                i = i + 1
    with open(file_loc) as file:
        data_lines = file.readlines()

    if return_lines:
        return i,data_lines
    else:
        return i

def edited_final_header(file_input):
    post_sabcor_file = os.path.splitext(file_input)
    file_sac_input = post_sabcor_file[0] + "_sac" + post_sabcor_file[1]

    # print(post_sabcor_file)

    header_before = calculate_header(file_input)
    header_after,data_lines = calculate_header(file_sac_input,return_lines=True)
    # print(header_after)
    diff_line = np.arange(header_before,header_after)

    with open(file_sac_input,'w') as outfile:
        for pos,line in enumerate(data_lines):
            if pos not in diff_line:
                outfile.write(line)

def calculate_dataline(dataline: str):
    """Helper functions to convert the dataline and calcualte the unwind value

    Args:
        dataline (str): str with the data line

    Returns:
        str: str with the unwind value
    """
    data_arr = re.split("\s+",dataline.strip())

    data_k = float(data_arr[0])
    data_kchi = float(data_arr[1])
    data_chi = data_kchi / data_k

    return f'  {data_k:.6e}   {data_chi:.6e}\n'

def unwind_K(file_input):
    """
    Unwind the k part from the post sabcor file

    After running sabcor, the data will become k, k*chi, we need to divided the k*chi by k to get the chi by itself.

    Args:
        file_input (str): file name of the input file
    """
    post_sabcor_file = os.path.splitext(file_input)
    file_sac_input = post_sabcor_file[0] + "_sac" + post_sabcor_file[1]

    header_after,data_lines = calculate_header(file_sac_input,return_lines=True)

    for i in range(header_after,len(data_lines)):
        data_lines[i] = calculate_dataline(data_lines[i])

    with open(file_sac_input,'w') as outfile:
        for line in data_lines:
            outfile.write(line)

def main():
    excut_paths = check_executable()
    args = get_args()

    data_file = args.file
    sabcor_inp = args.sabcor_inp_file

    params = read_sab(sabcor_inp)
    write_sab(params)
    call_executable(excut_paths,data_file)
    edited_final_header(data_file)
    unwind_K(data_file)
if __name__ == '__main__':
    main()
