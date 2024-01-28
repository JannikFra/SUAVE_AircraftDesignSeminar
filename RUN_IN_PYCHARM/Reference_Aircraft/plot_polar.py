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

import numpy as np
import pylab as plt

import copy, time
import random
from SUAVE.Attributes.Gases.Air import Air
import sys
#import vehicle file
from vehicle_setup import vehicle_setup
from Reference_Aircraft import configs_setup
import matplotlib.pyplot as plt


def main():
    iteration_setup = Data()
    iteration_setup.weight_iter = Data()
    iteration_setup.mission_iter = Data()
    iteration_setup.weight_iter.TOW = 279_000
    iteration_setup.weight_iter.BOW = 130_000
    iteration_setup.weight_iter.FUEL = 115_000
    iteration_setup.weight_iter.Design_Payload = 24_500
    iteration_setup.mission_iter.design_cruise_altitude = 32_000 * Units.ft
    iteration_setup.mission_iter.design_cruise_mach = 0.82
    iteration_setup.mission_iter.throttle_mid_cruise = 1.

    # initialize the vehicle
    vehicle = vehicle_setup(iteration_setup)
    configs = configs_setup(vehicle)

    # for wing in vehicle.wings:
    #     wing.areas.wetted   = 2.0 * wing.areas.reference
    #     wing.areas.exposed  = 0.8 * wing.areas.wetted
    #     wing.areas.affected = 0.6 * wing.areas.wetted

    t_c = vehicle.wings.main_wing.thickness_to_chord
    print(t_c)


    # initalize the aero model
    aerodynamics = SUAVE.Analyses.Aerodynamics.Fidelity_Zero()
    aerodynamics.settings.drag_coefficient_increment = Data()
    aerodynamics.settings.drag_coefficient_increment.base = 0
    aerodynamics.settings.drag_coefficient_increment.takeoff = 0
    aerodynamics.settings.drag_coefficient_increment.climb = 0
    aerodynamics.settings.drag_coefficient_increment.cruise = -18e-4
    aerodynamics.settings.drag_coefficient_increment.descent = 0
    aerodynamics.settings.drag_coefficient_increment.landing = 0
    aerodynamics.settings.recalculate_total_wetted_area = True
    aerodynamics.settings.use_surrogate = False
    aerodynamics.settings.model_fuselage = True
    aerodynamics.settings.model_nacelle = True
    aerodynamics.settings.compressibility_drag_correction_factor = 1.
    aerodynamics.settings.mach_star = 0.919#0.921
    aerodynamics.settings.compressibility_constant_n = 10#2.5
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

    Mc = 0.82 * np.ones((test_num,1))

    rho = atmosphere.compute_values(alt).density * np.ones((test_num, 1))

    mu = atmosphere.compute_values(alt).dynamic_viscosity * np.ones((test_num, 1))  # 0.0000144446

    T = atmosphere.compute_values(alt).temperature * np.ones((test_num, 1))

    pressure = atmosphere.compute_values(alt).pressure * np.ones((test_num, 1))

    a = atmosphere.compute_values(alt).speed_of_sound
    
    re = rho*a*Mc/mu


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
   
    # plt.plot(angle_of_attacks/Units.deg,cl)
    # plt.show()
    cl_quad = np.linspace(0.0, 0.8, 100)
    cd_quad = 0.0108 + 1/(np.pi*0.796*vehicle.wings.main_wing.aspect_ratio) * cl_quad**2
    plt.plot(cd_quad, cl_quad, label="quadratic")
    plt.plot(cd_tot, cl, label="SUAVE")
    plt.plot(cd_c, cl, label="compressibility")
    plt.plot(cd_i, cl, label="induced")
    plt.plot(cd_m, cl, label="miscellaneous")
    plt.plot(cd_p_fuse, cl, label="parasite fuselage")
    plt.plot(cd_p_wing, cl, label="parasite wing")
    cl_ref = np.array([0., 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.56, 0.57, 0.58, 0.59, 0.6, 0.65, 0.7, 0.75])
    cd_ref = np.array([0.0108, 0.0123, 0.0132, 0.0143, 0.0156, 0.0171, 0.0188, 0.0208, 0.0238, 0.0246, 0.0254, 0.0264, 0.0274,
          0.0288, 0.0366, 0.0530, 0.0947])
    plt.scatter(cd_ref, cl_ref, label="Airbus")
    plt.grid('on')
    plt.axis([0, 0.1, 0, 0.8])
    plt.legend()
    plt.show()

    plt.plot(cl_ref, cl_ref/cd_ref, label="Airbus")
    plt.plot(cl, cl/cd_tot, label="SUAVE")
    plt.legend()
    plt.axis([0., 1., 0., 25.])
    plt.show()

    print(cl)
    print(cl/cd_tot)


    return


if __name__ == '__main__':
    main()
      
