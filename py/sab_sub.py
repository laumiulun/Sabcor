import math
import numpy as np
import re

# Constants from exafs.hf
from exafs import PI, EV2ANG, EV2INVANG, MAX_TIT, FORMULA_LEN, EDGE_LEN, MAX_SYMS, AVOGADRO, VERSION
from stringlen import stringlen
from atomic_sub import get_atomic, form2sym, sym2Z
from mod_mucal import mucal

PI = np.float64(PI)
EV2ANG = np.float64(EV2ANG)
EV2INVANG = np.float64(EV2INVANG)

def lowercase(x):
    """
    Checks if a character is a lowercase letter.
    """
    return x.islower()

def uppercase(x):
    """
    Checks if a character is an uppercase letter.
    """
    return x.isupper()

def a_number(x):
    """
    Checks if a character is a digit or a decimal point.
    """
    return x.isdigit() or x == '.'

def fluor_corr(k, kchi_r, kchi_i, nf, nx, title, ntit, d, phi, theta,
               formvol, formula, edge, fluor_energy, concentration,
               io, option, elements):
    """
    Corrects for self-absorption in fluorescence measurements.
    """
    # Ensure inputs are float64
    k = np.asarray(k, dtype=np.float64)
    kchi_r = np.asarray(kchi_r, dtype=np.float64)
    kchi_i = np.asarray(kchi_i, dtype=np.float64)
    d = np.float64(d)
    phi = np.float64(phi)
    theta = np.float64(theta)
    formvol = np.float64(formvol)
    fluor_energy = np.float64(fluor_energy)
    concentration = np.float64(concentration)

    # Convert angles to radians
    phi_rad = np.float64(2.0 * PI * phi / 360.0)
    if theta < -1000.0:
        theta_rad = np.float64(PI / 2.0 - phi_rad)
    else:
        theta_rad = np.float64(2.0 * PI * theta / 360.0)

    g = np.sin(phi_rad) / np.sin(theta_rad)

    # Get atomic number Z, edge energy e_not, and edge code edge_code
    Z, e_not, edge_code = get_atomic(edge)
    e_not = np.float64(e_not)

    # Open output file if needed
    if io in ['f', 'a']:
        print('Outputting self-absorption correction to sab_cor.dat')
        sab_cor_file = open('sab_cor.dat', 'w')
        sab_cor_file.write('#\tk\tcorrection_coeff\tinfo_depth (Angstroms)\n')

    isthick = False
    for idat in range(nx):
        # Ensure k[idat] is non-negative
        k[idat] = np.float64(k[idat])
        if k[idat] >= 0.0:
            energy = e_not + (k[idat] / EV2INVANG) ** 2.0
        else:
            print(f'Trouble in fluor_corr? k={k[idat]}')
            continue

        # Get absorption coefficients
        tot_abs, fluor_abs, atomic_abs = get_mus(formula, edge, energy, fluor_energy, concentration, formvol, elements)


        # Compute chi
        chi = np.float64(kchi_r[idat]) / k[idat]

        # Correct chi
        new_chi, ierr = corr_chi(
            k[idat], chi, tot_abs, atomic_abs, fluor_abs,
            d * 1.0e-8, phi_rad, theta_rad, g, option)
        

        if ierr == 0 and isthick:
            continue
        elif ierr == 1 and not isthick:
            isthick = True

        correction = new_chi / chi

        kchi_r[idat] = new_chi * k[idat]


        # Correct imaginary part if present
        if nf in [2, 12]:
            kchi_i[idat] = correction * kchi_i[idat]

        # Compute information depth
        temp = 1.0e8 * info_depth(tot_abs, fluor_abs, phi_rad, theta_rad, g)
        if k[idat] <= 5.0:
            corr_at_5 = correction
            info_at_5 = temp

        # Write to file if needed
        if io in ['f', 'a']:
            sab_cor_file.write(f'{k[idat]}\t{correction}\t{temp}\n')

    # Close output file
    if io in ['f', 'a']:
        sab_cor_file.close()

    # Construct title messages
    tempstring = f'{corr_at_5:6.3f}'
    title_message_1 = f'Self-absorption corrected with {VERSION}, corr at 5 inv ang= {tempstring}'
    tempstring = f'{d:6.0f}'
    title_message_2 = f'using formula={formula} and thickness={tempstring} Angstroms.'

    # Combine the messages into a single large string
    info_string = (
        '\n# ----------------------------------------------------\n'
        f'# {title_message_1}\n'
        f'# {title_message_2}\n'
        '# ----------------------------------------------------\n'
    )

    # Print title messages explicitly
    # if io in ['p', 'a']:
    #     print('\n# ----------------------------------------------------')
    #     print(f'# {title_message_1}')
    #     print(f'# {title_message_2}')
    #     print('# ----------------------------------------------------')

    # Write title messages to file
    if io in ['f', 'a']:
        with open('sab_cor.dat', 'a') as sab_cor_file:
            sab_cor_file.write('# ----------------------------------------------------\n')
            sab_cor_file.write(f'# {title_message_1}\n')
            sab_cor_file.write(f'# {title_message_2}\n')
            sab_cor_file.write('# ----------------------------------------------------\n')

    # Print statistics
    if io in ['p', 'a']:
        print('\nSelf-Absorption correction statistics:\n')
        print(f'info depth at 5 inv ang:                  {info_at_5:8.1f} Angstroms')
        print(f'correction chi_true/chi_exp at 5 inv ang: {corr_at_5:6.2f}\n')
    return kchi_r, info_string

