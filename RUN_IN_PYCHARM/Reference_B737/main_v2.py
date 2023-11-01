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
from SUAVE.Core import Data
import numpy as np

from pathlib import Path
import os

from RUN_IN_PYCHARM.Reference_B737.mission_B737 import vehicle_setup, configs_setup, analyses_setup
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

    # append AVL aerodynamic analysis
    aerodynamics                                      = SUAVE.Analyses.Aerodynamics.AVL()
    aerodynamics.settings.number_spanwise_vortices    = 30        
    aerodynamics.settings.keep_files                  = True 
    aerodynamics.geometry                             = copy.deepcopy(configs.cruise)    
    configs_analyses.cruise.append(aerodynamics)                 
                                                                 


    # append AVL aerodynamic analysis
    aerodynamics.settings.regression_flag         = False
    aerodynamics.process.compute.lift.inviscid.settings.filenames.avl_bin_name  = file_path
    aerodynamics.settings.save_regression_results = True

    configs_analyses.cruise.append(aerodynamics)

    conditions = Data()
    conditions.freestream = Data()
    conditions.aerodynamics = Data()

    conditions.aerodynamics.angle_of_attack = 2 * np.pi / 180
    conditions.freestream.mach_number = 0.7
    conditions.freestream.density = 1.
    conditions.freestream.gravity = 9.81

    # run the vehicle model
    SUAVE.Methods.Aerodynamics.AVL.translate_conditions_to_cases(configs_analyses.cruise, conditions)
    SUAVE.Methods.Aerodynamics.AVL.run_analysis(configs_analyses.cruise, conditions)

    # ------------------------------------------------------------------
    #   Initialize the Mission
    # ------------------------------------------------------------------



if __name__ == '__main__': 
    main()     