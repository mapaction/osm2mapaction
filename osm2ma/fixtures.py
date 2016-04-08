"""
Fixtures used in unittests for osm2mapaction

Author:      asmith
Created:     23/01/2015
Copyright:   MapAction 2015
Licence:     GPL v3
"""

import os
import xlrd


def path_to_fixtures_xls():
    test_script_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(test_script_path, r"testfiles", r"fixtures.xls")

_workbook = xlrd.open_workbook(os.path.realpath(path_to_fixtures_xls()))
rawconf_good = _workbook.name_map.get("rawconf_good")[0].area2d(clipped=True)
rawconf_invalid_heirarchy = _workbook.name_map.get("rawconf_invalid_heirarchy")[0].area2d(clipped=True)
rawconf_too_few_columns = _workbook.name_map.get("rawconf_too_few_columns")[0].area2d(clipped=True)
rawconf_wrong_column_names = _workbook.name_map.get("rawconf_wrong_column_names")[0].area2d(clipped=True)
rawconf_wrong_column_order = _workbook.name_map.get("rawconf_wrong_column_order")[0].area2d(clipped=True)

scratch_table_good = [
    (u'aeroway', u'aerodrome', u'tran', u'air', u'Node Area', u'pt'),
    (u'aeroway',u'User defined', u'tran', u'air', u'Node Way', u'pt'),
    (u'military', u'airfield', u'tran', u'air', u'Node Area', u'pt'),
    (u'iata', u'User Defined', u'tran', u'air', u'Node Way Area', u'pt'),
    (u'icao', u'User Defined', u'tran', u'air', u'Node Way Area', u'pt'),
    (u'boundary', u'user defined', u'admn', u'ad', u'Node Way', u'pt'),
    (u'fixme', u'User defined', u'osms', u'met', u'Node Way Area Relation', u'pt'),
    (u'source', u'User defined', u'osms', u'met', u'Node Way Area Relation', u'pt'),
    (u'source', u'historical', u'osms', u'met', u'Node Way Area Relation', u'pt'),
    (u'source:name', u'User defined', u'osms', u'met', u'Node Way Area Relation', u'pt'),
    (u'wikipedia', u'URL or article title', u'osms', u'met', u'Node Way Area Relation', u'pt'),
    (u'aeroway', u'runway', u'tran', u'air', u'Way Area', u'ln'),
    (u'aeroway', u'User defined', u'tran', u'air', u'Node Way', u'ln'),
    (u'iata', u'User Defined', u'tran', u'air', u'Node Way Area', u'ln'),
    (u'icao', u'User Defined', u'tran', u'air', u'Node Way Area', u'ln'),
    (u'border_type', u'*',u'admn', u'ad', u'Way Area', u'ln'),
    (u'boundary', u'user defined', u'admn', u'ad', u'Node Way', u'ln'),
    (u'fixme', u'User defined', u'osms', u'met', u'Node Way Area Relation', u'ln'),
    (u'source', u'User defined', u'osms', u'met', u'Node Way Area Relation', u'ln'),
    (u'source', u'historical', u'osms', u'met', u'Node Way Area Relation', u'ln'),
    (u'source:name', u'User defined', u'osms', u'met', u'Node Way Area Relation', u'ln'),
    (u'wikipedia', u'URL or article title', u'osms',u'met', u'Node Way Area Relation', u'ln'),
    (u'aeroway', u'aerodrome', u'tran', u'air', u'Node Area', u'py'),
    (u'aeroway', u'runway', u'tran', u'air', u'Way Area', u'py'),
    (u'military', u'airfield', u'tran', u'air', u'Node Area', u'py'),
    (u'iata', u'User Defined', u'tran', u'air', u'Node Way Area', u'py'),
    (u'icao', u'User Defined', u'tran', u'air', u'Node Way Area', u'py'),
    (u'boundary', u'administrative', u'admn', u'ad', u'Area', u'py'),
    (u'boundary', u'maritime', u'admn', u'ad', u'Area', u'py'),
    (u'boundary', u'political', u'admn', u'ad', u'Area', u'py'),
    (u'border_type', u'*', u'admn', u'ad', u'Way Area', u'py'),
    (u'admin_level', u'Number', u'admn', u'ad', u'Area', u'py'),
    (u'fixme', u'User defined', u'osms', u'met', u'Node Way Area Relation', u'py'),
    (u'source', u'User defined', u'osms', u'met', u'Node Way Area Relation', u'py'),
    (u'source', u'historical', u'osms', u'met', u'Node Way Area Relation', u'py'),
    (u'source:name', u'User defined', u'osms', u'met', u'Node Way Area Relation', u'py'),
    (u'wikipedia', u'URL or article title', u'osms', u'met', u'Node Way Area Relation', u'py'),
    (u'fixme', u'User defined', u'osms', u'met', u'Node Way Area Relation', u'rel'),
    (u'source', u'User defined', u'osms', u'met', u'Node Way Area Relation', u'rel'),
    (u'source', u'historical', u'osms', u'met', u'Node Way Area Relation', u'rel'),
    (u'source:name', u'User defined', u'osms', u'met', u'Node Way Area Relation', u'rel'),
    (u'wikipedia', u'URL or article title', u'osms', u'met', u'Node Way Area Relation', u'rel')
]

