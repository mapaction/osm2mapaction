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

example_pbf = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                           r"testfiles",
                           r"oxfordshire-latest.osm.pbf"
                           )

_workbook = xlrd.open_workbook(os.path.realpath(path_to_fixtures_xls()))
rawconf_good = _workbook.name_map.get("rawconf_good")[0].area2d(clipped=True)
rawconf_invalid_heirarchy = _workbook.name_map.get("rawconf_invalid_heirarchy")[0].area2d(clipped=True)
rawconf_too_few_columns = _workbook.name_map.get("rawconf_too_few_columns")[0].area2d(clipped=True)
rawconf_wrong_column_names = _workbook.name_map.get("rawconf_wrong_column_names")[0].area2d(clipped=True)
rawconf_wrong_column_order = _workbook.name_map.get("rawconf_wrong_column_order")[0].area2d(clipped=True)

scratch_table_good = [
    (u'aeroway', u'aerodrome', u'tran', u'air', u'Node Area', u'pt', u'FALSE'),
    (u'aeroway',u'User defined', u'tran', u'air', u'Node Way', u'pt', u'FALSE'),
    (u'military', u'airfield', u'tran', u'air', u'Node Area', u'pt', u'FALSE'),
    (u'iata', u'User Defined', u'tran', u'air', u'Node Way Area', u'pt', u'FALSE'),
    (u'icao', u'User Defined', u'tran', u'air', u'Node Way Area', u'pt', u'FALSE'),
    (u'boundary', u'user defined', u'admn', u'ad', u'Node Way', u'pt', u'FALSE'),
    (u'aeroway', u'runway', u'tran', u'air', u'Way Area', u'ln', u'FALSE'),
    (u'aeroway', u'User defined', u'tran', u'air', u'Node Way', u'ln', u'FALSE'),
    (u'iata', u'User Defined', u'tran', u'air', u'Node Way Area', u'ln', u'FALSE'),
    (u'icao', u'User Defined', u'tran', u'air', u'Node Way Area', u'ln', u'FALSE'),
    (u'border_type', u'*',u'admn', u'ad', u'Way Area', u'ln', u'FALSE'),
    (u'boundary', u'user defined', u'admn', u'ad', u'Node Way', u'ln', u'FALSE'),
    (u'aeroway', u'aerodrome', u'tran', u'air', u'Node Area', u'py', u'FALSE'),
    (u'aeroway', u'runway', u'tran', u'air', u'Way Area', u'py', u'FALSE'),
    (u'military', u'airfield', u'tran', u'air', u'Node Area', u'py', u'FALSE'),
    (u'iata', u'User Defined', u'tran', u'air', u'Node Way Area', u'py', u'FALSE'),
    (u'icao', u'User Defined', u'tran', u'air', u'Node Way Area', u'py', u'FALSE'),
    (u'boundary', u'administrative', u'admn', u'ad', u'Area', u'py', u'FALSE'),
    (u'boundary', u'political', u'admn', u'ad', u'Area', u'py', u'FALSE'),
    (u'border_type', u'*', u'admn', u'ad', u'Way Area', u'py', u'FALSE'),
    (u'admin_level', u'Number', u'admn', u'ad', u'Area', u'py', u'FALSE'),
    (u'fixme', u'User defined', u'admn', u'ad', u'Node Way Area Relation', u'ln', u'TRUE'),
    (u'source', u'User defined', u'admn', u'ad', u'Node Way Area Relation', u'ln', u'TRUE'),
    (u'source', u'historical', u'admn', u'ad', u'Node Way Area Relation', u'ln', u'TRUE'),
    (u'source:name', u'User defined', u'admn', u'ad', u'Node Way Area Relation', u'ln', u'TRUE'),
    (u'wikipedia', u'URL or article title', u'admn', u'ad', u'Node Way Area Relation', u'ln', u'TRUE'),
    (u'fixme', u'User defined', u'admn', u'ad', u'Node Way Area Relation', u'pt', u'TRUE'),
    (u'source', u'User defined', u'admn', u'ad', u'Node Way Area Relation', u'pt', u'TRUE'),
    (u'source', u'historical', u'admn', u'ad', u'Node Way Area Relation', u'pt', u'TRUE'),
    (u'source:name', u'User defined', u'admn', u'ad', u'Node Way Area Relation', u'pt', u'TRUE'),
    (u'wikipedia', u'URL or article title', u'admn', u'ad', u'Node Way Area Relation', u'pt', u'TRUE'),
    (u'fixme', u'User defined', u'admn', u'ad', u'Node Way Area Relation', u'py', u'TRUE'),
    (u'source', u'User defined', u'admn', u'ad', u'Node Way Area Relation', u'py', u'TRUE'),
    (u'source', u'historical', u'admn', u'ad', u'Node Way Area Relation', u'py', u'TRUE'),
    (u'source:name', u'User defined', u'admn', u'ad', u'Node Way Area Relation', u'py', u'TRUE'),
    (u'wikipedia', u'URL or article title', u'admn', u'ad', u'Node Way Area Relation', u'py', u'TRUE'),
    (u'fixme', u'User defined', u'tran', u'air', u'Node Way Area Relation', u'ln', u'TRUE'),
    (u'source', u'User defined', u'tran', u'air', u'Node Way Area Relation', u'ln', u'TRUE'),
    (u'source', u'historical', u'tran', u'air', u'Node Way Area Relation', u'ln', u'TRUE'),
    (u'source:name', u'User defined', u'tran', u'air', u'Node Way Area Relation', u'ln', u'TRUE'),
    (u'wikipedia', u'URL or article title', u'tran', u'air', u'Node Way Area Relation', u'ln', u'TRUE'),
    (u'fixme', u'User defined', u'tran', u'air', u'Node Way Area Relation', u'pt', u'TRUE'),
    (u'source', u'User defined', u'tran', u'air', u'Node Way Area Relation', u'pt', u'TRUE'),
    (u'source', u'historical', u'tran', u'air', u'Node Way Area Relation', u'pt', u'TRUE'),
    (u'source:name', u'User defined', u'tran', u'air', u'Node Way Area Relation', u'pt', u'TRUE'),
    (u'wikipedia', u'URL or article title', u'tran', u'air', u'Node Way Area Relation', u'pt', u'TRUE'),
    (u'fixme', u'User defined', u'tran', u'air', u'Node Way Area Relation', u'py', u'TRUE'),
    (u'source', u'User defined', u'tran', u'air', u'Node Way Area Relation', u'py', u'TRUE'),
    (u'source', u'historical', u'tran', u'air', u'Node Way Area Relation', u'py', u'TRUE'),
    (u'source:name', u'User defined', u'tran', u'air', u'Node Way Area Relation', u'py', u'TRUE'),
    (u'wikipedia', u'URL or article title', u'tran', u'air', u'Node Way Area Relation', u'py', u'TRUE')
]

