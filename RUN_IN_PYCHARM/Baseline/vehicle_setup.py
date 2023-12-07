# vehicle_setup.py
#
# Created:  Nov 2023, J. Frank
# Modified:

""" Setup File for the Aircraft Design Seminar 2023/24 Baseline Aircraft
"""


# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------

import numpy as np
import SUAVE
from SUAVE.Core import Units
from SUAVE.Methods.Propulsion.turbofan_sizing import turbofan_sizing
from SUAVE.Methods.Geometry.Two_Dimensional.Planform import wing_planform, wing_segmented_planform, create_tapered_wing, wing_planform_v_tail, fuselage_planform

from copy import deepcopy 

# ----------------------------------------------------------------------
#   Define the Vehicle
# ----------------------------------------------------------------------

def vehicle_setup(iteration_setup):

    # ------------------------------------------------------------------
    #   Initialize the Vehicle
    # ------------------------------------------------------------------

    vehicle = SUAVE.Vehicle()
    vehicle.tag = 'Baseline_Aircraft'
    vehicle.systems.control = "fully powered"
    vehicle.systems.accessories = "longe range"

    # ------------------------------------------------------------------
    #   Vehicle-level Properties
    # ------------------------------------------------------------------

    # mass properties
    vehicle.mass_properties.max_payload               = 50000.  * Units.kilogram
    vehicle.mass_properties.max_takeoff               = iteration_setup.weight_iter.TOW
    vehicle.mass_properties.takeoff                   = iteration_setup.weight_iter.TOW
    vehicle.mass_properties.operating_empty           = iteration_setup.weight_iter.BOW
    vehicle.mass_properties.max_zero_fuel             = iteration_setup.weight_iter.BOW \
                                                        + vehicle.mass_properties.max_payload
                                                        #+ iteration_setup.weight_iter.Design_Payload
    vehicle.mass_properties.max_fuel                  = iteration_setup.weight_iter.FUEL   # kg
    vehicle.mass_properties.cargo                     = 14500.  * Units.kilogram
    #vehicle.mass_properties.center_of_gravity         = [[ 25.,   0.,  -0.48023939]]
    #vehicle.mass_properties.moments_of_inertia.tensor = [[3173074.17, 0 , 28752.77565],[0 , 3019041.443, 0],[0, 0, 5730017.433]] # estimated, not correct
    vehicle.design_mach_number                        = iteration_setup.mission_iter.design_cruise_mach
    vehicle.design_range                              = 10500 * Units['nautical_mile']
    vehicle.design_cruise_alt                         = iteration_setup.mission_iter.design_cruise_altitude

    # envelope properties
    vehicle.envelope.ultimate_load = 2.5 * 1.5
    vehicle.envelope.limit_load    = 2.5

    # basic parameters
    vehicle.reference_area         = vehicle.mass_properties.max_takeoff / iteration_setup.sizing_iter.wing_loading
    vehicle.passengers             = 100
  
    # ------------------------------------------------------------------
    #   Main Wing
    # ------------------------------------------------------------------

    wing = SUAVE.Components.Wings.Main_Wing()
    wing.tag = 'main_wing'

    wing.areas.reference         = vehicle.reference_area
    wing.origin                  = iteration_setup.sizing_iter.wing_origin

    wing.transition_x_upper = 0.08
    wing.transition_x_lower = 0.08

    wing.vertical                = False
    wing.symmetric               = True
    wing.high_lift               = True

    wing.flap_ratio = 0.3
    wing.dynamic_pressure_ratio  = 1.0

    wing.aspect_ratio = iteration_setup.sizing_iter.aspect_ratio
    wing.sweeps.quarter_chord = iteration_setup.sizing_iter.sweep_quarter_chord
    wing.thickness_to_chord = iteration_setup.sizing_iter.thickness_to_chord
    wing.taper = 0.2893

    # Wing Segments
    root_airfoil                          = SUAVE.Components.Airfoils.Airfoil()
    root_airfoil.coordinate_file          = 'Airfoils/B737a.txt'
    segment                               = SUAVE.Components.Wings.Segment()
    segment.tag                           = 'Root'
    segment.percent_span_location         = 0.0
    segment.twist                         = 0 * Units.deg
    segment.root_chord_percent            = 1.
    segment.thickness_to_chord            = 1.2 * iteration_setup.sizing_iter.thickness_to_chord
    segment.dihedral_outboard             = 3. * Units.degrees
    segment.sweeps.quarter_chord          = wing.sweeps.quarter_chord
    segment.append_airfoil(root_airfoil)
    wing.append_segment(segment)

    mid_airfoil                           = SUAVE.Components.Airfoils.Airfoil()
    mid_airfoil.coordinate_file           = 'Airfoils/B737b.txt'
    segment                               = SUAVE.Components.Wings.Segment()
    segment.tag                           = 'Section_2'
    segment.percent_span_location         = 0.4
    segment.twist                         = 0.00258 * Units.deg
    segment.root_chord_percent            = 0.8
    segment.thickness_to_chord            = iteration_setup.sizing_iter.thickness_to_chord
    segment.dihedral_outboard             = 3. * Units.degrees
    segment.sweeps.quarter_chord          = wing.sweeps.quarter_chord
    segment.append_airfoil(mid_airfoil)
    wing.append_segment(segment)

    tip_airfoil                           =  SUAVE.Components.Airfoils.Airfoil()
    tip_airfoil.coordinate_file           = 'Airfoils/B737c.txt'
    segment                               = SUAVE.Components.Wings.Segment()
    segment.tag                           = 'Tip'
    segment.percent_span_location         = 1.
    segment.twist                         = 0. * Units.degrees
    segment.root_chord_percent            = wing.taper
    segment.dihedral_outboard             = 0. * Units.degrees
    segment.sweeps.quarter_chord          = 0.
    segment.thickness_to_chord            = 0.9 * iteration_setup.sizing_iter.thickness_to_chord
    segment.append_airfoil(tip_airfoil)
    wing.append_segment(segment)

    # control surfaces -------------------------------------------
    slat                          = SUAVE.Components.Wings.Control_Surfaces.Slat()
    slat.tag                      = 'slat'
    slat.span_fraction_start      = 4.042 / 35.035
    slat.span_fraction_end        = 33.624 / 35.035
    slat.deflection               = 0.0 * Units.degrees
    slat.chord_fraction           = 750 / 5800
    wing.append_control_surface(slat)

    flap                          = SUAVE.Components.Wings.Control_Surfaces.Flap()
    flap.tag                      = 'flap'
    flap.span_fraction_start      = 2.777 / 35.035
    flap.span_fraction_end        = 22.493 / 35.035
    flap.deflection               = 0.0 * Units.degrees
    flap.configuration_type       = 'single_slotted'
    flap.chord_fraction           = 0.30
    wing.append_control_surface(flap)

    aileron                       = SUAVE.Components.Wings.Control_Surfaces.Aileron()
    aileron.tag                   = 'aileron'
    aileron.span_fraction_start   = 22.993 / 35.035
    aileron.span_fraction_end     = 33.024 / 35.035
    aileron.deflection            = 0.0 * Units.degrees
    aileron.chord_fraction        = 0.30
    wing.append_control_surface(aileron)

    # Fill out more segment properties automatically
    create_tapered_wing(wing, iteration_setup.sizing_iter.aspect_ratio, wing.areas.reference)
    wing_segmented_planform(wing, True)

    # add to vehicle
    vehicle.append_component(wing)
    # ------------------------------------------------------------------
    #  V-Tail
    # ------------------------------------------------------------------

    wing = SUAVE.Components.Wings.Horizontal_Tail()
    wing.tag = 'horizontal_stabilizer'

    wing.aspect_ratio            = 5.27
    wing.sweeps.quarter_chord    = 30. * Units.deg
    wing.thickness_to_chord      = 0.088
    wing.taper                   = 0.378

    wing.origin                  = [[55.337, 0, 2.082]]
    wing.aerodynamic_center      = [1,0,0]

    wing.transition_x_upper = 0.14
    wing.transition_x_lower = 0.14

    wing.vertical                = False
    wing.symmetric               = True

    wing.dynamic_pressure_ratio  = 0.9

    # Tailplane sizing
    deltaaerocenterhtp = 2
    c_ht = 0.483 * 2 #0.483
    c_vt = 0.035 * 2#0.035
    while abs(deltaaerocenterhtp) > 1e-10:
        oldaerocenter = wing.aerodynamic_center[0]

        l_ht = wing.origin[0][0] + wing.aerodynamic_center[0] - (vehicle.wings.main_wing.origin[0][0] +
                                                                 vehicle.wings.main_wing.aerodynamic_center[0])

        req_area_proj_x_y = vehicle.wings.main_wing.chords.mean_aerodynamic \
                            * vehicle.wings.main_wing.areas.reference \
                            * c_ht \
                            / l_ht
        req_area_proj_x_z = vehicle.wings.main_wing.spans.projected \
                            * vehicle.wings.main_wing.areas.reference \
                            * c_vt \
                            / l_ht

        #wing.areas.reference = (req_area_proj_x_y**2 + req_area_proj_x_z**2)**0.5
        wing.areas.reference = req_area_proj_x_y + req_area_proj_x_z
        wing.dihedral = np.arctan((req_area_proj_x_z / req_area_proj_x_y)**0.5)

        wing = wing_planform_v_tail(wing)

        newaerocenter = wing.aerodynamic_center[0]
        deltaaerocenterhtp = oldaerocenter - newaerocenter

    # Fill out more segment properties automatically
    # wing = wing_segmented_planform(wing)

    # control surfaces -------------------------------------------
    elevator                       = SUAVE.Components.Wings.Control_Surfaces.Elevator()
    elevator.tag                   = 'elevator'
    elevator.span_fraction_start   = 0.12
    elevator.span_fraction_end     = 0.92
    elevator.deflection            = 0.0  * Units.deg
    elevator.chord_fraction        = 0.3
    wing.append_control_surface(elevator)

    # add to vehicle
    vehicle.append_component(wing)
    # ------------------------------------------------------------------
    #  Fuselage
    # ------------------------------------------------------------------

    fuselage = SUAVE.Components.Fuselages.Fuselage()
    fuselage.tag = 'fuselage'

    fuselage.number_coach_seats    = vehicle.passengers
    fuselage.seats_abreast         = 6
    fuselage.seat_pitch            = 31. * Units.inches
    fuselage.fineness.nose         = 9.502 / 5.82
    fuselage.fineness.tail         = 18.7 / 5.82

    fuselage.lengths.nose          = 8.1
    fuselage.lengths.tail          = 17
    fuselage.lengths.cabin         = 36.
    fuselage.lengths.total         = fuselage.lengths.nose + fuselage.lengths.tail + fuselage.lengths.cabin
    #fuselage.lengths.fore_space    = 6.
    #fuselage.lengths.aft_space     = 5.

    fuselage.width                 = 5.64

    fuselage.heights.maximum       = 5.64
    fuselage.heights.at_quarter_length          = 0.95*fuselage.heights.maximum
    fuselage.heights.at_three_quarters_length   = 0.9*fuselage.heights.maximum
    fuselage.heights.at_wing_root_quarter_chord = fuselage.heights.maximum

    fuselage.areas.side_projected  = fuselage.heights.maximum * fuselage.lengths.total * 0.7
    fuselage.areas.wetted          = np.pi * (fuselage.width+fuselage.heights.maximum)/2 * fuselage.lengths.total * 0.7
    fuselage.areas.front_projected = np.pi * ((fuselage.width+fuselage.heights.maximum)/2)**2 / 4

    fuselage.effective_diameter    = (fuselage.width+fuselage.heights.maximum)/2

    fuselage.differential_pressure = 6.3e4 * Units.pascal # Maximum differential pressure

    # Segment
    segment                                     = SUAVE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_0'
    segment.percent_x_location                  = 0.0000
    segment.percent_z_location                  = -0.00144
    segment.height                              = 0.0100 * fuselage.heights.maximum / 3.74
    segment.width                               = 0.0100 * fuselage.width / 3.74
    fuselage.Segments.append(segment)

    # Segment
    segment                                     = SUAVE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_1'
    segment.percent_x_location                  = 0.00576
    segment.percent_z_location                  = -0.00144
    segment.height                              = 0.7500 * fuselage.heights.maximum / 3.74
    segment.width                               = 0.6500 * fuselage.width / 3.74
    fuselage.Segments.append(segment)

    # Segment
    segment                                     = SUAVE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_2'
    segment.percent_x_location                  = 0.02017
    segment.percent_z_location                  = 0.00000
    segment.height                              = 1.52783 * fuselage.heights.maximum / 3.74
    segment.width                               = 1.20043 * fuselage.width / 3.74
    fuselage.Segments.append(segment)

    # Segment
    segment                                     = SUAVE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_3'
    segment.percent_x_location                  = 0.03170
    segment.percent_z_location                  = 0.00000
    segment.height                              = 1.96435 * fuselage.heights.maximum / 3.74
    segment.width                               = 1.52783 * fuselage.width / 3.74
    fuselage.Segments.append(segment)

    # Segment
    segment                                     = SUAVE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_4'
    segment.percent_x_location                  = 0.04899
    segment.percent_z_location                  = 0.00431
    segment.height                              = 2.72826 * fuselage.heights.maximum / 3.74
    segment.width                               = 1.96435 * fuselage.width / 3.74
    fuselage.Segments.append(segment)

    # Segment
    segment                                     = SUAVE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_5'
    segment.percent_x_location                  = 0.07781
    segment.percent_z_location                  = 0.00861
    segment.height                              = 3.49217 * fuselage.heights.maximum / 3.74
    segment.width                               = 2.61913 * fuselage.width / 3.74
    fuselage.Segments.append(segment)

    # Segment
    segment                                     = SUAVE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_6'
    segment.percent_x_location                  = 0.10375
    segment.percent_z_location                  = 0.01005
    segment.height                              = 3.70130 * fuselage.heights.maximum / 3.74
    segment.width                               = 3.05565 * fuselage.width / 3.74
    fuselage.Segments.append(segment)

    # Segment
    segment                                     = SUAVE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_7'
    segment.percent_x_location                  = 0.16427
    segment.percent_z_location                  = 0.01148
    segment.height                              = 3.92870 * fuselage.heights.maximum / 3.74
    segment.width                               = 3.71043 * fuselage.width / 3.74
    fuselage.Segments.append(segment)

    # Segment
    segment                                     = SUAVE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_8'
    segment.percent_x_location                  = 0.22478
    segment.percent_z_location                  = 0.01148
    segment.height                              = 3.92870 * fuselage.heights.maximum / 3.74
    segment.width                               = 3.92870 * fuselage.width / 3.74
    fuselage.Segments.append(segment)

    # Segment
    segment                                     = SUAVE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_9'
    segment.percent_x_location                  = 0.69164
    segment.percent_z_location                  = 0.01292
    segment.height                              = 3.81957 * fuselage.heights.maximum / 3.74
    segment.width                               = 3.81957 * fuselage.width / 3.74
    fuselage.Segments.append(segment)

    # Segment
    segment                                     = SUAVE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_10'
    segment.percent_x_location                  = 0.71758
    segment.percent_z_location                  = 0.01292
    segment.height                              = 3.81957 * fuselage.heights.maximum / 3.74
    segment.width                               = 3.81957 * fuselage.width / 3.74
    fuselage.Segments.append(segment)

    # Segment
    segment                                     = SUAVE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_11'
    segment.percent_x_location                  = 0.78098
    segment.percent_z_location                  = 0.01722
    segment.height                              = 3.49217 * fuselage.heights.maximum / 3.74
    segment.width                               = 3.71043 * fuselage.width / 3.74
    fuselage.Segments.append(segment)

    # Segment
    segment                                     = SUAVE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_12'
    segment.percent_x_location                  = 0.85303
    segment.percent_z_location                  = 0.02296
    segment.height                              = 3.05565 * fuselage.heights.maximum / 3.74
    segment.width                               = 3.16478 * fuselage.width / 3.74
    fuselage.Segments.append(segment)

    # Segment
    segment                                     = SUAVE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_13'
    segment.percent_x_location                  = 0.91931
    segment.percent_z_location                  = 0.03157
    segment.height                              = 2.40087 * fuselage.heights.maximum / 3.74
    segment.width                               = 1.96435 * fuselage.width / 3.74
    fuselage.Segments.append(segment)

    # Segment
    segment                                     = SUAVE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_14'
    segment.percent_x_location                  = 1.00
    segment.percent_z_location                  = 0.04593
    segment.height                              = 1.09130 * fuselage.heights.maximum / 3.74
    segment.width                               = 0.21826 * fuselage.width / 3.74
    fuselage.Segments.append(segment)

    # add to vehicle
    vehicle.append_component(fuselage)

    # ------------------------------------------------------------------
    #   Propulsor
    # ------------------------------------------------------------------

    propulsor = SUAVE.Components.Energy.Networks.Turbofan_Raymer()
    propulsor.tag = 'turbofan'

    # setup
    # # This origin is overwritten by compute_component_centers_of_gravity(base,compute_propulsor_origin=True)
    propulsor.origin            = [[19., 8., -1.5],[19., -8, -1.5]]
    propulsor.number_of_engines = 2

    thrust_loading = max(iteration_setup.sizing_iter.thrust_loading, propulsor.get_thrust_loading_requirement_toc(
        iteration_setup.mission_iter.design_cruise_altitude, iteration_setup.mission_iter.design_cruise_mach,
        m4_m0=0.99, LoD_initial_cruise_altitude=26,
    ))

    sea_level_static_thrust = thrust_loading * vehicle.mass_properties.max_takeoff * 9.81
    propulsor.engine_length = 7.4 * (sea_level_static_thrust / 622720)**0.5
    bucket_sfc = 0.475
    propulsor.scale_factors(iteration_setup.mission_iter.design_cruise_altitude,
                            iteration_setup.mission_iter.design_cruise_mach,
                            sea_level_static_thrust,
                            iteration_setup.mission_iter.throttle_mid_cruise,
                            bucket_sfc=bucket_sfc)

    vehicle.append_component(propulsor)

    # ------------------------------------------------------------------
    #   Nacelles
    # ------------------------------------------------------------------
    nacelle = SUAVE.Components.Nacelles.Nacelle()
    nacelle.tag = 'nacelle_1'

    nacelle.length = 7.2 * (sea_level_static_thrust / 622720)**0.5
    nacelle.inlet_diameter = 3.6 * (sea_level_static_thrust / 622720)**0.5
    nacelle.diameter = 3.8 * (sea_level_static_thrust / 622720)**0.5
    nacelle.areas.wetted = 1.1 * np.pi * nacelle.diameter * nacelle.length
    nacelle.origin = [[19., 8., -1.5]]
    nacelle.flow_through = True
    nacelle.Airfoil.NACA_4_series_flag = True
    nacelle.Airfoil.coordinate_file = '2410'
    nacelle_2 = deepcopy(nacelle)
    nacelle_2.tag = 'nacelle_2'
    nacelle_2.origin = [[19., -8, -1.5]]
    #
    vehicle.append_component(nacelle)
    vehicle.append_component(nacelle_2)

    # ------------------------------------------------------------------
    #  Fuel
    # ------------------------------------------------------------------
    fuel                                  = SUAVE.Components.Physical_Component()
    vehicle.fuel                          = fuel
    fuel.mass_properties.mass             = vehicle.mass_properties.max_takeoff-vehicle.mass_properties.max_zero_fuel
    fuel.origin                           = vehicle.wings.main_wing.origin
    fuel.mass_properties.center_of_gravity= vehicle.wings.main_wing.aerodynamic_center

    # ------------------------------------------------------------------
    #  Landing Gear
    # ------------------------------------------------------------------
    landing_gear                          = SUAVE.Components.Landing_Gear.Landing_Gear()
    landing_gear.tag                      = "main_landing_gear"
    landing_gear.main_tire_diameter       = 1.12000 * Units.m
    landing_gear.nose_tire_diameter       = 0.6858 * Units.m
    landing_gear.main_strut_length        = 3.9 * Units.m       # TODO abhängigkeit modellieren
    landing_gear.nose_strut_length        = 2.4 * Units.m       # TODO abhängigkeit modellieren
    landing_gear.main_units               = 2    #number of main landing gear
    landing_gear.nose_units               = 1    #number of nose landing gear
    landing_gear.main_wheels              = 4 * landing_gear.main_units    #number of wheels on the main landing gear
    landing_gear.nose_wheels              = 2    #number of wheels on the nose landing gear
    vehicle.landing_gear                  = landing_gear

    # ------------------------------------------------------------------
    #   Vehicle Definition Complete
    # ------------------------------------------------------------------

    return vehicle


