import numpy as np
from SUAVE.Core import Units

NENG            = 2
Kng             = 1.017     # assuming the engine is pylon mounted
Nlt             = 2.71 / Units.ft
Nw              = 2.05 / Units.ft
Nz              = 3.75
Kp              = 1.    # assuming no prop engine
Ktr             = 1.    # assuming no thrust reverser, otherwise 1.18
WENG            = 8946 / Units.lbs
Wec             = 2.331 * WENG ** 0.901 * Kp * Ktr
Sn              = 2 * np.pi * Nw/2 * Nlt + np.pi * Nw**2/2
print('Sn = ', Sn * Units.ft**2)

CALIBRATION_NAC = 1.
WNAC            = CALIBRATION_NAC * 0.6724 * Kng * Nlt ** 0.1 * Nw ** 0.294 * Nz ** 0.119 \
                  * Wec ** 0.611 * NENG ** 0.984 * Sn ** 0.224
print('WNAC = ', WNAC * Units.lbs)
