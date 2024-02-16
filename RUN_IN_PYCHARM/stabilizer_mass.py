from SUAVE.Core import Units
import numpy as np

mass_v_tail = 2018 * Units.kg
print('mass_v_tail_suave', mass_v_tail)

Sref = 194866 / 700
mtom = 194865.6

SV = 0.14 * Sref
SH = 0.192 * Sref
SVTAIL = SV + SH

ARVTAIL = 5.27
ARH = 5.27
ARV = 1.524

BVTAIL = (SVTAIL*ARVTAIL)**0.5
BH = (SH*ARH)**0.5
BV = (SV*ARV)**0.5

elevator_fraction = 0.25

ultimate_load = 2.5*1.5
l_ht = 31.97

# V-Tail
Kuht    = 1 # not a all-moving unit horizontal tail
Fw      = 5.64 / Units.ft # 18.50
#Bh      = wing.spans.projected / Units.ft
Bh      = BVTAIL / Units.ft # Make it suitable for V-Tail 72.76
DG      = mtom / Units.lbs # 432682
Sht     = SVTAIL / Units.ft ** 2 # 1004.7
Lt      = l_ht / Units.ft # 104.9
Ky      = 0.3 * Lt # 31.46
sweep   = 33 / 180 * np.pi # 0.576
Ah      = ARVTAIL # 5.27
Se      = elevator_fraction * Sht # 251.17

CALIBRATION_HT = 0.938

tail_weight = CALIBRATION_HT * 0.0379 * Kuht * (1 + Fw / Bh) ** (-0.25) * DG ** 0.639 *\
              ultimate_load ** 0.1 * Sht ** 0.75 * Lt ** -1 *\
              Ky ** 0.704 * np.cos(sweep) ** (-1) * Ah ** 0.166 * (1 + Se / Sht) ** 0.1
vtail_weight =  tail_weight * Units.lbs

print('vtail weight', vtail_weight)

# H-Tail
Kuht    = 1 # not a all-moving unit horizontal tail
Fw      = 5.64 / Units.ft
#Bh      = wing.spans.projected / Units.ft
Bh      = BH / Units.ft # Make it suitable for V-Tail
DG      = mtom / Units.lbs
Sht     = SH / Units.ft ** 2
Lt      = l_ht / Units.ft
Ky      = 0.3 * Lt
sweep   = 30 / 180 * np.pi
Ah      = ARH
Se      = elevator_fraction * Sht

CALIBRATION_HT = 0.938

tail_weight = CALIBRATION_HT * 0.0379 * Kuht * (1 + Fw / Bh) ** (-0.25) * DG ** 0.639 *\
              ultimate_load ** 0.1 * Sht ** 0.75 * Lt ** -1 *\
              Ky ** 0.704 * np.cos(sweep) ** (-1) * Ah ** 0.166 * (1 + Se / Sht) ** 0.1
htail_weight =  tail_weight * Units.lbs

print('htail weight', htail_weight)

# Vert-Tail
DG          = mtom / Units.lbs
t_tail_flag = True
# wing_origin = wing.origin[0][0] / Units.ft
# wing_ac     = wing.aerodynamic_center[0] / Units.ft
# main_origin = vehicle.wings['main_wing'].origin[0][0] / Units.ft
# main_ac     = vehicle.wings['main_wing'].aerodynamic_center[0] / Units.ft
Svt         = SV / Units.ft ** 2
sweep       = 40 / 180 * np.pi
Av          = ARV
t_c         = 0.1
Nult        = ultimate_load

H = 0
if t_tail_flag:
    H = 1
Lt = l_ht
Kz = Lt

CALIBRATION_VT = 0.612

tail_weight = CALIBRATION_VT * 0.0026 * (1 + H) ** 0.225 * DG ** 0.556 * Nult ** 0.536 \
              * Lt ** (-0.5) * Svt ** 0.5 * Kz ** 0.875 * np.cos(sweep) ** (-1) * Av ** 0.35 * t_c ** (-0.5)
verttail_weight = tail_weight * Units.lb

print('htail weight', verttail_weight)

ttail_weight = verttail_weight + htail_weight
print('ttail_weight', ttail_weight)



