from SUAVE.Core import Units, Data
## @ingroup Methods-Weights-Correlations-Raymer
# prop_system.py
#
# Created:  May 2020, W. Van Gijseghem
# Modified: Nov 2023, L. Bauer

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
import numpy as np
from SUAVE.Methods.Weights.Correlations.FLOPS.prop_system import engine_FLOPS

## @ingroup Methods-Weights-Correlations-Raymer
def total_prop_Raymer(vehicle,prop):
    """ Calculate the weight of propulsion system using Raymer method, including:
        - fuel system weight
        - thurst reversers weight
        - electrical system weight
        - starter engine weight
        - nacelle weight
        - cargo containers
        The dry engine weight comes from the FLOPS relations since it is not listed in Raymer

        Assumptions:

        Source:
            Aircraft Design: A Conceptual Approach

        Inputs:
            vehicle - data dictionary with vehicle properties                   [dimensionless]
            prop    - data dictionary for the specific network that is being estimated [dimensionless]

        Outputs:
            output - data dictionary with weights                               [kilograms]
                    - output.wt_prop: total propulsive system weight
                    - output.wt_thrust_reverser: thurst reverser weight
                    - output.starter: starter engine weight
                    - output.wt_engine_controls: engine controls weight
                    - output.fuel_system: fuel system weight
                    - output.nacelle: nacelle weight
                    - output.wt_eng: dry engine weight

        Properties Used:
            N/A
    """    

    NENG            = prop.number_of_engines
    WFSYS           = fuel_system_Raymer(vehicle, NENG)
    WENG            = engine_FLOPS(vehicle, prop)
    WNAC            = nacelle_Raymer(vehicle, WENG)
    # WNAC = 0
    WEC, WSTART     = 0, 0  # misc_engine_Raymer(vehicle, prop, WENG)
    WTHR            = 0

    WPYL            = 0.225 * (NENG * WENG + WEC + WSTART + WTHR + WNAC)
    WPRO            = NENG * WENG + WEC + WSTART + WTHR + WNAC

    output                      = Data()
    output.wt_prop              = WPRO
    output.wt_thrust_reverser   = WTHR
    output.wt_starter           = WSTART
    output.wt_engine_controls   = WEC
    output.fuel_system          = WFSYS
    output.nacelle              = WNAC
    output.wt_eng               = WENG * NENG
    output.wt_pyl               = WPYL
    return output

## @ingroup Methods-Weights-Correlations-Raymer
def nacelle_Raymer(vehicle, WENG):
    """ Calculates the nacelle weight based on the Raymer method
        Assumptions:
            1) All nacelles are identical
            2) The number of nacelles is the same as the number of engines 
        Source:
            Aircraft Design: A Conceptual Approach (2nd edition)

        Inputs:
            vehicle - data dictionary with vehicle properties                           [dimensionless]
                -.ultimate_load: ultimate load factor of aircraft
            nacelle  - data dictionary for the specific nacelle that is being estimated [dimensionless]
                -lenght: total length of engine                                         [m]
                -diameter: diameter of nacelle                                          [m]
            WENG    - dry engine weight                                                 [kg]


        Outputs:
            WNAC: nacelle weight                                                        [kg]

        Properties Used:
            N/A
    """
    

    nacelle_tag     = list(vehicle.nacelles.keys())[0]
    ref_nacelle     = vehicle.nacelles[nacelle_tag]    
    NENG            = len(vehicle.nacelles)
    Kng             = 1.017         # assuming the engine is pylon mounted
    Nlt             = ref_nacelle.length / Units.ft
    Nw              = ref_nacelle.diameter / Units.ft
    Kp              = 1.            # assuming no prop engine
    Ktr             = 1.            # assuming no thrust reverser, otherwise 1.18
    Wec             = 2.331 * WENG ** 0.901 * Kp * Ktr
    Sn              = 2 * np.pi * Nw/2 * Nlt + np.pi * Nw**2/2

    CALIBRATION_NAC = 1.
    WNAC = CALIBRATION_NAC * 0.6724 * Kng * Nlt ** 0.1 * Nw ** 0.294 * vehicle.envelope.ultimate_load ** 0.119 \
           * Wec ** 0.611 * NENG ** 0.984 * Sn ** 0.224

    return WNAC * Units.lbs

## @ingroup Methods-Weights-Correlations-Raymer
def misc_engine_Raymer(vehicle, prop, WENG):
    """ Calculates the miscellaneous engine weight based on the Raymer method, electrical control system weight
        and starter engine weight
        Assumptions:

        Source:
            Aircraft Design: A Conceptual Approach

        Inputs:
            vehicle - data dictionary with vehicle properties                   [dimensionless]
                -.fuselages['fuselage'].lengths.total: length of fuselage   [m]
            prop    - data dictionary for the specific network that is being estimated [dimensionless]
                -.number_of_engines: number of engines

        Outputs:
            WEC: electrical engine control system weight                    [kg]
            WSTART: starter engine weight                                   [kg]

        Properties Used:
            N/A
    """
    NENG    = prop.number_of_engines
    Lec     = NENG * vehicle.fuselages['fuselage'].lengths.total / Units.ft
    WEC     = 5 * NENG + 0.8 * Lec
    WSTART  = 49.19*(NENG*WENG/1000)**0.541
    return WEC * Units.lbs, WSTART * Units.lbs

## @ingroup Methods-Weights-Correlations-Raymer
def fuel_system_Raymer(vehicle, NENG):
    """ Calculates the weight of the fuel system based on the Raymer method
        Assumptions:

        Source:
            Aircraft Design: A Conceptual Approach

        Inputs:
            vehicle - data dictionary with vehicle properties                   [dimensionless]
                -.design_mach_number: design mach number
                -.mass_properties.max_zero_fuel: maximum zero fuel weight   [kg]

        Outputs:
            WFSYS: Fuel system weight                                       [kg]

        Properties Used:
            N/A
    """
    VMAX    = vehicle.design_mach_number
    FMXTOT  = vehicle.mass_properties.max_zero_fuel / Units.lbs

    fuel_density = 5.7 * Units.lbs / Units.gallon
    Vt = vehicle.mass_properties.max_fuel / fuel_density / Units.gallon # total fuel volume, gal
    Vi = Vt  # integral tanks volume, gal
    Vp = 0  # self-sealing "protected" tanks volume, gal
    Nt = 5  # number of fuel tanks

    CALIBRATION_FSYS = 0.831
    WFSYS = CALIBRATION_FSYS * 2.405 * Vt ** 0.606 * (1 + Vi/Vt) ** (-1.0) * (1 + Vp/Vt) * Nt ** 0.5
    return WFSYS * Units.lbs