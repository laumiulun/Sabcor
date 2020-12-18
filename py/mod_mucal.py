#Haven't done much, but done something
#they want to be instances of a class!

class elements:
    #em starts at S (16) it seems, what should the 1st 15 be?
    def __init__(self, name, ek, el, ak, al, am, an, den, cf, atwt, coh, cih):
        self.name = name    #string
        self.ek = ek        
        self.el = el
        self.ak = ak        #number array
        self.al = al        #number array
        self.am = am        #number array
        self.an = an        #number array
        self.den = den
        self.cf = cf
        self.atwt = atwt
        self.coh = coh      #number array
        self.cih = cih      #number array


H = elements("H", 0.014, 0, [], [], [], [], 1.008, 1.674, 1.008, [], [])
H.ak = [2.44964, -3.34953, -0.0471370, 0.00709962]
H.al = [0, 0, 0, 0]
H.am = [0, 0, 0, 0]
H.an = [0, 0, 0, 0]
H.coh = [-0.119075, -0.937086, -0.200538, 0.0106587]
H.cih = [-2.15772, 1.32685, -0.305620, 0.0185025]

#print("name:", H.name, "ek:", H.ek, "ak:", H.ak, "cih:", H.cih)    #yay it works

He = elements("He", 0.0250000,  0, [], [], [], [], .0001785, 6.64700, 4.003, [], [])
He.ak = [6.06488, -3.29055, -0.107256,  0.0144465]
He.al = [0, 0, 0, 0]
He.am = [0, 0, 0, 0]
He.an = [0, 0, 0, 0]
He.coh = [1.04768, -0.0851805, -0.403527, 0.0269398]
He.cih = [-2.56357,  2.02536, -0.448710,  0.0279691]

Li = elements("Li", 0.0550000,  0, [], [], [], [], 0.534, 11.5200, 6.940, [], [])
Li.ak = [7.75370, -2.81801, -0.241378,  0.0262542]
Li.al = [0, 0, 0, 0]
Li.am = [0, 0, 0, 0]
Li.an = [0, 0, 0, 0]
Li.coh = [1.34366,  0.181557, -0.423981,  0.0266190]
Li.cih = [-1.08740, 1.03368, -0.190377,  0.00779955]

Be = elements("Be", )


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