[workflow-rh]: images/workflow-rh.png "Workflow for Relative Humidity Datasets"
[workflow-aerosol]: images/workflow-aerosol.png "Workflow for Aerosol Datasets"
[workflow-integration]: images/workflow-integration.png "Workflow for Integration"

# US Haze Effect Analysis

This is a full-stack data processing and visualizing project to show the common haze effect in the whole US land.

## Prerequisites

* [Python](https://www.python.org/)
* [SQLite](https://www.sqlite.org/)
* [ArcGIS](http://desktop.arcgis.com/)

## Data Source & Methods

Core datasets and the algorithms are from the program of [IMPROVE (Interagency Monitoring of Protected Visual Environments)](http://vista.cira.colostate.edu/Improve/). Apart from these, Census [TIGER (Topologically Integrated Geographic Encoding and Referencing database)](https://tigerweb.geo.census.gov/tigerwebmain/TIGERweb_main.html) boundary files are used for the study area and cartography. For the results, maps of initial-version algorithm are includes. For this method, it is called the zeroth personally and doesn't compute elemental carbon and Rayleigh scattering.

## Workflows

**Workflow of Processing Relative Humidity Datasets**

![Workflow for Relative Humidity Datasets][workflow-rh]

**Workflow of Processing Aerosol Datasets**

![Workflow for Aerosol Datasets][workflow-aerosol]

**Workflow of Integration**

![Workflow for Integration][workflow-integration]

## Results

All the results are in the form of map pictures and inside the directory of results.