temp_scratch_table_osm_only = [
    (u'fixme', u'User defined', u'admn', u'ad', u'Node Way Area Relation', u'ln', u'TRUE'),
    (u'source', u'User defined', u'admn', u'ad', u'Node Way Area Relation', u'ln', u'TRUE'),
    (u'source', u'historical', u'admn', u'ad', u'Node Way Area Relation', u'ln', u'TRUE'),
    (u'source:name', u'User defined', u'admn', u'ad', u'Node Way Area Relation', u'ln', u'TRUE'),
    (u'wikipedia', u'URL or article title', u'admn', u'ad', u'Node Way Area Relation', u'ln', u'TRUE'),
    (u'fixme', u'User defined', u'admn', u'ad', u'Node Way Area Relation', u'pt', u'TRUE'),
    (u'source', u'User defined', u'admn', u'ad', u'Node Way Area Relation', u'pt', u'TRUE'),
    (u'source', u'historical', u'admn', u'ad', u'Node Way Area Relation', u'pt', u'TRUE'),
    (u'source:name', u'User defined', u'admn', u'ad', u'Node Way Area Relation', u'pt', u'TRUE'),
    (u'wikipedia', u'URL or article title', u'admn', u'ad', u'Node Way Area Relation', u'pt', u'TRUE'),
    (u'fixme', u'User defined', u'admn', u'ad', u'Node Way Area Relation', u'py', u'TRUE'),
    (u'source', u'User defined', u'admn', u'ad', u'Node Way Area Relation', u'py', u'TRUE'),
    (u'source', u'historical', u'admn', u'ad', u'Node Way Area Relation', u'py', u'TRUE'),
    (u'source:name', u'User defined', u'admn', u'ad', u'Node Way Area Relation', u'py', u'TRUE'),
    (u'wikipedia', u'URL or article title', u'admn', u'ad', u'Node Way Area Relation', u'py', u'TRUE'),
    (u'fixme', u'User defined', u'tran', u'air', u'Node Way Area Relation', u'ln', u'TRUE'),
    (u'source', u'User defined', u'tran', u'air', u'Node Way Area Relation', u'ln', u'TRUE'),
    (u'source', u'historical', u'tran', u'air', u'Node Way Area Relation', u'ln', u'TRUE'),
    (u'source:name', u'User defined', u'tran', u'air', u'Node Way Area Relation', u'ln', u'TRUE'),
    (u'wikipedia', u'URL or article title', u'tran', u'air', u'Node Way Area Relation', u'ln', u'TRUE'),
    (u'fixme', u'User defined', u'tran', u'air', u'Node Way Area Relation', u'pt', u'TRUE'),
    (u'source', u'User defined', u'tran', u'air', u'Node Way Area Relation', u'pt', u'TRUE'),
    (u'source', u'historical', u'tran', u'air', u'Node Way Area Relation', u'pt', u'TRUE'),
    (u'source:name', u'User defined', u'tran', u'air', u'Node Way Area Relation', u'pt', u'TRUE'),
    (u'wikipedia', u'URL or article title', u'tran', u'air', u'Node Way Area Relation', u'pt', u'TRUE'),
    (u'fixme', u'User defined', u'tran', u'air', u'Node Way Area Relation', u'py', u'TRUE'),
    (u'source', u'User defined', u'tran', u'air', u'Node Way Area Relation', u'py', u'TRUE'),
    (u'source', u'historical', u'tran', u'air', u'Node Way Area Relation', u'py', u'TRUE'),
    (u'source:name', u'User defined', u'tran', u'air', u'Node Way Area Relation', u'py', u'TRUE'),
    (u'wikipedia', u'URL or article title', u'tran', u'air', u'Node Way Area Relation', u'py', u'TRUE'),
]

