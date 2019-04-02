[convergence]: images/convergence.png "Convergence Chart"
[sample1-in]: images/sample1-in.png "Sample 1"
[sample1-out]: images/sample1-out.png "Output from Sample 1"
[sample2-in]: images/sample2-in.png "Sample 2"
[sample2-out]: images/sample2-out.png "Output from Sample 2"
[sample3-in]: images/sample3-in.png "Sample 3"
[sample3-out]: images/sample3-out.png "Output from Sample 3"

# Super Resolution CNN

This is the implementation of SRCNN according to the paper "[Image Super-Resolution Using Deep Convolutional Networks](https://ieeexplore.ieee.org/document/7115171?arnumber=7115171)".

## Prerequisites

* [Torch](http://torch.ch/)
* [Lua](https://www.lua.org/home.html)
* [OpenCV-Python](https://pypi.org/project/opencv-python/)
* [NumPy](http://www.numpy.org/)
* [Python](https://www.python.org/)

## Data Source

The datasets used in this paper are selected images of high resolution imagery from the website of [TNM (The National Map)](https://www.usgs.gov/core-science-systems/national-geospatial-program/national-map/) in [USGS (US Geological Survey)](https://www.usgs.gov/). The data is easy to acquire via downloading selected data packages from [TNM viewer](https://viewer.nationalmap.gov/basic/).

## Results

The learning rate is changed for three times to reach a small loss value, and the initial learning rate is 1.0×10<sup>-4</sup> and changed to 2.0×10<sup>-4</sup>, 5.0×10<sup>-5</sup> and 2.0×10<sup>-5</sup> one by one. Due to the first time on deep learning and no data normalization uses, sample outputs have obvious color issue. Therefore, outputs get histogram adjusted and blended with original images. Additionally, outputs will be in the same image size of the inputs because of the relative large data volume.

**Convergence**
![Convergence][convergence]

**Sample 1**

Input | Output
:---: | :---:
![Sample 1][sample1-in] | ![Sample 1 Output][sample1-out]

**Sample 2**

Input | Output
:---: | :---:
![Sample 2][sample2-in] | ![Sample 2 Output][sample2-out]

**Sample 3**

Input | Output
:---: | :---:
![Sample 3][sample3-in] | ![Sample 3 Output][sample3-out]
