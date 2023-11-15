import SUAVE
from SUAVE.Core import Units
def mission_setup(analyses, iteration_setup):

    climb_throttle = 0.6
    idle_throttle = 0.05

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
    segment.altitude_end = 5_000 * Units.ft
    segment.air_speed = 125.0 * Units['m/s']
    segment.climb_rate = 4.0 * Units['m/s']

    # add to misison
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Second Climb Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "climb_2"

    segment.analyses.extend(analyses.cruise)

    segment.altitude_end = 15_000 * Units.ft
    segment.air_speed = 190.0 * Units['m/s']
    segment.climb_rate = 4.0 * Units['m/s']

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Third Climb Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "climb_3"

    segment.analyses.extend(analyses.cruise)

    segment.altitude_end = 31_000 * Units.ft
    segment.air_speed = 226.0 * Units['m/s']
    segment.climb_rate = 2.0 * Units['m/s']

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   1. Cruise Segment: Constant Speed Constant Altitude
    # ------------------------------------------------------------------

    segment = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment)
    segment.tag = "cruise_1"

    segment.analyses.extend(analyses.cruise)

    segment.altitude = 31_000 * Units.ft
    segment.air_speed = 301.852 * 0.82 * Units['m/s']
    segment.distance = iteration_setup.mission_iter.cruise_distance / 3
    segment.state.numerics.number_control_points = 8

    # post-process aerodynamic derivatives in cruise
    # segment.process.finalize.post_process.aero_derivatives = SUAVE.Methods.Flight_Dynamics.Static_Stability.compute_aero_derivatives

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   2. Cruise Segment: Constant Speed Constant Altitude
    # ------------------------------------------------------------------

    segment = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment)
    segment.tag = "cruise_2"

    segment.analyses.extend(analyses.cruise)

    segment.altitude = 31_000 * Units.ft
    segment.air_speed = 301.852 * 0.82 * Units['m/s']
    segment.distance = iteration_setup.mission_iter.cruise_distance / 3
    segment.state.numerics.number_control_points = 8

    # post-process aerodynamic derivatives in cruise
    # segment.process.finalize.post_process.aero_derivatives = SUAVE.Methods.Flight_Dynamics.Static_Stability.compute_aero_derivatives

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   3. Cruise Segment: Constant Speed Constant Altitude
    # ------------------------------------------------------------------

    segment = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment)
    segment.tag = "cruise_3"

    segment.analyses.extend(analyses.cruise)

    segment.altitude = 31_000 * Units.ft
    segment.air_speed = 301.852 * 0.82 * Units['m/s']
    segment.distance = iteration_setup.mission_iter.cruise_distance / 3
    segment.state.numerics.number_control_points = 8

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

    segment.altitude_start = 31_000 * Units.ft
    segment.altitude_end = 22_000 * Units.ft
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

    segment.altitude_end = 15_000 * Units.ft
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

    segment.altitude_end = 10_000 * Units.ft
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

    segment.altitude_end = 5_000 * Units.ft
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


    # ------------------------------------------------------------------
    #   Reserve Mission
    # ------------------------------------------------------------------


    # ------------------------------------------------------------------
    #   First Reserve Climb Segment: Constant Speed, Constant Rate
    # ------------------------------------------------------------------
    #
    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    # segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "reserve_climb_1"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 0.0 * Units.ft
    segment.altitude_end = 10.0 * Units.ft
    segment.air_speed = 160.0 * Units['m/s']
    segment.throttle = climb_throttle
    segment.state.numerics.number_control_points = 2
    # segment.climb_rate     = 1850.  * Units.ft / Units.min

    # add to misison
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Second Reserve Climb Segment: Constant Speed, Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    #segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "reserve_climb_2"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 1500.0 * Units.ft
    segment.altitude_end = 4000.0 * Units.ft
    segment.air_speed = 170.0 * Units['m/s']
    segment.throttle = climb_throttle
    #segment.climb_rate     = 1850.  * Units.ft / Units.min
    # segment.climb_rate     = 915.   * Units['ft/min']

    # add to misison
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Third Reserve Climb Segment: Constant Speed, Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "reserve_climb_3"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 4000.0 * Units.ft
    segment.altitude_end = 7000.0 * Units.ft
    segment.air_speed = 180.0 * Units['m/s']
    segment.throttle = climb_throttle

    # add to misison
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Fourth Reserve Climb Segment: Constant Speed, Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "reserve_climb_4"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 7000.0 * Units.ft
    segment.altitude_end = 9000.0 * Units.ft
    segment.air_speed = 190.0 * Units['m/s']
    segment.throttle = climb_throttle

    # add to misison
    mission.append_segment(segment)
    # ------------------------------------------------------------------
    #   Fifth Reserve Climb Segment: Constant Speed, Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "reserve_climb_5"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 9000.0 * Units.ft
    segment.altitude_end = 11000.0 * Units.ft
    segment.air_speed = 140. * Units['m/s']
    segment.throttle = climb_throttle

    # add to misison
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Reserve Cruise Segment: Constant Speed, Constant Altitude
    # ------------------------------------------------------------------

    segment = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment)
    segment.tag = "reserve_cruise"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise)

    segment.air_speed = 327.173 * 0.65 * Units['m/s']

    reserve_cruise_distance = iteration_setup.mission_iter.reserve_cruise_distance
    segment.distance = reserve_cruise_distance
    segment.state.numerics.number_control_points = 4

    # add to mission
    mission.append_segment(segment)
    #
    #
    # # ------------------------------------------------------------------
    # #   Third Reserve Descent Segment: Constant Speed, Constant Rate
    # # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    #segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    #segment = Segments.Descent.Constant_Speed_Constant_Angle(base_segment)
    segment.tag = "reserve_descent_3"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 11000.0 * Units.ft
    segment.altitude_end = 9000.0 * Units.ft
    segment.air_speed = 150 * Units['m/s']
    segment.throttle = idle_throttle
    #segment.descent_rate = 915. * Units['ft/min']
    #segment.descent_angle = 3 * Units.deg

    # add to misison
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   4# Reserve Descent Segment: Constant Speed, Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    #segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    #segment = Segments.Descent.Constant_Speed_Constant_Angle(base_segment)
    segment.tag = "reserve_descent_4"

    # connect vehicle configuration
    segment.analyses.extend(analyses.landing)

    segment.altitude_start = 9000.0 * Units.ft
    segment.altitude_end = 7000.0 * Units.ft
    segment.air_speed = 145.0 * Units['m/s']
    segment.throttle = idle_throttle
    #segment.descent_rate = 915. * Units['ft/min']
    #segment.descent_angle = 3 * Units.deg

    # add to misison
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   5# Reserve Descent Segment: Constant Speed, Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    #segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    #segment = Segments.Descent.Constant_Speed_Constant_Angle(base_segment)
    segment.tag = "reserve_descent_5"

    # connect vehicle configuration
    segment.analyses.extend(analyses.landing)

    segment.altitude_start = 7000.0 * Units.ft
    segment.altitude_end = 4000.0 * Units.ft
    segment.air_speed = 140.0 * Units['m/s']
    segment.throttle = idle_throttle
    #segment.descent_rate = 915. * Units['ft/min']
    #segment.descent_angle = 3 * Units.deg

    # add to misison
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   6# Reserve Descent Segment: Constant Speed, Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    #segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    #segment = Segments.Descent.Constant_Speed_Constant_Angle(base_segment)
    segment.tag = "reserve_descent_6"

    # connect vehicle configuration
    segment.analyses.extend(analyses.landing)

    segment.altitude_start = 4000.0 * Units.ft
    segment.altitude_end = 1500.0 * Units.ft
    segment.air_speed = 130.0 * Units['m/s']
    #segment.throttle = 1.
    #segment.descent_rate = 915. * Units['ft/min']
    segment.throttle = idle_throttle

    # add to misison
    mission.append_segment(segment)

    # # ------------------------------------------------------------------
    # #   7# Reserve Descent Segment: Constant Speed, Constant Rate
    # # ------------------------------------------------------------------
    #
    # segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    # segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    # segment = Segments.Descent.Constant_Speed_Constant_Angle(base_segment)
    # segment.tag = "reserve_descent_7"
    #
    # # connect vehicle configuration
    # segment.analyses.extend(analyses.landing)
    #
    # segment.altitude_start = 1500.0 * Units.ft
    # segment.altitude_end = 0.0 * Units.ft
    # segment.air_speed = 130.0 * Units['m/s']
    # # segment.throttle = 1.
    # # segment.descent_rate = 915. * Units['ft/min']
    # segment.descent_angle = 3 * Units.deg
    # segment.state.numerics.number_control_points = 2
    #
    # # add to mission
    # mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Reserve Hold Segment: Constant Speed, Constant Altitude
    # ------------------------------------------------------------------

    segment = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment)
    segment.tag = "hold"

    # connect vehicle configuration
    segment.analyses.extend(analyses.base)

    reserve_hold_time = iteration_setup.mission_iter.reserve_hold_time
    reserve_hold_speed = iteration_setup.mission_iter.reserve_hold_speed

    reserve_hold_distance = reserve_hold_speed * reserve_hold_time

    reserve_hold_altitude = iteration_setup.mission_iter.reserve_hold_altitude
    segment.altitude = reserve_hold_altitude

    segment.air_speed = reserve_hold_speed
    segment.distance = reserve_hold_distance
    segment.state.numerics.number_control_points = 8

    # add to mission
    mission.append_segment(segment)

    return mission