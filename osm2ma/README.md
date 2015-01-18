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
