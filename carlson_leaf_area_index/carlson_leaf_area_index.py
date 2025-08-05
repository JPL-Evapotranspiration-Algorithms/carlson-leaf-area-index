from typing import Union
import rasters as rt
from rasters import Raster
import numpy as np

# Extinction coefficient for PAR in Beer-Lambert law (typical value for many canopies)
KPAR = 0.5

# Minimum fraction of absorbed PAR (fIPAR); represents no absorption
MIN_FIPAR = 0.0

# Maximum fraction of absorbed PAR (fIPAR); represents full absorption
MAX_FIPAR = 1.0

# Minimum Leaf Area Index; represents no leaf area
MIN_LAI = 0.0

# Maximum Leaf Area Index; upper bound for most natural canopies
MAX_LAI = 10.0

def carlson_leaf_area_index(
        NDVI: Union[Raster, np.ndarray],
        min_fIPAR: float = MIN_FIPAR,
        max_fIPAR: float = MAX_FIPAR,
        min_LAI: float = MIN_LAI,
        max_LAI: float = MAX_LAI) -> Union[Raster, np.ndarray]:
    """
    Converts Normalized Difference Vegetation Index (NDVI) to Leaf Area Index (LAI) using a two-step process:

    Explanation:
        1. Estimate fIPAR (fraction of absorbed photosynthetically active radiation) from NDVI:
           fIPAR = clip(NDVI - 0.05, min_fIPAR, max_fIPAR)
           This linear relationship is commonly used in remote sensing to relate NDVI to canopy light absorption.
        2. Calculate LAI using the Beer-Lambert law:
           LAI = -ln(1 - fIPAR) / KPAR
           The Beer-Lambert law describes how light is attenuated through a medium (here, a plant canopy). KPAR is the extinction coefficient for PAR (typically 0.5).
        3. Results are clipped to the specified min/max LAI range.

    Constants:
        KPAR (float): Extinction coefficient for PAR (default 0.5). See Goudriaan (1977).
        MIN_FIPAR, MAX_FIPAR (float): Minimum and maximum fIPAR values (default 0.0, 1.0).
        MIN_LAI, MAX_LAI (float): Minimum and maximum LAI values (default 0.0, 10.0).

    Citations:
        - Carlson, T.N., & Ripley, D.A. (1997). On the relation between NDVI, fractional vegetation cover, and leaf area index. Remote Sensing of Environment, 62(3), 241-252. https://doi.org/10.1016/S0034-4257(97)00104-1
        - Monsi, M., & Saeki, T. (1953). Über den Lichtfaktor in den Pflanzengesellschaften und seine Bedeutung für die Stoffproduktion. Japanese Journal of Botany, 14, 22-52.
        - Goudriaan, J. (1977). Crop Micrometeorology: A Simulation Study.

    Parameters:
        NDVI (Union[Raster, np.ndarray]): Input NDVI data.
        min_fIPAR (float): Minimum fIPAR value (default 0.0).
        max_fIPAR (float): Maximum fIPAR value (default 1.0).
        min_LAI (float): Minimum LAI value (default 0.0).
        max_LAI (float): Maximum LAI value (default 10.0).

    Returns:
        Union[Raster, np.ndarray]: Converted LAI data.
    """
    # Step 1: Estimate fIPAR from NDVI, using a linear relationship and clip to valid range
    fIPAR = rt.clip(NDVI - 0.05, min_fIPAR, max_fIPAR)  # NDVI offset by 0.05, clipped to [min_fIPAR, max_fIPAR]
    
    # Step 2: Set fIPAR=0 to NaN (no absorption, no vegetation)
    fIPAR = np.where(fIPAR == 0, np.nan, fIPAR)         # Avoid log(0) in next step
    
    # Step 3: Calculate LAI using Beer-Lambert law, then clip to valid LAI range
    LAI = rt.clip(-np.log(1 - fIPAR) * (1 / KPAR), min_LAI, max_LAI)  # Beer-Lambert law for canopy
    
    return LAI

def inverse_carlson_NDVI(
        LAI: Union[Raster, np.ndarray],
        min_fIPAR: float = MIN_FIPAR,
        max_fIPAR: float = MAX_FIPAR,
        min_LAI: float = MIN_LAI,
        max_LAI: float = MAX_LAI) -> Union[Raster, np.ndarray]:
    """
    Inverse of carlson_leaf_area_index: Converts Leaf Area Index (LAI) back to NDVI using the inverse of the Beer-Lambert law and the original NDVI-fIPAR relationship.

    Explanation:
        1. Clip LAI to valid range.
        2. Compute fIPAR from LAI using the inverse Beer-Lambert law:
           fIPAR = 1 - exp(-KPAR * LAI)
        3. Clip fIPAR to valid range.
        4. Compute NDVI from fIPAR:
           NDVI = fIPAR + 0.05

    Parameters:
        LAI (Union[Raster, np.ndarray]): Input LAI data.
        min_fIPAR (float): Minimum fIPAR value (default 0.0).
        max_fIPAR (float): Maximum fIPAR value (default 1.0).
        min_LAI (float): Minimum LAI value (default 0.0).
        max_LAI (float): Maximum LAI value (default 10.0).

    Returns:
        Union[Raster, np.ndarray]: Estimated NDVI data.
    """
    # Step 1: Clip LAI to valid range
    LAI = rt.clip(LAI, min_LAI, max_LAI)

    # Step 2: Compute fIPAR from LAI (inverse Beer-Lambert law)
    fIPAR = 1 - np.exp(-KPAR * LAI)

    # Step 3: Clip fIPAR to valid range
    fIPAR = rt.clip(fIPAR, min_fIPAR, max_fIPAR)

    # Step 4: Compute NDVI from fIPAR
    NDVI = fIPAR + 0.05

    return NDVI
