"""
Fixtures used in unittests for osm2mapaction

Author:      asmith
Created:     23/01/2015
Copyright:   MapAction 2015
Licence:     GPL v3
"""

rawconf_good = [
    ["OSM_tag_name", "OSM_tag_value", "Element_icon", "Comment", "Useful_for_MapAction", "Data Category description",
     "Cat_value", "Date Theme description", "Theme_value", "Conforms_to_MA_Hierarchy", "OSM_Element", "Data type", "pt",
     "ln", "py", "rel"],
    ["aeroway", "aerodrome", "Node Area", "An Aerodrome (UK), Airport (US)", "Y", "Transport", "tran",
     "Airport / Airstrip", "air", "#N/A", "Node Area", "pt py", "pt", "#N/A", "py", "#N/A"],
    ["aeroway", "runway", "Way Area",
     "A strip of land kept clear and set aside for aeroplanes to take off from and land on. (Other languages)", "Y",
     "Transport", "tran", "Airport / Airstrip", "air", "#N/A", "Way Area", "ln py", "#N/A", "ln", "py", "#N/A"],
    ["aeroway", "User defined", "Node Way", "All commonly used values according to Taginfo", "Y", "Transport", "tran",
     "Airport / Airstrip", "air", "#N/A", "Node Way", "pt ln", "pt", "ln", "#N/A", "#N/A"],
    ["military", "airfield", "Node Area", "A place where military planes take off and land", "Y", "Transport", "tran",
     "Airport / Airstrip", "air", "#N/A", "Node Area", "pt py", "pt", "#N/A", "py", "#N/A"],
    ["iata", "User Defined", "Node Way Area", "IATA International airport codes", "Y", "Transport", "tran",
     "Airport / Airstrip", "air", "#N/A", "Node Way Area", "pt ln py", "pt", "ln", "py", "#N/A"],
    ["icao", "User Defined", "Node Way Area", "ICAO International airport codes", "Y", "Transport", "tran",
     "Airport / Airstrip", "air", "#N/A", "Node Way Area", "pt ln py", "pt", "ln", "py", "#N/A"],
    ["boundary", "administrative", "Area",
     "An administrative boundary. Subdivisions of areas/territories/jurisdictions recognised by governments or other organisations for administrative purposes. These range from large groups of nation states right down to small administrative districts and suburbs, as indicated by the 'admin_level=*' combo tag", "Y", "Admin", "admn", "Administrative boundary (various levels)", "ad", "#N/A", "Area", "py", "#N/A", "#N/A", "py", "#N/A"],
    ["boundary", "maritime", "Area", "Maritime boundaries", "Y", "Admin", "admn",
     "Administrative boundary (various levels)", "ad", "#N/A", "Area", "py", "#N/A", "#N/A", "py", "#N/A"],
    ["boundary", "political", "Area", "Electoral boundaries", "Y", "Admin", "admn",
     "Administrative boundary (various levels)", "ad", "#N/A", "Area", "py", "#N/A", "#N/A", "py", "#N/A"],
    ["border_type", "*", "Way Area",
     "To distinguish between types of boundary where admin_level isn't enough. Used in several different ways e.g in maritime contexts", "Y", "Admin", "admn", "Administrative boundary (various levels)", "ad", "#N/A", "Way Area", "ln py", "#N/A", "ln", "py", "#N/A"],
    ["boundary", "user defined", "Node Way", "All commonly used values according to Taginfo", "Y", "Admin", "admn",
     "Administrative boundary (various levels)", "ad", "#N/A", "Node Way", "pt ln", "pt", "ln", "#N/A", "#N/A"],
    ["admin_level", "Number", "Area",
     "Applies to boundary=administrative and is usually in the range 1 to 10, except for Germany where it might be 11 - see boundary.", "Y", "Admin", "admn", "Administrative boundary (various levels)", "ad", "#N/A", "Area", "py", "#N/A", "#N/A", "py", "#N/A"],
    ["fixme", "User defined", "Node Way Area Relation",
     "A description to yourself or to other mappers of a (possible) error in the map", "Y", "Open Street Map Specific",
     "osms", "Metadata", "met", "#N/A", "Node Way Area Relation", "pt ln py rel", "pt", "ln", "py", "rel"],
    ["source", "User defined", "Node Way Area Relation", "", "Y", "Open Street Map Specific", "osms", "Metadata", "met",
     "#N/A", "Node Way Area Relation", "pt ln py rel", "pt", "ln", "py", "rel"],
    ["source", "historical", "Node Way Area Relation", "from out-of-copyright mapping or other historical document",
     "Y", "Open Street Map Specific", "osms", "Metadata", "met", "#N/A", "Node Way Area Relation", "pt ln py rel", "pt",
     "ln", "py", "rel"],
    ["source:name", "User defined", "Node Way Area Relation",
     "Source used to gather name information; e.g., for street names", "Y", "Open Street Map Specific", "osms",
     "Metadata", "met", "#N/A", "Node Way Area Relation", "pt ln py rel", "pt", "ln", "py", "rel"],
    ["wikipedia", "URL or article title", "Node Way Area Relation", "Wikipedia article associated with an object", "Y",
     "Open Street Map Specific", "osms", "Metadata", "met", "#N/A", "Node Way Area Relation", "pt ln py rel", "pt",
     "ln", "py", "rel"]
]

# """
# Correct column names
# """
# rawconf_col_names = [
#     u'OSM_tag_name',
#     u'OSM_tag_value',
#     u'Element_icon ',
#     u'Comment ',
#     u'Useful_for_MapAction',
#     u'Data Category description',
#     u'Cat_value',
#     u'Date Theme description',
#     u'Theme_value',
#     u'Conforms_to_MA_Hierarchy',
#     u'OSM_Element',
#     u'Data type',
#     u'pt',
#     u'ln',
#     u'py',
#     u'rel'
# ]


"""Contains an invalid nesting of the Data Category and Data Theme hierarchy"""
#rawconf_invalid_heirarchy =

#xWalk_good =


def mock_from_table_xwalk(table):
    """
    Create a mock XWalk data structure from a simple table.
    :param table:
    :return:
    """
    pass