import numpy as np
from matplotlib import pyplot as plt
from math import pi as pi

plt.close("all")

engineType = 'c'
g = 9.80
h = 0.55
height = []
dt = 0.005

def calculateDrag(v, A, p):
    C = 0.75
    D = -0.5 * p * A * C * v * np.abs(v)
    return (D)

def rocket(engineType):
    massR, dMassR = 0.0481, 0.0014
    massA, dMassA = 0.0155, 0.0002
    massB, dMassB = 0.0183, 0.0002
    massC, dMassC = 0.0245, 0.0001
    diameter = 0.0247
    thicknessFin = 0.0015
    widthFin = 0.0425
    d_lug = 0.0045

    area = pi * (diameter**2 + d_lug**2) / 4 + 4 * (thicknessFin * widthFin) * (1 + np.random.randn() / 50)
    if engineType =='a':
        mass = (massR + dMassR * np.random.randn()) + (massA + dMassA * np.random.randn())
    elif engineType=='b':
        mass = (massR + dMassR * np.random.randn()) + (massB + dMassB * np.random.randn())
    elif engineType=='c':
        mass = (massR + dMassR * np.random.randn()) + (massC + dMassC * np.random.randn())
    else:
        mass = massR 
    return(mass,area)  
      
def impulse(engineType):
    if engineType == 'a':
        I, dI = 2.4, 0.1
    elif engineType == 'b':
        I, dI = 4.8, 0.2
    elif engineType == 'c':
        I, dI = 9.6, 0.4
    else:
        I, dI = 0.0, 0.0
    return(I + dI * np.random.randn())
    
def thrust(t, engineType, I):
    if engineType =='a':
        t1, t2 = 0.22, 0.28
        h1, h2 = 11.0, 2.2
        massP = 0.00312
    elif engineType =='b':
        t1, t2 = 0.18, 0.26
        h1, h2 = 12.0, 4.5
        massP = 0.00624
    elif engineType =='c':
        t1, t2 = 0.19, 0.26
        h1, h2 = 14.0, 4.5
        massP = 0.01248
    else:
        t1, t2 = 1.0, 2.0
        h1, h2 = 1.0, 2.0
        I, dI = 0.0, 0.0
        massP = 0.0
    t3 = (I - (t2 * h1 -(t1 + t2) * h2) / 2) / h2
    if t < t1:
        thrust = (h1 / t1) * t
        dMass = massP / t3
    elif t < t2:
        thrust = ((h2 - h1) * t + (t2 * h1 - t1 * h2)) / (t2 - t1)
        dMass = massP / t3
    elif t < t3:
        thrust = h2
        dMass = massP / t3
    else:
        thrust = 0.0
        dMass = 0
    return(thrust, dMass)
    
for n in xrange(0, 500):
    p, dp = 1.05, 0.02
    p = p + dp * np.random.randn()
    velocity = 0.0
    time = [0.0]
    y = [h]
    [mass, area] = rocket(engineType)
    Imp = impulse(engineType)
    
    while y[-1] > 0:
        [Fengine, dMass] = thrust(time[-1], engineType, Imp)
        acceleration = - g + (calculateDrag(velocity, area, p) + Fengine) / mass
        if time[-1] < 0.5 and acceleration < 0:
            aacceleration = 0
        y.append(y[-1] + velocity * dt)
        velocity = velocity + acceleration * dt
        time.append(time[-1] + dt)
        mass = mass - dMass * dt
        
    height.append(max(y))
    plt.plot(time, y)
    plt.xlabel("Time (s)")
    plt.ylabel("Height (m)")
    plt.title("Height vs. Time")
    
plt.show()

Ht = np.mean(height)
dHt = np.std(height)

print "Max height of rocket with engine", engineType, ": ", Ht, "m "
print "with uncertainty", dHt, "m."
    
            