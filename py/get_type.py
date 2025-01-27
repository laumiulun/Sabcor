import os

def get_type(filename):
    """
    Determines the file type based on the filename or current working directory.
    Returns file_type as a string ('ds', 'es', 'ks', 'rs') or None if not found.
    """
    string = filename

    for type_code in ['/ds/', '/es/', '/ks/', '/rs/']:
        type_pos = string.find(type_code)
        if type_pos != -1:
            # Extract the file type from the match
            file_type = type_code.strip('/')
            return file_type

    string = os.getcwd()
    base_dir = os.path.basename(string)
    # Get the last two characters of the base directory name
    file_type = base_dir[-2:]
    if file_type in ('ds', 'es', 'ks', 'rs'):
        return file_type
    else:
        return None
