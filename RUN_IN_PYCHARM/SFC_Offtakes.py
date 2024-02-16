# This Method is used to estimate the new SFC according to calculated offtakes
from SUAVE.Core import Units

reference_SFC_after_Offtakes = 0.4606 # lb/lbf/hr (from Avacon 2028)
print(' Base SFC (after Offtakes):', reference_SFC_after_Offtakes)

reference_bleed_air = 1.594 / 2 # kg/s
# reference_electric = 93.6 #kW
# reference_hydraulic = 14.08 #kW
# reference_shaft_power = 177.9 #kW

print(' Bleed air, per engine (in kg/s):', reference_bleed_air)

delta_sfc_factor = 0.038 / (2.5 * Units.lb) * reference_bleed_air
print(' Resulting delta SFC factor: %.4f' % delta_sfc_factor)

reference_SFC_before_Offtakes = reference_SFC_after_Offtakes - delta_sfc_factor * reference_SFC_after_Offtakes
print(' SFC (without ECS Offtakes): %.3f' % reference_SFC_before_Offtakes)

electric = 116_600 # W
electric = 1141 * 100 / 2

print(' Electric power, per engine (in W):', electric)

delta_sfc_factor_electric = 0.011 / (250 * Units.hp) * electric
print(' Resulting delta SFC factor (electric): %.4f' % delta_sfc_factor_electric)
SFC = reference_SFC_before_Offtakes + delta_sfc_factor_electric * reference_SFC_before_Offtakes

system_mass_factor = 1.57
print(' -> SFC: %.4f (should be 0.4498)' % SFC)

print('\n')
sfc_avacon = 0.475 / 1.006
print(' Avacon SFC:', sfc_avacon)
sfc_trent_700 = 0.565
sfc_ultrafan = sfc_trent_700 / 1.25
print(' Ultrafan SFC:', sfc_ultrafan)


