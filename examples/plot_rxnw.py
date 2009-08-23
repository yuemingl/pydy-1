from rxnw_eoms import f, animate
from scipy.integrate import odeint
from numpy import arange, zeros
import matplotlib.pyplot as plt

# Define the parameters
I1 = 2575.0
I2 = 0.0625
J1 = 5000.0
J2 = 0.125
l = 0.8
m1 = 100.0
m2 = 1.0
M = 10.
# Assemble parameters into a list (must be correct order)
params = [m1, m2, I1, I2, J1, J2, l, M]

# Initial Conditions
q0 = [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0]
u0 = [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
x0 = q0 + u0

# Integration time
ti = 0.0
ts = 0.01
tf = 10.0
t = arange(ti, tf+ts, ts)
n = len(t)

# Integrate the differential equations
x = odeint(f, x0, t, args = (params,))
u1 = x[:, 8]
u2 = x[:, 9]
u3 = x[:, 10]
"""
# Plot the results and save a .pdf
plt.figure(1)
plt.subplot(311)
plt.ylabel('$u_1$')
plt.plot(t, u1)
plt.subplot(312)
plt.ylabel('$u_2$')
plt.plot(t, u2)
plt.subplot(313)
plt.ylabel('$u_3$')
plt.plot(t, u3)
plt.xlabel('$t$')
plt.savefig('rxnw_plot.pdf')
plt.figure(2)
plt.plot(t, x[:,2])
"""
# Generate a nice animation
AO = zeros((n, 3))
BO = zeros((n, 3))
CO = zeros((n, 3))
A = zeros((n, 4))
B = zeros((n, 4))
C = zeros((n, 4))

# Animation rate multiplier
k = 1.0

cyl_l = 0.2
for i, state in enumerate(x[:,:8]):
    AO[i], BO[i], CO[i], A[i], B[i], C[i] = animate(state, params)
    BO[i] -= cyl_l*B[i,:3]/2.
    CO[i] -= cyl_l*C[i,:3]/2.
    B[i,:3] *= cyl_l
    C[i,:3] *= cyl_l

from visual import box, display, rate, arrow, cylinder
scene = display(title='Rigid body with reaction wheel @ %0.2f realtime'%k,
        width=800, height=800, uniform=1, background=(1,1,1), up=(0,0,1), forward=(1,0,0), exit=0)
black = (1,1,1)
red = (1, 0, 0)
green = (0, 1, 0)
blue = (0, 0, 1)
grey = (0.5,0.5,0.5)
n = [arrow(pos=(0,0,0),axis=(.5,0,0),color=red),
     arrow(pos=(0,0,0),axis=(0,.5,0),color=green),
     arrow(pos=(0,0,0),axis=(0,0,.5),color=blue)]
body = box(pos=AO[0, :], axis=A[0, :3], angle=A[0, 3],\
        length=2, height=1, width=1, color=red)
rxnw1 = cylinder(pos=BO[0,:], axis=B[0, :3], radius=0.5, color=green)
rxnw2 = cylinder(pos=CO[0,:], axis=C[0, :3], radius=0.5, color=blue)
i = 1
#stop

while i<n:
    rate(k/ts)
    body.pos = AO[i, :]
    body.axis = A[i, :3]
    body.angle = A[i, 3]
    #rxnw1.pos = BO[i, :]
    rxnw1.axis = B[i, :3]
    #rxnw1.angle = B[i, 3]
    #rxnw2.pos = CO[i, :]
    rxnw2.axis = C[i, :3]
    #rxnw2.angle = C[i, 3]
    i += 1
