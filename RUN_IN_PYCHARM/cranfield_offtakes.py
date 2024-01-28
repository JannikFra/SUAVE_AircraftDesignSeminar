# This Method descirbes the calculation of delta SFC according Cranfield University
# "Effects of Offtakes for Aircraft Secondary-Power Systems on Engine Performance"
# DOI: 10.2514/1.B34252

import SUAVE
from SUAVE.Core import Units
import matplotlib.pyplot as plt
import numpy as np


BPR = np.linspace(1, 50, 5)                       # Engine bypass ratio
SFC = 0.475 * Units.lb / Units.lbf / 3600    # Engine reference SFC

altitude = 10668                # Aircraft flight altitude in m
mach = 0.8                      # Aircraft flight mach number

W_b = 0.85                        # Bleed air mass flow in kg/s
delta_h_b = 588                 # Bleed air Enthalpy increase through the core, kJ/kg
T = 50                      # Engine net thrust, kN
ST = 1 / SFC                   # Engine specific thrust m/s

eta_f = 0.9                      # Fan isentropic efficiency
eta_l_pt = 0.86                   # Low pressure turbine isentropic efficiency

beta = W_b * ST * (BPR + 1) / T                   # Ratio of bleed-air mass flow upon core mass flow
print('beta', beta)
print('ST', ST)

atmosphere = SUAVE.Analyses.Atmospheric.US_Standard_1976()
atmo_data = atmosphere.compute_values(altitude)
speed_of_sound = atmo_data.speed_of_sound

V_0 = mach * speed_of_sound  # Aircraft flight velocity
print('V_0', V_0)

# Equation 16
eta_co_star_to_eta_co = 1 - (2 * W_b * delta_h_b * (BPR + 1)) / ((1 - beta) * T * (BPR / (eta_f * eta_l_pt) + 1) * (2 * V_0 + ST))
print(eta_co_star_to_eta_co)

# Equation 22
eta_0_star_to_eta_0 = - V_0 / ST + V_0 / ST * (1 + 2*ST/V_0 * eta_co_star_to_eta_co * (1 + ST / (2*V_0)))**0.5
print(eta_0_star_to_eta_0)

delta_SFC = 1 - eta_0_star_to_eta_0

plt.plot(BPR, delta_SFC.T)
plt.ylim(-0.05, 0.05)
plt.show()

