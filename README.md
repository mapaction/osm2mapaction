# OpenStreetMap to MapAction

This repository contains a series of scripts which:

1. Enable the MapAction support base to take OSM data from the geofabrik server
   (as a master PBF file). The scripts for doing this are `0_get_OSM_files.py`,
   followed by `1_create_difference_SB.py`. These should be run in from ArcGIS'
   toolbox (see `OSMChangeToolbox.tbx`), but will be able to be run from the
   CLI in due course.

2. Provide a method for the MapAction field team to apply the latest change
   file to the master. The script to achieve this is
   `2_append_difference_FT.py`. This too can be run from the toolbox.

3. Convert the OSM PBF file into ESRI shapefiles and split into the different
   themes and categories (as per the MapAction data naming convention). The
   script for this is `osm2ma/osm2mapaction.py`. Currently this only runs from
   the CLI and yo ucan give it a `-h` to see what the options/arguments are. An
   Arc Toolbox wrapper will be made for this in due course.

## Environment

### Part 1 and 2 (download PBFs, create changesets & apply)

For parts 1 and 2, you will need either ArcPy *or* just a regular python
environment and CLI. The scripts will failover to CLI if ArcPy is not present
and should work in both Windows and \*nix environments.

For parts 1 and 2 you will need java installed and osmosis:

[http://wiki.openstreetmap.org/wiki/Osmosis#Latest_stable_version]

On **Windows** this should be placed at `C:\osmosis`.

On **\*nix** this can be anywhere, and either added to your `PATH` environment
variable or passed on the CLI with `-o`.

### Part 3 (convert to SHP, rename)

For part 3 you will need OSGeo and/or `gdal`.