shpf_list_table_good = [
    (u'wrl_admn_ad_ln_su_osm_pp.shp', u'admn', u'ln',
     u'border_type, boundary, fixme, source, source:name, wikipedia',
     u"'border_type' IS NOT null or 'boundary' IS NOT null"),
    (u'wrl_admn_ad_pt_su_osm_pp.shp', u'admn', u'pt',
     u'boundary, fixme, source, source:name, wikipedia',
     u"'boundary' IS NOT null"),
    (u'wrl_admn_ad_py_su_osm_pp.shp', u'admn', u'py',
     u'admin_level, border_type, boundary, fixme, source, source:name, wikipedia',
     u"'admin_level' IS NOT null or 'border_type' IS NOT null or 'boundary'='administrative' or 'boundary'='political'"),
    (u'wrl_tran_air_ln_su_osm_pp.shp', u'tran', u'ln',
     u'aeroway, iata, icao, fixme, source, source:name, wikipedia',
     u"'aeroway' IS NOT null or 'iata' IS NOT null or 'icao' IS NOT null"),
    (u'wrl_tran_air_pt_su_osm_pp.shp', u'tran', u'pt',
     u'aeroway, iata, icao, military, fixme, source, source:name, wikipedia',
     u"'aeroway' IS NOT null or 'iata' IS NOT null or 'icao' IS NOT null or 'military'='airfield'"),
    (u'wrl_tran_air_py_su_osm_pp.shp', u'tran', u'py',
     u'aeroway, iata, icao, military, fixme, source, source:name, wikipedia',
     u"'aeroway'='aerodrome' or 'aeroway'='runway' or 'iata' IS NOT null or 'icao' IS NOT null or 'military'='airfield'")
]

temp_shpf_list_table_osm_only = [
    (u'wrl_osms_met_ln_su_osm_pp.shp', u'osms', u'ln', u'fixme, source, source:name, wikipedia',
     u"'fixme' IS NOT null or 'source' IS NOT null or 'source:name' IS NOT null or 'wikipedia' IS NOT null"),
    (u'wrl_osms_met_pt_su_osm_pp.shp', u'osms', u'pt', u'fixme, source, source:name, wikipedia',
     u"'fixme' IS NOT null or 'source' IS NOT null or 'source:name' IS NOT null or 'wikipedia' IS NOT null"),
    (u'wrl_osms_met_py_su_osm_pp.shp', u'osms', u'py', u'fixme, source, source:name, wikipedia',
     u"'fixme' IS NOT null or 'source' IS NOT null or 'source:name' IS NOT null or 'wikipedia' IS NOT null"),
    (u'wrl_osms_met_rel_su_osm_pp.shp', u'osms', u'rel', u'fixme, source, source:name, wikipedia',
     u"'fixme' IS NOT null or 'source' IS NOT null or 'source:name' IS NOT null or 'wikipedia' IS NOT null"),

]


