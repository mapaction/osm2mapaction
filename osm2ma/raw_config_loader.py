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
    _expected_col_names = [
        u'OSM_tag_name',
        u'OSM_tag_value',
        u'Element_icon',
        u'Comment',
        u'Useful_for_MapAction',
        u'Data Category description',
        u'Cat_value',
        u'Date Theme description',
        u'Theme_value',
        u'Conforms_to_MA_Hierarchy',
        u'OSM_Element',
        u'Data type',
        u'pt',
        u'ln',
        u'py',
        u'rel'
    ]

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
        found = colxhi - colxlo
        expected = len(RawConfig._expected_col_names)
        if expected == found:
            return True
        else:
            raise UserWarning("Incorrect number of columns in specified table. Found {f} columns."
                              "Expecting {e} columns".format(f=found, e=expected))

    @staticmethod
    def _raw_config_columns_names_valid(myarea2d):
        sheet_object, rowxlo, rowxhi, colxlo, colxhi = myarea2d
        # get the first row assumed to be column headings
        col_names = sheet_object.row_values(rowxlo, start_colx=colxlo, end_colx=colxhi)
        if col_names == RawConfig._expected_col_names:
            return True
        elif set(col_names) == set(RawConfig._expected_col_names):
            raise UserWarning("The column names in config file were not in the correct order.\n"
                              "The expected column names are expected in this order:\n{e}\n"
                              "The columns names in the config file are in this order :\n{c}\n"
                              .format(e="\t'" + "'\n\t'".join(RawConfig._expected_col_names) + "'\n",
                                      c="\t'" + "'\n\t'".join(col_names) + "'\n")
                              )
        else:
            missing = set(RawConfig._expected_col_names) - set(col_names)
            unnecessary = set(col_names) - set(RawConfig._expected_col_names)
            raise UserWarning("The column names in specified table were not correct.\n"
                              "The expected column names are:\n{e}\n"
                              "These expected columns are missing:\n{m}\n"
                              "These unnecessary columns were found columns:\n{u}\n"
                              .format(e="\t'" + "'\n\t'".join(RawConfig._expected_col_names) + "'\n",
                                      m="\t'" + "'\n\t'".join(missing) + "'\n",
                                      u="\t'" + "'\n\t'".join(unnecessary) + "'\n")
                              )

    def __init__(self, excel_file_path, excel_named_range):
        """
        The constructor will check that the excel file can be read, the named range is in place and that the correct
        column names are specified.
        """
        self._file_path = excel_file_path
        self._named_range = excel_named_range
        area2d = self._get_area2d()
        if RawConfig._raw_config_columns_names_valid(area2d) and RawConfig._raw_config_columns_count_valid(area2d):
            self.area2d = area2d


def raw_config_from_file(file_path):
    _excel = RawConfig(file_path, "xwalk")
    return _excel.get_raw_config()
