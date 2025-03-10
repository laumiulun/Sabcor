
import re

def read_feff_header(filename):
    """
    Reads the header from a Feff file.
    Returns ierr, title, ntit, feff_ver, r_pair
    """
    ierr = 0
    title = []
    ntit = 0
    feff_ver = ''
    r_pair = 0.0

    try:
        with open(filename, 'r') as f:
            lines = f.readlines()

        # Initialize variables
        feff_file = False
        temp = ''
        iver = -1
        ntit = 0
        r_pair = 0.0

        # Read first line and determine Feff version
        title_line = lines[0].strip()
        title.append(title_line)
        ntit += 1

        # Find 'Feff' in the first line
        iver = title_line.lower().find('feff ')
        if iver == -1:
            print('ERROR in read_feff_header')
            print(f"Read in file generated by {title_line}")
            print('WARNING: version not supported, check output...')
            print('Specifically, the phase may be defined differently.')
            print('Assuming Feff 5 or later version.')
            feff_ver = '5'  # Default to Feff 5
        else:
            # Extract version number
            feff_ver_str = title_line[iver:].split()[1]
            feff_ver = feff_ver_str[0]  # Take the first character as version
            # Check if the version is supported
            supported_versions = ['5', '6', '7', '8', '9', '10']
            if feff_ver not in supported_versions:
                print(f"Read in file generated by {title_line}")
                print('WARNING: version not supported, check output...')
                print('Specifically, the phase may be defined differently.')
                print('Assuming Feff 5 or later version.')
                feff_ver = '5'  # Default to Feff 5

        # Start reading subsequent lines
        idx = 1  # Current line index
        total_lines = len(lines)

        # Skip to the 'paths' section
        while idx < total_lines:
            temp = lines[idx].strip()
            if 'file' in temp.lower() and 'sig2' in temp.lower():
                break
            if 'path' in temp.lower():
                break
            idx += 1

        if 'path' in temp.lower():
            # Feffxxxx.dat file
            feff_file = True
            title.append(temp)
            ntit += 1
        else:
            # chi.dat file
            idx += 1
            if idx < total_lines:
                temp = lines[idx].strip()
                title.append(temp)
                ntit += 1
                # Extract r_pair from this line
                match = re.search(r'(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)', temp)
                if match:
                    r_pair = float(match.group(6))
                idx += 1

            # Read until 'paths used' is found
            while idx < total_lines:
                temp = lines[idx].strip()
                if 'paths used' in temp.lower():
                    break
                title.append(temp)
                ntit += 1
                idx += 1

        # Read until '------' is found
        while idx < total_lines and '------' not in lines[idx]:
            temp = lines[idx].strip()
            if feff_file:
                title.append(temp)
                ntit += 1
            idx += 1

        idx += 1  # Skip '------' line

        if feff_file and idx < total_lines:
            temp = lines[idx].strip()
            ntit += 1
            title.append(temp)
            idx += 1

            # Check if 'nleg' is in the line
            if 'nleg' in temp.lower():
                # Read nleg, l, r_pair
                tokens = temp.split()
                if len(tokens) >= 3:
                    nleg = int(tokens[0])
                    l_value = float(tokens[1])
                    r_pair = float(tokens[2])

                # Skip atom coordinates header and data
                for _ in range(nleg):
                    if idx < total_lines:
                        temp = lines[idx].strip()
                        ntit += 1
                        title.append(temp)
                        idx += 1
                    else:
                        break

                # Skip data header (one more line)
                if idx < total_lines:
                    temp = lines[idx].strip()
                    idx += 1

        ierr = 0

    except Exception as e:
        print(f'Error reading Feff header: {e}')
        ierr = 2

    return ierr, title, ntit, feff_ver, r_pair
