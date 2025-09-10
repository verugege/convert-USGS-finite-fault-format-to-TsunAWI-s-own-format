# convert-USGS-finite-fault-format-to-TsunAWI-s-own-format
Convert USGS Finite Fault Format to TsunAWI`s own format.

USGS finite fault format .param
A major provider of earthquake information is the United States Geological Survey, USGS, https://earthquake.usgs.gov/. TsunAWI supports the basic inversion format ‘PARAM’. More information on finite faults is given in https://earthquake.usgs.gov/data/finitefault/
Here is the head of an example, a finite fault of the 2011 Tohoku Tsunami, downloaded from https://earthquake.usgs.gov/archive/product/finite-fault/usp000hvnu/us/1539808472261/basic_inversion.param
For the use in TsunAWI, we assume that a param file always starts with a header of 4 lines, of which we analyse the second line to retrieve the number nx * ny, the length Dx and the width Dy of the subfaults. The bounding box given in the following 5 lines and the following comment is ignored.

For each subfault, TsunAWI scales the slip from [cm] to [m], and the length, width, and depth from [km] to [m]. Finally, the parameters are transformed from the center of the plate to TsunAWI’s default, the origin corner and passed to the routine to compute the displacement.

https://tsunami.awi.de/input/initial_conditions.html
