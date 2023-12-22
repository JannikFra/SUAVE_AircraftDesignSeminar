close all
clear
clc

%% User Inputs
MTOM = 230000;  % in kg, ref = 279000
g = 9.81;

% Operational
rho_0 = 1.225;   % ground air density in kg/m³
TOFL = 3200;     % take-off field length in m, TLAR
stallSpeed_kts = 130;   % in kts, probably not relevant for us
stallSpeed = 0.51444 * stallSpeed_kts;  % in m/s

climbAngleOEI = 0.024;   % in rad - CS-25 regulations for 2-engine a/c

cruiseAltitude_ft = 39000;  % in ft, ref = 35000
cruiseAltitude = 0.3048*cruiseAltitude_ft; % in m
cruiseMach = 0.82;
[~,a_cr,~,rho_cr] = atmosisa(cruiseAltitude);
cruiseSpeed = cruiseMach * a_cr; % in m/s
massRatioCruise = 0.99 * 0.99 * 0.995 * 0.98;    % cruise mass divided by MTOM, nach Roskam

approachSpeed_kts = 130;    % in kts, ref = 130
approachSpeed = 0.51444 * approachSpeed_kts;
massRatioLanding = 0.70;    % MLM divided by MTOM, ref = 0.70

% Aerodynamics
AR = 14;     % wing aspect ratio, ref = 9.988
oswald = 0.81;       % oswald factor, ref = 0.77 for low cL
LD_OEI = 14;         % L/D in climb configuration
LD_cruise = 26;      % L/D in cruise configuration
cL_max = 2.34;  % ref = 2.15
cL_max_TO = 0.8 * cL_max;
cD0 = 0.014;   % ref = 0.0108
k = 1/(pi * AR * oswald);   % induced drag constant

% Engines
numberOfEngines = 2;
k_TO = 2.45;
thrustRatioClimb = 1.15;    % TODO: muss verifiziert werden
thrustReverser = 0;   % set to 1 (true) or 0 (false)


%% Calculate constraints and draw sizing chart
[wingArea, engineThrust, mS_set, TW_set] = ...
    preliminarySizing(MTOM,g,cD0,LD_OEI,LD_cruise,k,rho_0,rho_0,rho_cr,stallSpeed,cruiseSpeed,cL_max, ...
    cL_max_TO,k_TO,TOFL,climbAngleOEI,numberOfEngines,thrustRatioClimb,massRatioCruise,massRatioLanding, ...
    thrustReverser,approachSpeed);

wingSpan = sqrt(wingArea*AR);
if wingSpan > 80
    warning('Wing span exceeds maximum allowed wing span of 80m!');
end


%% Print results
fprintf('Thrust to Weight Ratio: %.3f\n', TW_set);
fprintf('Wing Loading: %.0f kg/m² \n\n', mS_set);
fprintf('SLS Thrust: %.0f kN\n', engineThrust);
fprintf('Wing Reference Area: %.0f m²\n', wingArea);
fprintf('Wing Span: %.2f m\n', wingSpan);
