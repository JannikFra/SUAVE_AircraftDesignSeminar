# Created:  May 2022, J. Frank


# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
import copy
from SUAVE.Core import Units
from SUAVE.Core import Data

# ----------------------------------------------------------------------
#  Method
# ----------------------------------------------------------------------
## @ingroup Methods-Figures_of_Merit-Supporting_Functions
def material_costs(vehicle):
    """ This method computes the material costs
    """

    # Unpack inputs
    mc = Data()

    w_s = vehicle.mass_properties.operating_empty - vehicle.weight_breakdown.propulsion_breakdown.engines
    w_gt = vehicle.weight_breakdown.propulsion_breakdown.engines

    mc.airframe = 1150 * w_s
    mc.gas_turbine = 2500 * w_gt

    mc.total = mc.airframe + mc.gas_turbine
    return mc