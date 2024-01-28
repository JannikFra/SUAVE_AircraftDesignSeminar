## @ingroup Methods-Performance
# payload_range.py
#
# Created:  Apr 2014, T. Orra
# Modified: Jan 2016, E. Botero

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

from SUAVE.Core import Units
import time
import numpy as np

# ----------------------------------------------------------------------
#  Calculate vehicle Payload Range Diagram
# ----------------------------------------------------------------------

## @ingroup Methods-Performance
def payload_range_multiple_cruise(vehicle,mission,num_cruise_seg=4,reserves=0.):
    """Calculates a vehicle's payload range diagram. Includes plotting.

    Assumptions:
    Constant altitude cruise

    Source:
    N/A

    Inputs:
    vehicle.mass_properties.
      operating_empty                     [kg]
      max_zero_fuel                       [kg]
      max_takeoff                         [kg]
      max_payload                         [kg]
      max_fuel                            [kg]
      takeoff                             [kg]
    mission.segments[0].analyses.weights.
      vehicle.mass_properties.takeoff     [kg]
    cruise_segment_tag                    <string>

    Outputs:
    payload_range.
      range                             [m]
      payload                           [kg]
      fuel                              [kg]
      takeoff_weight                    [kg]
    PayloadRangeDiagram.dat (text file)

    Properties Used:
    N/A
    """        
    # elapsed time start
    start_time = time.time()

    # Flags for printing results in command line, write output file, and plot
    iprint = 1      # Flag for print output data in the prompt line
    iwrite = 1      # Flag for write an output file
    iplot  = 1      # Flag for plot payload range diagram
    ### could be an user input.
    ##      output_type: 1: Print only              (light)
    ##      output_type: 2: Print + Write           (medium)
    ##      output_type: 3: Print + Write + Plot    (complete)



    #unpack
    masses = vehicle.mass_properties
    if not masses.operating_empty:
        print("Error calculating Payload Range Diagram: Vehicle Operating Empty not defined")
        return True
    else:
        OEW = masses.operating_empty

    if not masses.max_zero_fuel:
        print("Error calculating Payload Range Diagram: Vehicle MZFW not defined")
        return True
    else:
        MZFW = vehicle.mass_properties.max_zero_fuel

    if not masses.max_takeoff:
        print("Error calculating Payload Range Diagram: Vehicle MTOW not defined")
        return True
    else:
        MTOW = vehicle.mass_properties.max_takeoff

    if not masses.max_payload:
        MaxPLD = MZFW - OEW  # If payload max not defined, calculate based in design weights
    else:
        MaxPLD = vehicle.mass_properties.max_payload
        MaxPLD = min(MaxPLD , MZFW - OEW) #limit in structural capability

    if not masses.max_fuel:
        MaxFuel = MTOW - OEW # If not defined, calculate based in design weights
    else:
        MaxFuel = vehicle.mass_properties.max_fuel  # If max fuel capacity not defined
        MaxFuel = min(MaxFuel, MTOW - OEW)


    # Define payload range points
    #Point  = [ RANGE WITH MAX. PLD   , RANGE WITH MAX. FUEL , FERRY RANGE   ]
    TOW     = [ MTOW                               , MTOW                   , OEW + MaxFuel ]
    FUEL    = [ min(TOW[1] - OEW - MaxPLD,MaxFuel) , MaxFuel                , MaxFuel       ]
    PLD     = [ MaxPLD                             , MTOW - MaxFuel - OEW   , 0.            ]

    # allocating Range array
    R       = [0,0,0]

    # evaluate the mission
    if iprint:
        print('\n\n\n .......... PAYLOAD RANGE DIAGRAM CALCULATION ..........\n')

    # loop for each point of Payload Range Diagram
    for i in range(len(TOW)):
