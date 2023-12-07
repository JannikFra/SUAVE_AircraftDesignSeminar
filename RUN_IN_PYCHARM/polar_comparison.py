import numpy as np
import matplotlib.pyplot as plt
from SUAVE.Core import Units
mach_star = 0.919

t_c_w   = 0.1
sweep_w = 0 * Units.deg
cos_sweep = np.cos(sweep_w)

t_c_w = np.linspace(0.04, 0.16, 5)

cl_w_1 = 1.
mach_dd_1 = mach_star / cos_sweep - t_c_w / cos_sweep**2 - 0.1 * (1.1*abs(cl_w_1))**1.5 / cos_sweep**4

cl_w_2 = 0.7
mach_dd_2 = mach_star / cos_sweep - t_c_w / cos_sweep**2 - 0.1 * (1.1*abs(cl_w_2))**1.5 / cos_sweep**4

cl_w_3 = 0.4
mach_dd_3 = mach_star / cos_sweep - t_c_w / cos_sweep**2 - 0.1 * (1.1*abs(cl_w_3))**1.5 / cos_sweep**4

x = np.array([2.733423545331529, 15.77807848443843, 4.005412719891746, 16.102841677943168, 4.411366711772666, 15.696887686062247]) * 0.01
y = np.array([0.8842287694974003, 0.7441941074523397, 0.8308492201039861, 0.7227036395147314, 0.7774696707105719, 0.676949740034662])

plt.plot([x[0], x[1]], [y[0], y[1]], color='black', label='NASA')
plt.plot([x[2], x[3]], [y[2], y[3]], color='black', label='NASA')
plt.plot([x[4], x[5]], [y[4], y[5]], color='black', label='NASA')

plt.plot(t_c_w, mach_dd_1)
plt.plot(t_c_w, mach_dd_2)
plt.plot(t_c_w, mach_dd_3)
plt.grid('on')
plt.legend()
plt.show()

