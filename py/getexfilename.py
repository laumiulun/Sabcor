import sys
import os
import glob
from get_type import get_type
from exafs import DATA_DIR, FILENAME_LEN


def getexfilename():
    """
    Interactively obtains a filename and file type from the user.
    It first checks for command-line arguments and then prompts the user
    for inputs if necessary.

    Returns:
    - filename: The full path to the selected file.
    - file_type: The type of the file (e.g., 'ds', 'es', 'ks', 'rs').
    """
    field_num = 1
    filename = ''
    file_type = ''
    sub_dir = ''
    data_dir = ''
    num_fields = len(sys.argv) - 1  # Exclude the script name

    # Check for command-line arguments
    if num_fields >= field_num:
        filename = sys.argv[field_num]
        if not os.path.isfile(filename):
            print(f'File does not exist: {filename}')
            sys.exit(0)
        field_num += 1
        file_type = get_type(filename)
        return filename, file_type
    elif num_fields > 0:
        sys.exit(0)

    # Get the data directory from environment variable or use default
    data_dir = os.getenv('EXDATA_DIR')
    if data_dir is None:
        data_dir = DATA_DIR  # Use default from header file

    while True:  # Outer loop for subdirectory
        sub_dir_input = input('Input exdata subdirectory: [RET=cwd, ?=list] ')
        if sub_dir_input.strip() == '?':
            # List the contents of the data directory
            try:
                subdirs = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]
                print('Available subdirectories:')
                for d in subdirs:
                    print(d)
            except FileNotFoundError:
                print(f'Data directory {data_dir} does not exist.')
            continue
        sub_dir_input = sub_dir_input.strip()
        if sub_dir_input == '':
            # Use current working directory
            sub_dir = os.getcwd()
        else:
            sub_dir = os.path.join(data_dir, sub_dir_input)
            if not os.path.isdir(sub_dir):
                print(f'{sub_dir} directory does not exist.')
                continue
        # Now prompt for file type
        while True:  # Inner loop for file type
            file_type = input('Input file type: (ds, es, ks, rs, !): ').strip()
            if file_type in ['ds', 'es', 'ks', 'rs']:
                break  # Valid file type, proceed
            elif file_type == '!':
                # Go back to outer loop to prompt for subdirectory
                break
            else:
                print(f'{file_type} is not understood.')
                continue  # Prompt for file type again
        if file_type == '!':
            continue  # Go back to prompt for subdirectory
        else:
            # Construct subdirectory including file_type
            sub_dir = os.path.join(sub_dir, file_type)
            if not os.path.isdir(sub_dir):
                print(f'{sub_dir} directory does not exist.')
                continue  # Go back to file type prompt
            # Now proceed to prompt for filename
            while True:
                filename_input = input('Name of file (?=dir,!): ').strip()
                if filename_input == '?':
                    wildcard = input('Wild Card: [RET=*] ').strip()
                    if wildcard == '':
                        wildcard = '*'
                    # List files matching the wildcard
                    matching_files = [os.path.basename(f) for f in
                                      glob.glob(os.path.join(sub_dir, wildcard))]
                    print('Matching files:')
                    for f in matching_files:
                        print(f)
                    continue  # Go back to prompt for filename
                elif filename_input == '!':
                    break  # Go back to prompt for subdirectory
                elif filename_input == '':
                    print('Please start name with legal character.')
                    continue  # Prompt for filename again
                else:
                    filename = os.path.join(sub_dir, filename_input)
                    if not os.path.isfile(filename):
                        print(f'File does not exist: {filename}')
                        continue  # Go back to prompt for filename
                    file_type = get_type(filename)
                    return filename, file_type
            # If we reach here, user entered '!' and we need to go back to prompt for subdirectory
            continue  # Go back to outer loop