# Raster-Value-Regular

## What is It ?
This repository is the source code of a QGIS Plugin.

## How to Use ?
This plugin can be downloaded on QGIS Plugin menu. Then run it.
Select described inputs and press "Ok"

## What it does ?
This plugin answer the following need: Smooth and interpolate grid from a Raster Layer using RegularGridInterpolator 
from scipy, then apply values to a vector layer as attribute.

## Inputs
- Point geometry Vector Layer
- Raster Layer and its band number
- Value attribute to store result in Vector Layer features

## Outputs
- Modified Point geometry Vector Layer
