import SUAVE
from SUAVE.Core import Units
def mission_setup(analyses):
    # ------------------------------------------------------------------
    #   Initialize the Mission
    # ------------------------------------------------------------------

    mission = SUAVE.Analyses.Mission.Sequential_Segments()
    mission.tag = 'the_mission'

    # airport
    airport = SUAVE.Attributes.Airports.Airport()
    airport.altitude = 0.0 * Units.ft
    airport.delta_isa = 0.0
    airport.atmosphere = SUAVE.Attributes.Atmospheres.Earth.US_Standard_1976()

    mission.airport = airport

    # unpack Segments module
    Segments = SUAVE.Analyses.Mission.Segments

    # base segment
    base_segment = Segments.Segment()

    # ------------------------------------------------------------------
    #   First Climb Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "climb_1"

    segment.analyses.extend(analyses.takeoff)

    segment.altitude_start = 0.0 * Units.km
    segment.altitude_end = 3.0 * Units.km
    segment.air_speed = 125.0 * Units['m/s']
    segment.climb_rate = 6.0 * Units['m/s']

    # add to misison
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Second Climb Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "climb_2"

    segment.analyses.extend(analyses.cruise)

    segment.altitude_end = 8.0 * Units.km
    segment.air_speed = 190.0 * Units['m/s']
    segment.climb_rate = 6.0 * Units['m/s']

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Third Climb Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "climb_3"

    segment.analyses.extend(analyses.cruise)

    segment.altitude_end = 10.5 * Units.km
    segment.air_speed = 226.0 * Units['m/s']
    segment.climb_rate = 3.0 * Units['m/s']

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Cruise Segment: Constant Speed Constant Altitude
    # ------------------------------------------------------------------

    segment = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment)
    segment.tag = "cruise"

    segment.analyses.extend(analyses.cruise)

    segment.altitude = 10.668 * Units.km  # small jump to test altitude updating
    segment.air_speed = 230.412 * Units['m/s']
    segment.distance = (3933.65 + 770 - 92.6) * Units.km

    segment.state.numerics.number_control_points = 10

    # post-process aerodynamic derivatives in cruise
    # segment.process.finalize.post_process.aero_derivatives = SUAVE.Methods.Flight_Dynamics.Static_Stability.compute_aero_derivatives

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   First Descent Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "descent_1"

    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 10.5 * Units.km  # small jump to test altitude updating
    segment.altitude_end = 8.0 * Units.km
    segment.air_speed = 220.0 * Units['m/s']
    segment.descent_rate = 4.5 * Units['m/s']

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Second Descent Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "descent_2"

    segment.analyses.extend(analyses.landing)

    analyses.landing.aerodynamics.settings.spoiler_drag_increment = 0.00

    segment.altitude_end = 6.0 * Units.km
    segment.air_speed = 195.0 * Units['m/s']
    segment.descent_rate = 5.0 * Units['m/s']

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Third Descent Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "descent_3"

    segment.analyses.extend(analyses.landing)

    analyses.landing.aerodynamics.settings.spoiler_drag_increment = 0.00

    segment.altitude_end = 4.0 * Units.km
    segment.air_speed = 170.0 * Units['m/s']
    segment.descent_rate = 5.0 * Units['m/s']

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Fourth Descent Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "descent_4"

    segment.analyses.extend(analyses.landing)

    analyses.landing.aerodynamics.settings.spoiler_drag_increment = 0.00

    segment.altitude_end = 2.0 * Units.km
    segment.air_speed = 150.0 * Units['m/s']
    segment.descent_rate = 5.0 * Units['m/s']

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Fifth Descent Segment:Constant Speed Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "descent_5"

    segment.analyses.extend(analyses.landing)
    analyses.landing.aerodynamics.settings.spoiler_drag_increment = 0.00

    segment.altitude_end = 0.0 * Units.km
    segment.air_speed = 145.0 * Units['m/s']
    segment.descent_rate = 3.0 * Units['m/s']

    # append to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Mission definition complete
    # ------------------------------------------------------------------

    return mission