def info_depth(tot_abs, fluor_abs, phi, theta, g):
    """
    Calculates the information depth.

    Parameters:
    - tot_abs: Total absorption coefficient (float64).
    - fluor_abs: Fluorescence absorption coefficient (float64).
    - phi: Angle of incident beam in radians (float64).
    - theta: Angle of exit beam in radians (float64).
    - g: sin(phi)/sin(theta) (float64).

    Returns:
    - info_depth: Information depth (float64).
    """
    # Ensure inputs are numpy float64
    tot_abs = np.float64(tot_abs)
    fluor_abs = np.float64(fluor_abs)
    phi = np.float64(phi)
    g = np.float64(g)

    # Calculate information depth
    tcrazy = np.sin(phi) / (tot_abs + fluor_abs * g)
    
    # Debugging: Check for invalid values
    if tcrazy < 0.0:
        print(f"DEBUG: Negative info_depth value. phi={phi}, g={g}, tot_abs={tot_abs}, fluor_abs={fluor_abs}")

    return tcrazy


import numpy as np

def corr_chi(k, chi_exp, mu_t, mu_a, mu_f, d_given, phi, theta, g, option):
    """
    Corrects the experimental chi value for self-absorption.

    Parameters:
    - k: Wavevector value (float64)
    - chi_exp: Experimental chi value (float64)
    - mu_t: Total absorption coefficient of the material (float64)
    - mu_a: Absorbing atom's contribution to mu_t (float64)
    - mu_f: Absorption at the fluorescence energy (float64)
    - d_given: Thickness of the material in cm (float64)
    - phi: Angle of incident beam in radians (float64)
    - theta: Angle of exit beam in radians (float64)
    - g: sin(phi) / sin(theta) (float64)
    - option: 'u' to undo correction, otherwise apply correction (str)

    Returns:
    - chi: Corrected chi value (float64)
    - ierr: Error code (0 for OK, 1 if thick limit was used)
    """
    import numpy as np

    ierr = 0

    k       = np.float64(k)
    chi_exp = np.float64(chi_exp)
    mu_t    = np.float64(mu_t)
    mu_a    = np.float64(mu_a)
    mu_f    = np.float64(mu_f)
    d       = np.float64(d_given)
    phi     = np.float64(phi)
    g       = np.float64(g)

    alpha = mu_t + mu_f * g
    beta  = alpha * mu_a * d * np.exp(-alpha * d / np.sin(phi)) / np.sin(phi)
    gamma = 1.0 - np.exp(-alpha * d / np.sin(phi))

    if option == 'u':
        thick = chi_exp * (alpha - mu_a) / (alpha + chi_exp * mu_a)
    else:
        thick = chi_exp / (1.0 - mu_a * (1.0 + chi_exp) / alpha)

    crit1 = (4.0 * beta * alpha * gamma * chi_exp) / (
             gamma * (alpha - mu_a * (chi_exp + 1.0)) + beta
            )
    crit2 = beta

    # Start with either the nearly-exact expression or the thick-limit approximation
    if abs(crit1) > 1.0e-7 and abs(crit2) > 1.0e-7 and d <= 0.01:
        if option == 'u':
            F = gamma * mu_a / (2.0 * beta)
            E = -(gamma * (alpha - mu_a) + beta) / (2.0 * beta)
            H = alpha * gamma / beta
            chi = (chi_exp * (chi_exp - 2.0 * E)) / (2.0 * F * chi_exp + H)
        else:
            chi = - (gamma * (alpha - mu_a * (chi_exp + 1.0)) + beta)
            chi = chi + np.sqrt(chi**2 + 4.0 * beta * alpha * gamma * chi_exp)
            chi = chi / (2.0 * beta)

        # ---------------------------------------------------------------------
        #  Add the final iterative refinement to match Fortran exactly:
        #  (Fortran's do-while loop up to 200 iterations)
        # ---------------------------------------------------------------------
        jj = 0
        while jj < 200:
            # Compute the "trial" chi_exp for our current guess of chi:
            chi_exp_trial = (
                (1.0 - np.exp(-(alpha + chi * mu_a) * d / np.sin(phi)))
                / (1.0 - np.exp(-alpha * d / np.sin(phi)))
                * (alpha * (chi + 1.0)) / (alpha + chi * mu_a)
                - 1.0
            )

            # Check difference against the real chi_exp
            diff = chi_exp - chi_exp_trial
            if abs(diff) < 1.0e-7:
                break

            # Update chi
            chi += diff
            jj += 1

        error = abs(chi_exp - chi_exp_trial)
        if error > 1.0e-6:
            print(f"DEBUG: k={k}, error={error}, jj={jj}")

    else:
        chi = thick
        ierr = 1

    return chi, ierr




