
def file_ascii(filename):
    """
    Determines whether a file is a "gnu"-type ASCII file based on its first character.
    Returns True if the file is ASCII (starts with '#'), False otherwise.
    """
    try:
        with open(filename, 'r') as f:
            first_line = f.readline()
            if first_line.startswith('#'):
                return True
            else:
                return False
    except Exception as e:
        print(f'Error opening file {filename}: {e}')
        return False
