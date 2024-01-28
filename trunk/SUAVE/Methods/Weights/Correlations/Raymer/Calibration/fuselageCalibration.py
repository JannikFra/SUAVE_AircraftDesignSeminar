import numpy as np
import math
from SUAVE.Core import Units

Klg = 1
DG = 279000 / Units.lbs
L = 63.202 / Units.ft
fuse_w = 5.85 / Units.ft
fuse_h = 5.787 / Units.ft

Kdoor = 1.12  # Assuming 2 cargo doors
D     = (fuse_w + fuse_h) / 2.
Sf = np.pi * (L / D - 1.7) * D ** 2  # Fuselage wetted area, ft**2
# Sf = np.pi * (fuse_w+fuse_h)/2 * L * 0.7

wingspan = 70
taper = 0.2893
sweep = 29.7 * Units.deg

Nz = 3.75

Kws = 0.75 * ((1 + 2 * taper) / (1 + taper)) * (wingspan / Units.ft *
                                                        np.tan(sweep) / L)

CALIBRATION = 1.279

weight_fuse = CALIBRATION * 0.328 * Kdoor * Klg * (DG * Nz) ** 0.5 * L ** 0.25 * \
              Sf ** 0.302 * (1 + Kws) ** 0.04 * (L / D) ** 0.1

print(weight_fuse * Units.lbs)
