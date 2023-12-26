function [S_w,engineThrust,mS_set,TW_set] = ...
    preliminarySizing(mtom,g,cD0,LD_OEI,LD_cruise,k, ...
    rho_0,rho_cl,rho_cr,V_stall,V_cr,cL_max,cL_max_TO,k_TO,TOFL,climbAngleOEI, ...
    n_e,thrustRatioClimb,massRatioCruise,massRatioLanding,thrustReverser,V_approach)
%%-----------------------------------------------------------------------%%
% This function calculates the constraints for Power-to-weight vs. Wing
% loading for a CS-25 aircraft with respect towards
% - take-off
% - climb
% - cruise 
% - slow flight (stall and approach)
% conditions and automatically sets the design point for highest possible
% wing loading (1st priority) and lowest possible power-to-weight ratio 
% (2nd priority)

% Inputs:
% - maximum take-off mass (kg)
% - gravitational acceleration (m/s^2)
% - zero-lift drag coefficient (-)
% - induced drag factor k (=1/(pi*AR*e)) (-)
% - air density in take-off, climb and cruise (kg/m³)
% - maximum stall velocity (m/s)
% - cruise velocity (m/s)
% - maximum lift coefficient of aircraft (-)
% - maximum lift coefficient in take-off conditions (-)
% - take-off parameter (m³/kg)
% - take-off field length (m)
% - required climb gradient in case of engine failure (rad)
% - number of engines
% - ratio of cruise mass to MTOM
% - ratio of MLW to MTOM
% - presence of thrust reversers (1 = true, 0 = false)
% - approach speed (m/s)

% Outputs:
% - required wing reference area in m² 
% - required thrust in kW
% - required Wing loading
% - required power to weight ratio
%%-----------------------------------------------------------------------%%

% Initialize wing loading vector
mS_min = 0; % Minimum wing loading in N/m²
mS_max = 1000; % Maximum wing loading in N/m²

mS = linspace(mS_min,mS_max);

% Thrust-to-weight in cruise
q_cr = 0.5 * rho_cr * V_cr^2;
thrustRatioCruise = 6;   % rho_0/rho_cr;
TW_cruise = thrustRatioCruise * (q_cr * cD0 ./ (mS.*g) + k / q_cr .* mS .* g * massRatioCruise^2);

% thrust to weight for take-off
CALIBRATION_TO = 0.9;
TW_to = CALIBRATION_TO * k_TO /(cL_max_TO * TOFL) .* mS;

% Thrust-to-weight for OEI climb
TW_OEI = thrustRatioClimb * n_e/(n_e - 1) * (climbAngleOEI + 1/LD_OEI);

% Thrust-to-weight for ICAC
climbAngleICAC = 1.5/V_cr;
TW_TOC = thrustRatioCruise * massRatioCruise * (climbAngleICAC + 1/LD_cruise);

% Wing loading to maintain given maximum stall speed
mS_stall = V_stall^2 * rho_0/(2*g) * cL_max;

% Wing loading approach speed
mS_approach = cL_max * rho_0 * V_approach^2 / (2*g*1.23^2*massRatioLanding);

% Wing loading landing distance
l_a = 305;  % obstacle clear distance for transport a/c
if thrustReverser == 1
    A = 0.66;
elseif thrustReverser == 0
    A = 1;
else
    error('ERROR: Set variable thrustReverser to 1 or 0');
end
mS_ldg = (TOFL/1.67 - l_a) * cL_max / (0.51*A*g*massRatioLanding);

% lift coefficient for best cruise (jet aircraft) according to
% Strohmayer Flugzeugentwurf 1, Teil 5, p. 47
cL_optCruise = sqrt(cD0 / (3*k));
% cL_LDmax = 0.5;     % reference A/C

% Best cruise for propeller aircraft
mS_optCruise = q_cr/g * cL_optCruise;

% Choose lowest wing loading value as upper boundary
mS_boundary = min([mS_stall, mS_approach, mS_ldg]);

% Computation of intersections in constraint diagramm 
y_ph = linspace(0,50);
mS_stall_stack = zeros(1,100);
mS_stall_stack(1,:) = mS_boundary;
mS_cruise_stack = zeros(1,100);
mS_cruise_stack(1,:) = mS_optCruise;
TW_climb_stack = max(TW_OEI, TW_TOC) .* ones(1,100);

mS_stack = zeros(5,1);
TW_stack = zeros(5,1);

[mS_stack(1),TW_stack(1)] = polyxpoly(mS,TW_to,mS_stall_stack,y_ph);  % intersection takeoff-stall
[mS_stack(2),TW_stack(2)] = polyxpoly(mS,TW_climb_stack,mS_stall_stack,y_ph);   % intersection climb-stall
[mS_stack(3),TW_stack(3)] = polyxpoly(mS,TW_cruise,mS_stall_stack,y_ph);    % intersection cruise-stall
[mS_stack(4),TW_stack(4)] = polyxpoly(mS,TW_climb_stack,mS_cruise_stack,y_ph);  % intersection climb-opt. cruise
[mS_stack(5),TW_stack(5)] = polyxpoly(mS,TW_cruise,mS_cruise_stack,y_ph); % intersection cruise-opt. cruise


% Set Design point according to function description
% if WS_stall < WS_cruise
    mS_set = mS_boundary;
    TW_set = max(TW_stack(1:3,1));
% else
%     WS_set = WS_cruise;
%     if TW_stack(4) > TW_stack(5)
%         TW_set = TW_stack(4);
%     else
%         TW_set = TW_stack(5);
%     end
% end

% Wing reference area and cruise power recalculation
S_w = mtom / mS_set;
engineThrust = TW_set * mtom * g / 1000;

% Plot Constraint Diagram
% Plots
figure
plot(mS,TW_cruise,'g','DisplayName','Cruise')
xlabel('Wing Loading [kg/m²]')
ylabel('Thrust to Weight [-]')
axis([mS_min mS_max 0 0.5])
hold on

% xline(mS_stall,'LineStyle','--','DisplayName','Stall');
xline(mS_approach,'Color','k','DisplayName','Approach');
% xline(mS_ldg,'LineStyle',':','DisplayName','Ldg Distance');
plot(mS,TW_to,'Color','k','DisplayName','TOFL')
yline(TW_OEI,'r','LineStyle','--','DisplayName','OEI Climb')
yline(TW_TOC,'r','DisplayName','TOC')
xline(mS_optCruise,'LineStyle','--','Color','b','DisplayName','Best Cruise')
plot(mS_set,TW_set,'Color','b','Marker','o','DisplayName','Design Point','LineStyle','none')
plot(568.7,0.228,'Color','b','Marker','+','DisplayName','Reference A/C','LineStyle','none')
legend('Location','northwest','NumColumns',2)

% plot_darkmode
hold off

end 
