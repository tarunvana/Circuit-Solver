"""
EE20B147
VANA TARUN KUMAR
apl assignment 2
"""
from numpy import *
from sys import argv , exit
# declaration of classes for each component to store the respective values as an object
if len(argv) != (2) :
    print("please provide the required files in command")
    exit()


class Resistor:
	def __init__(self,name , n1 , n2 , val):
		self.name = name 
		self.n1 = n1
		self.n2 = n2
		self.val = val
class Inductor :
	def __init__(self,name , n1 , n2 , val):
		self.name = name 
		self.n1 = n1
		self.n2 = n2
		self.val = val
class Capacitor:
	def __init__(self,name , n1 , n2 , val ):
		self.name = name 
		self.n1 = n1
		self.n2 = n2
		self.val = val
class VoltageSource :
	def __init__(self,name , n1 , n2 , val , phase = 0):
		self.name = name 
		self.n1 = n1
		self.n2 = n2
		self.val = val
		self.phase = phase
class CurrentSource :
	def __init__(self,name , n1 , n2 , val , phase = 0):
		self.name = name 
		self.n1 = n1
		self.n2 = n2
		self.val = val
		self.phase = phase



CIRCUIT = ".circuit"
END = ".end"
AC = ".ac"
ac_flag = 0

#reading the required values from the file in command line

try:
    with open(argv[1]) as f:
        lines = f.readlines()
        start = -2; end = -8
    for line in lines:              
        if CIRCUIT == line[:len(CIRCUIT)]:
            start = lines.index(line)
        elif AC == line[:len(AC)]:
            circuit_type = "AC"
            ac_flag = 1
            frequency = float(line.split()[2])
            w = 2*3.14*frequency
        elif END == line[:len(END)]:
            end = lines.index(line)
    if start>= end :
        print("Given circuit defination in netlist is wrong")
        exit()
    
    RESISTOR = []
    CAPACITOR = []
    INDUCTOR = []
    VOLTAGESOURCE = []
    CURRENTSOURCE = []
    circuitnodes = []
    l = []
    k = 0
    def StrToNum(str1,str2):
        if str1.isdigit() == 0 :
            a = str1.split('e')
            one = (float(a[0]))*(10**int(a[1]))
            phase = float(str2)
            two = complex(cos(phase*0.017445),sin(phase*0.017445))
            value = one*two
            return value
        else :
            one = float(str1)
            phase = float(str2)
            two = complex(cos(phase*0.017445),sin(phase*0.017445))
            value = one*two 
            return value
    def StrToNum2(str1) :
        if str1.isdigit() == 0 :
            a = str1.split('e')
            value = float(a[0])*(10**int(a[1]))
            return value 
        else :
            value = float(str1)
            return value 



    try:
        for line in lines[start+1:end] :
            circuit = line.split("#")[0].split()
            print(circuit)

            try :
                if circuit[1] not in circuitnodes :
                    circuitnodes.append(circuit[1])
                if circuit[2] not in circuitnodes :
                    circuitnodes.append(circuit[2])
            except IndexError :
                continue 

            if circuit[0][0] == 'R':
                component = Resistor(circuit[0],circuit[1],circuit[2],circuit[3])
                
            elif circuit[0][0] == 'C' :
                component = Capacitor(circuit[0],circuit[1],circuit[2],circuit[3])

            elif circuit[0][0] == 'L' :
                component = Inductor(circuit[0],circuit[1],circuit[2],circuit[3])

            elif circuit[0][0] == 'V' :
                if len(circuit) == 4 :
                    component = VoltageSource(circuit[0] , circuit[1] , circuit[2] , circuit[3] ) #DC value
                    k = k+1 

                elif len(circuit) == 6 :
                    component = VoltageSource(circuit[0] , circuit[1] , circuit[2] , circuit[4] , circuit[5] ) #AC value
                    k = k+1 

            elif circuit[0][0] == 'I' :
                if len(circuit) == 4 :
                    component = CurrentSource(circuit[0] , circuit[1] , circuit[2] , circuit[3] ) #DC value 

                elif len(circuit) == 6 :
                    component = CurrentSource(circuit[0] , circuit[1] , circuit[2] , circuit[4] , circuit[5] ) #AC value
            
            if len(circuit) == 6 :
                component.val = StrToNum(component.val,component.phase)
            if len(circuit) == 4 :
                component.val = StrToNum2(component.val)

            l.append(component)
            print(component.val)
 
    except IndexError :
        print("Please make sure the netlist is correct .")
        exit()
    node = {}
    for component in l :
        if component.n1 not in node :
            if component.n1 == 'GND' :
                node['n0'] = 'GND'
            else :
                name = "n" + component.n1
                node[name] = int(component.n1)
        if component.n2 not in node :
            if component.n2 == 'GND' :
                node['n0'] = 'GND'
            else :
                name = "n" + component.n2
                node[name] = int(component.n2)

    node['n0'] = 0
    n = len(node)

