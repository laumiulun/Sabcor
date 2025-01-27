def stringlen(string):
    """
    Returns the actual length of the string, assuming the end is padded with spaces.
    
    Parameters:
    string : str
        The input string, possibly padded with spaces at the end.
    
    Returns:
    int
        The length of the string without trailing spaces.
    """
    length = len(string)
    
    while length > 0 and string[length - 1] == ' ':
        length -= 1
    
    return length
