# carlson-leaf-area-index

Leaf Area Index (LAI) Remote Sensing Method from Carlson et al 1997 Python Package

Gregory H. Halverson (they/them)<br>
[gregory.h.halverson@jpl.nasa.gov](mailto:gregory.h.halverson@jpl.nasa.gov)<br>
NASA Jet Propulsion Laboratory 329G
  

## Overview

This package provides a Python implementation of the Leaf Area Index (LAI) algorithm described by Carlson & Ripley (1997) and related literature. It converts NDVI (Normalized Difference Vegetation Index) data to LAI using a two-step process based on canopy light absorption and the Beer-Lambert law, suitable for remote sensing applications.

## Features

- Converts NDVI to Leaf Area Index (LAI)
- Supports both NumPy arrays and `rasters.Raster` objects
- Based on peer-reviewed scientific literature

## Installation

Install via pip:

```fish
pip install carlson-leaf-area-index
```

## Usage


```python
import numpy as np
from carlson_leaf_area_index import carlson_leaf_area_index

# Example NDVI array
NDVI = np.array([[0.1, 0.3, 0.5], [0.04, 0.52, 0.25]])
LAI = carlson_leaf_area_index(NDVI)
print(LAI)
```


## Algorithm

The algorithm converts NDVI to LAI in two main steps:

1. **Estimate fIPAR (fraction of absorbed photosynthetically active radiation) from NDVI:**
	- `fIPAR = clip(NDVI - 0.05, min_fIPAR, max_fIPAR)`
	- This relates NDVI to the fraction of light absorbed by the canopy.

2. **Calculate LAI using the Beer-Lambert law:**
	- `LAI = -ln(1 - fIPAR) / KPAR`
	- KPAR is the extinction coefficient for PAR (default 0.5).

3. **Clipping:**
	- Results are clipped to a valid LAI range (default 0–10).

Values of fIPAR below the minimum are set to NaN (no absorption), and LAI is clipped to the specified range.

## References


- Carlson, T.N., & Ripley, D.A. (1997). On the relation between NDVI, fractional vegetation cover, and leaf area index. Remote Sensing of Environment, 62(3), 241-252. [https://doi.org/10.1016/S0034-4257(97)00104-1](https://doi.org/10.1016/S0034-4257(97)00104-1)
- Monsi, M., & Saeki, T. (1953). Über den Lichtfaktor in den Pflanzengesellschaften und seine Bedeutung für die Stoffproduktion. Japanese Journal of Botany, 14, 22-52.
- Goudriaan, J. (1977). Crop Micrometeorology: A Simulation Study.

## License

See LICENSE file for details.