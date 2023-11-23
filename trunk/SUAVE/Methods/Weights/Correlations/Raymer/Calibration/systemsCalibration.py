import numpy as np
import math
from SUAVE.Core import Units

L  = 62.839 * Units.meter / Units.ft
Bw = 70 * Units.meter / Units.ft
DG = 279000 * Units.kilogram / Units.lbs
# Scs = vehicle.wings['main_wing'].flap_ratio * vehicle.reference_area / Units.ft ** 2
design_mach = 0.82
num_pax = 100
fuse_w = 5.85 * Units.meter / Units.ft
fuse_h = 5.787 * Units.meter / Units.ft
cargo_weight = 14500 * Units.kilogram / Units.lbs
NENG = 2

flight_crew = 6
Ns = 4  # Number of flight control systems (typically 4)
Kr = 1  # assuming not a reciprocating engine
Ktp = 1  # assuming not a turboprop
Nf = 7  # number of functions performed by controls (typically 4-7)
Rkva = 60  # system electrical rating
Wuav = 1400  # uninstalled avionics weight

D = (fuse_w + fuse_h) / 2.
Sf = np.pi * (L / D - 1.7) * D ** 2  # Fuselage wetted area, ft**2

Vpr = D ** 2 * np.pi / 4 * (35 / Units.ft)

# WSC = 36.28 * design_mach ** 0.003 * Scs ** 0.489 * Ns ** 0.484 * flight_crew ** 0.124

WAPU = 500 * Units.kilogram / Units.lbs

WIN = 4.509 * Kr * Ktp * flight_crew ** 0.541 * NENG * (L + Bw) ** 0.5
print('WIN = ', WIN * Units.lbs / Units.kilogram)

CALIBRATION_HYD = 6.35
WHYD = CALIBRATION_HYD * 0.2673 * Nf * (L + Bw) ** 0.937
print('WHYD = ', WHYD * Units.lbs / Units.kilogram)

CALIBRATION_ELEC = 5.714
WELEC = CALIBRATION_ELEC * 7.291 * Rkva ** 0.782 * (2 * L) ** 0.346 * NENG ** 0.1
print('WELEC = ', WELEC * Units.lbs / Units.kilogram)

# WAVONC = 1.73 * Wuav ** 0.983

CALIBRATION_FURN = 4.285
WFURN = CALIBRATION_FURN * 0.0577 * flight_crew ** 0.1 * (cargo_weight) ** 0.393 * Sf ** 0.75
print('WFURN = ', WFURN * Units.lbs / Units.kilogram)

CALIBRATION_AC = 0.789
WAC = CALIBRATION_AC * 62.36 * num_pax ** 0.25 * (Vpr / 1000) ** 0.604 * Wuav ** 0.1
print('WAC = ', WAC * Units.lbs / Units.kilogram)

WSYS = WAC + WELEC + WHYD
# print('WSYS = ', WSYS * Units.lbs / Units.kilogram)

# Fuel System
Vt = 48433  # total fuel volume, gal
Vi = Vt     # integral tanks volume, gal
Vp = 0      # self-sealing "protected" tanks volume, gal
Nt = 5      # number of fuel tanks

CALIBRATION_FSYS = 0.831
WFSYS = CALIBRATION_FSYS * 2.405 * Vt ** 0.606 * (1 + Vi/Vt) ** (-1.0) * (1 + Vp/Vt) * Nt ** 0.5
print('WFSYS = ', WFSYS * Units.lbs / Units.kilogram)

# WAI = 0.002 * DG

