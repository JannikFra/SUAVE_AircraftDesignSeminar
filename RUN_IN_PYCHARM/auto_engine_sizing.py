import SUAVE
from SUAVE.Core import Units
from SUAVE.Components.Energy.Networks.Turbofan_Raymer import Turbofan_Raymer

atmosphere = SUAVE.Analyses.Atmospheric.US_Standard_1976()
tf = Turbofan_Raymer()
altitude = 42000 * Units.ft
mach = 0.82
temperature_deviation = 0
atmo_data =  atmosphere.compute_values(altitude, temperature_deviation)
v_v_300 = 300 * Units.ft / Units.min
v_initial_cruise_altitude = mach * atmo_data.speed_of_sound
LoD_initial_cruise_altitude = 26
m4_m0 = 0.98
rho_initial_cruise_altitude = atmo_data.density[0][0]
thrust_ratio = tf.get_max_thrust(0, 0) / tf.get_max_thrust(altitude, mach)

F_m_TOC = m4_m0 * (v_v_300/v_initial_cruise_altitude + 1/LoD_initial_cruise_altitude) * thrust_ratio


print(F_m_TOC)

