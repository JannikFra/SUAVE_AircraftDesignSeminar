function SFC = SFC_model(SFC_bucket,altitude,mach)
    altitude = altitude / 0.3048;
    if altitude < 36000
        SFC = SFC_bucket * (1 + 0.003 * (36000 - altitude)/1000);
    else
        SFC = SFC_bucket * (1 + 0.002 * (altitude - 36000)/1000);
    end
    SFC = SFC * (1 + 0.006 * (mach - 0.82)*100);
end