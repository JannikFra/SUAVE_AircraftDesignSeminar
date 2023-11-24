import numpy as np
from SUAVE.Core import Units

taper   = 0.0708    # 0.2893
sweep   = 0.5032    # 29.7 * Units.deg

Wdg     = 279000 / Units.lbs
Nz      = 3.75
Sw      = 490.6 / Units.ft ** 2
A       = 9.988
tc_root = 0.1299    # 0.1525
Scsw    = Sw * .1

CALIBRATION = 1.023

Wwing = CALIBRATION * 0.0051 * (Wdg * Nz) ** 0.557 * Sw ** 0.649 * A ** 0.5 * tc_root ** -0.4 * (1 + taper) ** 0.1 * \
            np.cos(sweep) ** -1. * Scsw ** 0.1
weight = Wwing * Units.lb

print('Wwing = ', weight)
