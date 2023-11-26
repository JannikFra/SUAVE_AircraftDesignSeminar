## @ingroup Methods-Aerodynamics-Common-Fidelity_Zero-Drag
# compressibility_drag_wing.py
# 
# Created:  Dec 2013, SUAVE Team
# Modified: Nov 2016, T. MacDonald
#           Apr 2020, M. Clarke        
#           Apr 2020, M. Clarke
#           May 2021, E. Botero

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

# SUAVE imports
from SUAVE.Core import Data
from SUAVE.Components import Wings

# package imports
import numpy as np
import scipy as sp


# ----------------------------------------------------------------------
#  The Function
# ----------------------------------------------------------------------

## @ingroup Methods-Aerodynamics-Common-Fidelity_Zero-Drag
def compressibility_drag_wing_torenbeek(state,settings,geometry):
    """Computes compressibility drag for a wing

    Assumptions:
    Subsonic to low transonic
    Supercritical airfoil

    Source:
    adg.stanford.edu (Stanford AA241 A/B Course Notes)

    Inputs:
    state.conditions.
      freestream.mach_number                         [Unitless]
      aerodynamics.lift_breakdown.compressible_wings [Unitless]
    geometry.thickness_to_chord                      [Unitless]
    geometry.sweeps.quarter_chord                    [radians]

    Outputs:
    total_compressibility_drag                       [Unitless]

    Properties Used:
    N/A
    """ 
    
    # unpack
    conditions     = state.conditions
    wing           = geometry
    cl_w           = conditions.aerodynamics.lift_breakdown.compressible_wings[wing.tag]         
    mach           = conditions.freestream.mach_number
    compressibility_drag_correction_factor = settings.compressibility_drag_correction_factor
    drag_breakdown = conditions.aerodynamics.drag_breakdown

    mach_star = settings.mach_star
    n = settings.compressiblity_constant_n
    dM = settings.compressiblity_constant_dM

    # unpack wing
    t_c_w   = wing.thickness_to_chord
    sweep_w = wing.sweeps.quarter_chord
    cos_sweep = np.cos(sweep_w)

    mach_dd = mach_star / cos_sweep - t_c_w / cos_sweep**2 - 0.1 * (1.1*abs(cl_w))**1.5 / cos_sweep**4

    cd_c = np.where(mach < mach_dd, 0.002 * (1 + n / dM * (mach_dd - mach))**-1, 0.002 * (1 + 1 / dM * (mach - mach_dd))**6)
    # if np.all(mach < mach_dd):
    #     cd_c = 0.002 * (1 + n / dM * (mach_dd - mach))**-1
    # else:
    #     cd_c = 0.002 * (1 + 1 / dM * (mach - mach_dd))**6

    cd_c = cd_c * compressibility_drag_correction_factor

    mcc = mach_dd / ( 1.02 + 0.08*(1 - cos_sweep) )
    tc = t_c_w / (cos_sweep)
    # dump data to conditions
    wing_results = Data(
        compressibility_drag      = cd_c    ,
        thickness_to_chord        = tc      ,
        wing_sweep                = sweep_w ,
        crest_critical            = mcc     ,
        divergence_mach           = mach_dd    ,
    )
    drag_breakdown.compressible[wing.tag] = wing_results
