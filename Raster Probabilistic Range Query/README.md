[step-1]: images/step1.png "Step 1 of Raster PRQ"
[step-2]: images/step2.png "Step 2 of Raster PRQ"
[step-3]: images/step3.png "Step 3 of Raster PRQ"
[step-4]: images/step4.png "Step 4 of Raster PRQ"
[tool-ui]: images/ui.png "UI of Raster PRQ"
[sample-map]: images/sample-map.png "Sample Map of Raster PRQ"

# Raster Probabilistic Range Query

Probabilistic range query (PRQ) is an approach to acquire required data from existing datasets which have uncertainty on some aspects. This means that common queries cannot find proper data which can fulfill diverse requests on these datasets due to uncertainty and probability. Then raster PRQ deals with more practical cases of remote sensing and is applied to geograpgic imageries which contain uncertain ground feature data. 


## Data Source

The datasets in this project are from the project of United States Department of Agriculture (USDA) named National Insect & Disease Risk Maps (NIDRM) and built from the tools of Forest Health Technology Enterprise Team (FHTET). Click [here](https://www.fs.fed.us/foresthealth/applied-sciences/mapping-reporting/gis-spatial-analysis/national-risk-maps.shtml) to see the data source page.

Then the exact datasets finally used in the project derive from the total [basal area (BA)](https://en.wikipedia.org/wiki/Basal_area) raster dataset with suitable offsets on original pixel values for the uncertainty of the computed total BA loss values. The calculation of cross-sectional area of a tree depends on the measurement of its diameter, and this measurement needs visual readings on the special tool. Therefore, offsets of uncertainty simulate the uncertainty from the precision of the tool and the accuracy of manual readings. Which needs notice is that these uncertain offsets are used to explore the theoretical feasibility of PRQ on the remote sensing imageries.

## Prerequisites

Spatial Analyst Toolbox and ModelBuilder of ArcGIS 10.3+

## Steps

**1. Generate study areas**

The first step uses Tthe tool "[Extract by Mask](http://desktop.arcgis.com/en/arcmap/10.3/tools/spatial-analyst-toolbox/extract-by-mask.htm)" to clip raster datasets according to the shape of the query region. In this project, there are only two raster datasets representing the minimum and maximum of the pixel value interval. Thus, in this step, two clipped raster datasets are acquired for further steps. Considering pixels within the query region, this step can exclude all pixels outside the query region, which prunes quite a lot of pixels in the spatial distribution of pixels.

![Step 1][step-1]

**2. Filter image cells by range**

The second step uses tool “[Raster Calculator](http://desktop.arcgis.com/en/arcmap/10.3/tools/spatial-analyst-toolbox/raster-calculator.htm)” to generate mask of candidate pixels, and mask is also a raster dataset containing only zero and one the former of which represents that the pixel value in the current pixel should be excluded while the latter of which is on the contrary. Then, select merely one values out of the mask via tool “[Extract by Attributes](http://desktop.arcgis.com/en/arcmap/10.3/tools/spatial-analyst-toolbox/extract-by-attributes.htm)”. This step is a value-based filtering on pixels, which will prune pixels whose value interval have no intersections with the query interval since these pixels are in zero values in the mask and then unselected in the next sub-step.

![Step 2][step-2]

**3. Compute cell probabilities**

The third step is to compute probabilities of pixels. Multiplying candidate pixels with respective raster datasets of upper bound and lower bound can generate corresponding candidate pixels in respective raster datasets. Then, by applying the formula of probabilities in the definition in accordance to the query interval, it is not hard to acquire the raster of probabilities of these candidate pixels.

![Step 3][step-3]

**4. Query cells with threshold **

The fourth step is to get pixels whose probabilities are no less than the threshold: generate the mask from comparison computations, then extract pixels of value one in the mask, and finally multiply these pixels with the original raster of probability values to get the qualified pixels as the output results. This step prunes those pixels having probabilities lower than the threshold.

![Step 4][step-4]

## Results

**Tool UI**

![Tool UI][tool-ui]

**The Map of 7 Arbitrary Study Areas**

![Sample Map][sample-map]
