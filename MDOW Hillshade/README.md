[mdow-hillshade]: images/mdow-hillshade.png "The MDOW Hillshade Example"
[arcgis-hillshade]: images/arcgis-hillshade.png "The ArcGIS Hillshade Example"

# MDOW Hillshade

MDOW hillshade is actually the __M__ ulti-__D__ irectional __O__ blique __W__ eighted hillshade. This is an extensive method based on the original hillshade approach to generate better hillshade from DEM (digital elevation model) datasets. The MDOW hillshade is created by combing one initial hillshade and four additional ones generated from different azimuths (225°, 270°, 315°, and 360°). The code is implemented according to the paper "[A Methodology for Creating Analytical Hillshading by Combining Different Lighting Directions](https://www.researchgate.net/publication/237548702_A_METHODOLOGY_FOR_CREATING_ANALYTICAL_HILL-SHADING_BY_COMBINING_DIFFERENT_LIGHTING_DIRECTIONS)" and with the help from ArcGIS document about [hillshade](http://desktop.arcgis.com/en/arcmap/10.3/tools/spatial-analyst-toolbox/how-hillshade-works.htm), [slope](http://desktop.arcgis.com/en/arcmap/10.3/tools/spatial-analyst-toolbox/how-slope-works.htm) and [aspect](http://desktop.arcgis.com/en/arcmap/10.3/tools/spatial-analyst-toolbox/how-aspect-works.htm).

---

## Features
* Better visual effects on generated hillshade
* Multiple threads for performance acceleration
* Uses for both Python module and command line tool

## Prerequisites
Make sure there are Python 2.7+ (with [futures](https://pypi.org/project/futures/) installed) / Python 3.4+, NumPy, SciPy, GDAL, Rasterio and Click (for command line) in the environment.

## API
**mdow.run**

run(*in_path*, *out_path*, *azimuth*, *altitude*)

Arguments:
* in_path: File path of the input file.
* out_path: File path of the output file.
* azimuth: Azimuth for generating hillshade (0° - 360°).
* altitude: Altitude for generating hillshade (0° - 90°).

## Usages

### Run in Command Line

```
python mdow.py --in DEM --out HILLSHADE --azimuth  AZIMUTH --altitude ALTITUDE
```
### Run in Code

Place the code in the proper directory and import to where you need it.
```python
import mdow
```
Process your DEM and get your hillshade.
```python
in_path = 'dem.tif'
out_path = 'hillshade.tif'
azimuth = 180
altitude = 45
mdow.run(in_path, out_path, azimuth, altitude)
```

## Example

**MDOW Hillshade**

![MDOW Hillshade Example][mdow-hillshade]

**ArcGIS Hillshade for Comparison**

![ArcGIS Hillshade Example][arcgis-hillshade]
