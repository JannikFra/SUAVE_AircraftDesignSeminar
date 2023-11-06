# vehicle_setup.py
#
# Created:  Nov 2023, J. Frank
# Modified:

""" Setup File for the Aircraft Design Seminar 2023/24 Reference Aircraft
"""


# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------

import numpy as np
import SUAVE
from SUAVE.Core import Units
from SUAVE.Methods.Propulsion.turbofan_sizing import turbofan_sizing
from SUAVE.Methods.Geometry.Two_Dimensional.Planform import wing_segmented_planform

from copy import deepcopy 

# ----------------------------------------------------------------------
#   Define the Vehicle
# ----------------------------------------------------------------------

def vehicle_setup():

    # ------------------------------------------------------------------
    #   Initialize the Vehicle
    # ------------------------------------------------------------------

    vehicle = SUAVE.Vehicle()
    vehicle.tag = 'Reference_Aircraft'

    # ------------------------------------------------------------------
    #   Vehicle-level Properties
    # ------------------------------------------------------------------

    # mass properties
    vehicle.mass_properties.max_takeoff               = 79015.8   # kg
    vehicle.mass_properties.takeoff                   = 79015.8   # kg
    vehicle.mass_properties.operating_empty           = 62746.4   # kg
    vehicle.mass_properties.takeoff                   = 79015.8   # kg
    vehicle.mass_properties.max_zero_fuel             = 62732.0   # kg
    vehicle.mass_properties.cargo                     = 10000.  * Units.kilogram
    vehicle.mass_properties.center_of_gravity         = [[ 15.30987849,   0.        ,  -0.48023939]]
    vehicle.mass_properties.moments_of_inertia.tensor = [[3173074.17, 0 , 28752.77565],[0 , 3019041.443, 0],[0, 0, 5730017.433]] # estimated, not correct
    vehicle.design_mach_number                        = 0.78
    vehicle.design_range                              = 3582 * Units.miles
    vehicle.design_cruise_alt                         = 35000.0 * Units.ft

    # envelope properties
    vehicle.envelope.ultimate_load = 3.75
    vehicle.envelope.limit_load    = 1.5

    # basic parameters
    vehicle.reference_area         = 124.862
    vehicle.passengers             = 170
    vehicle.systems.control        = "fully powered"
    vehicle.systems.accessories    = "medium range"
  
    # ------------------------------------------------------------------
    #   Main Wing
    # ------------------------------------------------------------------

    wing = SUAVE.Components.Wings.Main_Wing()
    wing.tag = 'main_wing'

    wing.aspect_ratio            = 10.18
    wing.sweeps.quarter_chord    = 25 * Units.deg
    wing.thickness_to_chord      = 0.1
    wing.taper                   = 0.1

    wing.spans.projected         = 34.32

    wing.chords.root             = 7.760 * Units.meter
    wing.chords.tip              = 0.782 * Units.meter
    wing.chords.mean_aerodynamic = 4.235 * Units.meter

    wing.areas.reference         = 124.862
    wing.areas.wetted            = 225.08
    
    wing.twists.root             = 4.0 * Units.degrees
    wing.twists.tip              = 0.0 * Units.degrees

    wing.origin                  = [[13.61,0,-0.93]]
    wing.aerodynamic_center      = [0,0,0]   

    wing.vertical                = False
    wing.symmetric               = True
    wing.high_lift               = True

    wing.dynamic_pressure_ratio  = 1.0


    # Wing Segments
    root_airfoil                          = SUAVE.Components.Airfoils.Airfoil()
    root_airfoil.coordinate_file          = 'Airfoils/B737a.txt'
    segment                               = SUAVE.Components.Wings.Segment()
    segment.tag                           = 'Root'
    segment.percent_span_location         = 0.0
    segment.twist                         = 4. * Units.deg
    segment.root_chord_percent            = 1.
    segment.thickness_to_chord            = 0.1
    segment.dihedral_outboard             = 2.5 * Units.degrees
    segment.sweeps.quarter_chord          = 28.225 * Units.degrees
    segment.thickness_to_chord            = .1
    segment.append_airfoil(root_airfoil)
    wing.append_segment(segment)

    yehudi_airfoil                        = SUAVE.Components.Airfoils.Airfoil()
    yehudi_airfoil.coordinate_file        = 'Airfoils/B737b.txt'
    segment                               = SUAVE.Components.Wings.Segment()
    segment.tag                           = 'Yehudi'
    segment.percent_span_location         = 0.324
    segment.twist                         = 0.047193 * Units.deg
    segment.root_chord_percent            = 0.5
    segment.thickness_to_chord            = 0.1
    segment.dihedral_outboard             = 5.5 * Units.degrees
    segment.sweeps.quarter_chord          = 25. * Units.degrees
    segment.thickness_to_chord            = .1
    segment.append_airfoil(yehudi_airfoil)
    wing.append_segment(segment)

    mid_airfoil                           = SUAVE.Components.Airfoils.Airfoil()
    mid_airfoil.coordinate_file           = 'Airfoils/B737c.txt'
    segment                               = SUAVE.Components.Wings.Segment()
    segment.tag                           = 'Section_2'
    segment.percent_span_location         = 0.963
    segment.twist                         = 0.00258 * Units.deg
    segment.root_chord_percent            = 0.220
    segment.thickness_to_chord            = 0.1
    segment.dihedral_outboard             = 5.5 * Units.degrees
    segment.sweeps.quarter_chord          = 56.75 * Units.degrees
    segment.thickness_to_chord            = .1
    segment.append_airfoil(mid_airfoil)
    wing.append_segment(segment)

    tip_airfoil                           =  SUAVE.Components.Airfoils.Airfoil()
    tip_airfoil.coordinate_file           = 'Airfoils/B737d.txt'
    segment                               = SUAVE.Components.Wings.Segment()
    segment.tag                           = 'Tip'
    segment.percent_span_location         = 1.
    segment.twist                         = 0. * Units.degrees
    segment.root_chord_percent            = 0.10077
    segment.thickness_to_chord            = 0.1
    segment.dihedral_outboard             = 0.
    segment.sweeps.quarter_chord          = 0.
    segment.thickness_to_chord            = .1
    segment.append_airfoil(tip_airfoil)
    wing.append_segment(segment)
    
    # Fill out more segment properties automatically
    wing = wing_segmented_planform(wing)    

    # control surfaces -------------------------------------------
    slat                          = SUAVE.Components.Wings.Control_Surfaces.Slat()
    slat.tag                      = 'slat'
    slat.span_fraction_start      = 0.2
    slat.span_fraction_end        = 0.963
    slat.deflection               = 0.0 * Units.degrees
    slat.chord_fraction           = 0.075
    wing.append_control_surface(slat)

    flap                          = SUAVE.Components.Wings.Control_Surfaces.Flap()
    flap.tag                      = 'flap'
    flap.span_fraction_start      = 0.2
    flap.span_fraction_end        = 0.7
    flap.deflection               = 0.0 * Units.degrees
    flap.configuration_type       = 'double_slotted'
    flap.chord_fraction           = 0.30
    wing.append_control_surface(flap)

    aileron                       = SUAVE.Components.Wings.Control_Surfaces.Aileron()
    aileron.tag                   = 'aileron'
    aileron.span_fraction_start   = 0.7
    aileron.span_fraction_end     = 0.963
    aileron.deflection            = 0.0 * Units.degrees
    aileron.chord_fraction        = 0.16
    wing.append_control_surface(aileron)
    


    # add to vehicle
    vehicle.append_component(wing)


    # ------------------------------------------------------------------
    #  Horizontal Stabilizer
    # ------------------------------------------------------------------

    wing = SUAVE.Components.Wings.Horizontal_Tail()
    wing.tag = 'horizontal_stabilizer'

    wing.aspect_ratio            = 4.99
    wing.sweeps.quarter_chord    = 28.2250 * Units.deg  
    wing.thickness_to_chord      = 0.08
    wing.taper                   = 0.3333 

    wing.spans.projected         = 14.4

    wing.chords.root             = 4.2731 
    wing.chords.tip              = 1.4243 
    wing.chords.mean_aerodynamic = 8.0

    wing.areas.reference         = 41.49
    wing.areas.exposed           = 59.354    # Exposed area of the horizontal tail
    wing.areas.wetted            = 71.81     # Wetted area of the horizontal tail
    wing.twists.root             = 3.0 * Units.degrees
    wing.twists.tip              = 3.0 * Units.degrees

    wing.origin                  = [[33.02,0,1.466]]
    wing.aerodynamic_center      = [0,0,0]

    wing.vertical                = False
    wing.symmetric               = True

    wing.dynamic_pressure_ratio  = 0.9


    # Wing Segments
    segment                        = SUAVE.Components.Wings.Segment()
    segment.tag                    = 'root_segment'
    segment.percent_span_location  = 0.0
    segment.twist                  = 0. * Units.deg
    segment.root_chord_percent     = 1.0
    segment.dihedral_outboard      = 8.63 * Units.degrees
    segment.sweeps.quarter_chord   = 28.2250  * Units.degrees 
    segment.thickness_to_chord     = .1
    wing.append_segment(segment)

    segment                        = SUAVE.Components.Wings.Segment()
    segment.tag                    = 'tip_segment'
    segment.percent_span_location  = 1.
    segment.twist                  = 0. * Units.deg
    segment.root_chord_percent     = 0.3333               
    segment.dihedral_outboard      = 0 * Units.degrees
    segment.sweeps.quarter_chord   = 0 * Units.degrees  
    segment.thickness_to_chord     = .1
    wing.append_segment(segment)
    
    # Fill out more segment properties automatically
    wing = wing_segmented_planform(wing)        

    # control surfaces -------------------------------------------
    elevator                       = SUAVE.Components.Wings.Control_Surfaces.Elevator()
    elevator.tag                   = 'elevator'
    elevator.span_fraction_start   = 0.09
    elevator.span_fraction_end     = 0.92
    elevator.deflection            = 0.0  * Units.deg
    elevator.chord_fraction        = 0.3
    wing.append_control_surface(elevator)

    # add to vehicle
    vehicle.append_component(wing)


    # ------------------------------------------------------------------
    #   Vertical Stabilizer
    # ------------------------------------------------------------------

    wing = SUAVE.Components.Wings.Vertical_Tail()
    wing.tag = 'vertical_stabilizer'

    wing.aspect_ratio            = 1.98865
    wing.sweeps.quarter_chord    = 31.2  * Units.deg   
    wing.thickness_to_chord      = 0.08
    wing.taper                   = 0.1183

    wing.spans.projected         = 8.33
    wing.total_length            = wing.spans.projected 
    
    wing.chords.root             = 10.1 
    wing.chords.tip              = 1.20 
    wing.chords.mean_aerodynamic = 4.0

    wing.areas.reference         = 34.89
    wing.areas.wetted            = 57.25 
    
    wing.twists.root             = 0.0 * Units.degrees
    wing.twists.tip              = 0.0 * Units.degrees

    wing.origin                  = [[26.944,0,1.54]]
    wing.aerodynamic_center      = [0,0,0]

    wing.vertical                = True
    wing.symmetric               = False
    wing.t_tail                  = False

    wing.dynamic_pressure_ratio  = 1.0


    # Wing Segments
    segment                               = SUAVE.Components.Wings.Segment()
    segment.tag                           = 'root'
    segment.percent_span_location         = 0.0
    segment.twist                         = 0. * Units.deg
    segment.root_chord_percent            = 1.
    segment.dihedral_outboard             = 0 * Units.degrees
    segment.sweeps.quarter_chord          = 61.485 * Units.degrees  
    segment.thickness_to_chord            = .1
    wing.append_segment(segment)

    segment                               = SUAVE.Components.Wings.Segment()
    segment.tag                           = 'segment_1'
    segment.percent_span_location         = 0.2962
    segment.twist                         = 0. * Units.deg
    segment.root_chord_percent            = 0.45
    segment.dihedral_outboard             = 0. * Units.degrees
    segment.sweeps.quarter_chord          = 31.2 * Units.degrees   
    segment.thickness_to_chord            = .1
    wing.append_segment(segment)

    segment                               = SUAVE.Components.Wings.Segment()
    segment.tag                           = 'segment_2'
    segment.percent_span_location         = 1.0
    segment.twist                         = 0. * Units.deg
    segment.root_chord_percent            = 0.1183 
    segment.dihedral_outboard             = 0.0 * Units.degrees
    segment.sweeps.quarter_chord          = 0.0    
    segment.thickness_to_chord            = .1  
    wing.append_segment(segment)
    
    # Fill out more segment properties automatically
    wing = wing_segmented_planform(wing)        

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
    fuselage.fineness.nose         = 1.6
    fuselage.fineness.tail         = 2.

    fuselage.lengths.nose          = 6.4
    fuselage.lengths.tail          = 8.0
    fuselage.lengths.cabin         = 28.85
    fuselage.lengths.total         = 38.02
    fuselage.lengths.fore_space    = 6.
    fuselage.lengths.aft_space     = 5.

    fuselage.width                 = 3.74

    fuselage.heights.maximum       = 3.74
    fuselage.heights.at_quarter_length          = 3.74
    fuselage.heights.at_three_quarters_length   = 3.65
    fuselage.heights.at_wing_root_quarter_chord = 3.74

    fuselage.areas.side_projected  = 142.1948
    fuselage.areas.wetted          = 385.51
    fuselage.areas.front_projected = 12.57

    fuselage.effective_diameter    = 3.74

    fuselage.differential_pressure = 5.0e4 * Units.pascal # Maximum differential pressure

    # Segment
    segment                                     = SUAVE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_0'
    segment.percent_x_location                  = 0.0000
    segment.percent_z_location                  = -0.00144
    segment.height                              = 0.0100
    segment.width                               = 0.0100
    fuselage.Segments.append(segment)

    # Segment
    segment                                     = SUAVE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_1'
    segment.percent_x_location                  = 0.00576
    segment.percent_z_location                  = -0.00144
    segment.height                              = 0.7500
    segment.width                               = 0.6500
    fuselage.Segments.append(segment)

    # Segment
    segment                                     = SUAVE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_2'
    segment.percent_x_location                  = 0.02017
    segment.percent_z_location                  = 0.00000
    segment.height                              = 1.52783
    segment.width                               = 1.20043
    fuselage.Segments.append(segment)

    # Segment
    segment                                     = SUAVE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_3'
    segment.percent_x_location                  = 0.03170
    segment.percent_z_location                  = 0.00000
    segment.height                              = 1.96435
    segment.width                               = 1.52783
    fuselage.Segments.append(segment)

    # Segment
    segment                                     = SUAVE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_4'
    segment.percent_x_location                  = 0.04899
    segment.percent_z_location                  = 0.00431
    segment.height                              = 2.72826
    segment.width                               = 1.96435
    fuselage.Segments.append(segment)

    # Segment
    segment                                     = SUAVE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_5'
    segment.percent_x_location                  = 0.07781
    segment.percent_z_location                  = 0.00861
    segment.height                              = 3.49217
    segment.width                               = 2.61913
    fuselage.Segments.append(segment)

    # Segment
    segment                                     = SUAVE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_6'
    segment.percent_x_location                  = 0.10375
    segment.percent_z_location                  = 0.01005
    segment.height                              = 3.70130
    segment.width                               = 3.05565
    fuselage.Segments.append(segment)

    # Segment
    segment                                     = SUAVE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_7'
    segment.percent_x_location                  = 0.16427
    segment.percent_z_location                  = 0.01148
    segment.height                              = 3.92870
    segment.width                               = 3.71043
    fuselage.Segments.append(segment)

    # Segment
    segment                                     = SUAVE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_8'
    segment.percent_x_location                  = 0.22478
    segment.percent_z_location                  = 0.01148
    segment.height                              = 3.92870
    segment.width                               = 3.92870
    fuselage.Segments.append(segment)

    # Segment
    segment                                     = SUAVE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_9'
    segment.percent_x_location                  = 0.69164
    segment.percent_z_location                  = 0.01292
    segment.height                              = 3.81957
    segment.width                               = 3.81957
    fuselage.Segments.append(segment)

    # Segment
    segment                                     = SUAVE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_10'
    segment.percent_x_location                  = 0.71758
    segment.percent_z_location                  = 0.01292
    segment.height                              = 3.81957
    segment.width                               = 3.81957
    fuselage.Segments.append(segment)

    # Segment
    segment                                     = SUAVE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_11'
    segment.percent_x_location                  = 0.78098
    segment.percent_z_location                  = 0.01722
    segment.height                              = 3.49217
    segment.width                               = 3.71043
    fuselage.Segments.append(segment)

    # Segment
    segment                                     = SUAVE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_12'
    segment.percent_x_location                  = 0.85303
    segment.percent_z_location                  = 0.02296
    segment.height                              = 3.05565
    segment.width                               = 3.16478
    fuselage.Segments.append(segment)

    # Segment
    segment                                     = SUAVE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_13'
    segment.percent_x_location                  = 0.91931
    segment.percent_z_location                  = 0.03157
    segment.height                              = 2.40087
    segment.width                               = 1.96435
    fuselage.Segments.append(segment)

    # Segment
    segment                                     = SUAVE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_14'
    segment.percent_x_location                  = 1.00
    segment.percent_z_location                  = 0.04593
    segment.height                              = 1.09130
    segment.width                               = 0.21826
    fuselage.Segments.append(segment)

    # add to vehicle
    vehicle.append_component(fuselage)
    
    # ------------------------------------------------------------------
    #   Nacelles
    # ------------------------------------------------------------------ 
    # nacelle                            = SUAVE.Components.Nacelles.Nacelle()
    # nacelle.tag                        = 'nacelle_1'
    # nacelle.length                     = 2.71
    # nacelle.inlet_diameter             = 1.90
    # nacelle.diameter                   = 2.05
    # nacelle.areas.wetted               = 1.1*np.pi*nacelle.diameter*nacelle.length
    # nacelle.origin                     = [[13.72, -4.86,-1.9]]
    # nacelle.flow_through               = True
    # nacelle.Airfoil.NACA_4_series_flag = True
    # nacelle.Airfoil.coordinate_file    = '2410'
    # nacelle_2                          = deepcopy(nacelle)
    # nacelle_2.tag                      = 'nacelle_2'
    # nacelle_2.origin                   = [[13.72, 4.86,-1.9]]
    #
    # vehicle.append_component(nacelle)
    # vehicle.append_component(nacelle_2)

    # ------------------------------------------------------------------
    #   Propulsor
    # ------------------------------------------------------------------

    propulsor = SUAVE.Components.Energy.Networks.Simple_Propulsor()
    propulsor.tag = 'turbofan'

    # setup
    # # This origin is overwritten by compute_component_centers_of_gravity(base,compute_propulsor_origin=True)
    propulsor.origin            = [[13.72, 4.86,-1.9],[13.72, -4.86,-1.9]]
    propulsor.engine_length = 2.
    propulsor.number_of_engines = 2
    propulsor.max_thrust = 400e3
    propulsor.fuel_flow = 1.

    vehicle.append_component(propulsor)

    # ------------------------------------------------------------------
    #  Fuel
    # ------------------------------------------------------------------
    fuel                                  = SUAVE.Components.Physical_Component()
    vehicle.fuel                          = fuel
    fuel.mass_properties.mass             = vehicle.mass_properties.max_takeoff-vehicle.mass_properties.max_fuel
    fuel.origin                           = vehicle.wings.main_wing.mass_properties.center_of_gravity
    fuel.mass_properties.center_of_gravity= vehicle.wings.main_wing.aerodynamic_center

    # ------------------------------------------------------------------
    #  Landing Gear
    # ------------------------------------------------------------------
    landing_gear                          = SUAVE.Components.Landing_Gear.Landing_Gear()
    landing_gear.tag                      = "main_landing_gear"
    landing_gear.main_tire_diameter       = 1.12000 * Units.m
    landing_gear.nose_tire_diameter       = 0.6858 * Units.m
    landing_gear.main_strut_length        = 1.8 * Units.m
    landing_gear.nose_strut_length        = 1.3 * Units.m
    landing_gear.main_units               = 1    #number of nose landing gear
    landing_gear.nose_units               = 1    #number of nose landing gear
    landing_gear.main_wheels              = 2    #number of wheels on the main landing gear
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