def get_mus(formula, edge, energy, fluor_energy, concentration, formvol, elements):
    """
    Calculates total absorption (tot_abs), fluorescence absorption (fluor_abs),
    and atomic absorption (atomic_abs).
    """
    # Ensure inputs are float64
    energy = np.float64(energy)
    fluor_energy = np.float64(fluor_energy)
    concentration = np.float64(concentration)
    formvol = np.float64(formvol)

    symbols, num_sym, tot_syms = form2sym(formula)
    atomic_sym = get_atomic_symbol_from_edge(edge, formula)

    # Calculate total absorption at energy and fluorescence energy
    tot_abs = get_tot_abs(formula, energy, formvol, elements)
    fluor_abs = get_tot_abs(formula, fluor_energy, formvol, elements)

    # Calculate atomic absorption
    r1 = get_tot_abs(atomic_sym, energy, formvol, elements)
    r2 = get_noedge_abs(atomic_sym, energy, formvol, elements)
    if concentration < 0.0:
        atomic_abs = r1 - r2
    else:
        atomic_abs = concentration * (r1 - r2)

    return tot_abs, fluor_abs, atomic_abs



def get_atomic_symbol_from_edge(edge, formula):
    """
    Extracts the atomic symbol (with count if any) from the edge string
    and validates it against the formula.

    Parameters:
    - edge: The edge string (e.g., 'Cu K').
    - formula: The chemical formula (e.g., 'Cu2O').

    Returns:
    - atomic_sym: The symbol of the absorbing atom with its count (e.g., 'Cu2').

    Raises:
    - ValueError: If the atomic symbol cannot be found in the formula.
    """
    # Split the edge string to extract the atomic symbol
    parts = edge.strip().split()
    if len(parts) < 2:
        raise ValueError(f"Invalid edge format: {edge}. Must include an element symbol and an edge type.")

    element_symbol = parts[0]  # e.g., 'Cu' from 'Cu K'

    # Find the symbol in the formula
    index_in_formula = formula.find(element_symbol)
    if index_in_formula == -1:
        raise ValueError(f"Element {element_symbol} from edge '{edge}' not found in formula '{formula}'.")

    # Extract the symbol and its count from the formula
    match = re.match(rf"({element_symbol})(\d*\.?\d*)", formula[index_in_formula:])
    if match:
        atomic_sym = match.group(0)  # 'Cu3' if formula contains 'Cu3O2'
    else:
        atomic_sym = element_symbol  # Default to 'Cu' if no count is specified

    return atomic_sym


