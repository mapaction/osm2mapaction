Instructions
============

1) Copy the entire contents of the "osm2mapaction" directory including subdirectories to a local directory.

2) Create a directory were you want export the shapefiles to.

3) Open a command prompt. In the following steps, anything below in angle brackets means you need to substitute
a suitable value.

4) type:
cd /d <the_directory_where_you_saved_everything>\osm2ma

5) type (all on a single line)
C:\OSGeo4W64\OSGeo4W.bat python path-to-osm2mapaction.py <path-to-pbf-file> <path-to-excel-file>
    <path-to-output-directory> <geoextent-name>

The paths can be relative, for example: 
D:\work\custom-software-group\code\github\osm2mapaction\osm2ma>C:\OSGeo4W64\OSGeo4W.bat python osm2mapaction.py
    testfiles\west-sussex-latest.osm.pbf ..\configfiles\OSM_to_MA_ascii.xls sussex wsx

