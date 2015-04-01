# This file was originally generated by PyScripter's unitest wizard

import unittest
import os
import xlrd
from configengine import xwalk_from_raw_config
import raw_config_loader
from raw_config_loader import RawConfig
import fixtures


class TestRawConfig(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @unittest.skip("not implemented")
    def test_raw_config_columns_count_valid(self):
        mysheet, rowxlo, rowxhi, colxlo, colxhi = fixtures.rawconf_good
        self.assertTrue(RawConfig._raw_config_columns_count_valid(fixtures.rawconf_good),
                        "Raw config column count for rawconf_good fixture")
        self.assertRaises(UserWarning, RawConfig._raw_config_columns_count_valid, fixtures.rawconf_too_few_columns)
        # "Raw config column count for rawconf_too_few_columns fixture")

    def test_raw_config_columns_names_valid(self):
        self.assertTrue(RawConfig._raw_config_columns_names_valid(fixtures.rawconf_good),
                        "Raw Config column names for rawconf_good fixture")
        self.assertRaises(UserWarning, RawConfig._raw_config_columns_names_valid, fixtures.rawconf_wrong_column_names)
        self.assertRaises(UserWarning, RawConfig._raw_config_columns_names_valid, fixtures.rawconf_wrong_column_order)

    def test_is_raw_config_heirarchy_compliant(self):
        pass


class TestGlobalFunctions(unittest.TestCase):
    """
    This is an intergration test for the entire raw_config_loader module.
    """
    def test_raw_config_from_file(self):
        mysheet, rowxlo, rowxhi, colxlo, colxhi = raw_config_loader.raw_config_from_file(fixtures.path_to_fixtures_xls())
        self.assertIsInstance(mysheet,xlrd.sheet.Sheet, "mysheet is not a string")
        self.assertIsInstance(rowxlo,int, "rowxlo is not a int")
        self.assertIsInstance(rowxhi,int, "rowxhi is not a int")
        self.assertIsInstance(colxlo,int, "colxlo is not a int")
        self.assertIsInstance(colxhi,int, "colxhi is not a int")




def runtests():
    # unittest.main()
    #TestGlobalFunctions().run()
    TestRawConfig().run()
    TestRawConfigIterator().run()

if __name__ == '__main__':
    runtests()
