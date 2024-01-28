# Baseline.py
# 
# Created:  Nov 2023, J. Frank
# Modified:

""" Main File for the Aircraft Design Seminar 2023/24 Baseline Aircraft
"""



# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------

import SUAVE
from SUAVE.Core import Data, Units
from SUAVE.Plots.Performance.Mission_Plots import *
from SUAVE.Plots.Geometry import * 
import matplotlib.pyplot as plt  
import numpy as np
from SUAVE.Methods.Center_of_Gravity.compute_component_centers_of_gravity import compute_component_centers_of_gravity
import sys
from pathlib import Path
import os
import time
from SUAVE.Methods.Performance import payload_range
from RUN_IN_PYCHARM.Baseline.vehicle_setup import vehicle_setup, configs_setup
from RUN_IN_PYCHARM.Baseline.mission_setup import mission_setup
from SUAVE.Input_Output.Results import print_mission_breakdown, print_weight_breakdown
from SUAVE.Components.Energy.Networks.Turbofan_Raymer import Turbofan_Raymer

#from Plots import plot_mission

sys.path.append('Vehicles')

# ----------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------

def main(iteration_setup):
    configs, analyses = full_setup(iteration_setup)

    weights = analyses.configs.base.weights
    breakdown = weights.evaluate(method="Raymer")

    deltacg = 2
    while abs(deltacg) > 1e-5:
        compute_component_centers_of_gravity(configs.base)
        oldcg = configs.base.mass_properties.center_of_gravity[0][0]
        configs.base.center_of_gravity()  # CG @ TOM
        configs.base.store_diff()

        newcg = configs.base.mass_properties.center_of_gravity[0][0]
        deltacg = newcg - oldcg

    # base = configs.base
    # base.pull_base()
    #
    # compute_component_centers_of_gravity(base)
    # base.center_of_gravity()
    # base.store_diff()

    # simple_sizing(configs, analyses)
    configs.finalize()
    analyses.finalize() 
 
    # mission analysis
    mission = analyses.missions.base
    results = mission.evaluate()


    return mission, results, configs, analyses

# ----------------------------------------------------------------------
#   Analysis Setup
# ----------------------------------------------------------------------
def results_show(results, vehicle):
    plot_aerodynamic_coefficients(results)
    plot_fuel_use(results)
    plot_flight_conditions(results)
    plot_stability_coefficients(results)
    plot_drag_components(results)
    plot_altitude_sfc_weight(results)
    # plot_mission(results,configs.base)
    plt.show(block=True)

    # print weights breakdown
    print_weight_breakdown(vehicle)

    # print mission breakdown
    print_mission_breakdown(results, units='si')

    # plot vehicle
    plot_vehicle(vehicle, plot_control_points=False, axis_limits=20)
    plt.show(block=True)

# ----------------------------------------------------------------------
#   Analysis Setup
# ----------------------------------------------------------------------

def full_setup(iteration_setup):
    # vehicle data
    vehicle  = vehicle_setup(iteration_setup)
    configs  = configs_setup(vehicle)

    # vehicle analyses
    configs_analyses = analyses_setup(configs)

    # mission analyses
    mission  = mission_setup(configs_analyses, iteration_setup)
    missions_analyses = missions_setup(mission)

    analyses = SUAVE.Analyses.Analysis.Container()
    analyses.configs  = configs_analyses
    analyses.missions = missions_analyses

    return configs, analyses

# ----------------------------------------------------------------------
#   Define the Vehicle Analyses
# ----------------------------------------------------------------------

def analyses_setup(configs):
    analyses = SUAVE.Analyses.Analysis.Container()

    # build a base analysis for each config
    for tag,config in list(configs.items()):
        analysis = base_analysis(config)
        analyses[tag] = analysis

    return analyses

