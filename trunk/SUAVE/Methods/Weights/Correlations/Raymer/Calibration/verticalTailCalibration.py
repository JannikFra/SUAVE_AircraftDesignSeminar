import numpy as np
import math
from SUAVE.Core import Units

DG = 279000 * Units.kilogram / Units.lbs
t_tail_flag = 0

Svt = 45.2 * Units.meter ** 2 / Units.ft ** 2
sweep = 40 * math.pi/180
Av = 1.524
t_c = 0.11
Nult = 3.75

H = 0
if t_tail_flag:
    H = 1
Lt = 26.423 * Units.meter / Units.ft
Kz = Lt

CALIBRATION = 0.612

tail_weight = CALIBRATION * 0.0026 * (1 + H) ** 0.225 * DG ** 0.556 * Nult ** 0.536 \
              * Lt ** (-0.5) * Svt ** 0.5 * Kz ** 0.875 * np.cos(sweep) ** (-1) * Av ** 0.35 * t_c ** (-0.5)

print(tail_weight * Units.lbs / Units.kilogram)