
## Master branch
[![Build Status](https://travis-ci.org/mapaction/osm2mapaction.svg?branch=master)](https://travis-ci.org/mapaction/osm2mapaction)  [![Coverage Status](https://coveralls.io/repos/mapaction/osm2mapaction/badge.svg?branch=master)](https://coveralls.io/r/mapaction/osm2mapaction?branch=unittest-configengine)

## branch unittest-configengine
[![Build Status](https://travis-ci.org/mapaction/osm2mapaction.svg?branch=unittest-configengine)](https://travis-ci.org/mapaction/osm2mapaction)  [![Coverage Status](https://coveralls.io/repos/mapaction/osm2mapaction/badge.svg?branch=unittest-configengine)](https://coveralls.io/r/mapaction/osm2mapaction?branch=unittest-configengine)
  
  
# Convert PBF to SHP and rename to MapAction scheme, instructions

1. Copy the entire contents of the `osm2mapaction` directory including
   subdirectories to a local directory.

2. Create a directory were you want export the shapefiles to.

3. Open a command prompt. In the following steps, anything below in angle
   brackets means you need to substitute a suitable value.

4. Type:
   `cd /d <the_directory_where_you_saved_everything>\osm2ma`

5. Type (all on a single line)
   `C:\OSGeo4W64\OSGeo4W.bat python path-to-osm2mapaction.py -c
   <path-to-excel-file> -o <path-to-output-directory> -g <geoextent-name> -s
   <scale> <path-to-pbf-file>`

   The paths can be relative, for example: 
   `D:\work\custom-software-group\code\github\osm2mapaction\osm2ma>
   C:\OSGeo4W64\OSGeo4W.bat
   -c ..\config_files\OSM_to_MA_ascii_v6.xlsx -o output_dir cumulative.osm.pbf`

    Note that you can review the options/arguments by running the script with
    `-h` -- for example, the geoextent and scale are entirely optional and
    default to `wrl` and `su` respectively, while the output dir will default to
    wherever you are on the command line, and the Excel config file will default
    to the `OSM_to_MA_ascii_v6.xlsx` found in the `config_files` dir, above
    this one.

	
About the config spreadsheet
----------------------------
* The spreadsheet should be an MS Excel 2003 xls spreadsheet. A Excel 2007+ 
  *.xlsx file will not be read
* The spreadsheet should contain a Named Range called "xwalk". See here.... for how to define a named range in excel
* The named range should include the following columns:

|Column			|Purpose			|
|--------------------------:|:--------------------------------------------------|
|OSM_tag_name				|Name of the OSM tag.								|
|OSM_tag_value				|Value of the OSM tag. May be string, number or '*' for a wildcard.	|
|Element_icon				|													|
|Comment					|													|
|Useful_for_MapAction		|Boolean. Controls whether on not the feature should be included in the exported shapefiles.|
|Data Category				|See MapAction's Data Naming Convention.			|
|Cat_value					|Abbreviation of the Data Category.					|
|Date Theme description		|See MapAction's Data Naming Convention.			|	
|Theme_value				|Abbreviation of the Data Category.					|
|Conforms_to_MA_Hierarchy	|Boolean, calculated via lookup in the spreadsheet. Confirms whether or not the Data Category and Theme values nest hierarchy as defined in MapAction's	Data Naming Convention. Not used by osm2ma.|
|OSM_Element				|List of OSM geometry types included in the feature. Should be a space separated list of one or more of "node", "way", "area", "closed" and "relation" (order and case insensitive). |
|Data type					|List of ESRI geometry types to be included in the exported features. Should be a space separated list of one or more of "pt", "ln", "py", "rel" (order	and case insensitive).|
|pt							|Boolean - whether or not the feature includes a point geometry. Calculated by the spreadsheet. Not used by osm2ma.|
|ln							|Boolean - whether or not the feature includes a line geometry. Calculated by the spreadsheet. Not used by osm2ma.|
|py							|Boolean - whether or not the feature includes a polygon geometry. Calculated by the spreadsheet. Not used by osm2ma.|
|rel						|Boolean - whether or not the feature includes a relationship. Calculated by the spreadsheet. Not used by osm2ma.|