"""
A list of which are unsorted, contain duplicates and contains blank strings.
"""
attrib_list_args = [('ffff', 'FALSE'),
                    ('aaaa', 'FALSE'),
                    ('bbbb', 'TRUE' ),
                    ('cccc', 'FALSE'),
                    ('dddd', 'FALSE'),
                    ('',     'FALSE'),
                    ('eeee', 'FALSE'),
                    ('aaaa', 'FALSE'),
                    ('aaaa', 'FALSE')]
attrib_list_result = 'aaaa, cccc, dddd, eeee, ffff, bbbb'

"""
A list of tuples.
Each tuple has as its first item
- A list of tuples of string pairs, representing OSM key value pairs and a "meta" field indicating whether
  the key/value pair represents feature level metadata.
- A string of the resulting selct clause

If the meta field is True for all instances of a particular attribute then the attribute should be
excluded from the attribute list. EG in this case there are two entries for attribute 'a'. In one case the
meta field False therefore 'a' is included. 'z' only occurs with meta value True, therefore is exlcuded
"""
select_clause_args_and_result_pairs = [
    (
        [
            (u"border_type",    u"*",   u'FALSE')
        ],
        u"'border_type' IS NOT null"
    ),
    (
        [
            (u"boundary",	    u"administrative",  u'FALSE'),
            (u"boundary",	    u"maritime",        u'FALSE'),
            (u"boundary",	    u"political",       u'FALSE'),
            (u"boundary",	    u"user defined",    u'FALSE'),
            (u"border_type",    u"*",               u'FALSE')
        ],
        u"'border_type' IS NOT null or 'boundary' IS NOT null"
    ),
    (
        [
            (u"boundary",	    u"administrative",  u'FALSE'),
            (u"boundary",	    u"maritime",        u'FALSE'),
            (u"boundary",	    u"political",       u'FALSE')
        ],
        u"'boundary'='administrative' or 'boundary'='maritime' or 'boundary'='political'"
    ),
    (
        [
            (u"boundary",	    u"administrative",  u'FALSE'),
            (u"boundary",	    u"maritime",        u'FALSE'),
            (u"boundary",	    u"political",       u'FALSE'),
            (u"source",	        u"historical",      u'TRUE'),
            (u"wikipedia",	    u"URL",             u'TRUE')
        ],
        u"'boundary'='administrative' or 'boundary'='maritime' or 'boundary'='political'"
    ),
    (
        [
            (u"admin_level",	    u"Number",      u'FALSE'),
        ],
        u"'admin_level' IS NOT null"
    ),
    (
        [],
        u''
    )
]

output_dir_listing = [
    [
        ".",
        ['admn', 'tran'],
        []
    ],
    [
        "admn",
        [],
        ['wrl_admn_ad_ln_su_osm_pp.dbf', 'wrl_admn_ad_ln_su_osm_pp.prj',
         'wrl_admn_ad_ln_su_osm_pp.shp', 'wrl_admn_ad_ln_su_osm_pp.shx',
         'wrl_admn_ad_pt_su_osm_pp.dbf', 'wrl_admn_ad_pt_su_osm_pp.prj',
         'wrl_admn_ad_pt_su_osm_pp.shp', 'wrl_admn_ad_pt_su_osm_pp.shx',
         'wrl_admn_ad_py_su_osm_pp.dbf', 'wrl_admn_ad_py_su_osm_pp.prj',
         'wrl_admn_ad_py_su_osm_pp.shp', 'wrl_admn_ad_py_su_osm_pp.shx']
    ],
    [
        "tran",
        [],
        ['wrl_tran_air_ln_su_osm_pp.dbf', 'wrl_tran_air_ln_su_osm_pp.prj',
         'wrl_tran_air_ln_su_osm_pp.shp', 'wrl_tran_air_ln_su_osm_pp.shx',
         'wrl_tran_air_pt_su_osm_pp.dbf', 'wrl_tran_air_pt_su_osm_pp.prj',
         'wrl_tran_air_pt_su_osm_pp.shp', 'wrl_tran_air_pt_su_osm_pp.shx',
         'wrl_tran_air_py_su_osm_pp.dbf', 'wrl_tran_air_py_su_osm_pp.prj',
         'wrl_tran_air_py_su_osm_pp.shp', 'wrl_tran_air_py_su_osm_pp.shx']
    ]
]