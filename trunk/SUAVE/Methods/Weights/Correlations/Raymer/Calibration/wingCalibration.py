import numpy as np
import math
from SUAVE.Core import Units

taper   = 0.2893
sweep   = 29.7 * math.pi/180

Wdg     = 279000 * Units.kilogram / Units.lbs
Nz      = 3.75
Sw      = 490.6 * Units.meter ** 2 / Units.ft ** 2
A       = 9.988
tc_root = 0.1525
Scsw    = Sw * .1

CALIBRATION = 1.023

Wwing = CALIBRATION * 0.0051 * (Wdg * Nz) ** .557 * Sw ** .649 * A ** .5 * tc_root ** -.4 * (1 + taper) ** .1 * np.cos(
    sweep) ** -1. * Scsw ** .1
weight = Wwing * Units.lb / Units.kilogram

print(weight)