shpf_list_table_good = [
    (u'wrl_admn_ad_ln_su_osm_pp.shp', u'admn', u'ln', u'border_type, boundary', u"'border_type' IS NOT null or 'boundary' IS NOT null"),
    (u'wrl_admn_ad_pt_su_osm_pp.shp', u'admn', u'pt', u'boundary', u"'boundary' IS NOT null"),
    (u'wrl_admn_ad_py_su_osm_pp.shp', u'admn', u'py', u'admin_level, border_type, boundary', u"'admin_level' IS NOT null or 'border_type' IS NOT null or 'boundary'='administrative' or 'boundary'='maritime' or 'boundary'='political'"),
    (u'wrl_osms_met_ln_su_osm_pp.shp', u'osms', u'ln', u'fixme, source, source:name, wikipedia', u"'fixme' IS NOT null or 'source' IS NOT null or 'source:name' IS NOT null or 'wikipedia' IS NOT null"),
    (u'wrl_osms_met_pt_su_osm_pp.shp', u'osms', u'pt', u'fixme, source, source:name, wikipedia', u"'fixme' IS NOT null or 'source' IS NOT null or 'source:name' IS NOT null or 'wikipedia' IS NOT null"),
    (u'wrl_osms_met_py_su_osm_pp.shp', u'osms', u'py', u'fixme, source, source:name, wikipedia', u"'fixme' IS NOT null or 'source' IS NOT null or 'source:name' IS NOT null or 'wikipedia' IS NOT null"),
    (u'wrl_osms_met_rel_su_osm_pp.shp', u'osms', u'rel', u'fixme, source, source:name, wikipedia', u"'fixme' IS NOT null or 'source' IS NOT null or 'source:name' IS NOT null or 'wikipedia' IS NOT null"),
    (u'wrl_tran_air_ln_su_osm_pp.shp', u'tran', u'ln', u'aeroway, iata, icao', u"'aeroway' IS NOT null or 'iata' IS NOT null or 'icao' IS NOT null"),
    (u'wrl_tran_air_pt_su_osm_pp.shp', u'tran', u'pt', u'aeroway, iata, icao, military', u"'aeroway' IS NOT null or 'iata' IS NOT null or 'icao' IS NOT null or 'military'='airfield'"),
    (u'wrl_tran_air_py_su_osm_pp.shp', u'tran', u'py', u'aeroway, iata, icao, military', u"'aeroway'='aerodrome' or 'aeroway'='runway' or 'iata' IS NOT null or 'icao' IS NOT null or 'military'='airfield'")
]


"""
A list of which are unsorted, contain duplicates and contains blank strings.
"""
attrib_list_args = ['f', 'a', 'b', 'c', 'd', '', 'e', 'a', 'a']
# Fixture changed to reflect the fact that attriblist is now parsed to a set
attrib_list_result = set(['a', 'b', 'c', 'd', 'e', 'f'])

"""
A list of tuples.
Each tuple has as its first item
- A list of tuples of string pairs, representing OSM key value pairs
- A string of the resulting selct clause
"""
select_clause_args_and_result_pairs = [
    (
        [
            (u"border_type",    u"*")
        ],
        u"'border_type' IS NOT null"
    ),
    (
        [
            (u"boundary",	    u"administrative"),
            (u"boundary",	    u"maritime"),
            (u"boundary",	    u"political"),
            (u"boundary",	    u"user defined"),
            (u"border_type",    u"*")
        ],
        #u"'border_type' IS NOT null or 'boundary' IS NOT null"
        u"(border_type IS NOT null AND border_type NOT IN ('', 'None')) OR "+
        u"(boundary IS NOT null AND boundary NOT IN ('', 'None'))"
    ),
    (
        [
            (u"boundary",	    u"administrative"),
            (u"boundary",	    u"maritime"),
            (u"boundary",	    u"political")
        ],
        u"'boundary'='administrative' or 'boundary'='maritime' or 'boundary'='political'"
    ),
    (
        [
            (u"admin_level",	    u"Number"),
        ],
        #u"'admin_level' IS NOT null"
    ),
    (
        [],
        u''
    )
]
