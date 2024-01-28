## @ingroup Methods-Figures_of_Merit
# direct_operating_costs.py
#
# Created:  Apr 2022, J. Frank


# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
from SUAVE.Core import Units
from SUAVE.Core import Data

# ----------------------------------------------------------------------
#  Method
# ----------------------------------------------------------------------
## @ingroup Methods-Figures_of_Merit
def direct_operating_costs(results, vehicle):


    doc = Data()

    segments = [key for key in results.segments.keys() if ('reserve' not in key) and ('hold' not in key)]
    first_segment = segments[0]
    last_segment = segments[-1]

    block_time = (results.segments[last_segment].conditions.frames.inertial.time[-1] - \
                  results.segments[first_segment].conditions.frames.inertial.time[0]) / Units.hours

    flight_cycles_per_year = 100 # TODO

    structural_weight = vehicle.mass_properties.operating_empty - vehicle.weight_breakdown.propulsion_breakdown.total
    OME = vehicle.mass_properties.operating_empty / 1000

    B = 2
    n_eng = vehicle.networks.turbofan.number_of_engines
    t_single_eng_in_t = vehicle.networks.turbofan.sealevel_static_thrust / vehicle.networks.turbofan.number_of_engines / 9.81 / 1000

    # MAINTENANCE
    maintenance_labor_per_hour = 50

    doc.af_mat = (OME * (0.21 * block_time + 13.7) + 57.5) * flight_cycles_per_year # Passt
    doc.af_per = maintenance_labor_per_hour * (1+B)*((0.655+0.01*OME*block_time)+0.254+0.01*OME)* flight_cycles_per_year
    doc.eng = (n_eng * (1.5 * (t_single_eng_in_t + 30.5 * block_time + 10.6)))* flight_cycles_per_year

    doc.maintenance = doc.af_mat + doc.af_per + doc.eng

    n_flight_attendant = 6
    n_crew_complements = 2
    salary_flight_attendant = 60_000
    salary_cockpit_crew = 300_000
    doc.crew = n_crew_complements * (salary_flight_attendant * n_flight_attendant + salary_cockpit_crew) # Passt

    FB_A1 = results.segments[first_segment].conditions.weights.total_mass[0] - \
            results.segments[last_segment].conditions.weights.total_mass[-1]
    price_A1 = 1.5
    doc.energy = flight_cycles_per_year * FB_A1 * price_A1

    # CAPITAL
    k_ome = 1150
    k_eng = 2500
    IR = 0.05
    f_rv_ac = 0.1
    DP_ac = 14
    a_ac = IR * (1 - f_rv_ac * (1 / (1 + IR)) ** DP_ac) / (1 - (1 / (1 + IR)) ** DP_ac)

    Ins = 0.005
    doc.capital_aircraft = (k_ome*structural_weight+k_eng*vehicle.weight_breakdown.propulsion_breakdown.total)*(a_ac+Ins)

    doc.capital = doc.capital_aircraft

    # FEES
    k_nav = 0.7 #1 intra EU, 0.7 transatlantic, 0.6 fernost
    total_range = results.segments[last_segment].conditions.frames.inertial.position_vector[-1][0] / Units.km
    mtom = vehicle.mass_properties.max_takeoff /1000
    doc.nav = k_nav * total_range * (mtom / 50)**0.5 * flight_cycles_per_year

    k_landing = 0.01
    doc.landing = k_landing * mtom * 1000 * flight_cycles_per_year

    weight_payload = vehicle.payload.passengers.mass_properties.mass + vehicle.payload.cargo.mass_properties.mass + vehicle.payload.baggage.mass_properties.mass
    k_ground = 0.1
    doc.ground = k_ground * weight_payload * flight_cycles_per_year

    doc.fees = doc.landing + doc.ground + doc.nav

    # SUM UP TO GET TOTAL DIRECT OPERATING COSTS
    doc.total = doc.energy + doc.crew + doc.maintenance + doc.capital + doc.fees

    return doc