# Reference_Aircraft.py
# 
# Created:  Nov 2023, J. Frank
# Modified:

""" Main File for the Aircraft Design Seminar 2023/24 Reference Aircraft
"""



# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------

import SUAVE
from SUAVE.Plots.Performance.Mission_Plots import *
from SUAVE.Plots.Geometry import * 
import matplotlib.pyplot as plt  
import numpy as np
from SUAVE.Methods.Center_of_Gravity.compute_component_centers_of_gravity import compute_component_centers_of_gravity
import sys
from pathlib import Path
import os
import time
from RUN_IN_PYCHARM.Reference_Aircraft.vehicle_setup import vehicle_setup, configs_setup
from RUN_IN_PYCHARM.Reference_Aircraft.mission_setup import mission_setup
from SUAVE.Input_Output.Results import print_mission_breakdown, print_weight_breakdown

sys.path.append('Vehicles')

# ----------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------

def main():
    configs, analyses = full_setup()

    simple_sizing(configs, analyses)
    configs.finalize()
    analyses.finalize() 
 
    # mission analysis
    mission = analyses.missions.base
    results = mission.evaluate()

    plot_aerodynamic_coefficients(results)
    plot_flight_conditions(results)
    plot_stability_coefficients(results)
    plt.show(block=True)
    
    # print weights breakdown
    print_weight_breakdown(configs.cruise)

    #print mission breakdown
    print_mission_breakdown(results, units='si')

    # plot vehicle 
    plot_vehicle(configs.base,plot_control_points = False, axis_limits=15)
    return


# ----------------------------------------------------------------------
#   Analysis Setup
# ----------------------------------------------------------------------

def full_setup():
    # vehicle data
    vehicle  = vehicle_setup()
    configs  = configs_setup(vehicle)

    # vehicle analyses
    configs_analyses = analyses_setup(configs)

    # mission analyses
    mission  = mission_setup(configs_analyses)
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

    # takeoff_analysis
    analyses.takeoff.aerodynamics.settings.drag_coefficient_increment = 0.0000

    # landing analysis
    aerodynamics = analyses.landing.aerodynamics
    # do something here eventually

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
    analyses.append(weights)

    # ------------------------------------------------------------------
    #  Aerodynamics & Stability Analysis
    tool_path = Path(__file__).resolve().parents[2]
    file_path = Path(tool_path, "AVL", sys.platform, "avl")
    avl_files_path = os.path.join(tool_path, "RUN_IN_PYCHARM/Reference_Aircraft/avl_files")
    aero_training_path = os.path.join(tool_path, "RUN_IN_PYCHARM/Reference_Aircraft/aero_data")
    stability_training_path = os.path.join(tool_path, "RUN_IN_PYCHARM/Reference_Aircraft/aero_data/")

    aerodynamics = SUAVE.Analyses.Aerodynamics.AVL()
    aerodynamics.geometry                            = vehicle
    aerodynamics.settings.number_spanwise_vortices = 30
    aerodynamics.settings.keep_files = True

    stability = SUAVE.Analyses.Stability.AVL()
    stability.geometry = vehicle
    stability.settings.number_spanwise_vortices = 30
    stability.settings.keep_files = True

    run_new_regression = True
    if run_new_regression:
        # append AVL aerodynamic analysis
        aerodynamics.settings.regression_flag = False
        aerodynamics.process.compute.lift.inviscid.settings.filenames.avl_bin_name = file_path
        aerodynamics.process.compute.lift.inviscid.settings.filenames.run_folder = avl_files_path
        aerodynamics.settings.save_regression_results = True
        stability.settings.regression_flag = False
        stability.settings.save_regression_results = True
        stability.settings.filenames.avl_bin_name = file_path
        stability.settings.filenames.run_folder = avl_files_path
    else:
        aerodynamics.settings.regression_flag = True
        aerodynamics.settings.save_regression_results = False
        aerodynamics.settings.training_file = aero_training_path
        aerodynamics.process.compute.lift.inviscid.settings.filenames.avl_bin_name = file_path
        aerodynamics.process.compute.lift.inviscid.settings.filenames.run_folder = avl_files_path
        stability.settings.regression_flag = True
        stability.settings.save_regression_results = False
        stability.training_file                         = stability_training_path
        stability.settings.filenames.avl_bin_name = file_path
        stability.settings.filenames.run_folder = avl_files_path

    analyses.append(aerodynamics)
    analyses.append(stability)

    # ------------------------------------------------------------------
    #  Energy
    energy = SUAVE.Analyses.Energy.Energy()
    energy.network = vehicle.networks #what is called throughout the mission (at every time step))
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

def simple_sizing(configs, analyses):
    base = configs.base
    base.pull_base()

    # zero fuel weight
    base.mass_properties.max_zero_fuel = 0.9 * base.mass_properties.max_takeoff 

    # wing areas
    for wing in base.wings:
        wing.areas.wetted   = 2.0 * wing.areas.reference
        wing.areas.exposed  = 0.8 * wing.areas.wetted
        wing.areas.affected = 0.6 * wing.areas.wetted

    # fuselage seats
    # base.fuselages['fuselage'].number_coach_seats = base.passengers
    
    # weight analysis
    #need to put here, otherwise it won't be updated
    weights = analyses.configs.base.weights
    breakdown = weights.evaluate(method='New SUAVE')
    
    #compute centers of gravity
    #need to put here, otherwise, results won't be stored
    compute_component_centers_of_gravity(base)
    base.center_of_gravity()
    
    # diff the new data
    base.store_diff()
    # done!
    return

def missions_setup(base_mission):
    missions = SUAVE.Analyses.Mission.Mission.Container()
    missions.base = base_mission
    return missions

if __name__ == '__main__':
    time0 = time.time()
    main()
    plt.show()
    deltaT = time.time() - time0
    print('total time = ', deltaT)
