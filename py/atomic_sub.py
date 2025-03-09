import re

# c	given two chacacter sym, returns Z (atomic number).  Only has first
# c	100 elements of periodic table.
# c
# c	Returns -1 if element not found
# c
# c	Last modified by Corwin Booth 2/24/93
#   1/9/2025 Levi Recla translation from Fortran to Python
# c
# c*****************************************************************************

# Constants
MAX_Z = 100
MAX_SYMS = 20

# List of element symbols from Z=1 to Z=100
symbols = [
    'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne',
    'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca',
    'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',
    'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr',
    'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn',
    'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd',
    'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb',
    'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg',
    'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th',
    'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm'
]

# Create mapping from symbol to atomic number Z
symbol_to_Z = {symbol.capitalize(): Z for Z, symbol in enumerate(symbols, start=1)}

# Atomic weights for elements Z=1 to Z=100
atomic_weights = [
    1.008, 4.003, 6.940, 9.012, 10.811, 12.011, 14.007,
    15.999, 18.998, 20.180, 22.990, 24.305, 26.982, 28.085, 30.974,
    32.065, 35.453, 39.948, 39.098, 40.078, 44.956, 47.867, 50.942,
    51.996, 54.938, 55.845, 58.933, 58.693, 63.546, 65.380,
    69.723, 72.640, 74.922, 78.960, 79.904, 83.798, 85.468,
    87.620, 88.906, 91.224, 92.906, 95.940, 98.000, 101.070,
    102.906, 106.420, 107.868, 112.411, 114.818, 118.710,
    121.760, 127.600, 126.904, 131.293, 132.905, 137.327,
    138.906, 140.116, 140.908, 144.242, 145.000, 150.360,
    151.964, 157.250, 158.925, 162.500, 164.930, 167.259,
    168.934, 173.055, 174.967, 178.490, 180.948, 183.840,
    186.207, 190.230, 192.217, 195.084, 196.967, 200.592,
    204.383, 207.200, 208.980, 209.000, 210.000, 222.000,
    223.000, 226.000, 227.000, 232.038, 231.036, 238.029,
    237.000, 244.000, 243.000, 247.000, 247.000, 251.000,
    252.000, 257.000
]

# Functions
def sym2Z(sym):
    """
    Given an element symbol, returns its atomic number Z.
    Returns -1 if the element is not found.
    """
    sym = sym.strip().capitalize()
    return symbol_to_Z.get(sym, -1)

def Z2sym(Z):
    """
    Given an atomic number Z, returns the element symbol.
    Returns 'EE' if Z is out of range.
    """
    if 1 <= Z <= MAX_Z:
        return symbols[Z - 1]
    else:
        return 'EE'

def atomic_weight(Z):
    """
    Returns the atomic weight of the element with atomic number Z.
    """
    if 1 <= Z <= MAX_Z:
        return atomic_weights[Z - 1]
    else:
        # Optionally, raise an exception or return None
        print(f'Element not found, Z={Z}')
        return 0.0


def tot_weight(formula):
    """
    Calculates the total molecular weight of a chemical formula.
    """
    symbol_list, num_list, tot_syms = form2sym(formula)
    weight = 0.0
    for i in range(tot_syms):
        Z = sym2Z(symbol_list[i])
        weight += atomic_weight(Z) * num_list[i]
    return weight

def form2sym(formula):
    """
    Parses a chemical formula into symbols and their counts.
    Returns lists of symbols and counts, and the total number of symbols.
    """
    symbol_list = []
    num_list = []
    pattern = r'([A-Z][a-z]?)([0-9\.]*)'
    tokens = re.findall(pattern, formula)
    for (symbol, count) in tokens:
        if count == '':
            count = 1
        else:
            count = float(count)
        symbol_list.append(symbol)
        num_list.append(count)
    tot_syms = len(symbol_list)
    return symbol_list, num_list, tot_syms

def get_atomic(in_string):
    """
    Given an edge string like 'Cu K', returns Z, e_not, and edge_code.
    """
    in_string = in_string.strip()
    Zsym = in_string[0:2].strip()
    if len(in_string) > 2 and in_string[2] != ' ':
        edge_sym = in_string[2:].strip()
    else:
        edge_sym = in_string[3:].strip()
    Z = sym2Z(Zsym)
    edge_code_map = {'K': 0, 'LI': 1, 'L1': 1, 'LII': 2, 'L2': 2, 'LIII': 3, 'L3': 3}
    edge_code = edge_code_map.get(edge_sym.upper())
    if edge_code is None:
        print(f'ERROR:get_atomic. symbol bad: {Zsym}, {edge_sym}')
        return -1, None, None
    e_not = get_e_not(Z, edge_code)
    return Z, e_not, edge_code

