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
import os
import argparse
import logging

from configengine import xwalk_from_raw_config
from raw_config_loader import raw_config_from_file
from ogrwrapper import batch_convert

logging.basicConfig(level=logging.DEBUG)


def main(args):
    """Parse commandline parameters and call convert()."""
    excel_full_path = args.config_path
    osmconf_path = args.osmconf_path

    geoextent_clause = args.geoextent
    scale_clause = args.scale
    pbf_file = args.PBF_path

    output_dir = args.output_dir

    # now do the conversion
    convert(
        excel_full_path, osmconf_path, geoextent_clause, scale_clause, pbf_file,
        output_dir
    )


def convert(raw_config_path, osmconf_path, geoextent_clause, scale_clause, pbf_file,
            output_dir):
    """Read the config file and convert PBF file to multiple shapefiles."""
    # Load the raw (denormalised) config from Excel
    _raw_conf = raw_config_from_file(raw_config_path)
    # Normalise the raw config table
    _xwalk = xwalk_from_raw_config(_raw_conf, geoextent_clause, scale_clause)
    # Do the conversion
    batch_convert(_xwalk, pbf_file, osmconf_path, output_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Converts the OSM PBF file into ESRI shapefiles & splits'
        'into the different themes and categories (as per the MapAction data'
        'naming convention).'
    )
    parser.add_argument('PBF_path')  # positional, rather than option.
    parser.add_argument(
        '-c', '--config-path',
        default=os.path.join(
            os.getcwd(), '..', 'config_files', 'OSM_to_MA_ascii_v6.xlsx')
    )
    parser.add_argument(
        '-f', '--osmconf_path',
        default=os.path.join(
            os.getcwd(), '..', 'config_files', 'osmconf_mapaction.ini')
    )
    parser.add_argument('-g', '--geoextent', default='wrl')
    parser.add_argument('-s', '--scale', default='su')
    parser.add_argument('-o', '--output-dir', default=os.getcwd())
    args = parser.parse_args()
    main(args)
