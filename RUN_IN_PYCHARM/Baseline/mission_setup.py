import SUAVE
from SUAVE.Core import Units
def mission_setup(analyses, iteration_setup):

    atmosphere = SUAVE.Analyses.Atmospheric.US_Standard_1976()
    rho0 = 1.225

    cruise_1_alt=iteration_setup.mission_iter.design_cruise_altitude
    cruise_1_tas = atmosphere.compute_values(cruise_1_alt).speed_of_sound * iteration_setup.mission_iter.design_cruise_mach

    rho_cr1 = atmosphere.compute_values(cruise_1_alt).density
    cruise_1_ias = (rho_cr1 / rho0)**0.5 * cruise_1_tas

    climb_throttle = 1.
    idle_throttle = 0.03
    climb_speed_factor = 1.

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

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "climb_1"

    segment.analyses.extend(analyses.takeoff)

    segment.altitude_start = 0.0 * Units.km
    segment.altitude_end = 5_000 * Units.ft

    rho = atmosphere.compute_values((segment.altitude_start+segment.altitude_end)/2).density
    segment.air_speed = cruise_1_ias / (rho / rho0)**0.5 * climb_speed_factor

    segment.throttle = climb_throttle

    # add to misison
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Second Climb Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "climb_2"

    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 5_000 * Units.ft
    segment.altitude_end = 10_000 * Units.ft
    rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5 * climb_speed_factor
    segment.throttle = climb_throttle

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Third Climb Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "climb_3"

    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 10_000 * Units.ft
    segment.altitude_end = 15_000 * Units.ft
    rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5 * climb_speed_factor
    segment.throttle = climb_throttle

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Fourth Climb Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "climb_4"

    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 15_000 * Units.ft
    segment.altitude_end = 20_000 * Units.ft
    rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5 * climb_speed_factor
    segment.throttle = climb_throttle

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Fifth Climb Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "climb_5"

    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 20_000 * Units.ft
    segment.altitude_end = 24_000 * Units.ft
    rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5 * climb_speed_factor
    segment.throttle = climb_throttle
    #segment.state.numerics.number_control_points = 10

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Sixth Climb Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "climb_6"

    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 24_000 * Units.ft
    segment.altitude_end = 28_000 * Units.ft
    rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5 * climb_speed_factor
    segment.throttle = climb_throttle

    # add to mission
    mission.append_segment(segment)
    last_seg_alt = segment.altitude_end
    # ------------------------------------------------------------------
    #   Seventh Climb Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------
    if iteration_setup.mission_iter.design_cruise_altitude > 33_000 * Units.ft:
        segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
        segment.tag = "climb_7"

        segment.analyses.extend(analyses.cruise)

        segment.altitude_start = 28_000 * Units.ft
        segment.altitude_end = 31_000 * Units.ft
        rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
        segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5 * climb_speed_factor
        segment.throttle = climb_throttle

        # add to mission
        mission.append_segment(segment)
        last_seg_alt = segment.altitude_end

    # ------------------------------------------------------------------
    #   Eighth Climb Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------
    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "climb_8"

    segment.analyses.extend(analyses.cruise)
    segment.altitude_start = last_seg_alt
    segment.altitude_end = iteration_setup.mission_iter.design_cruise_altitude - 2_000 * Units.ft
    rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5 * climb_speed_factor
    segment.throttle = climb_throttle

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   1. Cruise Segment: Constant Speed Constant Altitude
    # ------------------------------------------------------------------

    segment = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment)
    segment.tag = "cruise_1"

    segment.analyses.extend(analyses.cruise)

    segment.altitude = iteration_setup.mission_iter.design_cruise_altitude - 2_000 * Units.ft
    segment.air_speed = atmosphere.compute_values(segment.altitude).speed_of_sound * iteration_setup.mission_iter.design_cruise_mach
    segment.distance = iteration_setup.mission_iter.cruise_distance / 3
    segment.state.numerics.number_control_points = 8


    # post-process aerodynamic derivatives in cruise
    # segment.process.finalize.post_process.aero_derivatives = SUAVE.Methods.Flight_Dynamics.Static_Stability.compute_aero_derivatives

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   First Step Climb Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "step_climb_1"

    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = iteration_setup.mission_iter.design_cruise_altitude - 2_000 * Units.ft
    segment.altitude_end = iteration_setup.mission_iter.design_cruise_altitude
    segment.air_speed = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).speed_of_sound * iteration_setup.mission_iter.design_cruise_mach
    segment.throttle = climb_throttle
    segment.state.numerics.number_control_points = 4


    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   2. Cruise Segment: Constant Speed Constant Altitude
    # ------------------------------------------------------------------

    segment = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment)
    segment.tag = "cruise_2"

    segment.analyses.extend(analyses.cruise)

    segment.altitude = iteration_setup.mission_iter.design_cruise_altitude
    segment.air_speed = atmosphere.compute_values(segment.altitude).speed_of_sound * iteration_setup.mission_iter.design_cruise_mach
    segment.distance = iteration_setup.mission_iter.cruise_distance / 3
    segment.state.numerics.number_control_points = 8

    rho_cr1 = atmosphere.compute_values(segment.altitude).density
    cruise_1_ias = (rho_cr1 / rho0) * segment.air_speed

    # post-process aerodynamic derivatives in cruise
    # segment.process.finalize.post_process.aero_derivatives = SUAVE.Methods.Flight_Dynamics.Static_Stability.compute_aero_derivatives

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Second Step Climb Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "step_climb_2"

    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = iteration_setup.mission_iter.design_cruise_altitude
    segment.altitude_end = iteration_setup.mission_iter.design_cruise_altitude + 2_000 * Units.ft
    segment.air_speed = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).speed_of_sound * iteration_setup.mission_iter.design_cruise_mach
    segment.throttle = climb_throttle
    segment.state.numerics.number_control_points = 4

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   3. Cruise Segment: Constant Speed Constant Altitude
    # ------------------------------------------------------------------

    segment = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment)
    segment.tag = "cruise_3"

    segment.analyses.extend(analyses.cruise)

    segment.altitude = iteration_setup.mission_iter.design_cruise_altitude + 2_000 * Units.ft
    segment.air_speed = atmosphere.compute_values(segment.altitude).speed_of_sound * iteration_setup.mission_iter.design_cruise_mach
    segment.distance = iteration_setup.mission_iter.cruise_distance / 3
    segment.state.numerics.number_control_points = 8

    # post-process aerodynamic derivatives in cruise
    # segment.process.finalize.post_process.aero_derivatives = SUAVE.Methods.Flight_Dynamics.Static_Stability.compute_aero_derivatives

    # add to mission
    mission.append_segment(segment)
    last_seg_alt = iteration_setup.mission_iter.design_cruise_altitude + 2_000 * Units.ft
    if iteration_setup.mission_iter.design_cruise_altitude > 33_000 * Units.ft:
        segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
        segment.tag = "descent_0"

        segment.analyses.extend(analyses.cruise)

        segment.altitude_start = iteration_setup.mission_iter.design_cruise_altitude + 2_000 * Units.ft
        segment.altitude_end = 32_000 * Units.ft
        rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
        segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5
        segment.state.numerics.number_control_points = 10
        segment.throttle = idle_throttle
        last_seg_alt = segment.altitude_end

        # add to mission
        mission.append_segment(segment)
    # ------------------------------------------------------------------
    #   First Descent Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "descent_1"

    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = last_seg_alt
    segment.altitude_end = 27_000 * Units.ft
    rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5
    segment.state.numerics.number_control_points = 10
    segment.throttle = idle_throttle

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Second Descent Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "descent_2"

    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 27_000 * Units.ft
    segment.altitude_end = 23_000 * Units.ft
    rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5
    segment.state.numerics.number_control_points = 10
    segment.throttle = idle_throttle

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Third Descent Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "descent_3"

    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 23_000 * Units.ft
    segment.altitude_end = 19_000 * Units.ft
    rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5
    segment.state.numerics.number_control_points = 8
    segment.throttle = idle_throttle

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Fourth Descent Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "descent_4"

    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 19_000 * Units.ft
    segment.altitude_end = 15_000 * Units.ft
    rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5
    segment.state.numerics.number_control_points = 8
    segment.throttle = idle_throttle

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Fifth Descent Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "descent_5"

    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 15_000 * Units.ft
    segment.altitude_end = 10_000 * Units.ft
    rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5
    segment.state.numerics.number_control_points = 10
    segment.throttle = idle_throttle

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Sixth Descent Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "descent_6"

    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 10_000 * Units.ft
    segment.altitude_end = 5_000 * Units.ft
    rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5
    segment.state.numerics.number_control_points = 10
    segment.throttle = idle_throttle

    # add to mission
    mission.append_segment(segment)

    # # ------------------------------------------------------------------
    # #   First Descent Segment: Constant Speed Constant Rate
    # # ------------------------------------------------------------------
    #
    # segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    # segment.tag = "descent_7"
    #
    # segment.analyses.extend(analyses.cruise)
    #
    # segment.altitude_start = 5_000 * Units.ft
    # segment.altitude_end = 0 * Units.ft
    # rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    # segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5 * 1.2 # TODO
    # segment.throttle = idle_throttle
    #
    # # add to mission
    # mission.append_segment(segment)

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
    # segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    # segment.tag = "reserve_climb_1"
    #
    # # connect vehicle configuration
    # segment.analyses.extend(analyses.cruise)
    #
    # segment.altitude_start = 0.0 * Units.ft
    # segment.altitude_end = 5_000 * Units.ft
    # rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    # segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5
    # segment.throttle = climb_throttle
    # segment.state.numerics.number_control_points = 2
    #
    # # add to misison
    # mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Second Reserve Climb Segment: Constant Speed, Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "reserve_climb_2"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 5_000 * Units.ft
    segment.altitude_end = 10_000 * Units.ft
    rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5
    segment.throttle = climb_throttle

    # add to misison
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Third Reserve Climb Segment: Constant Speed, Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "reserve_climb_3"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 10_000 * Units.ft
    segment.altitude_end = 15_000 * Units.ft
    rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5
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

    segment.altitude_start = 15_000 * Units.ft
    segment.altitude_end = 20_000 * Units.ft
    rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5
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
    segment.altitude = 20_000 * Units.ft
    rho = atmosphere.compute_values(segment.altitude).density
    segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5

    reserve_cruise_distance = iteration_setup.mission_iter.reserve_cruise_distance
    segment.distance = reserve_cruise_distance
    segment.state.numerics.number_control_points = 4

    # add to mission
    mission.append_segment(segment)


    # ------------------------------------------------------------------
    #   First Reserve Descent Segment: Constant Speed, Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "reserve_descent_1"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 20_000 * Units.ft
    segment.altitude_end = 15_000 * Units.ft
    rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5
    segment.state.numerics.number_control_points = 10
    segment.throttle = idle_throttle

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Second Reserve Descent Segment: Constant Speed, Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "reserve_descent_2"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 15_000 * Units.ft
    segment.altitude_end = 10_000 * Units.ft
    rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5
    segment.state.numerics.number_control_points = 10
    segment.throttle = idle_throttle

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Third Reserve Descent Segment: Constant Speed, Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "reserve_descent_3"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 10_000 * Units.ft
    segment.altitude_end = 5_000 * Units.ft
    rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5
    segment.state.numerics.number_control_points = 10
    segment.throttle = idle_throttle

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Fourth Reserve Descent Segment: Constant Speed, Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "reserve_descent_4"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 5_000 * Units.ft
    segment.altitude_end = 1_500.0 * Units.ft
    rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5
    segment.state.numerics.number_control_points = 8
    segment.throttle = idle_throttle

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Hold Segment: Constant Speed, Constant Altitude
    # ------------------------------------------------------------------

    segment = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment)
    segment.tag = "hold"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise)

    reserve_hold_time = iteration_setup.mission_iter.reserve_hold_time
    reserve_hold_altitude = iteration_setup.mission_iter.reserve_hold_altitude

    rho = atmosphere.compute_values(reserve_hold_altitude).density
    reserve_hold_speed = cruise_1_ias / (rho / rho0) ** 0.5
    iteration_setup.mission_iter.reserve_hold_speed = reserve_hold_speed

    segment.altitude = reserve_hold_altitude

    reserve_hold_distance = reserve_hold_speed * reserve_hold_time


    segment.air_speed = reserve_hold_speed
    segment.distance = reserve_hold_distance
    segment.state.numerics.number_control_points = 8

    # add to mission
    mission.append_segment(segment)

    # # ------------------------------------------------------------------
    # #   Fifth Reserve Descent Segment: Constant Speed, Constant Rate
    # # ------------------------------------------------------------------
    #
    # segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    # segment.tag = "reserve_descent_5"
    #
    # # connect vehicle configuration
    # segment.analyses.extend(analyses.landing)
    # segment.altitude_start = 1_500 * Units.ft
    # segment.altitude_end = 0.0 * Units.ft
    # rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    # segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5
    # segment.throttle = idle_throttle
    #
    # # add to mission
    # mission.append_segment(segment)

    return mission