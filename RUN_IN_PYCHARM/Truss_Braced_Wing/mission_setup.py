import SUAVE
from SUAVE.Core import Units
def mission_setup(analyses, iteration_setup):

    atmosphere = SUAVE.Analyses.Atmospheric.US_Standard_1976()
    rho0 = 1.225

    cruise_1_alt =  iteration_setup.mission_iter.design_cruise_altitude - 3_000 * Units.ft
    cruise_1_tas = atmosphere.compute_values(cruise_1_alt).speed_of_sound * iteration_setup.mission_iter.design_cruise_mach
    rho_cr1 = atmosphere.compute_values(cruise_1_alt).density
    cruise_1_ias = (rho_cr1 / rho0)**0.5 * cruise_1_tas

    climb_throttle = 1.
    idle_throttle = 0.03
    climb_speed_factor = 1.

    cruise_frac_1 = 0.25
    cruise_frac_2 = 0.25
    cruise_frac_3 = 0.25
    cruise_frac_4 = 1 - cruise_frac_1 - cruise_frac_2 - cruise_frac_3

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
    segment.air_speed = min(cruise_1_ias / (rho / rho0)**0.5 * climb_speed_factor, 250 * Units.knots)

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
    segment.air_speed = min(cruise_1_ias / (rho / rho0)**0.5 * climb_speed_factor, 250 * Units.knots)
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
    # ------------------------------------------------------------------
    #   Seventh Climb Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------
    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "climb_7"

    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 28_000 * Units.ft
    segment.altitude_end = 30_000 * Units.ft
    rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5 * climb_speed_factor
    segment.throttle = climb_throttle

    # add to mission
    mission.append_segment(segment)


    if iteration_setup.mission_iter.design_cruise_altitude > 34_000 * Units.ft:
        # ------------------------------------------------------------------
        #   Eigth Climb Segment: Constant Speed Constant Rate
        # ------------------------------------------------------------------
        segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
        segment.tag = "climb_8"

        segment.analyses.extend(analyses.cruise)

        segment.altitude_start = 30_000 * Units.ft
        segment.altitude_end = 32_000 * Units.ft
        rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
        segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5 * climb_speed_factor
        segment.state.numerics.number_control_points = 10
        segment.throttle = climb_throttle

        # add to mission
        mission.append_segment(segment)

        if iteration_setup.mission_iter.design_cruise_altitude > 36_000 * Units.ft:
            # ------------------------------------------------------------------
            #   Ninth Climb Segment: Constant Speed Constant Rate
            # ------------------------------------------------------------------
            segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
            segment.tag = "climb_9"

            segment.analyses.extend(analyses.cruise)

            segment.altitude_start = 32_000 * Units.ft
            segment.altitude_end = 34_000 * Units.ft
            rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
            segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5 * climb_speed_factor
            segment.throttle = climb_throttle

            # add to mission
            mission.append_segment(segment)

            if iteration_setup.mission_iter.design_cruise_altitude >= 38_000 * Units.ft:
                # ------------------------------------------------------------------
                #   Tenth Climb Segment: Constant Speed Constant Rate
                # ------------------------------------------------------------------
                segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
                segment.tag = "climb_10"

                segment.analyses.extend(analyses.cruise)

                segment.altitude_start = 34_000 * Units.ft
                segment.altitude_end = 36_000 * Units.ft
                rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
                segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5 * climb_speed_factor
                segment.state.numerics.number_control_points = 10
                segment.throttle = climb_throttle

                # add to mission
                mission.append_segment(segment)

                if iteration_setup.mission_iter.design_cruise_altitude > 40_000 * Units.ft:
                    # ------------------------------------------------------------------
                    #   Eleventh Climb Segment: Constant Speed Constant Rate
                    # ------------------------------------------------------------------
                    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
                    segment.tag = "climb_11"

                    segment.analyses.extend(analyses.cruise)

                    segment.altitude_start = 36_000 * Units.ft
                    segment.altitude_end = 38_000 * Units.ft
                    rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
                    segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5 * climb_speed_factor
                    segment.state.numerics.number_control_points = 10
                    segment.throttle = climb_throttle

                    # add to mission
                    mission.append_segment(segment)

                    if iteration_setup.mission_iter.design_cruise_altitude > 42_000 * Units.ft:
                        # ------------------------------------------------------------------
                        #   Twelfth Climb Segment: Constant Speed Constant Rate
                        # ------------------------------------------------------------------
                        segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
                        segment.tag = "climb_12"

                        segment.analyses.extend(analyses.cruise)

                        segment.altitude_start = 38_000 * Units.ft
                        segment.altitude_end = 40_000 * Units.ft
                        rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
                        segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5 * climb_speed_factor
                        segment.state.numerics.number_control_points = 10
                        segment.throttle = climb_throttle

                        # add to mission
                        mission.append_segment(segment)

                        if iteration_setup.mission_iter.design_cruise_altitude > 44_000 * Units.ft:
                            # ------------------------------------------------------------------
                            #   Thirteenth Climb Segment: Constant Speed Constant Rate
                            # ------------------------------------------------------------------
                            segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
                            segment.tag = "climb_13"

                            segment.analyses.extend(analyses.cruise)

                            segment.altitude_start = 40_000 * Units.ft
                            segment.altitude_end = 42_000 * Units.ft
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

    segment.altitude = iteration_setup.mission_iter.design_cruise_altitude - 3_000 * Units.ft
    segment.air_speed = atmosphere.compute_values(segment.altitude).speed_of_sound * iteration_setup.mission_iter.design_cruise_mach
    segment.distance = iteration_setup.mission_iter.cruise_distance * cruise_frac_1
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

    segment.altitude_start = iteration_setup.mission_iter.design_cruise_altitude - 3_000 * Units.ft
    segment.altitude_end = iteration_setup.mission_iter.design_cruise_altitude - 1_000 * Units.ft
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

    segment.altitude = iteration_setup.mission_iter.design_cruise_altitude - 1_000 * Units.ft
    segment.air_speed = atmosphere.compute_values(segment.altitude).speed_of_sound * iteration_setup.mission_iter.design_cruise_mach
    segment.distance = iteration_setup.mission_iter.cruise_distance * cruise_frac_2
    segment.state.numerics.number_control_points = 8

    # rho_cr1 = atmosphere.compute_values(segment.altitude).density
    # cruise_1_ias = (rho_cr1 / rho0) * segment.air_speed

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

    segment.altitude_start = iteration_setup.mission_iter.design_cruise_altitude - 1_000 * Units.ft
    segment.altitude_end = iteration_setup.mission_iter.design_cruise_altitude + 1_000 * Units.ft
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

    segment.altitude = iteration_setup.mission_iter.design_cruise_altitude + 1_000 * Units.ft
    segment.air_speed = atmosphere.compute_values(segment.altitude).speed_of_sound * iteration_setup.mission_iter.design_cruise_mach
    segment.distance = iteration_setup.mission_iter.cruise_distance * cruise_frac_3
    segment.state.numerics.number_control_points = 8

    # post-process aerodynamic derivatives in cruise
    # segment.process.finalize.post_process.aero_derivatives = SUAVE.Methods.Flight_Dynamics.Static_Stability.compute_aero_derivatives

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Second Step Climb Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "step_climb_3"

    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = iteration_setup.mission_iter.design_cruise_altitude + 1_000 * Units.ft
    segment.altitude_end = iteration_setup.mission_iter.design_cruise_altitude + 3_000 * Units.ft
    segment.air_speed = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).speed_of_sound * iteration_setup.mission_iter.design_cruise_mach
    segment.throttle = climb_throttle
    segment.state.numerics.number_control_points = 4

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   3. Cruise Segment: Constant Speed Constant Altitude
    # ------------------------------------------------------------------

    segment = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment)
    segment.tag = "cruise_4"

    segment.analyses.extend(analyses.cruise)

    segment.altitude = iteration_setup.mission_iter.design_cruise_altitude + 3_000 * Units.ft
    segment.air_speed = atmosphere.compute_values(
        segment.altitude).speed_of_sound * iteration_setup.mission_iter.design_cruise_mach
    segment.distance = iteration_setup.mission_iter.cruise_distance * cruise_frac_4
    segment.state.numerics.number_control_points = 8

    # post-process aerodynamic derivatives in cruise
    # segment.process.finalize.post_process.aero_derivatives = SUAVE.Methods.Flight_Dynamics.Static_Stability.compute_aero_derivatives

    cruise_1_alt = iteration_setup.mission_iter.design_cruise_altitude + 3_000 * Units.ft
    cruise_1_tas = atmosphere.compute_values(cruise_1_alt).speed_of_sound * iteration_setup.mission_iter.design_cruise_mach
    rho_cr1 = atmosphere.compute_values(cruise_1_alt).density
    cruise_1_ias = (rho_cr1 / rho0) ** 0.5 * cruise_1_tas


    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Second Step Climb Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------

    # segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    # segment.tag = "step_climb_4"
    #
    # segment.analyses.extend(analyses.cruise)
    #
    # segment.altitude_start = iteration_setup.mission_iter.design_cruise_altitude + 2_000 * Units.ft
    # segment.altitude_end = iteration_setup.mission_iter.design_cruise_altitude + 4_000 * Units.ft
    # segment.air_speed = atmosphere.compute_values((
    #                                                           segment.altitude_start + segment.altitude_end) / 2).speed_of_sound * iteration_setup.mission_iter.design_cruise_mach
    # segment.throttle = climb_throttle
    # segment.state.numerics.number_control_points = 4
    #
    # # add to mission
    # mission.append_segment(segment)
    #
    # # ------------------------------------------------------------------
    # #   3. Cruise Segment: Constant Speed Constant Altitude
    # # ------------------------------------------------------------------
    #
    # segment = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment)
    # segment.tag = "cruise_5"
    #
    # segment.analyses.extend(analyses.cruise)
    #
    # segment.altitude = iteration_setup.mission_iter.design_cruise_altitude + 4_000 * Units.ft
    # segment.air_speed = atmosphere.compute_values(
    #     segment.altitude).speed_of_sound * iteration_setup.mission_iter.design_cruise_mach
    # segment.distance = iteration_setup.mission_iter.cruise_distance * cruise_frac_4
    # segment.state.numerics.number_control_points = 8
    #
    # # post-process aerodynamic derivatives in cruise
    # # segment.process.finalize.post_process.aero_derivatives = SUAVE.Methods.Flight_Dynamics.Static_Stability.compute_aero_derivatives
    #
    # cruise_1_alt = iteration_setup.mission_iter.design_cruise_altitude  # + 3_000 * Units.ft
    # cruise_1_tas = atmosphere.compute_values(
    #     cruise_1_alt).speed_of_sound * iteration_setup.mission_iter.design_cruise_mach
    # rho_cr1 = atmosphere.compute_values(cruise_1_alt).density
    # cruise_1_ias = (rho_cr1 / rho0) ** 0.5 * cruise_1_tas
    #
    # # add to mission
    # mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Zeroth Descent Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------
    if iteration_setup.mission_iter.design_cruise_altitude > 43_000 * Units.ft:
        segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
        segment.tag = "descent_0"

        segment.analyses.extend(analyses.cruise)

        segment.altitude_start = 47_000 * Units.ft
        segment.altitude_end = 45_000 * Units.ft
        rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
        segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5
        segment.state.numerics.number_control_points = 10
        segment.throttle = idle_throttle

        # add to mission
        mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   First Descent Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------
    if iteration_setup.mission_iter.design_cruise_altitude > 41_000 * Units.ft:
        segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
        segment.tag = "descent_1"

        segment.analyses.extend(analyses.cruise)

        segment.altitude_start = 45_000 * Units.ft
        segment.altitude_end = 43_000 * Units.ft
        rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
        segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5
        segment.state.numerics.number_control_points = 10
        segment.throttle = idle_throttle

        # add to mission
        mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Second Descent Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------
    if iteration_setup.mission_iter.design_cruise_altitude >= 38_000 * Units.ft:
        segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
        segment.tag = "descent_2"

        segment.analyses.extend(analyses.cruise)


        segment.altitude_start = 43_000 * Units.ft
        segment.altitude_end = 41_000 * Units.ft
        rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
        segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5
        segment.state.numerics.number_control_points = 10
        segment.throttle = idle_throttle

        # add to mission
        mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Third Descent Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------
    if iteration_setup.mission_iter.design_cruise_altitude > 35_000 * Units.ft:
        segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
        segment.tag = "descent_3"

        segment.analyses.extend(analyses.cruise)

        segment.altitude_start = 39_000 * Units.ft
        segment.altitude_end = 37_000 * Units.ft
        rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
        segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5
        segment.state.numerics.number_control_points = 10
        segment.throttle = idle_throttle

        # add to mission
        mission.append_segment(segment)

    # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    if iteration_setup.mission_iter.design_cruise_altitude > 33_000 * Units.ft:
        segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
        segment.tag = "descent_4"

        segment.analyses.extend(analyses.cruise)

        segment.altitude_start = 37_000 * Units.ft
        segment.altitude_end = 35_000 * Units.ft
        rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
        segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5
        segment.state.numerics.number_control_points = 10
        segment.throttle = idle_throttle

        # add to mission
        mission.append_segment(segment)

    # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    if iteration_setup.mission_iter.design_cruise_altitude > 31_000 * Units.ft:
        segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
        segment.tag = "descent_5"

        segment.analyses.extend(analyses.cruise)

        segment.altitude_start = 35_000 * Units.ft
        segment.altitude_end = 33_000 * Units.ft
        rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
        segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5
        segment.state.numerics.number_control_points = 10
        segment.throttle = idle_throttle
        last_seg_alt = segment.altitude_end

        # add to mission
        mission.append_segment(segment)

    # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    if iteration_setup.mission_iter.design_cruise_altitude > 29_000 * Units.ft:
        segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
        segment.tag = "descent_6"

        segment.analyses.extend(analyses.cruise)

        segment.altitude_start = 33_000 * Units.ft
        segment.altitude_end = 31_000 * Units.ft
        rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
        segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5
        segment.state.numerics.number_control_points = 10
        segment.throttle = idle_throttle
        last_seg_alt = segment.altitude_end

        # add to mission
        mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Seventh Descent Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "descent_7"

    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 31_000 * Units.ft
    segment.altitude_end = 29_000 * Units.ft
    rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5
    segment.state.numerics.number_control_points = 8
    segment.throttle = idle_throttle

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Eigth Descent Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "descent_8"

    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 29_000 * Units.ft
    segment.altitude_end = 27_000 * Units.ft
    rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5
    segment.state.numerics.number_control_points = 8
    segment.throttle = idle_throttle

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Ninth Descent Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "descent_9"

    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 27_000 * Units.ft
    segment.altitude_end = 24_000 * Units.ft
    rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5
    segment.state.numerics.number_control_points = 8
    segment.throttle = idle_throttle

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Tenth Descent Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "descent_10"

    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 24_000 * Units.ft
    segment.altitude_end = 21_000 * Units.ft
    rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5
    segment.state.numerics.number_control_points = 8
    segment.throttle = idle_throttle

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Eleventh Descent Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "descent_11"

    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 21_000 * Units.ft
    segment.altitude_end = 18_000 * Units.ft
    rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5
    segment.state.numerics.number_control_points = 8
    segment.throttle = idle_throttle

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Twelfth Descent Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "descent_12"

    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 18_000 * Units.ft
    segment.altitude_end = 15_000 * Units.ft
    rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5
    segment.state.numerics.number_control_points = 10
    segment.throttle = idle_throttle

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Thirteenth Descent Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "descent_13"

    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 15_000 * Units.ft
    segment.altitude_end = 12_000 * Units.ft
    rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5
    segment.state.numerics.number_control_points = 10
    segment.throttle = idle_throttle

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Fourteenth Descent Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "descent_14"

    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 12_000 * Units.ft
    segment.altitude_end = 10_000 * Units.ft
    rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    segment.air_speed = cruise_1_ias / (rho / rho0) ** 0.5
    segment.state.numerics.number_control_points = 10
    segment.throttle = idle_throttle

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Fifteenth Descent Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "descent_15"

    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 10_000 * Units.ft
    segment.altitude_end = 6_000 * Units.ft
    rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    segment.air_speed = min(cruise_1_ias / (rho / rho0) ** 0.5, 250 * Units.knots)
    segment.state.numerics.number_control_points = 10
    segment.throttle = idle_throttle

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Sixteenth Descent Segment: Constant Speed Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "descent_16"

    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 6_000 * Units.ft
    segment.altitude_end = 3_000 * Units.ft
    rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    segment.air_speed = min(cruise_1_ias / (rho / rho0) ** 0.5, 250 * Units.knots)
    segment.state.numerics.number_control_points = 10
    segment.throttle = idle_throttle

    # add to mission
    mission.append_segment(segment)


    # ------------------------------------------------------------------
    #   Reserve Mission
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    #   First Reserve Climb Segment: Constant Speed, Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "reserve_climb_1"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 3_000.0 * Units.ft
    segment.altitude_end = 6_000 * Units.ft
    rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    segment.air_speed = min(cruise_1_ias / (rho / rho0) ** 0.5, 250 * Units.knots)
    segment.throttle = climb_throttle
    segment.state.numerics.number_control_points = 4

    # add to misison
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Second Reserve Climb Segment: Constant Speed, Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "reserve_climb_2"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 6_000 * Units.ft
    segment.altitude_end = 10_000 * Units.ft
    rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    segment.air_speed = min(cruise_1_ias / (rho / rho0) ** 0.5, 250 * Units.knots)
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
    segment.altitude_end = 17_000 * Units.ft
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

    segment.altitude_start = 17_000 * Units.ft
    segment.altitude_end = 14_000 * Units.ft
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

    segment.altitude_start = 14_000 * Units.ft
    segment.altitude_end = 10_000 * Units.ft
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

    segment.altitude_start = 10_000 * Units.ft
    segment.altitude_end = 8_000.0 * Units.ft
    rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    segment.air_speed = min(cruise_1_ias / (rho / rho0) ** 0.5, 250 * Units.knots)
    segment.state.numerics.number_control_points = 8
    segment.throttle = idle_throttle

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Fifth Reserve Descent Segment: Constant Speed, Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "reserve_descent_5"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 8_000 * Units.ft
    segment.altitude_end = 5_000.0 * Units.ft
    rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    segment.air_speed = min(cruise_1_ias / (rho / rho0) ** 0.5, 250 * Units.knots)
    segment.state.numerics.number_control_points = 8
    segment.throttle = idle_throttle

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Sixth Reserve Descent Segment: Constant Speed, Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "reserve_descent_6"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 5_000 * Units.ft
    segment.altitude_end = 3_000.0 * Units.ft
    rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    segment.air_speed = min(cruise_1_ias / (rho / rho0) ** 0.5, 250 * Units.knots)
    segment.state.numerics.number_control_points = 8
    segment.throttle = idle_throttle

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Seventh Reserve Descent Segment: Constant Speed, Constant Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag = "reserve_descent_7"

    # connect vehicle configuration
    segment.analyses.extend(analyses.cruise)

    segment.altitude_start = 3_000 * Units.ft
    segment.altitude_end = 1_500.0 * Units.ft
    rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    segment.air_speed = min(cruise_1_ias / (rho / rho0) ** 0.5, 250 * Units.knots)
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
    reserve_hold_speed = min(cruise_1_ias / (rho / rho0) ** 0.5, 250 * Units.knots)
    iteration_setup.mission_iter.reserve_hold_speed = reserve_hold_speed

    segment.altitude = reserve_hold_altitude

    reserve_hold_distance = reserve_hold_speed * reserve_hold_time


    segment.air_speed = reserve_hold_speed
    segment.distance = reserve_hold_distance
    segment.state.numerics.number_control_points = 8

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    # #   Fifth Reserve Descent Segment: Constant Speed, Constant Rate
    # # ------------------------------------------------------------------
    #
    # segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    # segment.tag = "reserve_descent_8"
    #
    # # connect vehicle configuration
    # segment.analyses.extend(analyses.landing)
    # segment.altitude_start = 1_500 * Units.ft
    # segment.altitude_end = 0.0 * Units.ft
    # rho = atmosphere.compute_values((segment.altitude_start + segment.altitude_end) / 2).density
    # segment.air_speed = min(cruise_1_ias / (rho / rho0) ** 0.5, 250 * Units.knots)
    # segment.throttle = idle_throttle
    #
    # # add to mission
    # mission.append_segment(segment)

    return mission