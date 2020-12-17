#Haven't done much, but done something
#these might actually want to be a dictionary? can a dictionary have 3 or more?

names = ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Pa", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", null, null, "Rn", null, null, null, "Th", null, "U", null, "Pu", "Am"]

#not entirely sure about use of null for 84, 85, 87-89, 91, 93
ek = [0.014, 0.025, 0.055, 0.112, 0.188, 0.284, 0.402, 0.537, 0.686, 0.867, 1.072, 1.305, 1.56, 1.839, 2.149, 2.472, 2.822, 3.202, 3.607, 4.038, 4.493, 4.965, 5.465, 5.989, 6.54, 7.112, 7.709, 8.333, 8.979, 9.659, 10.367, 11.104, 11.868, 12.658, 13.474, 14.322, 15.2, 16.105, 17.08, 17.998, 18.986, 19.999, 21.045, 22.117, 23.22, 24.35, 25.514, 26.711, 27.94, 29.2, 30.491, 31.813, 33.169, 34.582, 35.985, 37.441, 38.925, 40.444, 41.991, 43.569, 45.184, 46.835, 48.52, 50.24, 51.996, 53.789, 55.618, 57.486, 59.39, 61.332, 63.314, 65.351, 67.414, 69.524, 71.676, 73.872, 76.112, 78.395, 80.723, 83.103, 85.528, 88.006, 90.527, null, null, 98.417, null, null, null, 109.649, null, 115.603, null, 121.76, 124.982]

el = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.063, 0.087, 0.118, 0.153, 0.193, 0.238, 0.287, 0.341, 0.4, 0.463, 0.531, 0.604, 0.682, 0.754, 0.842, 0.929, 1.012, 1.1, 1.196, 1.302, 1.414, 1.53, 1.653, 1.782, 1.92, 2.065, 2.216, 2.373, 2.532, 2.698, 2.866, 3.043, 3.224, 3.412, 3.605, 3.806, 4.018, 4.238, 4.465, 4.698, 4.939, 5.188, 5.452, 5.713, 5.987, 6.267, 6.549, 6.835, 7.126, 7.428, 7.737, 8.052, 8.376, 8.708, 9.047, 9.395, 9.752, 10.116, 10.488, 10.87, 11.272, 11.68, 12.098, 12.525, 12.964, 13.424, 13.892, 14.353, 14.846, 15.344, 15.86, 16.385, null, null, 18.055, null, null, null, 20.47, null, 21.756, null, 23.095, 23.808]

#em starts at S (16) it seems, how should the 1st 15 members of an array be filled?


""" Do not have
 "Po", "At" (84, 85), "Fr", "Ra", "Ac" (87-89), "Pa" (91), "Np" (93), "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og" (96-118) 
"""

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