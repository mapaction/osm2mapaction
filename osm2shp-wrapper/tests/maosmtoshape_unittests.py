import maosmtoshape
import xlrd
import unittest

class TestMAOSMtoShape(unittest.TestCase):

    def setUp(self):
        self.o2s = maosmtoshape

    # example polygon output
    def test_compose_ogr2ogr_cmd_1(self):
        example_str = r"ogr2ogr -overwrite -sql \"SELECT osm_id, osm_way_id," \
        " name, building from 'multipolygons' where 'building'='barn'\" -f "\
        "\"ESRI Shapefile\" oxf_argi_bldg_py_su_osm_pp.shp oxfordshire-latest.osm.pbf -lco "\
        "\"SHP=POLYGON\""

        test_str = self.o2s.compose_ogr2ogr_cmd(geo_extd="oxf",
        data_cat = "argi",
        data_thm = "bldg",
        geom_type = "py",
        scale = "su",
        osm_atrbs = "osm_id, osm_way_id, name, building",
        condition = "'building'='barn'",
        pbf_filename = "oxfordshire-latest.osm.pbf")

    # example line output
    def test_compose_ogr2ogr_cmd_2(self):
        ref_str = r"ogr2ogr -overwrite -sql \"SELECT osm_id, osm_way_id," \
        " name, building from 'lines' where 'building'='barn'\" -f "\
        "\"ESRI Shapefile\" oxf_argi_bldg_ln_su_osm_pp.shp oxfordshire-latest.osm.pbf -lco "\
        "\"SHP=lines\""

        test_str = self.o2s.compose_ogr2ogr_cmd(geo_extd="oxf",
        data_cat = "argi",
        data_thm = "bldg",
        geom_type = "ln",
        scale = "su",
        osm_atrbs = "osm_id, osm_way_id, name, building",
        condition = "'building'='barn'",
        pbf_filename = "oxfordshire-latest.osm.pbf")

        self.assertEqual(test_str.lower(), ref_str.lower())

    # example point output
    @unittest.skip("not implenemted")
    def test_compose_ogr2ogr_cmd_2(self):
        pass

    # example table output
    @unittest.skip("not implenemted")
    def test_compose_ogr2ogr_cmd_3(self):
        pass

    def test_osm_atrb_str_from_list_1(self):
        test_list = ["a", "b", "c"]
        ref_str = "a, b, c"
        result_str = maosmtoshape.str_reduced_from_list(test_list)
        self.assertEqual(result_str, ref_str)

    def test_osm_atrb_str_from_list_2(self):
        test_list = ["b", "a", "c"]
        ref_str = "a, b, c"
        result_str = maosmtoshape.str_reduced_from_list(test_list)
        self.assertEqual(result_str, ref_str)

    def test_osm_atrb_str_from_list_3(self):
        test_list = ["b", "a", "c"]
        ref_str = "b, a, c"
        result_str = maosmtoshape.str_reduced_from_list(test_list)
        self.assertNotEqual(result_str, ref_str)

    def test_compose_condition_clause(self):
        my_key_list = ["building",          "building", "building", "building",     "building", "building"]
        my_val_list = ["farm_auxiliary",    "barn",     "cowshed",  "greenhouse",   "stable",   "sty"]
        example_str = "'building'='barn' OR 'building'='cowshed' OR 'building'='farm_auxiliary' OR 'building'='greenhouse' OR 'building'='stable' OR 'building'='sty'"

        result_str = maosmtoshape.compose_condition_clause(my_key_list, my_val_list)
        self.assertEqual(result_str, example_str)

    def test_load_excel(self):
        mysheet, rowxlo, rowxhi, colxlo, colxhi = maosmtoshape.load_excel("OSM_to_MAv2.xls", "xwalk", r"D:\work\custom-software-group\osm-ma-shp")
        dims = (rowxlo, rowxhi, colxlo, colxhi)

        self.assertIsInstance(mysheet, xlrd.sheet.Sheet, "mysheet not of type xlrd.sheet.Sheet")
        self.assertEqual(dims , (0, 967, 0, 14) , "table size incorrect")

    def test_get_column_indicies(self):
        maosmtoshape.get_column_indicies(
        maosmtoshape.load_excel("OSM_to_MAv2.xls", "xwalk", r"D:\work\custom-software-group\osm-ma-shp"),
        ["a", "b", "c"])

if __name__ == '__main__':
    maosmtoshape = reload(maosmtoshape)
    unittest.main()