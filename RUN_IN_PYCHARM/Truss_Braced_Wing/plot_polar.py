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
from Truss_Braced_Wing import configs_setup
import matplotlib.pyplot as plt


def main(altitude, mach, wing_loading, plot=True):
    #print("ALT: ",altitude)
    #print("MACH: ", mach)
    iteration_setup = Data()
    iteration_setup.weight_iter = Data()
    iteration_setup.mission_iter = Data()
    iteration_setup.sizing_iter = Data()
    iteration_setup.weight_iter.TOW = 192_997
    iteration_setup.weight_iter.BOW = 102_278
    iteration_setup.weight_iter.FUEL = 66_218
    iteration_setup.weight_iter.Design_Payload = 24_500
    iteration_setup.mission_iter.design_cruise_altitude = altitude
    iteration_setup.mission_iter.design_cruise_mach = mach

    iteration_setup.mission_iter.throttle_mid_cruise = 1.
    #iteration_setup.sizing_iter.wing_loading = 750.
    iteration_setup.sizing_iter.wing_loading = wing_loading
    iteration_setup.sizing_iter.thrust_loading = 0.23
    iteration_setup.sizing_iter.aspect_ratio = 20.
    iteration_setup.sizing_iter.thickness_to_chord = 0.10
    iteration_setup.sizing_iter.sweep_quarter_chord = 28 * Units.deg
    iteration_setup.sizing_iter.wing_origin = [[20., 0, 4.]]

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
    aerodynamics.settings.drag_coefficient_increment.cruise = -12e-4 + 19e-4 -5e-4
    aerodynamics.settings.drag_coefficient_increment.descent = 0
    aerodynamics.settings.drag_coefficient_increment.landing = 0
    aerodynamics.settings.recalculate_total_wetted_area = True
    aerodynamics.settings.use_surrogate = False
    aerodynamics.settings.model_fuselage = True
    aerodynamics.settings.model_nacelle = True
    aerodynamics.settings.compressibility_drag_correction_factor = 1.
    aerodynamics.settings.mach_star = 0.91  # 0.921
    aerodynamics.settings.compressibility_constant_n = 20.  # 2.5
    aerodynamics.settings.compressibility_constant_dM = 0.05

    aerodynamics.settings.oswald_efficiency_factor = 0.89

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

    cd0 = np.interp(0, cl[:, 0], cd_tot[:, 0])
    print('cd0', cd0)
    #print(l_d)

    specific_air_range = 1 / l_d * ref_sfc / (design_cruise_mach * a) * 9.81 * iteration_setup.weight_iter.TOW
    #print('Specific Air Range ', specific_air_range[0][0])

    # plt.plot(angle_of_attacks/Units.deg,cl)
    # plt.show()
    if plot:
        cl_quad = np.linspace(0.0, 0.8, 100)
        cd_quad = 0.0108 + 1/(np.pi*0.796*vehicle.wings.main_wing.aspect_ratio) * cl_quad**2
        #plt.plot(cd_quad, cl_quad, label="quadratic")
        #plt.plot(cd_tot, cl, label="SUAVE")
        #plt.plot(cd_c, cl, label="compressibility")
        #plt.plot(cd_i, cl, label="induced")
        #plt.plot(cd_m, cl, label="miscellaneous")
        #plt.plot(cd_p_fuse, cl, label="parasite fuselage")
        #plt.plot(cd_p_wing, cl, label="parasite wing")
        #plt.hlines(cl_actual, 0, 1)
        cl_ref = np.array([0., 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.56, 0.57, 0.58, 0.59, 0.6, 0.65, 0.7, 0.75])
        cd_ref = np.array([0.0108, 0.0123, 0.0132, 0.0143, 0.0156, 0.0171, 0.0188, 0.0208, 0.0238, 0.0246, 0.0254, 0.0264, 0.0274,
              0.0288, 0.0366, 0.0530, 0.0947])
        #plt.scatter(cd_ref, cl_ref, label="Airbus")
        #plt.grid('on')
        #plt.axis([0, 0.1, 0, 1.])
        #plt.legend()
        #plt.show()

        cl_base = [-0.64663888, -0.59831168, -0.54992253, -0.50147641, -0.45297826, -0.40443301, -0.35584557,
                   -0.30722081, -0.2585636, -0.20987878, -0.16117117, -0.11244559, -0.06370684, -0.0149597, 0.03379105,
                   0.08254064, 0.1312843, 0.18001727, 0.2287348, 0.27743212, 0.32610448, 0.37474711, 0.42335524,
                   0.4719241, 0.5204489, 0.56892484, 0.61734711, 0.6657109, 0.71401137, 0.76224365, 0.81040287,
                   0.85848414, 0.90648253, 0.9543931, 1.00221088, 1.04993088, 1.09754807, 1.14505739, 1.19245376,
                   1.23973206, 1.28688713, 1.33391378, 1.38080678, 1.42756089, 1.47417078, 1.52063112, 1.56693653,
                   1.61308158, 1.65906082, 1.70486872]
        l_d_base = [-26.96722445, -26.72716744, -26.25232156, -25.52774633, -24.52755119, -23.22323278, -21.5886409,
                    -19.60439632, -17.26233012, -14.56974088, -11.55285761, -8.25869177, -4.7545068, -1.12448739,
                    2.53516019, 6.12604248, 9.55645225, 12.74805371, 15.64088077, 18.19568892, 20.3934762, 22.232694,
                    23.72517459, 24.89119799, 25.75365948, 26.32934123, 26.60686467, 26.43664087, 24.92181177,
                    22.27184786, 18.52438237, 14.27949349, 10.31625245, 7.13225344, 4.82051353, 3.23762194, 2.18367231,
                    1.48783601, 1.02709072, 0.71921012, 0.51093982, 0.36812393, 0.26881799, 0.19881261, 0.14880573,
                    0.11263177, 0.08615078, 0.06654667, 0.05187949, 0.04079644]
        cl_ref = [-0.56647585, -0.523942, -0.4813547, -0.43871854, -0.39603805, -0.35331778, -0.31056222, -0.26777586,
                  -0.22496317, -0.1821286, -0.13927658, -0.09641154, -0.05353788, -0.01066, 0.03221772, 0.0750909,
                  0.11795517, 0.16080617, 0.20363953, 0.2464509, 0.28923593, 0.33199025, 0.37470951, 0.41738936,
                  0.46002542, 0.50261333, 0.5451487, 0.58762716, 0.6300443, 0.67239571, 0.71467699, 0.75688368,
                  0.79901133, 0.84105549, 0.88301167, 0.92487535, 0.96664203, 1.00830713, 1.04986611, 1.09131437,
                  1.13264728, 1.17386021, 1.21494848, 1.2559074, 1.29673223, 1.33741823, 1.37796062, 1.41835456,
                  1.45859522, 1.49867772]
        l_d_ref = [-23.77599443, -24.14551249, -24.19428046, -23.98099152, -23.48597872, -22.66693254, -21.4737788,
                   -19.85752702, -17.77920174, -15.2199354, -12.19132609, -8.74377888, -4.96978734, -0.99957763,
                   3.00999422, 6.89715809, 10.5174494, 13.75869211, 16.54955242, 18.85976837, 20.69379178, 22.08095855,
                   23.06449075, 23.69060747, 23.99570791, 23.97832716, 23.45469243, 21.71231127, 19.21609773,
                   16.00480456, 12.5207997, 9.27949895, 6.6163014, 4.61359898, 3.18906481, 2.20587947, 1.5358441,
                   1.0799412, 0.76817277, 0.55309506, 0.40312557, 0.29734006, 0.22183793, 0.16732038, 0.1275094,
                   0.09812221, 0.07620521, 0.05969907, 0.0471524, 0.03753149]

        cl_calib =[-0.032,0.007,0.046,0.087,0.127,0.166,0.206,0.246,0.286,0.326,0.367,0.408,0.447,0.485,0.524,0.56,0.598,0.634,0.671,0.708,0.743,0.779,0.812,0.851,0.887]
        l_d_calib = [-1.97, 0.447, 2.87, 5.386, 7.856, 10.2, 12.426, 14.69, 16.80, 18.68, 20.56, 22.25, 23.79, 25.0, 26.1, 26.95, 27.43, 27.31, 24.57, 20.05, 15.1, 10.39, 7.17, 4.52, 2.92]

        #plt.plot(cl_base, l_d_base, label='Baseline')
        #plt.plot(cl_ref, l_d_ref, label='Reference')
        plt.plot(cl, cl/cd_tot, label="TBW")
        plt.plot(cl_calib, l_d_calib, label="Calibration")
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
    sar, sfc, l_d = main(38_000*Units.ft, 0.82, 700)
    print('sar', sar)
    print('sfc', sfc)
    print('l_d', l_d)
    #sweep()
