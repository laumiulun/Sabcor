#Haven't done much, but done something

names = ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Pa", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "", "", "Rn", "","","", "Th", "", "U", "", "Pu", "Am"]

""" Do not have
 "Po", "At" (84, 85), "Fr", "Ra", "Ac" (87-89), "Pa" (91), "Np" (93), "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og" (96-118) 
"""

# not quite sure what "call upcase(mane)" is but first guess is it's a function

try:
	#whatever the python eqvlt to "call upcase(mane)" will be
	if z = 84 or z = 85 or z = 87 or z = 88 or z = 89 or z = 91 or z = 93:
		raise UnAcceptedValueError("sorry no documents for Z=84,85,87-89,91,93")
    #UnAcceptedValueError is from a tutorial example copy/pasted in the comment below
except UnAcceptedValueError as e: 
	print ("Received error:", e.data)
	

"""
Hydrogen from the original mod_mucal.f file

 data name( 1),  ek( 1),el( 1)/
     $     'H ',  0.140000e-01,  0.000000e+00/
      data ak(0, 1),ak(1, 1),ak(2, 1),ak(3, 1)/
     $     0.244964e+01, -0.334953e+01, -0.471370e-01,  0.709962e-02/
      data al(0, 1),al(1, 1),al(2, 1),al(3, 1)/
     $     0.000000e+00,  0.000000e+00,  0.000000e+00,  0.000000e+00/
      data am(0, 1),am(1, 1),am(2, 1),am(3, 1)/
     $     0.000000e+00,  0.000000e+00,  0.000000e+00,  0.000000e+00/
      data an(0, 1),an(1, 1),an(2, 1),an(3, 1)/
     $     0.000000e+00,  0.000000e+00,  0.000000e+00,  0.000000e+00/
      data den( 1),cf( 1),atwt(1)/1.008, 0.167400e+01,1.008/
      data coh(0, 1),coh(1, 1),coh(2, 1),coh(3, 1)/
     $     -0.119075e+00, -0.937086e+00, -0.200538e+00,  0.106587e-01/
      data cih(0, 1),cih(1, 1),cih(2, 1),cih(3, 1)/
     $     -0.215772e+01,  0.132685e+01, -0.305620e+00,  0.185025e-01/ 

first if statement with error message from original mod_mucal.f
if(z.eq.84.or.z.eq.85.or.z.eq.87.or.z.eq.88.or.z.eq.89.or.
     $     z.eq.91.or.z.eq.93) then
         er=3
         if(erf) 
     $        print*,'**sorry no documents for Z=84,85,87-89,91,93**'
         goto 10001

Exception handling Python: Python Custom Exceptions example from tutorial
https://www.datacamp.com/community/tutorials/exception-handling-python
class UnAcceptedValueError(Exception):   
    def __init__(self, data):    
        self.data = data
    def __str__(self):
        return repr(self.data)

Total_Marks = int(input("Enter Total Marks Scored: "))
try:
    Num_of_Sections = int(input("Enter Num of Sections: "))
    if(Num_of_Sections < 1):
        raise UnAcceptedValueError("Number of Sections can't be less than 1")
except UnAcceptedValueError as e:
    print ("Received error:", e.data)

"""