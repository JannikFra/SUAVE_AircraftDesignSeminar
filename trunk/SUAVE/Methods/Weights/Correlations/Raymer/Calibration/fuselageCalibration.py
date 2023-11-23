import numpy as np
import math
from SUAVE.Core import Units

Klg = 1
DG = 279000 * Units.kilogram / Units.lbs
L = 62.839 * Units.meter / Units.ft

Kdoor = 1.12  # Assuming 2 cargo doors
D = 5.82 * Units.meter / Units.ft
Sf = np.pi * (L / D - 1.7) * D ** 2  # Fuselage wetted area, ft**2

wingspan = 70 / Units.ft
taper = 0.2893
sweep = 29.7 * math.pi/180

Nz = 3.75

Kws = 0.75 * ((1 + 2 * taper) / (1 + taper)) * (wingspan / Units.ft *
                                                        np.tan(sweep) / L)

CALIBRATION = 1.253

weight_fuse = CALIBRATION * 0.328 * Kdoor * Klg * (DG * Nz) ** 0.5 * L ** 0.25 * \
              Sf ** 0.302 * (1 + Kws) ** 0.04 * (L / D) ** 0.1

print(weight_fuse * Units.lbs / Units.kilogram)
