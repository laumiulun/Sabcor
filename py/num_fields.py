def num_fields(ascii_line):
    """
    Determines the number of separate fields in an ASCII line.
    Fields are separated by spaces, commas, or tabs.

    Parameters:
    ascii_line (str): The input ASCII line as a string.

    Returns:
    int: The number of separate fields in the line.
    """
    itemp = 0
    new = True  # Indicates if the previous character was a delimiter
    delimiters = {' ', ',', '\t'}  # Set of delimiter characters

    for char in ascii_line:
        if char in delimiters:
            new = True
        else:
            if new:
                itemp += 1  # Increment field count at the start of a new field
            new = False  # We are inside a field

    return itemp
