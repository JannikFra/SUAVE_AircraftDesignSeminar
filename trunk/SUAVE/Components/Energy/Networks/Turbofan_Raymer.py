## @ingroup Components-Energy-Networks
# Simple_Propulsor.py
# 
# Created:  Ago 2018, M. Gallani


# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

# suave imports
import SUAVE

# package imports
import numpy as np
from SUAVE.Components.Energy.Networks import Network
import scipy.interpolate
from pathlib import Path
import os
from SUAVE.Core import Data, Units

# ----------------------------------------------------------------------
#  Network
# ----------------------------------------------------------------------

## @ingroup Components-Energy-Networks
class Turbofan_Raymer(Network):
    """ A simple prpulsor network that just outputs thrust as a function of a Max Thrust and throttle settings.
        
        Unknowns:
            Throttle
    
        Assumptions:
        
        Source:
        None
    """      
    def __defaults__(self):
        """ This sets the default values for the network to function.
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            None
    
            Outputs:
            None
    
            Properties Used:
            N/A
        """            

        self.sealevel_static_thrust = 0.
        self.max_thrust_factor = 1.
        self.tsfc_factor               = 1.
        self.nacelle_diameter  = None
        self.engine_length     = None
        self.number_of_engines = None
        self.tag               = 'network'

        tool_path = Path(__file__).resolve().parents[3]

        max_thrust_surrogate_path = os.path.join(tool_path, "Data_Files", "maxthrust.csv")
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
                                                                        max_thrust_data[
                                                                            np.where(max_thrust_data[:, 0] == ALT)[
                                                                                0], 1],
                                                                        max_thrust_data[
                                                                            np.where(max_thrust_data[:, 0] == ALT)[
                                                                                0], 2],
                                                                        fill_value='extrapolate',
                                                                        kind='quadratic')(max_thrust_mach_vector))
                                                                   )
        self.max_thrust_interp = scipy.interpolate.RegularGridInterpolator(
            (max_thrust_altitude_vector, max_thrust_mach_vector), max_thrust_over_all_altitudes_and_mach, bounds_error=False, fill_value=70000)

        tsfc_surrogate_path = os.path.join(tool_path, "Data_Files", "tsfc.csv")
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

        self.tsfc_interp = scipy.interpolate.RegularGridInterpolator(
            (tsfc_mach_vector, tsfc_throttle_vector, tsfc_altitude_vector), tsfc_total, bounds_error=False, fill_value=0.55)

    
    # manage process with a driver function
    def evaluate_thrust(self,state):
        """ Calculate thrust given the current state of the vehicle
    
            Assumptions:
                
            Source:

    
            Inputs:

    
            Outputs:
    
    
            Properties Used:
            Defaulted values
        """          
    
        # unpack
        conditions  = state.conditions

        altitude        = conditions.freestream.altitude[:,0,None]
        mach            = conditions.freestream.mach_number[:,0,None]
        eta         = conditions.propulsion.throttle[:,0,None]  #beschreibt Stellung des Schubhebels
        