def get_e_not(Z, edge_code):
    """
    Returns the energy e_not for a given atomic number Z and edge_code.
    Edge codes: 0=K, 1=LI, 2=LII, 3=LIII
    """
    # Data arrays for edge energies
    K_e_not = [13.6,25.00,55.00,112.00,188.00,284.00,402.00,537.00,
               686.00,867.00,1072.00,1305.00,1560.00,1839.00,2149.00,2472.00,
               2822.00,2822.00,3607.00,4038.00,4493.00,4965.00,5465.00,5989.00,
               6540.00,7112.00,7709.00,8333.00,8979.00,9659.00,10367.00,
               11104.00,11868.00,12658.00,13474.00,14322.00,15200.00,16105.00,
               17080.00,17998.00,18986.00,19999.00,21045.00,22117.00,23220.00,
               24350.00,25514.00,26711.00,27940.00,29200.00,30491.00,31813.00,
               33169.00,34582.00,35985.00,37441.00,38925.00,40444.00,41991.00,
               43569.00,45184.00,46835.00,48520.00,50240.00,51996.00,53789.00,
               55618.00,57486.00,59390.00,61332.00,63314.00,65351.00,67414.00,
               69524.00,71676.00,73872.00,76112.00,78395.00,80723.00,83103.00,
               85528.00,88006.00,90527.00,90527.00,90527.00,98417.00,98417.00,
               98417.00,98417.00,109649.00,109649.00,115603.00,115603.00,
               121760.00,121760.00,121760.00,121760.00,121760.00,121760.00,
               121760.00]
    
    LI_e_not = [0,0,0,0,0,0,37.3,41.6,0,48.5,63.5,88.6,117.8,
                149.7,189,2309,270,326.3,378.6,438.4,498.0,
                560.9,626.7,695.7,769.1,844.6,925.1,1008.6,
                1096.7,1196.2,1299.0,1414.6,1527.0,1652.0,
                1782,1921,2065,2216,2373,2532,2698,2866,3043,
                3224,3412,3604,3806,4018,4238,4465,4698,4939,
                5188,5453,5714,5989,6266,6548,6835,7126,7428,
                7737,8052,7376,7808,9046,9394,9751,10116,
                10486,10870,11271,11682,12100,12527,12968,13419,
                13880,14353,14839,15347,15861,16388,16939,17493,
                18049,18639,19237,19840,20472,21105,21757,22427.0,
                23104.0,23808.0,
                24526.0,25256.0,26010.0,0,0]
    LII_e_not = [0,0,0,0,0,0,0,0,0,21.7,30.4,49.6,72.9,99.8,136,
                 163.6,202,250.6,297.6,349.7,403.6,461.2,519.8,
                 583.8,649.9,719.9,793.3,870.0,952.3,1044.9,1143.2,
                 1248.1,1359.1,1474.3,1596,1730.9,1864,2007,2156,
                 2307,2465,2625,2793,2967,3146,3330,3524,3727,3938,
                 4156,4380,4612,4852,5104,5359,5624,5891,6164,6440,
                 6722,7013,7312,7617,7930,8252,8581,8918,9264,9617,
                 13273,13734,14209,14698,15200,15711,16244,16785,
                 17337,17907,18484,19083,19693,20314,20948,21600,22266.,
                 22952.0,23651.0,24371.0,25108.0,0,0]
    LIII_e_not = [0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,
                  49.20,72.50,99.20,135.00,162.50,200.00,200.00,294.60,346.20,
                  398.70,453.80,512.10,574.10,638.70,706.80,778.10,855.00,932.00,
                  1021.00,1115.00,1218.00,1325.00,1436.00,1550.00,1675.00,1805.00,
                  1940.00,2080.00,2223.00,2371.00,2520.00,2677.00,2838.00,3003.00,
                  3173.00,3351.00,3537.00,3730.00,3929.00,4132.00,4341.00,4557.00,
                  4781.00,5012.00,5247.00,5483.00,5724.00,5965.00,6208.00,6460.00,
                  6717.00,6977.00,7243.00,7515.00,7790.00,8071.00,8358.00,8648.00,
                  8943.00,9244.00,9561.00,9881.00,10204.00,10534.00,10871.00,
                  11215.00,11564.00,11918.00,12284.00,12657.00,13035.00,13418.00,
                  13418.00,13418.00,14612.00,14612.00,14612.00,14612.00,16300.00,
                  16300.00,17166.00,17610.00,18057.00,18510.0,18970.0,19435.0,
                  19907.0,0,0]
    
    # Ensure Z is within range
    if 1 <= Z <= MAX_Z:
        index = Z - 1
        if edge_code == 0:
            e_not = K_e_not[index]
        elif edge_code == 1:
            e_not = LI_e_not[index]
        elif edge_code == 2:
            e_not = LII_e_not[index]
        elif edge_code == 3:
            e_not = LIII_e_not[index]
        else:
            raise ValueError('ERROR in get_e_not: Edge not supported.')
    else:
        raise ValueError('ERROR: get_e_not. Invalid Z.')
    return e_not

def check_edge_string(string):
    """
    Checks the syntax of an edge string.
    Returns True if valid, False otherwise.
    """
    string = string.strip()
    if len(string) < 2:
        return False
    iZ = sym2Z(string[0:2].strip())
    if iZ < 1:
        return False
    edge_part = string[3:].strip()
    valid_edges = ['K', 'LI', 'LII', 'LIII', 'L1', 'L2', 'L3']
    return edge_part.upper() in valid_edges