def base_analysis(vehicle):
    # ------------------------------------------------------------------
    #   Initialize the Analyses
    # ------------------------------------------------------------------     
    analyses = SUAVE.Analyses.Vehicle()

    # ------------------------------------------------------------------
    #  Basic Geometry Relations
    sizing = SUAVE.Analyses.Sizing.Sizing()
    sizing.features.vehicle = vehicle
    analyses.append(sizing)

    # ------------------------------------------------------------------
    #  Weights
    weights = SUAVE.Analyses.Weights.Weights_Transport()
    weights.vehicle = vehicle
    weights.settings.weight_reduction_factors.main_wing = 0.05
    weights.settings.weight_reduction_factors.empennage = 0.05
    weights.settings.weight_reduction_factors.fuselage = 0.1
    weights.settings.weight_reduction_factors.structural = 0
    weights.settings.weight_reduction_factors.systems = 0
    weights.settings.weight_reduction_factors.operating_items = 0
    weights.settings.weight_reduction_factors.landing_gear = 0
    weights.settings.weight_reduction_factors.propulsion = 0
    analyses.append(weights)

    # ------------------------------------------------------------------
    #  Aerodynamics & Stability Analysis
    #
    # --> AVL
    #
    # tool_path = Path(__file__).resolve().parents[2]
    # file_path = Path(tool_path, "AVL", sys.platform, "avl")
    # avl_files_path = os.path.join(tool_path, "RUN_IN_PYCHARM/Reference_Aircraft/avl_files")
    # aero_training_path = os.path.join(tool_path, "RUN_IN_PYCHARM/Reference_Aircraft/aero_data")
    # stability_training_path = os.path.join(tool_path, "RUN_IN_PYCHARM/Reference_Aircraft/aero_data/base_stability_data.txt")
    #
    # aerodynamics = SUAVE.Analyses.Aerodynamics.AVL()
    # aerodynamics.geometry                            = vehicle
    # aerodynamics.settings.number_spanwise_vortices = 80
    # aerodynamics.settings.keep_files = True
    # aerodynamics.settings.print_output = True
    # aerodynamics.recalculate_total_wetted_area = True
    # aerodynamics.settings.wing_parasite_drag_form_factor = 0.7 # 1.1
    # aerodynamics.settings.fuselage_parasite_drag_form_factor = 1.5 # 2.3
    # aerodynamics.settings.viscous_lift_dependent_drag_factor = 0.2 # 0.38
    #
    # stability = SUAVE.Analyses.Stability.AVL()
    # stability.geometry = vehicle
    # stability.settings.number_spanwise_vortices = 80
    # stability.settings.keep_files = True
    # stability.settings.print_output = True
    #
    # run_new_regression = True
    # if run_new_regression:
    #     # append AVL aerodynamic analysis
    #     aerodynamics.settings.regression_flag = False
    #     aerodynamics.process.compute.lift.inviscid.settings.filenames.avl_bin_name = file_path
    #     aerodynamics.process.compute.lift.inviscid.settings.filenames.run_folder = avl_files_path
    #     aerodynamics.settings.save_regression_results = True
    #     stability.settings.regression_flag = False
    #     stability.settings.save_regression_results = True
    #     stability.training_file = stability_training_path
    #     stability.settings.filenames.avl_bin_name = file_path
    #     stability.settings.filenames.run_folder = avl_files_path
    # else:
    #     aerodynamics.settings.regression_flag = True
    #     aerodynamics.settings.save_regression_results = False
    #     aerodynamics.settings.training_file = aero_training_path
    #     aerodynamics.process.compute.lift.inviscid.settings.filenames.avl_bin_name = file_path
    #     aerodynamics.process.compute.lift.inviscid.settings.filenames.run_folder = avl_files_path
    #     stability.settings.regression_flag = True
    #     stability.settings.save_regression_results = True
    #     stability.training_file = stability_training_path
    #     stability.settings.filenames.avl_bin_name = file_path
    #     stability.settings.filenames.run_folder = avl_files_path
    #
    # aerodynamics.settings.drag_coefficient_increment = Data()
    # aerodynamics.settings.drag_coefficient_increment.takeoff = 0
    # aerodynamics.settings.drag_coefficient_increment.base = 0.
    # aerodynamics.settings.drag_coefficient_increment.climb = 0.
    # aerodynamics.settings.drag_coefficient_increment.cruise = 0.
    # aerodynamics.settings.drag_coefficient_increment.descent = 0.
    # aerodynamics.settings.drag_coefficient_increment.landing = 0.
    #
    #
    # analyses.append(aerodynamics)
    # analyses.append(stability)

    aerodynamics = SUAVE.Analyses.Aerodynamics.Fidelity_Zero()
    aerodynamics.geometry = vehicle
    aerodynamics.settings.drag_coefficient_increment = Data()
    aerodynamics.settings.drag_coefficient_increment.base = 0
    aerodynamics.settings.drag_coefficient_increment.takeoff = 0
    aerodynamics.settings.drag_coefficient_increment.climb = 0
    aerodynamics.settings.drag_coefficient_increment.cruise = -12e-4#-12e-4
    aerodynamics.settings.drag_coefficient_increment.descent = 0
    aerodynamics.settings.drag_coefficient_increment.landing = 0
    aerodynamics.settings.recalculate_total_wetted_area = True
    aerodynamics.settings.use_surrogate = True
    aerodynamics.settings.model_fuselage = True
    aerodynamics.settings.model_nacelle = True
    aerodynamics.settings.compressibility_drag_correction_factor = 1.
    aerodynamics.settings.mach_star = 0.919  # 0.921
    aerodynamics.settings.compressibility_constant_n = 10  # 2.5
    aerodynamics.settings.compressibility_constant_dM = 0.05

    aerodynamics.settings.oswald_efficiency_factor = 0.84

    analyses.append(aerodynamics)


    # ------------------------------------------------------------------
    #  Stability Analysis
    stability = SUAVE.Analyses.Stability.Fidelity_Zero()
    stability.geometry = vehicle
    analyses.append(stability)

    # ------------------------------------------------------------------
    #  Energy
    energy = SUAVE.Analyses.Energy.Energy()
    energy.network = vehicle.networks   #what is called throughout the mission (at every time step))
    analyses.append(energy)

    # ------------------------------------------------------------------
    #  Planet Analysis
    planet = SUAVE.Analyses.Planets.Planet()
    analyses.append(planet)

    # ------------------------------------------------------------------
    #  Atmosphere Analysis
    atmosphere = SUAVE.Analyses.Atmospheric.US_Standard_1976()
    atmosphere.features.planet = planet.features
    analyses.append(atmosphere)   

    # done!
    return analyses    