#creating an empty matrix for solving the equations 
    M = zeros(((n+k-1),(n+k-1)),dtype = "complex")

    b = zeros(((n+k-1),1),dtype = "complex")
    
    p=0

# writing code to fill the matrix with the conductance equations 

    for component in l :
        if component.name[0] == 'R':
            if component.n2 == 'GND' : 
                M[int(component.n1)-1][int(component.n1)-1] += 1/component.val
            elif component.n1 == 'GND' :
                M[int(component.n2)-1][int(component.n2)-1] += 1/component.val
            else :
                M[int(component.n1)-1][int(component.n1)-1] += 1/component.val
                M[int(component.n2)-1][int(component.n2)-1] += 1/component.val
                M[int(component.n1)-1][int(component.n2)-1] += -1/component.val
                M[int(component.n2)-1][int(component.n1)-1] += -1/component.val

        elif component.name[0] == 'C' :

            if ac_flag == 1 :
                Zc = -1 / (float(component.val)*w)
                component.val = complex(0,Zc)

            
            if component.n2 == 'GND' :
                M[int(component.n1)-1][int(component.n1)-1] += 1/component.val
            elif component.n1 == 'GND' :
                M[int(component.n2)-1][int(component.n2)-1] += 1/component.val
            else :
                M[int(component.n1)-1][int(component.n1)-1] += 1/component.val
                M[int(component.n2)-1][int(component.n2)-1] += 1/component.val
                M[int(component.n1)-1][int(component.n2)-1] += -1/component.val
                M[int(component.n2)-1][int(component.n1)-1] += -1/component.val

        
        elif component.name[0] == 'L' :

            if ac_flag == 1 :
                Zl = float(component.val)*w
                component.val = complex(0,Zl)

            
            if component.n2 == 'GND' :
                M[int(component.n1)-1][int(component.n1)-1] += 1/component.val
            elif component.n1 == 'GND' :
                M[int(component.n2)-1][int(component.n2)-1] += 1/component.val
            else :
                M[int(component.n1)-1][int(component.n1)-1] += 1/component.val
                M[int(component.n2)-1][int(component.n2)-1] += 1/component.val
                M[int(component.n1)-1][int(component.n2)-1] += -1/component.val
                M[int(component.n2)-1][int(component.n1)-1] += -1/component.val


        elif component.name[0] == 'I' :
            if component.n2 == 'GND' :
                b[int(component.n1)-1][0] += component.val

            elif component.n1 == 'GND' :
                b[int(component.n2)-1][0] += -component.val

            else :
                b[int(component.n1)-1][0] += component.val
                b[int(component.n2)-1][0] += -component.val

        elif component.name[0] == 'V' :
            if component.n2 == 'GND':
                M[int(component.n1)-1][n-1+p] += 1
                M[n-1+p][int(component.n1)-1] += 1
                b[n-1+p] += component.val
                p = p+1			
            elif component.n1 == 'GND':
                M[int(component.n2)-1][n-1+p] += -1
                M[n-1+p][int(component.n2)-1] += -1
                b[n-1+p] += component.val
                p = p+1			
            else:	
                M[int(component.n1)-1][n-1+p] += 1
                M[int(component.n2)-1][n-1+p] += -1
                M[n-1+p][int(component.n1)-1] += 1
                M[n-1+p][int(component.n2)-1] += -1
                b[n-1+p] += component.val
                p = p+1

    print(M,'\n')
    print(b,'\n')
    V = linalg.solve(M,b)
    print(V , "\n")

    for i in range(n-1):
        print("V",i+1,"=",V[i],"\n")
    for i in range(k) : 
        print("I",i+1,"=" , V[i+n-1],"\n")

except IOError:
    print("Invalid File.")
    exit()