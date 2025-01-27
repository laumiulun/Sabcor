
import math
import numpy as np
from elements_data import elements


# c----------------------------------------------------------------------+
# c	MODIFIED FROM ORIGINAL BY CORWIN BOOTH
# c	added xsec(11)=total crossection not including current edge.
# c	change L3 edge of U to 17166 eV from 17167 eV to be consistent with 
# c	orange book.
# c									|
# c	Modified 2/7/2014 by Dan Olive					|
# c	Added xsec(1) to subroutine output. Changed L edge to use	|
# c	L coefficients and divide out jump, instead of M coefficients	|
# c	and multiply in jumps. Difference in slope gave rise to ~2.5%	|
# c	change in cross section over the L3 and L2 edges. Fixed glitches|
# c	that occurred at 1 keV in all cross sections. Fixed noedge	|
# c	so cross section doesn't dip in L2 region, and now instead of	|
# c	M coefficients for all L regions, noedge uses M for L3, L3 in	|
# c	the L2 region, and L2 in the L1 region.				|
# c									|
# c	4/16/2014 DTO							|
# c	Corrected U L edge coefficients					|
# c	Corrected L alpha and L beta of the following elements:		|
# c	La,Nd,Pm,Sm,Eu,Gd,Tb,Dy,Ho,Er					|
# c									|
# c	Also fixed density of H and C					|
# c									|
# c	to go to the begining of the acual programme search for        |
# c	"programme starts".                                            |
# c     this is a program to calculate x-sections useing mcmaster        |
# c     data in may 1969 edition. written by pathikrit bandyopadhyay     |
# c     at the university of notre dame.i am thankful to                 |
# c     dr. b. a. bunker and mr. q. t. islam for their helpful           |
# c     suggestions. special thanks goes to mr. m. zanabria              |
# c     for helping to get all the data in.                              |
# c     ***note:this program has data for all the elements from 1 to 94  |
# c     with the following exceptions:                                   |
# c     84  po \                                                         |
# c     85  at |                                                         |
# c     87  fr |                                                         |
# c     88  ra  > mc master did not have any data for these.             |
# c     89  ac |                                                         |
# c     91  pa |                                                         |
# c     93  np /                                                         |
# c     input:                                                           |
# c     en=energy at which we need the x-section                         |
# c     mane=name of material                                     **     |
# c     unit=units to be used.'C' for cm**2/gm,'B' for barns/atom        |
# c     z=if you do not know what it is,what are you doing here ? **     |
# c     erf=true or false (true will print error message on terminal)    |
# c                                                                      |
# c     returned values:                                                 |
# c     xsec(1)=photoelectric x-section                                  |
# c     xsec(2)=coherent x-section                                       |
# c     xsec(3)=incoherent x-section                                     |
# c     xsec(4)=total x-section                                          |
# c     xsec(5)=conversion factor                                        |
# c     xsec(6)=absorption coefficient                                   |
# c     xsec(7)=atomic weight                                            |
# c     xsec(8)=density                                                  |
# c     xsec(9)=l2-edge jump                                             |
# c     xsec(10)=l3-edge jump                                            |
# c     xsec(11)=total x-section not including current edge
# c                                                                      |
# c     energy(1)=k-edge energy                                          |
# c     energy(2)=l1-edge energy                                         |
# c     energy(3)=l2-edge energy                                         |
# c     energy(4)=l3-edge energy                                         |
# c     energy(5)=m-edge energy                                          |
# c     energy(6)=k-alpha1                                               |
# c     energy(7)=k-beta1                                                |
# c     energy(8)=l-alpha1                                               |
# c     energy(9)=l-beta1                                                |
# c                                                                      |
# c     fly(1)= k fluorescence yield				       |
# c     fly(2)= l1 fluorescence yield				       |
# c     fly(3)= l2 fluorescence yield				       |
# c     fly(4)= l3 fluorescence yield				       |
# c                                                                      |
# c     er=error code                                                    |
# c                                                                      |
# c     error codes:                                                     |
# c     er=1: energy input is zero                                       |
# c     er=2: name does not match                                        |
# c     er=3: no documentation for given element (z<94)                  |
# c     er=4: no documentation for given element (z>94)                  |
# c     er=5: l-edge calculation may be wrong for z<30 as mcmaster       |
# c     uses l1 only.                                                    |
# c     er=6: energy at the middle of edge                               |
# c     er=7: no name or z supplied                                      |
# c                                                                      |
# c     ** these will be returned if not given                           |
# c     put all returned values in array xsec/jul,28 _pat                |
# c     can call it either by element name or z/jul,31 _pat              |
# c     data input completed on sept 1,1985 ______pat                    |
# c     change call format,include energy array,includ density           |
# c     in xsec,add error # & error flag/sep,6 _pat                      |
# c     correct l-edge calculation using step jump                       |
# c     and warning for z<30/sep,9 _pat                                  |
# c     return l-edges /sep 10,_ pat                                     |
# c     return l-edge jumps,error 6 /sep 12,_ pat                        |
# c     check for no name & z,error 7 /sep 13,_ pat                      |
# c     thanks to quazi ljump can not be calculated for z<30 -pat        |
# c     revision date dec 9,1985 _____________ pat                       |
# c     l-edges for elements z=12-26 supplied from nsls handbook         |
# c     & corrections as noted by kim of nrl, april6,1991 ______anne     |
# c     add if statement so accept energy e=1. kev, and                  |
# c     print ljump for z=27 and 28,april10,1991______________anne       |
# c----------------------------------------------------------------------+
# c     $Log:	mucal.f,v $
# c Revision 1.7  91/09/06  14:48:38  patb
# c 
# Code translated to Python from Fortran by Levi Recla 01/08/2025        