# def simple_sizing(configs, analyses):
#     base = configs.base
#     base.pull_base()
#
#     # weight analysis
#     #need to put here, otherwise it won't be updated
#     weights = analyses.configs.base.weights
#     breakdown = weights.evaluate(method='Raymer')
#
#     #compute centers of gravity
#     #need to put here, otherwise, results won't be stored
#     compute_component_centers_of_gravity(base)
#     base.center_of_gravity()
#
#     # diff the new data
#     base.store_diff()
#     # done!
#     return

def missions_setup(base_mission):
    missions = SUAVE.Analyses.Mission.Mission.Container()
    missions.base = base_mission
    return missions

def Baseline(parameters):
    iteration_setup = Data()

    iteration_setup.weight_iter = Data()
    iteration_setup.weight_iter.MTOW = 279_000 * Units.kg
    iteration_setup.weight_iter.BOW = 130_000 * Units.kg
    iteration_setup.weight_iter.Design_Payload = 24_500 * Units.kg
    iteration_setup.weight_iter.FUEL = iteration_setup.weight_iter.MTOW - iteration_setup.weight_iter.BOW  \
                                       - iteration_setup.weight_iter.Design_Payload

    iteration_setup.mission_iter = Data()
    iteration_setup.mission_iter.mission_distance = 10_500 * Units['nautical_mile']
    iteration_setup.mission_iter.cruise_distance = 9_900 * Units['nautical_mile']
    iteration_setup.mission_iter.throttle_mid_cruise = 1.
    iteration_setup.mission_iter.design_cruise_altitude = parameters.design_cruise_altitude
    iteration_setup.mission_iter.design_cruise_mach = parameters.design_cruise_mach
    iteration_setup.mission_iter.reserve_hold_time = 30 * Units.min
    iteration_setup.mission_iter.reserve_hold_altitude = 1500. * Units.ft
    iteration_setup.mission_iter.reserve_hold_speed = 250 * Units['kts']
    iteration_setup.mission_iter.reserve_trip_pct = 0.03
    iteration_setup.mission_iter.reserve_distance = 200. * Units.nautical_mile
    iteration_setup.mission_iter.reserve_cruise_distance = 100. * Units.nautical_miles

    iteration_setup.sizing_iter = Data()
    iteration_setup.sizing_iter.wing_loading = parameters.wing_loading
    iteration_setup.sizing_iter.thrust_loading = parameters.thrust_loading
    iteration_setup.sizing_iter.aspect_ratio = parameters.aspect_ratio
    iteration_setup.sizing_iter.sweep_quarter_chord = parameters.sweep_quarter_chord
    iteration_setup.sizing_iter.thickness_to_chord = parameters.thickness_to_chord
    iteration_setup.sizing_iter.wing_origin = [[22.408,0,-0.957]]

    landing_weight = 0.0
    block_distance = 0.0

    error = 2.
    error_reserve = 2
    it = 0
    while (error > 2.0) or (abs(landing_weight - iteration_setup.weight_iter.BOW - iteration_setup.weight_iter.Design_Payload) > 1.0) or (error_reserve > 1.0) or abs(delta_percent_mac) > 1.0:
        it += 1
        iteration_setup.weight_iter.TOW = iteration_setup.weight_iter.BOW + iteration_setup.weight_iter.Design_Payload \
                                          + iteration_setup.weight_iter.FUEL

        mission, results, configs, analyses = main(iteration_setup)

        climb_segments = [key for key in results.segments.keys() if (('climb' in key) and ('reserve' not in key) and ('second_leg' not in key) and ('step' not in key))]
        first_climb_segment = climb_segments[0]
        last_climb_segment = climb_segments[-1]
        descent_segments = [key for key in results.segments.keys() if (('descent' in key) and ('reserve' not in key) and ('second_leg' not in key))]
        first_descent_segment = descent_segments[0]
        last_descent_segment = descent_segments[-1]
        step_climb_segments = [key for key in results.segments.keys() if (('climb' in key) and ('reserve' not in key) and ('second_leg' not in key) and ('step' in key))]
        cruise_segments = [key for key in results.segments.keys() if (('cruise' in key) and ('reserve' not in key) and ('second_leg' not in key))]
        first_cruise_segment = cruise_segments[0]
        last_cruise_segment = cruise_segments[-1]

        reserve_climb_segments = [key for key in results.segments.keys() if
                                  (('climb' in key) and ('reserve' in key) and ('second_leg' not in key) and ('step' not in key))]
        n_reserve_climb_segments = len(reserve_climb_segments)
        first_reserve_climb_segment = reserve_climb_segments[0]
        last_reserve_climb_segment = reserve_climb_segments[-1]
        reserve_descent_segments = [key for key in results.segments.keys() if
                                    (('descent' in key) and ('reserve' in key) and ('second_leg' not in key))]
        n_reserve_descent_segments = len(reserve_descent_segments)
        first_reserve_descent_segment = reserve_descent_segments[0]
        last_reserve_descent_segment = reserve_descent_segments[-1]

        climb_fuel = results.segments[first_climb_segment].conditions.weights.total_mass[0][0] - \
                     results.segments[last_climb_segment].conditions.weights.total_mass[-1][0]

        descent_fuel = results.segments[first_descent_segment].conditions.weights.total_mass[0][0] - \
                     results.segments[last_descent_segment].conditions.weights.total_mass[-1][0]

        block_fuel = results.segments[first_climb_segment].conditions.weights.total_mass[0][0] - \
                     results.segments[last_descent_segment].conditions.weights.total_mass[-1][0]

        cruise_fuel = results.segments[first_cruise_segment].conditions.weights.total_mass[0][0] - \
                      results.segments[last_cruise_segment].conditions.weights.total_mass[-1][0]

        alternate_fuel = results.segments[first_reserve_climb_segment].conditions.weights.total_mass[0][0] - \
                         results.segments[last_reserve_descent_segment].conditions.weights.total_mass[-1][0]

        reserve_cruise_fuel = results.segments.reserve_cruise.conditions.weights.total_mass[0][0] - \
                              results.segments.reserve_cruise.conditions.weights.total_mass[-1][0]

        hold_fuel = results.segments['hold'].conditions.weights.total_mass[0][0] - \
                    results.segments['hold'].conditions.weights.total_mass[-1][0]

        reserve_fuel_pct = block_fuel * iteration_setup.mission_iter.reserve_trip_pct

        reserve_fuel = reserve_fuel_pct + alternate_fuel + hold_fuel

        block_distance = (results.segments[last_descent_segment].conditions.frames.inertial.position_vector[-1][0] - \
                          results.segments[first_climb_segment].conditions.frames.inertial.position_vector[0][0])

        climb_distance = (results.segments[last_climb_segment].conditions.frames.inertial.position_vector[-1][0] - \
                          results.segments[first_climb_segment].conditions.frames.inertial.position_vector[0][0])

        step_climb_distance = 0.
        for step_climb_segment in step_climb_segments:
            step_climb_distance += (results.segments[step_climb_segment].conditions.frames.inertial.position_vector[-1][0] - \
                              results.segments[step_climb_segment].conditions.frames.inertial.position_vector[0][0])

        cruise_distance = 0.
        for cruise_segment in cruise_segments:
            cruise_distance += (results.segments[cruise_segment].conditions.frames.inertial.position_vector[-1][0] - \
                               results.segments[cruise_segment].conditions.frames.inertial.position_vector[0][0])

        descent_distance = (results.segments[last_descent_segment].conditions.frames.inertial.position_vector[-1][0] - \
                            results.segments[first_descent_segment].conditions.frames.inertial.position_vector[0][0])

        reserve_climb_distance = (results.segments[
                                      last_reserve_climb_segment].conditions.frames.inertial.position_vector[-1][0] - \
                                  results.segments[
                                      first_reserve_climb_segment].conditions.frames.inertial.position_vector[0][0])

        reserve_cruise_distance = (results.segments.reserve_cruise.conditions.frames.inertial.position_vector[-1][0] - \
                                   results.segments.reserve_cruise.conditions.frames.inertial.position_vector[0][0])

        reserve_descent_distance = (results.segments[
                                        last_reserve_descent_segment].conditions.frames.inertial.position_vector[-1][
                                        0] - \
                                    results.segments[
                                        first_reserve_descent_segment].conditions.frames.inertial.position_vector[0][
                                        0])

        landing_weight = results.segments['hold'].conditions.weights.total_mass[-1][0] - reserve_fuel_pct

        percent_mac = np.array([])
        for segment in results.segments.values():
            percent_mac = np.append(percent_mac, segment.conditions.stability.static.percent_mac[:, 0])

        percent_mac_min = np.min(percent_mac)
        percent_mac_max = np.max(percent_mac)
        reference_mac = (percent_mac_min+percent_mac_max)/2  # or min!!!

        percent_mac_iter = 24  # Raymer
        iteration_setup.sizing_iter.wing_origin[0][0] = iteration_setup.sizing_iter.wing_origin[0][0] - (
                    percent_mac_iter - reference_mac) / 100 * configs.base.wings.main_wing.chords.mean_aerodynamic
        delta_percent_mac = (percent_mac_iter - reference_mac) * 5

        iteration_setup.weight_iter.FUEL = block_fuel + reserve_fuel
        iteration_setup.mission_iter.throttle_mid_cruise = np.mean(results.segments['cruise_2'].conditions.propulsion.throttle[:][0])

        error = abs(block_distance - iteration_setup.mission_iter.mission_distance) / Units['nautical_mile']
        error_reserve = abs(iteration_setup.mission_iter.reserve_distance - (reserve_climb_distance + reserve_cruise_distance + reserve_descent_distance)) / Units['nautical_mile']

        iteration_setup.mission_iter.cruise_distance = iteration_setup.mission_iter.mission_distance - (climb_distance + descent_distance + step_climb_distance)
        iteration_setup.mission_iter.reserve_cruise_distance = iteration_setup.mission_iter.reserve_distance - (reserve_climb_distance + reserve_descent_distance)

        # Konvergenzbeschleunigung
        deltaBOW = configs.base.mass_properties.operating_empty - iteration_setup.weight_iter.BOW
        if abs(deltaBOW) > 500.:
            iteration_setup.weight_iter.BOW = iteration_setup.weight_iter.BOW + 2. * deltaBOW  # + 1650
        elif abs(deltaBOW) > 50.:
            iteration_setup.weight_iter.BOW = iteration_setup.weight_iter.BOW + 1.2 * deltaBOW  # + 1650
        else:
            iteration_setup.weight_iter.BOW = iteration_setup.weight_iter.BOW + 0.8 * deltaBOW  # + 1650

        deltaweight = landing_weight - iteration_setup.weight_iter.BOW - iteration_setup.weight_iter.Design_Payload
        print('Error: %.1f NM' % error)
        print('Error reserve: %.1f NM' % error_reserve)
        print('delta weight: %.1f kg' % deltaweight)
        print('delta percent mac: %.1f' % delta_percent_mac)
        print('TOW: %.1f kg' % iteration_setup.weight_iter.TOW)
        print('BOW: %.1f kg' % iteration_setup.weight_iter.BOW)
        print('PAYLOAD: %.1f kg' % iteration_setup.weight_iter.Design_Payload)
        print('FUEL: %.1f kg' % iteration_setup.weight_iter.FUEL)
        print('BLOCK DISTANCE: %.1f NM' % (block_distance / Units['nautical_mile']))
        print('Landing weight: %.1f kg' % landing_weight)
        print('------------------------------')
        #results_show(results, configs.base)

    print('Total fuel : %.1f kg' % iteration_setup.weight_iter.FUEL)
    print('Climb fuel : %.1f kg' % climb_fuel)
    print('Cruise fuel : %.1f kg' % cruise_fuel)
    print('Descent fuel : %.1f kg' % descent_fuel)
    print('Reserve fuel : %.1f kg' % reserve_fuel)
    print('Wing span : %.2f m' % configs.base.wings.main_wing.spans.projected)
    print('Wing area : %.2f m' % configs.base.wings.main_wing.areas.reference)
    results_show(results, configs.base)

    # payload_range_run = False
    # if payload_range_run == True:
    #     payload_range = payload_range(configs.cruise, results, "cruise_2", reserves=reserve_fuel)

    return iteration_setup.weight_iter.FUEL


