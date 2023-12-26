close all
clear
clc

%% Inputs
g = 9.81;
MTOW = 220000;  % in kg
climb_fuel = 8000;  % in kg

cruise_distance = 10000;    % in nm
cruise_mach = 0.82;
cruise_altitude_initial = 37000;    % in ft
altitude_step = 2000;     % in ft
stepClimb_ROC = 300;    % in ft/min

SFC_bucket = 0.475;     % in lb/h/lbf

cD0 = 0.0154;
AR = 20;
oswald = 0.84;
k = 1/pi/AR/oswald;
refArea = 357;  % in m²

%%  Conversion to metric
cruise_distance = 1852 * cruise_distance;
cruise_altitude_initial = 0.3048 * cruise_altitude_initial;
stepClimb_ROC = 0.3048 * stepClimb_ROC / 60;
altitude_step = 0.3048 * altitude_step;
SFC_bucket = 9.81 * 3600 / (10^9) * SFC_bucket; 

%% Initialize Iteration
weight = MTOW - climb_fuel;
altitude = cruise_altitude_initial;
distance_covered = 0;
delta_s_cruise = 10000;  % in m
i = 1;
j = 1;

%% Calculate missison fuel burn
while distance_covered < cruise_distance
    altitude_virtual = altitude + altitude_step;
    
    [LD,SFC,fuelFlow] = flight_performanceData(weight,altitude,cruise_mach,refArea,cD0,k,SFC_bucket);
    [LD_virtual,SFC_virtual,fuelFlow_virtual] = ...
        flight_performanceData(weight,altitude_virtual,cruise_mach,refArea,cD0,k,SFC_bucket);

    efficiency = SFC/LD;
    efficiency_virtual = SFC_virtual/LD_virtual;

    if efficiency/efficiency_virtual > 1.05
        altitude = altitude_virtual;
        fuelFlow = fuelFlow_virtual;
        distance_step(j) = distance_covered;
        j = j+1;
    end

    [~,a_cr,~,~] = atmosisa(altitude);
    V_cr = a_cr * cruise_mach;
    delta_t = delta_s_cruise/V_cr;

    weight = weight - fuelFlow * delta_t;
    distance_covered = distance_covered + delta_s_cruise;

    weight_stack(i) = weight;
    distance_stack(i) = distance_covered;
    altitude_stack(i) = altitude;
    LD_stack(i) = LD;
    efficiency_stack(i) = SFC/LD;
    fuelFlow_stack(i) = fuelFlow;

    i = i+1;
end

blockFuel = round(max(weight_stack) - min(weight_stack))

altitude_stack = altitude_stack ./ 304.8;
distance_stack = distance_stack ./ 1000;

% figure
% axis([0 cruise_distance/1000 0 70])
% xlabel('Distance [km]')
% ylabel('Altitude [kft]')
% hold on
% plot(distance_stack,altitude_stack)

figure
axis([0 cruise_distance/1000 5e-07 8e-07])
xlabel('Distance [km]')
ylabel('SFC/(L/D)')
hold on
plot(distance_stack,efficiency_stack)

figure
axis([0 cruise_distance/1000 0 2])
xlabel('Distance [km]')
ylabel('Fuel Flow [kg/s]')
hold on
plot(distance_stack,fuelFlow_stack)