##    for i in [2]:
        if iprint:
            print(('   EVALUATING POINT : ' + str(i+1)))

        # Define takeoff weight
        mission.segments[0].analyses.weights.vehicle.mass_properties.takeoff = TOW[i]

        # Evaluate mission with current TOW
        results = mission.evaluate()
        first_cruise_seg = results.segments["cruise_1"]
        last_cruise_seg = results.segments["cruise_"+str(num_cruise_seg)]

        # Distance convergency in order to have total fuel equal to target fuel
        #
        # User don't have the option of run a mission for a given fuel. So, we
        # have to iterate distance in order to have total fuel equal to target fuel
        #

        maxIter = 20 # maximum iteration limit
        tol = 1.     # fuel convergency tolerance
        err = 9999.  # error to be minimized
        iter = 0     # iteration count

        while abs(err) > tol and iter < maxIter:
            iter = iter + 1

            # Current total fuel burned in mission
            TotalFuel  = TOW[i] - results.segments[-1].conditions.weights.total_mass[-1,0]

            # Difference between burned fuel and target fuel
            missingFuel = FUEL[i] - TotalFuel - reserves

            # Current distance and fuel consuption in the cruise segment
            CruiseDist = first_cruise_seg.conditions.frames.inertial.position_vector[-1][0] - first_cruise_seg.conditions.frames.inertial.position_vector[0][0]
            CruiseFuel = first_cruise_seg.conditions.weights.total_mass[0,0] - first_cruise_seg.conditions.weights.total_mass[-1,0]
            if num_cruise_seg >= 2:
                CruiseFuel += results.segments["cruise_2"].conditions.weights.total_mass[0,0] - results.segments["cruise_2"].conditions.weights.total_mass[-1,0]
                CruiseDist += results.segments["cruise_2"].conditions.frames.inertial.position_vector[-1][0] - results.segments["cruise_2"].conditions.frames.inertial.position_vector[0][0]
            if num_cruise_seg >= 3:
                CruiseFuel += results.segments["cruise_3"].conditions.weights.total_mass[0,0] - results.segments["cruise_3"].conditions.weights.total_mass[-1,0]
                CruiseDist += results.segments["cruise_3"].conditions.frames.inertial.position_vector[-1][0] - results.segments["cruise_3"].conditions.frames.inertial.position_vector[0][0]
            if num_cruise_seg >= 4:
                CruiseFuel += results.segments["cruise_4"].conditions.weights.total_mass[0,0] - results.segments["cruise_4"].conditions.weights.total_mass[-1,0]
                CruiseDist += results.segments["cruise_4"].conditions.frames.inertial.position_vector[-1][0] - results.segments["cruise_4"].conditions.frames.inertial.position_vector[0][0]
            # Current specific range (m/kg)
            CruiseSR    = CruiseDist / CruiseFuel        # [m/kg]

            # Estimated distance that will result in total fuel burn = target fuel
            DeltaDist  =  CruiseSR *  missingFuel
            mission.segments["cruise_1"].distance = (CruiseDist + DeltaDist) / num_cruise_seg
            mission.segments["cruise_2"].distance = (CruiseDist + DeltaDist) / num_cruise_seg
            if num_cruise_seg >= 3:
                mission.segments["cruise_3"].distance = (CruiseDist + DeltaDist) / num_cruise_seg
            if num_cruise_seg >= 4:
                mission.segments["cruise_4"].distance = (CruiseDist + DeltaDist) / num_cruise_seg

            # running mission with new distance
            results = mission.evaluate()

            # Difference between burned fuel and target fuel
            err = ( TOW[i] - results.segments[-1].conditions.weights.total_mass[-1,0] ) - FUEL[i] + reserves

            if iprint:
                print(('     iter: ' +str('%2g' % iter) + ' | Target Fuel: '   \
                  + str('%8.0F' % FUEL[i]) + ' (kg) | Current Fuel: ' \
                  + str('%8.0F' % (err+FUEL[i]))+' (kg) | Residual : '+str('%8.0F' % err)))

        # Allocating resulting range in ouput array.
        segments = [key for key in mission.segments.keys() if ('reserve' not in key) and ('hold' not in key)]
        last_segment = segments[-1]

        climb_segments = [key for key in results.segments.keys() if (('climb' in key) and ('reserve' not in key) and ('second_leg' not in key) and ('step' not in key))]
        first_climb_segment = climb_segments[0]
        # print(last_segment)
        R[i] = ( results.segments[last_segment].conditions.frames.inertial.position_vector[-1,0] - results.segments[first_climb_segment].conditions.frames.inertial.position_vector[0][0]) * Units.m / Units.nautical_mile      #Distance [nm]

    # Inserting point (0,0) in output arrays
    R.insert(0,0)
    PLD.insert(0,MaxPLD)
    FUEL.insert(0,0)
    TOW.insert(0,0)

    # packing results
    payload_range_multiple_cruise.range     = np.multiply(R,1.0*Units.nautical_mile / Units.m) # [m]
    payload_range_multiple_cruise.payload   = PLD
    payload_range_multiple_cruise.fuel      = FUEL
    payload_range_multiple_cruise.takeoff_weight = TOW
    payload_range_multiple_cruise.reserves = reserves

    # Write output file
    if iwrite:
        import datetime                 # importing library

        fid = open('PayloadRangeDiagram.dat','w')   # Open output file
        fid.write('Output file with Payload Range Diagram details\n\n') #Start output printing

        fid.write( ' Maximum Takeoff Weight ...........( MTOW ).....: ' + str( '%8.0F'   %   MTOW   ) + ' kg\n' )
        fid.write( ' Operational Empty Weight .........( OEW  ).....: ' + str( '%8.0F'   %   OEW    ) + ' kg\n' )
        fid.write( ' Maximum Zero Fuel Weight .........( MZFW ).....: ' + str( '%8.0F'   %   MZFW   ) + ' kg\n' )
        fid.write( ' Maximum Payload Weight ...........( PLDMX  )...: ' + str( '%8.0F'   %   MaxPLD ) + ' kg\n' )
        fid.write( ' Maximum Fuel Weight ..............( FUELMX )...: ' + str( '%8.0F'   %   MaxFuel) + ' kg\n' )
        fid.write( ' Reserve Fuel  .................................: ' + str( '%8.0F'   %   reserves)+ ' kg\n\n' )

        fid.write( '    RANGE    |   PAYLOAD   |   FUEL      |    TOW      |  \n')
        fid.write( '     nm      |     kg      |    kg       |     kg      |  \n')

        for i in range(len(TOW)):
            fid.write( str('%10.0f' % R[i]) + '   |' + str('%10.0f' % PLD[i]) + '   |' + str('%10.0f' % FUEL[i]) + '   |' + ('%10.0f' % TOW[i]) + '   |\n')

        # Print timestamp
        fid.write(2*'\n'+ 43*'-'+ '\n' + datetime.datetime.now().strftime(" %A, %d. %B %Y %I:%M:%S %p"))
        fid.close

    # Print data in command line
    if iprint:
        print( '\n\n                        RESULTS\n')
        print( '    RANGE    |   PAYLOAD   |   FUEL      |    TOW      |')
        print( '     nm      |     kg      |    kg       |     kg      |')
        for i in range(len(TOW)):
            print(( str('%10.0f' % R[i]) + '   |' + str('%10.0f' % PLD[i]) + '   |' + str('%10.0f' % FUEL[i]) + '   |' + ('%10.0f' % TOW[i]) + '   |'))
        print(('\n\n   Elapsed time: ' + str('%6.2f' % (time.time() - start_time)) + 's'))

    #   Plot Payload Range
    if iplot:

        #import pylab
        import pylab as plt

        title = "Payload Range Diagram"
        plt.figure(0)
        plt.plot(R,PLD,'r', label='GovEnAir')
        R_ref = [0, 7881, 10500, 11149]
        PLD_ref = PLD
        plt.plot(R_ref, PLD_ref, 'b', label='Reference')
        plt.xlabel('Range (nm)'); plt.ylabel('Payload (kg)'); plt.title(title)
        plt.legend()
        plt.grid(True)
        plt.show()

    return payload_range_multiple_cruise
