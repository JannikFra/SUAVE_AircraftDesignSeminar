# This Method is used to estimate the new SFC according to calculated offtakes
from SUAVE.Core import Units

reference_SFC_after_Offtakes = 0.475 # lb/lbf/hr (from Avacon 2028)
reference_bleed_air = 1.594 / 2 # kg/s
# reference_electric = 93.6 #kW
# reference_hydraulic = 14.08 #kW
# reference_shaft_power = 177.9 #kW


delta_sfc_factor = 0.038 / (2.5 * Units.lb) * reference_bleed_air
print(delta_sfc_factor)
reference_thrust = 1.

reference_SFC_before_Offtakes = reference_SFC_after_Offtakes - delta_sfc_factor * reference_thrust
print(reference_SFC_before_Offtakes)

electric = 116_600 # W
electric = 1141 * 100 / 2

delta_sfc_factor_electric = 0.011 / (250 * Units.hp) * electric
SFC = reference_SFC_before_Offtakes + delta_sfc_factor_electric * reference_SFC_before_Offtakes

system_mass_factor = 1.57
print('-> SFC: ', SFC)
print('-> Electric Power: ', (electric/1000*2), 'kW')