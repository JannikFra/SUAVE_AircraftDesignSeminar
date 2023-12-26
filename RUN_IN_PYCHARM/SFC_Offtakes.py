# This Method is used to estimate the new SFC according to calculated offtakes

reference_SFC_after_Offtakes = 0.475 # lb/lbf/hr (from Avacon 2028)
reference_bleed_air = 1.594 # kg/s
# reference_electric = 93.6 #kW
# reference_hydraulic = 14.08 #kW
# reference_shaft_power = 177.9 #kW

reference_thrust = 1.

reference_SFC_before_Offtakes = 0.4

#bleed_air = 0.
electric = 116_600 # W
electric = 1.141 * 100
#hydraulic = 0.

SFC = 1.

print('-> SFC: ', SFC)