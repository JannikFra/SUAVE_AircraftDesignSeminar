# aerodynamics.py
# 
# Created:  Sep 2014, T. MacDonald
# Modified: Nov 2016, T. MacDonald
#           Apr 2020, M. Clarke

# Modified to match compressibility drag updates

# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------


import SUAVE
from SUAVE.Core import Units
from SUAVE.Core import Data
from SUAVE.Plots.Geometry import *

import numpy as np
import pylab as plt

import copy, time
import random
from SUAVE.Attributes.Gases.Air import Air
import sys
#import vehicle file
from vehicle_setup import vehicle_setup
from Baseline import configs_setup
import matplotlib.pyplot as plt


def main(altitude, mach, wing_loading, plot=True):
    #print("ALT: ",altitude)
    #print("MACH: ", mach)
    iteration_setup = Data()
    iteration_setup.weight_iter = Data()
    iteration_setup.mission_iter = Data()
    iteration_setup.sizing_iter = Data()
    iteration_setup.weight_iter.TOW = 230_000
    iteration_setup.weight_iter.BOW = 130_000
    iteration_setup.weight_iter.FUEL = 100_000
    iteration_setup.weight_iter.Design_Payload = 24_500
    iteration_setup.mission_iter.design_cruise_altitude = altitude
    iteration_setup.mission_iter.design_cruise_mach = mach

    iteration_setup.mission_iter.throttle_mid_cruise = 1.
    #iteration_setup.sizing_iter.wing_loading = 750.
    iteration_setup.sizing_iter.wing_loading = wing_loading
    iteration_setup.sizing_iter.thrust_loading = 0.2275
    iteration_setup.sizing_iter.aspect_ratio = 13.5
    iteration_setup.sizing_iter.thickness_to_chord = 0.105
    iteration_setup.sizing_iter.sweep_quarter_chord = 29 * Units.deg
    iteration_setup.sizing_iter.wing_origin = [[22.408, 0, -1]]

    design_cruise_altitude = iteration_setup.mission_iter.design_cruise_altitude
    design_cruise_mach = iteration_setup.mission_iter.design_cruise_mach
    bucket_sfc = 0.475
    design_cruise_altitude = design_cruise_altitude / Units.ft
    if design_cruise_altitude < 36000.:
        ref_sfc = (1 + .003 * (abs(design_cruise_altitude - 36000.) / 1000)) * bucket_sfc
    else:
        ref_sfc = (1 + .002 * (abs(design_cruise_altitude - 36000.) / 1000)) * bucket_sfc
    ref_sfc = ref_sfc + 0.006 * (design_cruise_mach - 0.82) / 0.01
    #ref_sfc = ref_sfc / 3600.

    # initialize the vehicle
    vehicle = vehicle_setup(iteration_setup)
    configs = configs_setup(vehicle)

    # for wing in vehicle.wings:
    #     wing.areas.wetted   = 2.0 * wing.areas.reference
    #     wing.areas.exposed  = 0.8 * wing.areas.wetted
    #     wing.areas.affected = 0.6 * wing.areas.wetted

    t_c = vehicle.wings.main_wing.thickness_to_chord
    #print(t_c)
        

    # initalize the aero model
    aerodynamics = SUAVE.Analyses.Aerodynamics.Fidelity_Zero()
    aerodynamics.settings.drag_coefficient_increment = Data()
    aerodynamics.settings.drag_coefficient_increment.base = 0
    aerodynamics.settings.drag_coefficient_increment.takeoff = 0
    aerodynamics.settings.drag_coefficient_increment.climb = 0
    aerodynamics.settings.drag_coefficient_increment.cruise = -12e-4
    aerodynamics.settings.drag_coefficient_increment.descent = 0
    aerodynamics.settings.drag_coefficient_increment.landing = 0
    aerodynamics.settings.recalculate_total_wetted_area = True
    aerodynamics.settings.use_surrogate = False
    aerodynamics.settings.model_fuselage = True
    aerodynamics.settings.model_nacelle = True
    aerodynamics.settings.compressibility_drag_correction_factor = 1.
    aerodynamics.settings.mach_star = 0.919  # 0.921
    aerodynamics.settings.compressibility_constant_n = 10  # 2.5
    aerodynamics.settings.compressibility_constant_dM = 0.05

    aerodynamics.settings.oswald_efficiency_factor = 0.84

    aerodynamics.geometry = configs.cruise

    aerodynamics.initialize()
    
    
    #no of test points
    test_num = 50
    
    #specify the angle of attack
    angle_of_attacks = np.linspace(-5.,10.,test_num)[:,None] * Units.deg
    
    
    # Cruise conditions (except Mach number)
    state = SUAVE.Analyses.Mission.Segments.Conditions.State()
    state.conditions = SUAVE.Analyses.Mission.Segments.Conditions.Aerodynamics()
    
    
    state.expand_rows(test_num)

    atmosphere = SUAVE.Analyses.Atmospheric.US_Standard_1976()
    alt = iteration_setup.mission_iter.design_cruise_altitude

    Mc = mach * np.ones((test_num,1))
    
    rho = atmosphere.compute_values(alt).density * np.ones((test_num,1))
    
    mu =  atmosphere.compute_values(alt).dynamic_viscosity * np.ones((test_num,1)) # 0.0000144446
    
    T = atmosphere.compute_values(alt).temperature * np.ones((test_num,1))
    
    pressure = atmosphere.compute_values(alt).pressure * np.ones((test_num,1))

    a = atmosphere.compute_values(alt).speed_of_sound
    
    re = rho*a*Mc/mu

    cl_actual = iteration_setup.sizing_iter.wing_loading * 9.81 * 0.98 / (rho / 2 * (a * Mc)**2)

    state.conditions.freestream.mach_number = Mc
    state.conditions.freestream.density = rho
    state.conditions.freestream.dynamic_viscosity = mu
    state.conditions.freestream.temperature = T
    state.conditions.freestream.pressure = pressure
    state.conditions.freestream.reynolds_number = re
    state.conditions.freestream.velocity = a * Mc
    
    state.conditions.aerodynamics.angle_of_attack = angle_of_attacks   

    results = aerodynamics.evaluate(state)

    cl   = state.conditions.aerodynamics.lift_coefficient
    cd = state.conditions.aerodynamics.drag_coefficient



    drag_breakdown = state.conditions.aerodynamics.drag_breakdown
    cd_c           = drag_breakdown.compressible['main_wing'].compressibility_drag
    cd_i           = drag_breakdown.induced.total
    cd_m           = drag_breakdown.miscellaneous.total
    # cd_m_fuse_base = drag_breakdown.miscellaneous.fuselage_base
    # cd_m_fuse_up   = drag_breakdown.miscellaneous.fuselage_upsweep
    # cd_m_nac_base  = drag_breakdown.miscellaneous.nacelle_base['turbofan']
    # cd_m_ctrl      = drag_breakdown.miscellaneous.control_gaps
    cd_p_fuse      = drag_breakdown.parasite['fuselage'].parasite_drag_coefficient
    cd_p_wing      = drag_breakdown.parasite['main_wing'].parasite_drag_coefficient
    cd_tot         = drag_breakdown.total

    l_d = cl_actual[0][0] / np.interp(cl_actual[0][0], cl[:, 0], cd_tot[:, 0])
    #print(l_d)

    specific_air_range = 1 / l_d * ref_sfc / (design_cruise_mach * a) * 9.81 * iteration_setup.weight_iter.TOW
    #print('Specific Air Range ', specific_air_range[0][0])

    # plt.plot(angle_of_attacks/Units.deg,cl)
    # plt.show()
    if plot:
        cl_quad = np.linspace(0.0, 0.8, 100)
        cd_quad = 0.0108 + 1/(np.pi*0.796*vehicle.wings.main_wing.aspect_ratio) * cl_quad**2
        plt.plot(cd_quad, cl_quad, label="quadratic")
        plt.plot(cd_tot, cl, label="SUAVE")
        plt.plot(cd_c, cl, label="compressibility")
        plt.plot(cd_i, cl, label="induced")
        #plt.plot(cd_m, cl, label="miscellaneous")
        #plt.plot(cd_p_fuse, cl, label="parasite fuselage")
        #plt.plot(cd_p_wing, cl, label="parasite wing")
        plt.hlines(cl_actual, 0, 1)
        cl_ref = np.array([0., 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.56, 0.57, 0.58, 0.59, 0.6, 0.65, 0.7, 0.75])
        cd_ref = np.array([0.0108, 0.0123, 0.0132, 0.0143, 0.0156, 0.0171, 0.0188, 0.0208, 0.0238, 0.0246, 0.0254, 0.0264, 0.0274,
              0.0288, 0.0366, 0.0530, 0.0947])
        plt.scatter(cd_ref, cl_ref, label="Airbus")
        plt.grid('on')
        plt.axis([0, 0.1, 0, 1.])
        plt.legend()
        plt.show()

        plt.plot(cl_ref, cl_ref/cd_ref, label="Airbus")
        plt.plot(cl, cl/cd_tot, label="SUAVE")
        print(cl)
        print(cl/cd_tot)
        plt.vlines(cl_actual, 0, 50)
        plt.legend()
        plt.axis([0., 1., 0., 30.])
        plt.show()

    plot_vehicle(vehicle, plot_control_points=False, axis_limits=30)
    plt.show()
    return specific_air_range, ref_sfc, l_d


def sweep():

    wing_loading = np.linspace(300, 500, 10)
    altitudes = np.linspace(12000, 14800, 10)
    mach = 0.82

    X, Y = np.meshgrid(altitudes, wing_loading)

    sar = np.zeros_like(X)
    sfc = np.zeros_like(X)
    l_d = np.zeros_like(X)
    for i, alt in enumerate(altitudes):
        for j, wl in enumerate(wing_loading):
            sar[j, i], sfc[j, i], l_d[j, i] = main(alt, mach, wl, plot=False)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot_surface(X, Y, l_d)
    plt.show()

    print(np.min(sar))
    min_index = np.unravel_index(np.argmin(sar), sar.shape)
    print(sfc[min_index])
    print(l_d[min_index])
    print(X[min_index])
    print(Y[min_index])
    # ax.plot_surface(X, Y, sfc)
    # ax.plot_surface(X, Y, l_d)

if __name__ =='__main__':
    sar, sfc, l_d = main(35000*Units.ft, 0.82, 700)
    print('sar', sar)
    print('sfc', sfc)
    print('l_d', l_d)
    #sweep()
