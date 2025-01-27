import numpy as np

def spline(x, y, yp1, ypn):
    """
    Calculates the second derivatives of a cubic spline interpolation
    for a given set of data points.

    Parameters:
    x : array_like
        Independent variable data points (must be increasing).
    y : array_like
        Dependent variable data points.
    yp1 : float
        First derivative at the first point. Set to a large value (e.g., > 0.99e30)
        for a natural spline boundary condition (second derivative zero).
    ypn : float
        First derivative at the last point. Set to a large value (e.g., > 0.99e30)
        for a natural spline boundary condition (second derivative zero).

    Returns:
    y2 : ndarray
        Second derivatives of the interpolating function at the data points.
    """
    # Ensure all inputs are float64
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    yp1 = np.float64(yp1)
    ypn = np.float64(ypn)

    n = len(x)
    y2 = np.zeros(n, dtype=np.float64)
    u = np.zeros(n - 1, dtype=np.float64)  # Temporary array for calculations

    # Boundary condition at the first point
    if yp1 > np.float64(0.99e30):  #Natural spline condition
        y2[0] = np.float64(0.0)
        u[0] = np.float64(0.0)
    else:
        y2[0] = np.float64(-0.5)
        u[0] = np.float64((3.0 / (x[1] - x[0])) * ((y[1] - y[0]) / (x[1] - x[0]) - yp1))

    # Loop through the interior points to compute second derivatives
    for i in range(1, n - 1):
        sig = np.float64((x[i] - x[i - 1]) / (x[i + 1] - x[i - 1]))
        p = np.float64(sig * y2[i - 1] + 2.0)
        y2[i] = np.float64((sig - 1.0) / p)
        u[i] = np.float64(((6.0 * ((y[i + 1] - y[i]) / (x[i + 1] - x[i]) -
                                   (y[i] - y[i - 1]) / (x[i] - x[i - 1])) /
                            (x[i + 1] - x[i - 1]) - sig * u[i - 1]) / p))

    # Boundary condition at the last point
    if ypn > np.float64(0.99e30):
        qn = np.float64(0.0)
        un = np.float64(0.0)
    else:
        qn = np.float64(0.5)
        un = np.float64((3.0 / (x[n - 1] - x[n - 2])) *
                        (ypn - (y[n - 1] - y[n - 2]) / (x[n - 1] - x[n - 2])))

    y2[n - 1] = np.float64((un - qn * u[n - 2]) / (qn * y2[n - 2] + 1.0))

    # Back-substitution to compute the second derivatives
    for k in range(n - 2, -1, -1):
        y2[k] = np.float64(y2[k] * y2[k + 1] + u[k])

    return y2