nel = 94
n = 0
z = 0
er = 0
erf = False

bax = 0.0
xsec = [0.0] * 11
energy = [0.0] * 9

# Global constants
LJ1 = 1.16
LJ2 = 1.41

# Function to recursively convert all numeric values to float64
def convert_to_float64(data):
    if isinstance(data, dict):
        return {k: convert_to_float64(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_to_float64(v) for v in data]
    elif isinstance(data, (int, float)):
        return np.float64(data)
    else:
        return data  # Return non-numeric data as-is

# Convert the elements dictionary
elements_float64 = convert_to_float64(elements)


def mucal(mane, z, en, elements, erf=False, unit=" "):
    """
    c*******************************************************************
    c     programme starts (phew!)                                     *
    c*******************************************************************
    c------------------------------------------------------------------+
    c     do not have 84,85,87-89 91 93                                |
    c------------------------------------------------------------------+
    Python translation of the Fortran mucal routine.
    """

    lj1 = LJ1
    lj2 = LJ2

    # We'll track an integer error code er. Default to 0 = OK.
    er = 0

    # Convert mane to uppercase (like call upcase(mane)).
    mane = mane.upper()
    unit = unit.upper()  # For final check on units

    # Fortran check: if Z is in {84,85,87,88,89,91,93}, return er=3
    problematic_Z = {84, 85, 87, 88, 89, 91, 93}
    if z in problematic_Z:
        er = 3
        if erf:
            print("**sorry no documents for Z=84,85,87-89,91,93**")
        # Fortran: goto 10001 => end of routine. In Python, return.
        return ([0]*11, [0]*9, [0]*4, er)

    # If mane is in {Po, At, Fr, Ra, Ac, Pa, Np}, return er=3
    problematic_names = {"PO", "AT", "FR", "RA", "AC", "PA", "NP"}
    if mane in problematic_names:
        er = 3
        if erf:
            print("**sorry no documents for Po,At,Fr,Ra,Ac,Pa, and Np**")
        return ([0]*11, [0]*9, [0]*4, er)

    # If mane is empty (or just spaces) and z=0 => er=7
    if (mane.strip() == "") and (z == 0):
        er = 7
        if erf:
            print("**no name no z what do you want?**")
        return ([0]*11, [0]*9, [0]*4, er)

    # We need a valid index n in the dictionary. We’ll try two paths:
    # 1) If mane != '' => search by name
    # 2) else if z > 94 => error
    # 3) else => n=z, mane = name(n)
    if mane.strip() != "":
        # Path 1: We have a name; we try to find which z matches that name
        found_z = None

        # We'll scan 1..94 (like Fortran do j=1,94),
        # but in Python, real data might only exist for certain z.
        # We'll do a quick loop; if we find a match, we set found_z = j
        for j in range(1, 95):
            if j in elements and elements[j]["name"].upper() == mane:
                found_z = j
                break
        
        if found_z is None:
            # Fortran: er=2 => "**WRONG NAME**"
            er = 2
            if erf:
                print("**WRONG NAME**")
            return ([0]*11, [0]*9, [0]*4, er)
        else:
            n = found_z
            z = found_z

    else:
        # Path 2: mane is empty => check if z>94 => error
        if z > 94:
            er = 4
            if erf:
                print("**no documents for Z > 94**")
            return ([0]*11, [0]*9, [0]*4, er)
        else:
            # Path 3: n = z
            if z not in elements:
                # If you have no data for z, it's an error
                er = 2
                if erf:
                    print("**WRONG Z or missing data**")
                return ([0]*11, [0]*9, [0]*4, er)
            n = z
            # In Fortran: mane = name(n). In Python, we do:
            mane = elements[n]["name"]

    # Now we have n,z mapped, and we can look up everything from elements[n].
    data = elements[n]

    # If en < 0 => the original code does "goto 20000"
    # which eventually sets xsec(7)=atwt(n), etc. We’ll handle that near the end.
    # If en=0 => er=1 => cannot calc for zero energy
    if en == 0.0:
        er = 1
        if erf:
            print("**cannot calculate for zero energy**")
        # Return now
        return ([0]*11, [0]*9, [0]*4, er)
    else:
        e = en 

    xsec = [0.0]*11
    energy = [0.0]*9
    fly = [0.0]*4

    # If en<0 => skip the main calculation but eventually fill xsec(7..10),
    if en < 0.0:
        pass
    else:
        # Initialize sums
        sum_ = 0.0
        sumbelow = 0.0
        bsum = 0.0
        belowsum = 0.0
        chs = 0.0
        csum_ = 0.0
        cis = 0.0
        cisum = 0.0

        # Check if e is near the middle of an edge (like e<ek(n) and e>ek(n)-0.001, etc.)
        # helper to see if e is "within 0.001 below" a threshold:
        def near_edge(val):
            return (e < val) and (e > (val - 0.001))

        ek_ = data.get("ek", 0.0)
        el_ = data.get("el", 0.0)
        em_ = data.get("em", 0.0)
        l2_ = data.get("l2", 0.0)
        l3_ = data.get("l3", 0.0)

        if near_edge(ek_) or near_edge(el_) or near_edge(em_):
            er = 6
            if erf:
                print("**energy at the middle of edge: using pre-edge fit results may be wrong**")


        #helper to do sum of a polynomial in log(e).
        def poly_sum(coeffs, e):
            s = 0.0
            lnE = math.log(e)
            for i in range(4):
                s += coeffs[i] * (lnE**i)
            return s

        ak_ = data.get("ak", [0,0,0,0])
        al_ = data.get("al", [0,0,0,0])
        am_ = data.get("am", [0,0,0,0])
        an_ = data.get("an", [0,0,0,0])

        # Because the Fortran code references lj1, lj2 as real scalars,
        # you need to decide how to store them. For demonstration, let's assume:
        lj1 = data.get("lj1", 1.0)  # or from some global variable
        lj2 = data.get("lj2", 1.0)
        # For L3, the code references lj3(n). We'll read that from data:
        lj3_ = data.get("lj3", 1.0)

        # We’ll track sum_ for “above” the edge and sumbelow for “below” the edge.
        # The Fortran code uses different arrays for the “below” portion in some edges.
        if e >= ek_:
            # 70 => a K edge
            for i in range(4):
                sum_      += ak_[i] * (math.log(e)**i)
                sumbelow += al_[i] * (math.log(e)**i)

        elif (e < ek_) and (e >= l2_):
            # 40 => an L1,2 edge
            for i in range(4):
                sum_      += al_[i] * (math.log(e)**i)
                sumbelow += al_[i] * (math.log(e)**i)

        elif (e < l2_) and (e >= l3_):
            # 45 => an L3 edge
            for i in range(4):
                sum_      += al_[i] * (math.log(e)**i)
                sumbelow += am_[i] * (math.log(e)**i)

        elif (e < el_) and (e >= em_):
            # 50 => an M edge
            for i in range(4):
                sum_      += am_[i] * (math.log(e)**i)
                sumbelow += an_[i] * (math.log(e)**i)

        elif (e < em_):
            # 60 => less than an M edge
            for i in range(4):
                sum_      += an_[i] * (math.log(e)**i)
                sumbelow += an_[i] * (math.log(e)**i)

        # In Fortran, there's a special block 79 for Z<=29 => "WARNING: McMaster uses L1 edge..."
        # We'll mimic that:
        if n <= 29 and not (e >= ek_):
            # If we are in an L or M edge for Z<=29
            er = 5
            if erf:
                print("**WARNING:McMaster uses L1 edge results may be imprecise for Z < 30**")

        # Bax = exp(sum)
        bax = math.exp(sum_)
        ba_noedge_x = math.exp(sumbelow)

        #   if(e >= l3(n) and e < l2(n)) => bax=bax/(lj1*lj2)
        #   if(e >= l2(n) and e < el(n)) => ba_noedge_x=bax/(lj1*lj2); bax=bax/lj1
        #   if(e >= el(n) and e < ek(n)) => ba_noedge_x=bax/lj1
        if (e >= l3_) and (e < l2_):
            # L3 edge => correct for L1 in bax
            bax = bax / (lj1 * lj2)
        if (e >= l2_) and (e < el_):
            # L2 edge => correct for L1, noedge uses L3
            ba_noedge_x = bax / (lj1 * lj2)
            bax = bax / lj1
        if (e >= el_) and (e < ek_):
            # L1 edge
            ba_noedge_x = bax / lj1

        # Now compute coherent (bcox) and incoherent (binx) cross sections
        coh_ = data.get("coh", [0,0,0,0])
        cih_ = data.get("cih", [0,0,0,0])

        chs = 0.0
        for i in range(4):
            chs += coh_[i] * (math.log(e)**i)
        bcox = math.exp(chs)

        cis = 0.0
        for i in range(4):
            cis += cih_[i] * (math.log(e)**i)
        binx = math.exp(cis)

        btox = bax + bcox + binx
        bto_noedge_x = ba_noedge_x + bcox + binx

        # Now check what unit to use
        cf_ = data.get("cf", 1.0)
        if unit == "C":  # “cm^2/g” scale
            xsec[0]  = bax / cf_
            xsec[1]  = bcox / cf_
            xsec[2]  = binx / cf_
            xsec[3]  = btox / cf_
            xsec[10] = bto_noedge_x / cf_  # xsec(11) in Fortran
        else:
            xsec[0]  = bax
            xsec[1]  = bcox
            xsec[2]  = binx
            xsec[3]  = btox
            xsec[10] = bto_noedge_x

        # Fortran lines 10000 / 20000 (stuff xsec(5..10)):
        # xsec(5)=cf(n), xsec(6)=btox*den(n)/cf(n), xsec(7)=atwt(n), xsec(8)=den(n)
        # if(n>=27) xsec(9)=lj2, xsec(10)=lj3(n)
        den_ = data.get("den", 1.0)
        atwt_ = data.get("atwt", 0.0)

        xsec[4] = cf_  # xsec(5)
        xsec[5] = btox * den_ / cf_  # xsec(6)
        xsec[6] = atwt_  # xsec(7)
        xsec[7] = den_   # xsec(8)

        if n >= 27:
            xsec[8] = lj2     # xsec(9)
        xsec[9] = lj3_        # xsec(10)

    # Fill the energy array => energy(1)=ek(n), (2)=el(n), (3)=l2(n), (4)=l3(n),
    #   (5)=em(n), (6)=ka(n), (7)=kb(n), (8)=la(n), (9)=lb(n).
    energy[0] = data.get("ek", 0.0)
    energy[1] = data.get("el", 0.0)
    energy[2] = data.get("l2", 0.0)
    energy[3] = data.get("l3", 0.0)
    energy[4] = data.get("em", 0.0)
    energy[5] = data.get("ka", 0.0)
    energy[6] = data.get("kb", 0.0)
    energy[7] = data.get("la", 0.0)
    energy[8] = data.get("lb", 0.0)

    # Fill the fluorescence yield array => fly(1)=fek(n), fly(2)=fel(1,n), ...
    # In Python, we store them 0-based => fly[0..3].
    fly[0] = data.get("fek", 0.0)
    fel_ = data.get("fel", [0.0, 0.0, 0.0])
    # fel has 3 elements => fel(1..3) in Fortran => in Python that’s fel_[0..2].
    if len(fel_) >= 3:
        fly[1] = fel_[0]
        fly[2] = fel_[1]
        fly[3] = fel_[2]

    # Finally, return everything
    return (xsec, energy, fly, er)







