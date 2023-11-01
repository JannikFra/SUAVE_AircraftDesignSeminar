# test_AVL.py
# 
# Created:  May 2017, M. Clarke
# Modified: Apr 2020, M. Clarke

""" setup file for a mission with a 737 using AVL
"""

# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------

import SUAVE
from SUAVE.Core import Units 
import numpy as np

from pathlib import Path
import os

from RUN_IN_PYCHARM.Reference_B737.mission_B737 import vehicle_setup, configs_setup, analyses_setup, missions_setup, simple_sizing
import copy

# ----------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------

def main():
    tool_path = Path(__file__).resolve().parents[1]
    file_path = os.path.join(tool_path, "AVL/AVL")


    # vehicle data
    vehicle  = vehicle_setup()
    configs  = configs_setup(vehicle)

    # vehicle analyses
    configs_analyses = analyses_setup(configs)

    
    run_new_regression = True
    
    # append AVL aerodynamic analysis
    aerodynamics                                      = SUAVE.Analyses.Aerodynamics.AVL()  
    aerodynamics.settings.number_spanwise_vortices    = 30        
    aerodynamics.settings.keep_files                  = True 
    aerodynamics.geometry                             = copy.deepcopy(configs.cruise)    
    configs_analyses.cruise.append(aerodynamics)                 
                                                                 
    # append AVL stability analysis                              
    stability                                         = SUAVE.Analyses.Stability.AVL()   
    stability.settings.number_spanwise_vortices       = 30   
    stability.settings.keep_files                     = True   
    stability.geometry                                = copy.deepcopy(configs.cruise) 
    
    if run_new_regression: 
        # append AVL aerodynamic analysis 
        aerodynamics.settings.regression_flag         = False  
        aerodynamics.process.compute.lift.inviscid.settings.filenames.avl_bin_name  = file_path
        aerodynamics.settings.save_regression_results = True    
        stability.settings.regression_flag            = False  
        stability.settings.save_regression_results    = True   
        stability.settings.filenames.avl_bin_name     = file_path
         
    else:    
        aerodynamics.settings.regression_flag         = True   
        aerodynamics.settings.save_regression_results = False  
        aerodynamics.settings.training_file           = 'cruise_aero_data.txt'   
        stability.settings.regression_flag            = True 
        stability.settings.save_regression_results    = False   
        stability.training_file                       = 'cruise_stability_data.txt'     
   
    configs_analyses.cruise.append(aerodynamics)   
    configs_analyses.cruise.append(stability)
    
    # ------------------------------------------------------------------
    #   Initialize the Mission
    # ------------------------------------------------------------------

    mission = SUAVE.Analyses.Mission.Sequential_Segments()
    mission.tag = 'the_mission'

    #airport
    airport = SUAVE.Attributes.Airports.Airport()
    airport.altitude   =  0.0  * Units.ft
    airport.delta_isa  =  0.0
    airport.atmosphere = SUAVE.Attributes.Atmospheres.Earth.US_Standard_1976()
    mission.airport = airport    

    # unpack Segments module
    Segments = SUAVE.Analyses.Mission.Segments

    # base segment
    base_segment = Segments.Segment()


    # ------------------------------------------------------------------    
    #   Cruise Segment: constant speed, constant altitude
    # ------------------------------------------------------------------    

    segment = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment)
    segment.tag = "cruise"

    segment.analyses.extend( configs_analyses.cruise )

    segment.air_speed = 230. * Units['m/s']
    segment.distance  = 4000. * Units.km
    segment.altitude  = 10.668 * Units.km
    
    segment.state.numerics.number_control_points = 4

    # add to mission
    mission.append_segment(segment)

    missions_analyses = missions_setup(mission)

    analyses = SUAVE.Analyses.Analysis.Container()
    analyses.configs  = configs_analyses
    analyses.missions = missions_analyses
    
    simple_sizing(configs, analyses)

    configs.finalize()
    analyses.finalize()
 
    # mission analysis
    mission = analyses.missions.base    
    results = mission.evaluate()

    # lift coefficient check
    lift_coefficient              = results.segments.cruise.conditions.aerodynamics.lift_coefficient[0][0]
    lift_coefficient_true         = 0.6125259974142665

    print(lift_coefficient)
    diff_CL                       = np.abs(lift_coefficient  - lift_coefficient_true) 
    print('CL difference')
    print(diff_CL)

    # moment coefficient check
    moment_coefficient            = results.segments.cruise.conditions.stability.static.CM[0][0]
    moment_coefficient_true       = -0.5764667256663776
    
    print(moment_coefficient)
    diff_CM                       = np.abs(moment_coefficient - moment_coefficient_true)
    print('CM difference')
    print(diff_CM)
    return

if __name__ == '__main__': 
    main()     