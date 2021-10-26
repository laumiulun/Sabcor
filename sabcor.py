# sabcor Wrapper files
import pathlib
import argparse
import subprocess
import shutil
def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store_true')
    # parser.add_argument('-a', action='store_true')
    parser.add_argument('file',type=str)
    # parser.add_argument('output_file',type=str)
    parser.add_argument('sabcor_inp_file',nargs='?',type=str,default='sab.inp')

    args = parser.parse_args()

    return args

def check_executable():
    """
    Check if executable exists
    """
    excut_paths = pathlib.Path.cwd() / 'bin/sabcor'
    exists = excut_paths.is_file()
    # Compile sabcor
    if exists == False:
        subprocess.run(['make'])

    return excut_paths
def if_params(full_params,params_name,params):
    if params[0] == params_name:
        full_params[params_name] = params[1]

    return full_params

def checkParams(params,params_name,default):
    if params[params_name] == default:
        print('Missing ' + params_name + ' !')
        exit()
def read_sab(file):
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

def write_sab(params):
    """
    Move SAB input file
    """
    # Write the file
    with open('sab_test.inp', 'w', encoding='utf-8') as f:
        f.write('PHI ' + str(params['PHI']) + '\n')
        f.write('VOLUME ' + str(params['VOLUME']) + '\n')
        f.write('THICKNESS ' + str(params['THICKNESS']) + '\n')
        f.write('FORMULA ' + str(params['FORMULA']) + '\n')
        f.write('EDGE ' + str(params['EDGE']) + '\n')
        f.write('FLUOR ' + str(params['FLUOR']) + '\n')

def call_executable(excut_paths,sac_file):
    # Call the subprocess
    subprocess.run([excut_paths,str(sac_file)])


def main():
    """
    To do

    1.  Need to strip the header
    2.  Unwind the K
    """
    excut_paths = check_executable()
    args = get_args()

    data_file = args.file
    sabcor_inp = args.sabcor_inp_file
    print(data_file)
    print(sabcor_inp)
    params = read_sab(sabcor_inp)
    # print(params)
    write_sab(params)
    call_executable(excut_paths,data_file)

if __name__ == '__main__':
    main()
