#-------------------------------------------------------------------------------
# Name:        osm2ma
# Purpose:     This is the shell
#
# Author:      asmith
#
# Created:     01/09/2014
# Copyright:   (c) asmith 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from configengine import xWalkFromRawConfig
from raw_config_loader import rawConfigFromFile
from ogrwrapper import batch_convert
import logging

logging.basicConfig(level=logging.DEBUG)

def main():
    # Nasty hack until I write some proper code to bring in parameters
    _excel_full_path = r"D:\work\custom-software-group\code\mapaction-toolbox\OSMChangeToolbox\osm2ma\testfiles\OSM_to_MA_ascii.xls"
    # _excel_full_path = r"D:\work\custom-software-group\code\mapaction-toolbox\OSMChangeToolbox\osm2ma\testfiles\OSM_to_MA_short.xls"
    _geoextent_clause = u'wrl'
    _scale_clause = u'su'
    _pbf_file = r"D:\work\custom-software-group\code\mapaction-toolbox\OSMChangeToolbox\osm2ma\testfiles\oxfordshire-latest.osm.pbf"
    _output_dir = r"D:\work\custom-software-group\code\mapaction-toolbox\OSMChangeToolbox\osm2ma\testfiles\output"
    # now do the conversion
    convert(_excel_full_path, _geoextent_clause, _scale_clause, _pbf_file, _output_dir)


def convert(raw_config_path, geoextent_clause, scale_clause, pbf_file, output_dir):
    # Load the raw (denormalised) config from Excel
    _raw_conf = rawConfigFromFile(raw_config_path)
    # Normalise the raw config table
    _xwalk = xWalkFromRawConfig(_raw_conf, geoextent_clause, scale_clause)
    # Do the conversion
    batch_convert(_xwalk, pbf_file, output_dir)

if __name__ == '__main__':
    main()