#        eta[eta > 1.0] = 1.0
        max_thrust = self.get_max_thrust(altitude, mach)
        tsfc = self.get_tsfc(altitude, mach, eta)

        F = eta * max_thrust * [1,0,0] * self.number_of_engines
        mdot = eta * max_thrust / 9.81 * tsfc * self.number_of_engines

        conditions.propulsion.thrust = F
        results = Data()
        results.thrust_force_vector     = F
        results.vehicle_mass_rate       = mdot
        results.network_y_axis_rotation = conditions.ones_row(1) * 0.0
        return results

    def get_max_thrust(self, altitude, mach):
        altitude = altitude / Units.ft
        points = np.array([altitude, mach]).T
        maxthrust = self.max_thrust_interp(points)
        maxthrust = maxthrust.T * Units.lbf * self.max_thrust_factor
        return maxthrust

    def get_tsfc(self, altitude, mach, throttle):
        altitude = altitude / Units.ft
        points = np.array([mach, throttle, altitude]).T
        tsfc = self.tsfc_interp(points)
        tsfc = tsfc.T / 3600 * self.tsfc_factor
        return tsfc

    def scale_factors(self, design_cruise_altitude, design_cruise_mach, sea_level_static_thrust, throttle_mid_cruise, bucket_sfc=0.533981):
        self.tsfc_factor = 1.
        self.max_thrust_factor = 1.
        sea_level_static_thrust_per_engine = sea_level_static_thrust / self.number_of_engines
        surrogate_sea_level_static_thrust_per_engine = self.get_max_thrust(0, 0)
        max_thrust_factor = sea_level_static_thrust_per_engine / surrogate_sea_level_static_thrust_per_engine

        design_cruise_altitude = design_cruise_altitude / Units.ft
        if design_cruise_altitude < 36000.:
            ref_sfc = (1 + .003 * (abs(design_cruise_altitude-36000.)/1000)) * bucket_sfc
        else:
            ref_sfc = (1 + .002 * (abs(design_cruise_altitude - 36000.) / 1000)) * bucket_sfc
        ref_sfc = ref_sfc + 0.006 * (design_cruise_mach-0.82)/0.01

        ref_sfc = ref_sfc / 3600.
        surrogate_sfc = self.get_tsfc(design_cruise_altitude*Units.ft, design_cruise_mach, throttle_mid_cruise)
        sfc_factor = ref_sfc / surrogate_sfc

        self.sealevel_static_thrust = sea_level_static_thrust
        self.max_thrust_factor = max_thrust_factor
        self.tsfc_factor = sfc_factor
    
    def unpack_unknowns(self,segment,state):
        """ This is an extra set of unknowns which are unpacked from the mission solver and send to the network.
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            state.unknowns.propeller_power_coefficient [None]
    
            Outputs:
            state.conditions.propulsion.propeller_power_coefficient [None]
    
            Properties Used:
            N/A
        """       
        
        return
    
    def residuals(self,segment,state):
        """ This packs the residuals to be send to the mission solver.
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            state.conditions.propulsion:
                motor_torque                          [N-m]
                propeller_torque                      [N-m]
            
            Outputs:
            None
    
            Properties Used:
            None
        """  
        
        # Here we are going to pack the residuals from the network
        # Equation 1: Power balance between motor and propeller
        
        return        
            
    __call__ = evaluate_thrust

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    tf = Turbofan_Raymer()
    tf.number_of_engines = 2.
    design_altitudes = np.array([32000., 35000., 38000.]) * Units.ft
    altitudes = np.linspace(30000., 40000, 100) * Units.ft
    mach = 0.82

    for i, DALT in enumerate(design_altitudes):
        tf.scale_factors(DALT, mach, 140000 * Units.lbf)
        print('DALT:', DALT, 'SFC_F:', tf.tsfc_factor)
        machs = mach * np.ones_like(altitudes)
        throttles = np.ones_like(altitudes)
        tsfcs = tf.get_tsfc(altitudes, machs, throttles)
        tsfcs = tsfcs * 3600.
        plt.plot(altitudes/Units.ft, tsfcs, label=round(DALT/Units.ft,0))

    ref_sfc = np.ones_like(altitudes)
    for i, ALT in enumerate(altitudes):
        ALT = ALT / Units.ft
        if ALT < 36000.:
            ref_sfc[i] = (1 + .003 * (abs(ALT - 36000.) / 1000)) * 0.533981
        else:
            ref_sfc[i] = (1 + .002 * (abs(ALT - 36000.) / 1000)) * 0.533981
        ref_sfc[i] = ref_sfc[i] + 0.006 * (mach - 0.82) / 0.01
    plt.plot(altitudes/Units.ft, ref_sfc, label='Airbus')
    plt.legend()
    plt.show()

    design_machs = np.array([0.82, 0.85, 0.88])
    machs = np.linspace(0.82, 0.88, 50)
    DALT = 32000 * Units.ft

    for i, DMACH in enumerate(design_machs):
        tf.scale_factors(DALT, DMACH, 140000 * Units.lbf)
        alts = DALT * np.ones_like(machs)
        throttles = np.ones_like(machs)
        tsfcs = tf.get_tsfc(alts, machs, throttles)
        tsfcs = tsfcs * 3600.
        plt.plot(machs, tsfcs, label=DMACH)

    DALT = DALT / Units.ft
    if DALT < 36000.:
        ref_sfc = (1 + .003 * (abs(DALT - 36000.) / 1000)) * 0.533981
    else:
        ref_sfc = (1 + .002 * (abs(DALT - 36000.) / 1000)) * 0.533981
    ref_sfc = ref_sfc + 0.006 * (machs - 0.82) / 0.01
    plt.plot(machs, ref_sfc, label='Airbus')
    plt.legend()
    plt.show()

