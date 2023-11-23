import numpy as np
import math
from SUAVE.Core import Units

Kmp         = 1  # assuming not a kneeling gear
WLDG        = 195000 * Units.kilogram / Units.lbs
Ngear       = 3  # gear load factor, usually around 3
Nl          = Ngear * 1.5  # ultimate landing load factor
Lm          = 3.9 / Units.inch
Nmss        = 2  # number of main gear shock struts assumed to be 2
Nmw         = 8 * 2
Vstall      = 130 * Units.kts  # stall speed
Knp         = 1  # assuming not a kneeling gear
Ln          = 2.4 / Units.inch
Nnw         = 2

CALIBRATION = 0.802

wt_main_landing_gear = CALIBRATION * 0.0106 * Kmp * WLDG ** 0.888 * Nl ** 0.25 * Lm ** 0.4 * Nmw ** 0.321 * Nmss ** (-0.5) * Vstall ** 0.1
wt_nose_landing_gear = CALIBRATION * 0.032 * Knp * WLDG ** 0.646 * Nl ** 0.2 * Ln ** 0.5 * Nnw ** 0.45

wt_landing_gear = (wt_nose_landing_gear + wt_main_landing_gear) * Units.lbs / Units.kilogram
print(wt_landing_gear)
