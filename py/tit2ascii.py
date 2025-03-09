from exafs import TIT_LEN

def tit2ascii(f, tit, ntit):
    """
    Writes the titles from the list 'tit' to a file object 'f', 
    each prefixed with '# ' and formatted to TIT_LEN characters.
    After writing all titles, it writes a separator line.

    Parameters:
    - f: File object opened for writing.
    - tit: List of title strings.
    - ntit: Number of titles to write from the 'tit' list.
    """
    for i in range(ntit):
        # Ensure the title is exactly TIT_LEN characters
        title_line = tit[i][:TIT_LEN].ljust(TIT_LEN)
        # Write the formatted title to the file with a '# ' prefix
        f.write('# ' + title_line + '\n')
    # Write the separator line
    f.write('# ----------------------------------------------------\n')
