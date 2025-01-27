def splint(xa, ya, y2a, x):
    """
    Performs cubic spline interpolation for a given x-value using the
    precomputed second derivatives y2a.

    Parameters:
    xa : array_like
        Independent variable data points (must be increasing).
    ya : array_like
        Dependent variable data points.
    y2a : array_like
        Second derivatives of the interpolating function at the data points,
        as computed by the spline function.
    x : float
        The x-value where interpolation is desired.

    Returns:
    y : float
        Interpolated y-value at x.
    """
    n = len(xa)
    klo = 0
    khi = n - 1

    # Binary search to find the right place in the table
    while khi - klo > 1:
        k = (khi + klo) // 2
        if xa[k] > x:
            khi = k
        else:
            klo = k

    h = xa[khi] - xa[klo]
    if h == 0.0:
        raise ValueError("Bad xa input to splint: h=0")

    a = (xa[khi] - x) / h
    b = (x - xa[klo]) / h
    y = (a * ya[klo] + b * ya[khi] +
         ((a**3 - a) * y2a[klo] + (b**3 - b) * y2a[khi]) * (h**2) / 6.0)
    return y
