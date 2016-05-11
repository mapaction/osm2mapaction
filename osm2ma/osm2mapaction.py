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
    schema_scan_strategy = args.schema_scan
    # now do the conversion
    convert(
        excel_full_path, osmconf_path, geoextent_clause, scale_clause, pbf_file,
        output_dir, schema_scan_strategy
    )


def convert(raw_config_path, osmconf_path, geoextent_clause, scale_clause, pbf_file,
            output_dir, schema_scan_strategy):
    """Read the config file and convert PBF file to multiple shapefiles."""
    # Load the raw (denormalised) config from Excel
    _raw_conf = raw_config_from_file(raw_config_path)
    # Normalise the raw config table
    _xwalk = xwalk_from_raw_config(_raw_conf, geoextent_clause, scale_clause)
    # Do the conversion
    batch_convert(_xwalk, pbf_file, osmconf_path, output_dir, schema_scan_strategy)


class SmartFormatter(argparse.HelpFormatter):
#http://stackoverflow.com/a/22157136/4150190
    def _split_lines(self, text, width):
        if text.startswith('R|'):
            return text[2:].splitlines()
        # this is the RawTextHelpFormatter._split_lines
        return argparse.HelpFormatter._split_lines(self, text, width)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Converts the OSM PBF file into ESRI shapefiles & splits'
        'into the different themes and categories (as per the MapAction data'
        'naming convention).',
        formatter_class=SmartFormatter
    )
    parser.add_argument('PBF_path')  # positional, rather than option.
    parser.add_argument(
        '-c', '--config-path',
        default=os.path.join(
            os.getcwd(), '..', 'config_files', 'OSM_to_MA_ascii_v6.xls'),
        help="Path to the OSM_to_MA excel config file (XLS version)"
    )
    parser.add_argument(
        '-f', '--osmconf_path',
        default=os.path.join(
            os.getcwd(), '..', 'config_files', 'osmconf_mapaction.ini'),
        help="Path to the mapaction osmconf.ini file. This ensures all the "+
            "required OSM fields are exposed by the reader."
    )
    parser.add_argument('-g', '--geoextent', default='wrl',
        help="DNC-compliant Geoextent clause, e.g. 'wrl' or ISO country code")

    parser.add_argument('-s', '--scale', default='su',
        help="DNC_compliant Scale clause e.g. 's0', 's1'...")

    parser.add_argument('-o', '--output-dir', default=os.getcwd(),
        help="Top level output dir: subfolders for themes will be created "+
            "below this")

    parser.add_argument('--schema_scan', default='full',
        choices=['full', 'fast', 'none'],
        help='R|What strategy to use to scan input for field widths? \n'+
        'full (scan whole file, smallest .dbfs but slower) \n'+
        'fast (scan first 5000 features, smaller .dbfs but \n'+
        '  risks truncation of later v long values)\n'+
        'none (all fields 80 width -  largest .dbfs)')
    args = parser.parse_args()
    main(args)