# ----------------------------------------------------------------------
#   Define the Configurations
# ---------------------------------------------------------------------

def configs_setup(vehicle):

    # ------------------------------------------------------------------
    #   Initialize Configurations
    # ------------------------------------------------------------------
    configs = SUAVE.Components.Configs.Config.Container()

    base_config = SUAVE.Components.Configs.Config(vehicle)
    base_config.tag = 'base'
    base_config.landing_gear.gear_condition                               = 'up'
    configs.append(base_config)

    # ------------------------------------------------------------------
    #   Cruise Configuration
    # ------------------------------------------------------------------
    config = SUAVE.Components.Configs.Config(base_config)
    config.tag = 'cruise' 
    configs.append(config)
    config.wings['main_wing'].control_surfaces.flap.deflection       = 0. * Units.deg
    config.wings['main_wing'].control_surfaces.slat.deflection       = 0. * Units.deg

    # ------------------------------------------------------------------
    #   Takeoff Configuration
    # ------------------------------------------------------------------
    config = SUAVE.Components.Configs.Config(base_config)
    config.tag                                                       = 'takeoff'
    config.wings['main_wing'].control_surfaces.flap.deflection       = 20. * Units.deg
    config.wings['main_wing'].control_surfaces.slat.deflection       = 25. * Units.deg

    configs.append(config)

    # ------------------------------------------------------------------
    #   Landing Configuration
    # ------------------------------------------------------------------

    config = SUAVE.Components.Configs.Config(base_config)
    config.tag = 'landing'

    config.wings['main_wing'].control_surfaces.flap.deflection       = 30. * Units.deg
    config.wings['main_wing'].control_surfaces.slat.deflection       = 25. * Units.deg  

    configs.append(config)

    return configs
