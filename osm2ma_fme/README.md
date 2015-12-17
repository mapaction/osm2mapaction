This folder contains two FME workbenches associated with the OSM2MA python tools.
(They are not required to run the python tools).

Create_OSMCONF_File.fmw generates the osmconf.ini file that will be needed to successfully use the OGR PBF reader. It reads the excel config file, and a template osmconf file, and creates an output osmconf file that causes the OGR PBF reader to expose as fields all the OSM tags required by MapAction. This has already been done, and would only need repeating if the excel config file is changed. The osmconf.ini file should then either be placed in the C:\OSGeo4W\share\gdal directory (replacing the one already there) or can be left in the osm2ma directory and the path to it would then need to be specified in the code (not currently done).

OSM2MapAction.fmw duplicates the entire functionality of the osm2ma python scripts going from source osm data to mapaction dnc shapefiles (except an initial conversion must be done first via ogr2ogr: details are in the workbench). This workbench was created in order to generate "test" output data to compare the results of the python scripts against. However as it's quite easy to use it might be useful to use this in some circumstances. 

Both workbenches were generated in FME 2015 so that will be needed to open them.