def sweep():
    '''
    This method gives the possiblity to make a parameter study
    '''

    wing_loadings = np.linspace(730, 750, 2)
    altitudes = np.linspace(36_000., 40_000., 3) * Units.ft
    X, Y = np.meshgrid(altitudes, wing_loadings)
    fuels = np.zeros_like(X)
    for i, alt in enumerate(altitudes):
        for j, wl in enumerate(wing_loadings):
            parameters = Data()
            parameters.wing_loading = wl
            parameters.aspect_ratio = 21.
            parameters.thickness_to_chord = 0.09
            parameters.design_cruise_altitude = alt
            parameters.design_cruise_mach = 0.82
            atmosphere = SUAVE.Analyses.Atmospheric.US_Standard_1976()
            tf = Turbofan_Raymer()
            altitude = parameters.design_cruise_altitude - 2_000 * Units.ft
            mach = parameters.design_cruise_mach
            temperature_deviation = 0
            atmo_data = atmosphere.compute_values(altitude, temperature_deviation)
            v_v_300 = 300 * Units.ft / Units.min
            v_initial_cruise_altitude = mach * atmo_data.speed_of_sound
            LoD_initial_cruise_altitude = 22
            m4_m0 = 1.
            thrust_ratio = tf.get_max_thrust(0, 0) / tf.get_max_thrust(altitude, mach)
            F_m_TOC = m4_m0 * (v_v_300 / v_initial_cruise_altitude + 1 / LoD_initial_cruise_altitude) * thrust_ratio
            parameters.thrust_loading = F_m_TOC[0][0]
            fuels[j,i] = Baseline(parameters)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, fuels)
    plt.show()



if __name__ == '__main__':
    parameters = Data()
    parameters.wing_loading = 700.
    parameters.aspect_ratio = 13.
    parameters.thickness_to_chord = 0.105
    parameters.design_cruise_altitude = 37_000 * Units.ft
    parameters.design_cruise_mach = 0.82
    parameters.sweep_quarter_chord = 29 * Units.deg
    parameters.thrust_loading = 0.22
    Baseline(parameters)

    #sweep()