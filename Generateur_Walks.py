import sys, argparse, random, math
import tidynamics
import matplotlib.pyplot as plt
import numpy as np
from Generateur_LCG import PRNG

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--steps", type=int, help="Specify how many steps to simulate", default=1)
parser.add_argument("-w", "--walk", type=str, help="random=C, nonreversing=S, avoiding=U", default=None)
args = parser.parse_args()

if(args.walk == None):
    sys.stderr.write("/!\ Args Missing /!\ \n => Please use -h to show the documentation\n")

#Define the map
xMap = args.steps * [0]
yMap = args.steps * [0]
accomplished = args.steps

def walk(val, i):
    """
    Add a walk on map
    0 = forward
    1 = left
    2 = right
    3 = backward
    """    
    if val == 0: 
        xMap[i] = xMap[i-1]
        yMap[i] = yMap[i-1] + 1
    elif val == 1: 
        xMap[i] = xMap[i-1] - 1
        yMap[i] = yMap[i-1]  
    elif val == 2: 
        xMap[i] = xMap[i-1] + 1
        yMap[i] = yMap[i-1] 
    elif val == 3: 
        xMap[i] = xMap[i-1] 
        yMap[i] = yMap[i-1] - 1

def reverse_walk(val):
    """Compute reverse_walk of a walk"""   
    x = None
    if(val == 0):
        x = 3
    elif(val == 1):
        x = 2
    elif(val == 2):
        x = 1
    elif(val == 3):
        x = 0
    return x

def isVisited(i):
    """Check if the walk is already known"""   
    for j in range(1, i-1):
        if(xMap[i] == xMap[j] and yMap[i] == yMap[j]):
            return True
    return False

def RandomWalk(n):
    for i in range(1,n):
        val = int(PRNG(0,4))
        walk(val, i)

def NonreversingWalk(n):
    previous = None
    for i in range(1,n):
        val = int(PRNG(0,4))
        while(val == reverse_walk(previous)):
            val = int(PRNG(0,4))
        walk(val, i)            
        previous = val

def SelfAvoiding(n):
    previous = None
    Deadend = None
    for i in range(1,n):
        val = int(PRNG(0,4))
        while(val == reverse_walk(previous)):
            val = int(PRNG(0,4))
        walk(val, i)
        cpt = 0
        while(isVisited(i)):
            cpt +=1
            val = int(PRNG(0,4))
            walk(val, i)
            sys.stderr.write(" stuck : "+ str(cpt) + "\r")
            if(cpt >= 1000):
                Deadend = True
                global accomplished
                accomplished = i
                sys.stderr.write("\nDead-end, cutting the walk at step : "+str(accomplished)+"\n")
                break
        if(Deadend):
            break

def ExecuteWalk(walk):
    global walk_name
    if(walk == "C"):
        walk_name = "Random"
        RandomWalk(args.steps)
    elif(walk == "S"):
        walk_name = "Nonreversing"
        NonreversingWalk(args.steps)
    elif(walk == "U"):
        walk_name = "SelfAvoiding"
        SelfAvoiding(args.steps)
    else:
        sys.stderr.write("/!\ Args Missing /!\ \n => Please use -h to show the documentation\n")

ExecuteWalk(args.walk)

# Save the walk graph
plt.title(walk_name+" ($n = " + str(args.steps) + "$ steps)") 
plt.plot(xMap[:accomplished],yMap[:accomplished])
plt.savefig(walk_name+"_"+str(args.steps)+".png",bbox_inches="tight",dpi=600)
plt.clf()

xTotal = 0
yTotal = 0
# Compute distance
for i in range(0,args.steps):
    xTotal += xMap[i]
    yTotal += yMap[i]
RnSquared = xTotal**2 + yTotal**2
Rn = math.sqrt(RnSquared)
sys.stdout.write("\n"+walk_name+" walk travel distance is "+str(Rn)+"\n")