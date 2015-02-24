"""
raw_config_loader reads a suitably formatted Excel sheet and returns a table.
The table returned is an (as far as possible) an exact replica of the content
Excel file. Minimal attempt is made in this module to verify that the
spreadsheet is in a suitable/correct format.

The only requirements enforced in this module are:
- The table in the spreadsheet must have a named range called "xwalk"

Any other requirements of this table are specified or enforced elsewhere.


Author:      asmith
Created:     01/09/2014
Copyright:   MapAction 2014
Licence:     GPL v3
"""

import os
import xlrd


class RawConfig:
    """
    A RawConfig object holds the reference to a particular named range in a
    particular excel spreadsheet.
    """
    def get_raw_config(self):
        return self.area2d

    def _get_area2d(self):
        """
        Open the Excel file and return the specificed Named Range.

        The returned value in the in form specified here:
        https://secure.simplistix.co.uk/svn/xlrd/trunk/xlrd/doc/xlrd.html?p=4966#__init__.Name.area2d-method
        """

        # TODO catch invalid file path, or non-excel file
        workbook = xlrd.open_workbook(os.path.realpath(self._file_path))
        namedrange = workbook.name_map.get(self._named_range)[0]
        return namedrange.area2d(clipped=True)

    @staticmethod
    def _raw_config_columns_count_valid(myarea2d):
        sheet_object, rowxlo, rowxhi, colxlo, colxhi = myarea2d
        return 16 == colxhi - colxlo

    @staticmethod
    def _raw_config_columns_names_valid(myarea2d):
        sheet_object, rowxlo, rowxhi, colxlo, colxhi = myarea2d
        # get the first row assumed to be column headings
        col_names = sheet_object.row_values(rowxlo, start_colx=colxlo, end_colx=colxhi)
        return col_names

    def __init__(self, excel_file_path, excel_named_range):
        """
        Currently the constructor does not check that the file path is valid,
        nor does it check that the named range is present.
        """
        self._file_path = excel_file_path
        self._named_range = excel_named_range
        self.area2d = self._get_area2d()



    # RawConfig.is_table_schema_raw_config(self.rawconf_good), "Raw Config table schema OK")
    # self.assertFalse(RawConfig.is_table_schema_raw_config(self.rawconf_too_few_columns), "Raw Config table; too few columns")
    # self.assertFalse(RawConfig.is_table_schema_raw_config(self.rawconf_wrong_column_names),

def raw_config_from_file(file_path):
    _excel = RawConfig(file_path, "xwalk")
    return _excel.get_raw_config()
