"""
osm2mapaction converts OSM and PBF files, to shapefiles according to
MapAction's data naming convention.

Usage:
osm2mapaction
-p <full path to PBF file>
-c <full path to config file (excel)
-g <geoextent clause>
-s <scale clause>
-o <full path to output directory>

Author:      asmith
Created:     01/09/2014
Copyright:   MapAction 2014
Licence:     GPL v3
"""

import logging

from configengine import xwalk_from_raw_config
from raw_config_loader import raw_config_from_file
from ogrwrapper import batch_convert

logging.basicConfig(level=logging.DEBUG)


def main():
    """
    Parse commandline parameters and call convert()

    Raise exception if parameter is missing or invalid.
    """
    # TODO Raise exception if parameter is missing or invalid.
    # Nasty hack until I write some proper code to bring in parameters
    _excel_full_path = (
        r"D:\work\custom-software-group\code\mapaction-toolbox"
        r"\OSMChangeToolbox\osm2ma\testfiles\OSM_to_MA_ascii.xls"
    )

    # _excel_full_path = r"D:\work\custom-software-group\code
    # r"\mapaction-toolbox\OSMChangeToolbox\osm2ma\testfiles"
    # r"\OSM_to_MA_short.xls"
    _geoextent_clause = u'wrl'
    _scale_clause = u'su'
    _pbf_file = (
        r"D:\work\custom-software-group\code\mapaction-toolbox"
        r"\OSMChangeToolbox\osm2ma\testfiles\oxfordshire-latest.osm.pbf"
    )

    _output_dir = (r"D:\work\custom-software-group\code\mapaction-toolbox"
                   r"\OSMChangeToolbox\osm2ma\testfiles\output")

    # now do the conversion
    convert(_excel_full_path, _geoextent_clause,
            _scale_clause, _pbf_file, _output_dir)


def convert(raw_config_path, geoextent_clause,
            scale_clause, pbf_file, output_dir):
    """
    Read the config file and convert PBF file to multiple shapefiles.
    """
    # Load the raw (denormalised) config from Excel
    _raw_conf = raw_config_from_file(raw_config_path)
    # Normalise the raw config table
    _xwalk = xwalk_from_raw_config(_raw_conf, geoextent_clause, scale_clause)
    # Do the conversion
    batch_convert(_xwalk, pbf_file, output_dir)


if __name__ == '__main__':
    main()
