import os

def check_edge_string(edge):
    """
    Validates the edge string.

    For simplicity, this function will check if the edge string is non-empty.

    Returns True if valid, False otherwise.
    """
    if edge and isinstance(edge, str):
        return True
    else:
        return False

def readinp(inp_filename):
    """
    Reads input directions from inp_filename. Input is in the form of
    "cards" with information following the cards. Allowed cards are:

    THICKNESS, PHI, ABC, FORMULA, EDGE, FLUOR_ENERGY, CONCENTRATION

    Returns a dictionary with the parameters.

    Raises:
        FileNotFoundError: If the input file does not exist.
        ValueError: If the edge string is invalid.
    """
    # Initialize variables
    d = None
    phi = None
    theta = -10000.0  # default value indicating THETA not specified
    a = b = c = None
    formvol = None
    formula = ''
    edge = ''
    fluor_energy = None
    concentration = -1.0  # default value indicating not specified

    # Check if file exists
    if not os.path.exists(inp_filename):
        raise FileNotFoundError(f"File does not exist: {inp_filename}")

    # Open the file
    with open(inp_filename, 'r') as f:
        for line in f:
            ascii_line = line.rstrip('\n')
            if ascii_line.startswith('THICKNESS '):
                try:
                    d = float(ascii_line[10:].strip())
                except ValueError:
                    print("Error parsing THICKNESS value.")
            elif ascii_line.startswith('PHI '):
                try:
                    phi = float(ascii_line[4:].strip())
                except ValueError:
                    print("Error parsing PHI value.")
            elif ascii_line.startswith('THETA '):
                try:
                    theta = float(ascii_line[6:].strip())
                except ValueError:
                    print("Error parsing THETA value.")
            elif ascii_line.startswith('ABC '):
                parts = ascii_line[4:].strip().split()
                a = float(parts[0])
                b = float(parts[1])
                c = float(parts[2])
                formvol = a * b * c  # Calculate formvol explicitly from lattice parameters.
            elif ascii_line.startswith('VOLUME '):
                formvol = float(ascii_line[7:].strip())
            elif ascii_line.startswith('FORMULA '):
                formula = ascii_line[8:].strip()
            elif ascii_line.startswith('EDGE '):
                edge = ascii_line[5:12].strip()
            elif ascii_line.startswith('FLUOR '):
                try:
                    fluor_energy = float(ascii_line[6:].strip())
                except ValueError:
                    print("Error parsing FLUOR_ENERGY value.")
            elif ascii_line.startswith('CONCENTRATION '):
                try:
                    concentration = float(ascii_line[13:].strip())
                except ValueError:
                    print("Error parsing CONCENTRATION value.")
            # Continue reading lines

    # Check edge string
    if not check_edge_string(edge):
        raise ValueError("Trouble with edge string.")

    # Return the parameters
    return {
        'd': d,
        'phi': phi,
        'theta': theta,
        'a': a,
        'b': b,
        'c': c,
        'formvol': formvol,
        'formula': formula,
        'edge': edge,
        'fluor_energy': fluor_energy,
        'concentration': concentration,
    }
