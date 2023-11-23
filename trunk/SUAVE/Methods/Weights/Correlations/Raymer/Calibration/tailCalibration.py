import numpy as np
import math
from SUAVE.Core import Units

# horizontal tail
Kuht = 1  # not a all-moving unit horizontal tail
Fw = 5.85 / Units.ft
Bh = 19.404 / Units.ft
DG = 279000 / Units.lbs
Sht = 71.4 / Units.ft ** 2
Lt = 28.025 / Units.ft
Ky = 0.3 * Lt
sweep = 30 * Units.deg
Ah = 5.27
Se = 0.25 * Sht
Nz = 3.75

CALIBRATION_HT = 0.938

tail_weight = CALIBRATION_HT * 0.0379 * Kuht * (1 + Fw / Bh) ** (-0.25) * DG ** 0.639 * \
          Nz ** 0.1 * Sht ** 0.75 * Lt ** -1 * \
          Ky ** 0.704 * np.cos(sweep) ** (-1) * Ah ** 0.166 * (1 + Se / Sht) ** 0.1

print('HT WEIGHT: ',tail_weight * Units.lbs)

# vertical tail
DG = 279000 / Units.lbs
t_tail_flag = 0

Svt = 45.2 / Units.ft ** 2
sweep = 40 * Units.deg
Av = 1.524
t_c = 0.11
Nult = 3.75

H = 0
if t_tail_flag:
    H = 1
Lt = 26.423 * Units.meter / Units.ft
Kz = Lt

CALIBRATION_VT = 0.612

tail_weight = CALIBRATION_VT * 0.0026 * (1 + H) ** 0.225 * DG ** 0.556 * Nult ** 0.536 \
              * Lt ** (-0.5) * Svt ** 0.5 * Kz ** 0.875 * np.cos(sweep) ** (-1) * Av ** 0.35 * t_c ** (-0.5)

print('VT WEIGHT: ',tail_weight * Units.lbs)
