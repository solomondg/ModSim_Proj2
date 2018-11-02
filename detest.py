I = 0
dI = 0
d2I = 0

Q = 0
dQ = 0
d2Q = 0

V = 1
dV = 0

R = 50
L = 25
C = 220e-3



dt = 0.01

lastV = 0

lastI = 0
lastdI = 0


#for i in range(1000):
#    dV = (V-lastV)/dt
#    lastV = V
#
#
#    di = (I-lastI)/dt
#    lastI = I
#
#
#    d2i = (di-lastdi)/dt
#    lastdi = di


from modsim import System, State, run_ode_solver, linspace, unpack, plot, decorate, get_last_label
import numpy as np

Vmag = 5 # |5V| AC input voltage
dV0 = 0  # Start at bottom of sine wave (t=0)
freq = 30  # input frequency for evaluation

init=State(V=0, dV=0)

sys = System(
    init=init,
    R=R,
    L=L,
    C=C,
    Vmag=Vmag,
    dV0=dV0,
    freqIn=freq,
    dt=0.1,
    t_end = 2.5,
)

from math import sin

def slope_func(state, t, system):
    V, dV = state
    unpack(system)

    #print(Vmag*sin(freq*t))
    d2V = L/R * C * Vmag * sin(freq*t) - 1/R * L * C * V - 1/L * dV
    d2V = ((L/R*C) * (Vmag*sin((freq)*t)) - ((1/R*L*C)*V) - ((1/L)*dV))
    #print(L/R * C * Vmag * sin(freq*t) - 1/R * L * C * _V - 1/L * dV)
    # LI'' + RI' + 1/C I = V'

    return dV, d2V

#print(slope_func(State(V=5, dV=2), 0, sys))


_state = sys.init
dt = 0.001
for t in range(0, 1000):
    dv, d2v = slope_func(_state, t/1000, sys)
    #_state.V += dv * dt
    #_state.dV += d2v * dt
    _v, _dv = _state.V, _state.dV
    _state = State(V=_v + dv*dt, dV=_dv + d2v*dt)
    #print(dv*dt, d2v*dt)
    print(t/1000,",", _state.V, ",",_state.dV, ",", Vmag*sin(freq*t/1000))

results, details = run_ode_solver(sys, slope_func, t_eval=
                                  linspace(0, 2.5, 400*2.5))


csv = ""

for i, r in results.iterrows():
    #print(i)
    csv += str(i) + "," + str(r.V) + "," + str(r.dV) + "\n"

with open('output.csv', 'w') as f:
    f.write(csv)