def get_tot_abs(formula, energy, formvol, elements):
    """
    Calculates the total absorption coefficient for a given formula and energy.

    Parameters:
    - formula: chemical formula of the sample (str)
    - energy: energy at which to calculate absorption (in eV)
    - formvol: formula unit volume (in cubic Angstroms)
    - elements: dictionary containing element-specific data (for mucal)

    Returns:
    - cross_section: total absorption coefficient (in inverse cm)
    """
    # Break down the formula
    symbols, num_sym, _ = form2sym(formula)

    # In Fortran, density(...) returns the sum of num_sym(i)/formvol
    conv_density = density(formula, formvol)

    cross_section = 0.0

    # Loop over each symbol in the formula
    for sym, n in zip(symbols, num_sym):
        Z = sym2Z(sym)

        # mucal returns a tuple, e.g. ([xsec array], [e_nots], [fly], errcode)
        xsec_tuple = mucal(
            mane=elements[Z]["name"],
            z=Z,
            en=energy / 1000.0,  # convert eV -> keV
            elements=elements
        )

        # The first item in the tuple (xsec_tuple[0]) is the main cross-section list.
        # The 4th element in that list (index 3 in Python) should match xsec(4) in Fortran.
        temp = xsec_tuple[0][3]  # total cross section in barns/atom

        # Multiply by (n * conv_density) to get cm^-1, assuming you handle barn->cm² elsewhere
        mu_Z = n * conv_density * temp

        # Accumulate the total absorption
        cross_section += mu_Z

    return cross_section


def density(formula, formvol):
    """
    Returns the density in units of (atoms) per (barn cm), which
    is effectively atoms per cubic angstrom in this code.

    Parameters:
    - formula: The chemical formula of your sample (str).
    - formvol: The formula unit volume (in cubic Angstroms).

    Returns:
    - The sum of (atomic counts / formvol), i.e. the total atoms
      per formula unit volume.
    """
    _, num_sym, tot_syms = form2sym(formula)
    
    temp = 0.0
    for i in range(tot_syms):
        temp += num_sym[i] / formvol
    
    return temp




def get_noedge_abs(formula, energy, formvol, elements):
    """
    Calculates the absorption coefficient excluding the current absorption edge.
    """
    energy = np.float64(energy)
    formvol = np.float64(formvol)

    symbols, num_sym, _ = form2sym(formula)
    cross_section = np.float64(0.0)

    for sym, num in zip(symbols, num_sym):
        Z = sym2Z(sym)
        mane = elements[Z]["name"]
        xsec, _, _, _ = mucal(mane, Z, energy / 1000.0, elements)  # Convert eV to keV
        temp = xsec[10]  # Accessing the 11th element of the first list in mucal's output

        # Convert to inverse cm using density
        conversion = np.float64(num / formvol)  # Atoms per cubic angstrom
        mu_Z = conversion * temp  # Multiply by cross-section
        cross_section += mu_Z

    return cross_section



