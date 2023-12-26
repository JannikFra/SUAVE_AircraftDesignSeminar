## @ingroup Methods-Weights-Correlations-Raymer
# wing_main_raymer.py
#
# Created:  May 2020, W. Van Gijseghem
# Modified:

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
from SUAVE.Core import Units
import numpy as np

## @ingroup Methods-Weights-Correlations-Raymer
def wing_main_raymer(vehicle, wing):
    """ Calculate the wing weight of the aircraft based the Raymer method

    Assumptions:

    Source:
        Aircraft Design: A Conceptual Approach (2nd edition)

    Inputs:
        vehicle - data dictionary with vehicle properties                   [dimensionless]
                -.mass_properties.max_takeoff: MTOW                         [kg]
                -.envelope.ultimate_load: ultimate loading factor
                -.systems.accessories: type of aircraft (short-range, commuter
                                                        medium-range, long-range,
                                                        sst, cargo)
        wing    - data dictionary with specific wing properties             [dimensionless]
                -.taper: taper ratio
                -.sweeps.quarter_chord: quarter chord sweep angle           [deg]
                -.thickness_to_chord: thickness to chord
                -.aspect_ratio: aspect ratio of wing
                -.areas.reference: wing surface area                        [m^2]

    Outputs:
        weight - weight of the wing                  [kilograms]


    Properties Used:
        N/A
    """

    # unpack inputs
    taper   = wing.taper
    sweep   = wing.sweeps.quarter_chord
    area    = wing.areas.reference
    t_c_w   = wing.Segments.root.thickness_to_chord

    Wdg     = vehicle.mass_properties.max_takeoff / Units.lb
    Nz      = vehicle.envelope.ultimate_load
    Sw      = area / Units.ft ** 2
    A       = wing.aspect_ratio
    tc_root = t_c_w
    taper   = taper
    Scsw    = Sw * 0.1

    CALIBRATION = 1.023

    # if vehicle.systems.accessories == 'sst':
    #     sweep = 0
    Wwing = CALIBRATION * 0.0051 * (Wdg * Nz) ** 0.557 * Sw ** 0.649 * A ** 0.5 * tc_root ** -0.4 * (1 + taper) ** 0.1 * \
            np.cos(sweep) ** -1. * Scsw ** 0.1

    # Folding mechanism weight estimation for wingspans > 80 m
    # Source: Gur et al., Development of Framework for Truss-Braced Wing Conceptual MDO
    if wing.spans.projected > 80 * Units.meter:
        # We assume that the hinge line is located at 40 m half-span
        eta_fold = (80 * Units.meter)/wing.spans.projected
        Fs_MTOW = 0.5 * (1 - 2/np.pi * eta_fold * (1 - eta_fold**2) ** 0.5 - 2/np.pi * np.arcsin(eta_fold))
        Wfold = 0.07 * Wdg * Fs_MTOW
        print('Folding Mechanism Weight: ', Wfold * Units.lb)
    else:
        Wfold = 0

    weight = (Wwing + Wfold) * Units.lb
    return weight
