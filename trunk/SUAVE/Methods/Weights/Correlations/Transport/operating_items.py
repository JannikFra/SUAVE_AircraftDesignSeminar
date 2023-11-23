## @ingroup Methods-Weights-Correlations-Transport
# operating_items.py
#
# Created:  Jan 2014, A. Wendorff
# Modified: Feb 2014, A. Wendorff
#           Feb 2016, E. Botero
#           May 2020, W. Van Gijseghem
#           Nov 2023, L. Bauer

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
from SUAVE.Core import Units, Data
import numpy as np

## @ingroup Methods-Weights-Correlations-Transport
def operating_items(vehicle):
    """ Calculate the weight of operating items, including:
        - crew
        - baggage
        - unusable fuel
        - engine oil
        - passenger service
        - ammunition and non-fixed weapons
        - cargo containers

        Assumptions:

        Source:
            http://aerodesign.stanford.edu/aircraftdesign/AircraftDesign.html

        Inputs:
            vehicle - data dictionary with vehicle properties                   [dimensionless]
                -.passengers: number of passengers
                -.systems.accessories: type of aircraft (short-range, commuter
                                                        medium-range, long-range,
                                                        sst, cargo)

        Outputs:
            output - data dictionary with weights                               [kilograms]
                    - output.oper_items: unusable fuel, engine oil, passenger service weight and cargo containers
                    - output.flight_crew: flight crew weight
                    - output.flight_attendants: flight attendants weight
                    - output.total: total operating items weight

        Properties Used:
            N/A
    """
    # num_seats   = vehicle.passengers
    # ac_type     = vehicle.systems.accessories
    # if ac_type == "short-range":  # short-range domestic, austere accomodations
    #     operitems_wt = 17.0 * num_seats * Units.lb
    # elif ac_type == "medium-range":  # medium-range domestic
    #     operitems_wt = 28.0 * num_seats * Units.lb
    # elif ac_type == "long-range":  # long-range overwater
    #     operitems_wt = 28.0 * num_seats * Units.lb
    # elif ac_type == "business":  # business jet
    #     operitems_wt = 28.0 * num_seats * Units.lb
    # elif ac_type == "cargo":  # all cargo
    #     operitems_wt = 56.0 * Units.lb
    # elif ac_type == "commuter":  # commuter
    #     operitems_wt = 17.0 * num_seats * Units.lb
    # elif ac_type == "sst":  # sst
    #     operitems_wt = 40.0 * num_seats * Units.lb
    # else:
    #     operitems_wt = 28.0 * num_seats * Units.lb

    flight_crew = 3         # number of pilots
    flight_attendants = 6   # number of flight attendants

    wt_flight_attendants = flight_attendants * (175 + 30)  # Roskam
    wt_flight_crew = flight_crew * (175 + 30)  # Roskam

    operitems_wt = 15_000 - wt_flight_crew * Units.lbs - wt_flight_attendants * Units.lbs

    output                           = Data()
    output.operating_items_less_crew = operitems_wt
    output.flight_crew               = wt_flight_crew * Units.lbs
    output.flight_attendants         = wt_flight_attendants * Units.lbs
    output.total                     = output.operating_items_less_crew + output.flight_crew + \
                                       output.flight_attendants
    return output
