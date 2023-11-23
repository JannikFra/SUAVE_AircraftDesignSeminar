import numpy as np
from pathlib import Path
import os
import scipy.interpolate
import pandas as pd
from SUAVE.Core import Units
class Turbofan:
    def __init__(self):
        tool_path = Path(__file__).resolve().parents[1]

        max_thrust_surrogate_path = os.path.join(tool_path, "trunk", "SUAVE", "Data_Files", "maxthrust.csv")
        max_thrust_data = np.loadtxt(max_thrust_surrogate_path, delimiter=",", skiprows=1)

        max_thrust_altitude_vector = np.unique(max_thrust_data[:, 0])
        max_thrust_mach_vector = np.linspace(0, 0.9, 20)

        max_thrust_over_all_altitudes_and_mach = np.array([])
        for i, ALT in enumerate(max_thrust_altitude_vector):
            if i == 0:
                max_thrust_over_all_altitudes_and_mach = scipy.interpolate.interp1d(
                    max_thrust_data[np.where(max_thrust_data[:, 0] == ALT)[0], 1],
                    max_thrust_data[np.where(max_thrust_data[:, 0] == ALT)[0], 2],
                    fill_value='extrapolate',
                    kind='quadratic')(max_thrust_mach_vector)
            else:
                max_thrust_over_all_altitudes_and_mach = np.vstack((max_thrust_over_all_altitudes_and_mach,
                                                           scipy.interpolate.interp1d(
                                                               max_thrust_data[np.where(max_thrust_data[:, 0] == ALT)[0], 1],
                                                               max_thrust_data[np.where(max_thrust_data[:, 0] == ALT)[0], 2],
                                                               fill_value='extrapolate',
                                                               kind='quadratic')(max_thrust_mach_vector))
                                                          )
        self.max_thrust_interp = scipy.interpolate.RegularGridInterpolator((max_thrust_altitude_vector, max_thrust_mach_vector), max_thrust_over_all_altitudes_and_mach)

        tsfc_surrogate_path = os.path.join(tool_path, "trunk", "SUAVE", "Data_Files", "tsfc.csv")
        tsfc_data = np.loadtxt(tsfc_surrogate_path, delimiter=",", skiprows=1)

        tsfc_altitude_vector = np.unique(tsfc_data[:, 0])
        tsfc_mach_vector = np.unique(tsfc_data[:, 1])
        tsfc_throttle_vector = np.linspace(0, 1, 20)

        for i, ALT in enumerate(tsfc_altitude_vector):
            for j, MACH in enumerate(tsfc_mach_vector):
                if j == 0:
                    tsfc_data_alt_fit = tsfc_data[np.where(tsfc_data[:, 0] == ALT)]
                    if MACH > max(tsfc_data_alt_fit[:, 1]):
                        MACH = max(tsfc_data_alt_fit[:, 1])
                    elif MACH < min(tsfc_data_alt_fit[:, 1]):
                        MACH = min(tsfc_data_alt_fit[:, 1])

                    points = np.array([ALT, MACH]).T
                    max_thrust = self.max_thrust_interp(points)
                    tsfc_thrust_vector = tsfc_throttle_vector * max_thrust
                    tsfc_data_alt_and_mach_fit = tsfc_data_alt_fit[np.where(tsfc_data_alt_fit[:, 1] == MACH)]

                    if np.ndim(tsfc_data_alt_and_mach_fit) == 2:
                        tsfc_for_this_mach_total = scipy.interpolate.interp1d(
                            tsfc_data_alt_and_mach_fit[:, 2],
                            tsfc_data_alt_and_mach_fit[:, 3],
                            fill_value='extrapolate',
                            kind='linear')(tsfc_thrust_vector)
                    else:
                        tsfc_for_this_mach_total = 2 * np.ones_like(tsfc_thrust_vector)
                else:
                    tsfc_data_alt_fit = tsfc_data[np.where(tsfc_data[:, 0] == ALT)]
                    if MACH > max(tsfc_data_alt_fit[:, 1]):
                        MACH = max(tsfc_data_alt_fit[:, 1])
                    elif MACH < min(tsfc_data_alt_fit[:, 1]):
                        MACH = min(tsfc_data_alt_fit[:, 1])

                    points = np.array([ALT, MACH]).T
                    max_thrust = self.max_thrust_interp(points)
                    tsfc_thrust_vector = tsfc_throttle_vector * max_thrust
                    tsfc_data_alt_and_mach_fit = tsfc_data_alt_fit[np.where(tsfc_data_alt_fit[:, 1] == MACH)]

                    if np.ndim(tsfc_data_alt_and_mach_fit) == 2:
                        tsfc_for_this_mach_current = scipy.interpolate.interp1d(
                            tsfc_data_alt_and_mach_fit[:, 2],
                            tsfc_data_alt_and_mach_fit[:, 3],
                            fill_value='extrapolate',
                            kind='linear')(tsfc_thrust_vector)
                    else:
                        tsfc_for_this_mach_current = 2 * np.ones_like(tsfc_thrust_vector)

                    tsfc_for_this_mach_total = np.vstack((tsfc_for_this_mach_total, tsfc_for_this_mach_current))

            if i == 0:
                tsfc_total = tsfc_for_this_mach_total
            else:
                tsfc_total = np.dstack((tsfc_total, tsfc_for_this_mach_total))

        self.tsfc_interp = scipy.interpolate.RegularGridInterpolator((tsfc_mach_vector, tsfc_throttle_vector, tsfc_altitude_vector), tsfc_total)

    def get_max_thrust(self, altitude, mach):
        altitude = altitude# / Units.ft
        points = np.array([altitude, mach]).T
        maxthrust = self.max_thrust_interp(points)
        maxthrust = maxthrust * Units.lb
        return maxthrust

    def get_tsfc(self, altitude, mach, throttle):
        altitude = altitude / Units.ft
        points = np.array([mach, throttle, altitude]).T
        tsfc = self.tsfc_interp(points)
        return tsfc


if __name__ == '__main__':
    tf = Turbofan()
    import matplotlib.pyplot as plt

    alts = np.array([10000]) * Units.ft
    machs = np.array([0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
    throttle = np.linspace(0, 1, 100)

    # for alt in alts:
    #     altis = np.ones_like(mach) * alt
    #     max_thrust = tf.get_max_thrust(altis, mach) / Units.lb
    #     plt.plot(mach, max_thrust, label=alt)

    for alt in alts:
        for mach in machs:
            altis = np.ones_like(throttle) * alt
            machis = np.ones_like(throttle) * mach
            tsfc = tf.get_tsfc(altis, machis, throttle)
            max_thrust = tf.get_max_thrust(altis, machis) / Units.lb
            thrust = throttle * max_thrust
            plt.plot(thrust, tsfc, label=mach)

    #plt.axis([0., 14000., 0.4, 1.1])
    #plt.legend()
    plt.title(alts / Units.ft)
    plt.show()

#     altitude = 45000 * Units.ft
#     mach = 0.3
#     throttle = 1
#     print(tf.get_tsfc(altitude, mach, throttle)
# )



