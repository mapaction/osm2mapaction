Instructions
============

1) Copy the python script (maosmtoshape.py), the pbf files, and the excel file to a local directory

2) Create a directory were you want export the shapefiles to

3) Open a command prompt. Anything below in angle brackets mean you need to substitute a suitable value

4) type:
cd /d <the_directory_where_you_saved_everything>

5) type
C:\OSGeo4W64\OSGeo4W.bat python <path-to-python-script-file> <path-to-pbf-file> <path-to-excel-file> <path-to-output-directory> <geoextent-name> 

The paths can be relative, for example: 

D:\work\custom-software-group\osm-ma-shp>C:\OSGeo4W64\OSGeo4W.bat python maosmtoshape.py osm\west-sussex-latest.osm.pbf OSM_to_MA_ascii.xls sussex wsx