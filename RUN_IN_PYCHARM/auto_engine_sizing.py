import SUAVE
from SUAVE.Core import Units
from SUAVE.Components.Energy.Networks.Turbofan_Raymer import Turbofan_Raymer

atmosphere = SUAVE.Analyses.Atmospheric.US_Standard_1976()
tf = Turbofan_Raymer()
altitude = 35000 * Units.ft
mach = 0.8
temperature_deviation = 0
atmo_data =  atmosphere.compute_values(altitude, temperature_deviation)

thrust_ratio = tf.get_max_thrust(0, 0) / tf.get_max_thrust(altitude, mach)
print(thrust_ratio)

mtom = 140_000
thrust_loading = 230_800 * 2 / mtom / 9.81
print('thrust_loading', thrust_loading)

print(230_800 / Units.lbf)

max_thrust_in_cruise = 230_800 / thrust_ratio / Units.lbf
print('max_thrust_in_cruise lbf', max_thrust_in_cruise)

# print(0.046995667731751595 * Units.kg / Units.lb / (Units.N / Units.lbf))
# print(0.475 * Units.lb / Units.kg / (Units.lbf / Units.N))