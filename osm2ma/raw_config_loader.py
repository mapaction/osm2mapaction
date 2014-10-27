#-------------------------------------------------------------------------------
# Name:        raw_config_loader
# Purpose:
#
# Author:      asmith
#
# Created:     02/09/2014
# Copyright:   (c) asmith 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import xlrd
import os

class RawConfig:

    def get_raw_config(self):
        workbook = xlrd.open_workbook(os.path.realpath(self._filepath))
        namedrange = workbook.name_map.get(self._namedrange)[0]
        return namedrange.area2d(clipped=True)

    def __init__(self, excelfilepath, excelnamedrange):
        self._filepath = excelfilepath
        self._namedrange = excelnamedrange

def rawConfigFromFile(filepath):
    _excel =  RawConfig(filepath, "xwalk")
    return _excel.get_raw_config()
