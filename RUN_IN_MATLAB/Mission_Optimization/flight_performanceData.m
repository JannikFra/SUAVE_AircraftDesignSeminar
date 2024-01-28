function [LD,SFC,fuelFlow] = flight_performanceData(weight,altitude,mach,refArea,cD0,k,SFC_bucket)
    g = 9.81;
    [~,a_cr,~,rho_cr] = atmosisa(altitude);
    V_cr = a_cr * mach;

    cL = 2*weight*g/(rho_cr * V_cr^2 * refArea);
    cD = cD0 + k*cL^2;
    LD = cL/cD;

    thrust = 0.5*rho_cr*V_cr^2 * cD * refArea;
    SFC = SFC_model(SFC_bucket,altitude,mach);
    fuelFlow = SFC * thrust;
end