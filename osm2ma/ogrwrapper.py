

from osgeo import ogr
from osgeo import gdal
import os
import logging
import json

logging.basicConfig(level=logging.INFO)

def _create_datacat_dir(output_dir, data_cat):
    """Create a per-datacategory subdirectory if required"""
    if os.path.isdir(output_dir):
        cat_dir_path = os.path.join(output_dir, data_cat)
        if not os.path.isdir(cat_dir_path):
            os.mkdir(cat_dir_path)
        return cat_dir_path
    # TODO raise error if invalid input


def _create_new_shpfile(shpf_name, shpf_dir, dest_geom_type, dest_srs):
    """Creates an output shapefile (but does add any attributes)"""
    logging.info('Creating shapefile: {}'.format(shpf_name))
    # Create the output Layer
    shpf_path = os.path.join(shpf_dir, shpf_name)
    shpf_driver = ogr.GetDriverByName("ESRI Shapefile")

    # Remove output shapefile if it already exists
    if os.path.exists(shpf_path):
        shpf_driver.DeleteDataSource(shpf_path)

    # Create the output shapefile
    shp_data_source = shpf_driver.CreateDataSource(shpf_path)
    # out_lyr_name = os.path.splitext( os.path.split( outShapefile )[1] )[0]
    # This should be just the shapefile name without extension - need to check
    out_layer = None

    shpf_name = shpf_name.encode('utf-8')
    out_layer = shp_data_source.CreateLayer(
        os.path.splitext(shpf_name)[1], srs=dest_srs, geom_type=dest_geom_type
    )
    # out_layer = shpDataSource.CreateLayer(name=u'wrl_util_bdg_py_su_osm_pp')
    return shp_data_source, out_layer

def _copy_attributes(source_lyr, dest_lyr, target_attribs):
    ''' Creates in dest_lyr the attribs named in target_attribs, iif they exist in source_lyr.

    target_attribs is now a set rather than a single comma-separated string.
    This helps avoid the wrong attribs being copied over.
    '''
    logging.debug('copying attributes')
    logging.debug(str(target_attribs))

    # Add input Layer Fields to the output Layer if it is the one we want
    source_lyr_defn = source_lyr.GetLayerDefn()
    for i in range(0, source_lyr_defn.GetFieldCount()):
        field_defn = source_lyr_defn.GetFieldDefn(i)
        field_name = field_defn.GetName()
        # This "if x in y" check doesn't work well if y is a single string
        # e.g. if source attribs are
        #   ["osm_id", "id", "preying_mantid", "man"]
        # and target attribs is
        #   "preying_mantid, mandible_size"
        # then we will end up copying over id, preying_mantid, and man,
        # even though the only one of them we wanted was "preying_mantid"
        # Whereas now target_attribs is a set of separate strings that won't
        # happen.
        # It is also now easier for client ogrwrapper code to add extra attribs
        # e.g. name that weren't specified in the excel config file
        if field_name in target_attribs:
            dest_lyr.CreateField(field_defn)

def _copy_features(source_lyr, dest_lyr, target_attribs):
    '''Copy the specified attributed features from an input layer, with query set, to an output
    '''
    logging.debug('copying features')
    logging.debug('copying features, value sourceLyr {}'.format(source_lyr))
    logging.debug('copying features, value destLyr {}'.format(dest_lyr))
    logging.debug('copying features, value target_attribs {}'.format(
        target_attribs))

    dest_lyr_defn = dest_lyr.GetLayerDefn()
    src_lyr_defn = source_lyr.GetLayerDefn()
    logging.debug('copying features, got dest_lyr_defn {}'.format(
        dest_lyr_defn))

    source_lyr.ResetReading()

    # track the number of features we copy this way, since the GetFeatureCount
    # doesn't work
    n = 0

    # dest lyr only has the target attribs already so we don't need to recheck
    destFields = [dest_lyr_defn.GetFieldDefn(i).GetName()
        for i in range(dest_lyr_defn.GetFieldCount())]

    # there was a bug here, using the same index i to get the field from the
    # source and destination layers. The destination layer doesn't have all
    # the fields of the source, so the indices aren't the same. This resulted
    # in fields getting values from the wrong input fields.

    # Instead, map the destination to the source field indices:
    destSrcMap = {
        i : src_lyr_defn.GetFieldIndex(destFields[i])
            for i in range(len(destFields))
    }

    for s_feature in source_lyr:
        # Create output Feature
        d_feature = ogr.Feature(dest_lyr_defn)

        # Add field values from input Layer
        for dIdx, sIdx in destSrcMap.iteritems():
            if sIdx != -1:
                d_feature.SetField(dIdx, s_feature.GetField(sIdx))
            # else the name requested isn't found in the source.
            # This would happen if it just doesn't occur in the present data file
            # so isn't necessarily a problem. May be worth logging them though in
            # case it's indicative of a misspelling in the config file.

        # Set geometry as centroid
        geom = s_feature.GetGeometryRef()
        d_feature.SetGeometry(geom.Clone())
        # Add new feature to output Layer
        dest_lyr.CreateFeature(d_feature)
        n += 1
        # s_feature.Destroy() # maybe ought to do this?
    return n

##def _copy_features_interleaved(source_lyr, dest_lyr, target_attribs):
##    '''As for _copy_features but disposes of features, to (hopefully) fix interleaved reading
##
##    See http://lists.osgeo.org/pipermail/gdal-dev/2014-April/038634.html for sample code.
##    This isn't working: it may be that there is a bug or limitation in reading interleaved
##    when the scenario is more "complicated" i.e. a definition query is in place.
##    '''
##    thereIsDataInLayer = True
##    n=0
##    dest_lyr_defn = dest_lyr.GetLayerDefn()
##
##    while thereIsDataInLayer:
##        thereIsDataInLayer = False
##        s_feature = source_lyr.GetNextFeature()
##        while(s_feature is not None):
##            thereIsDataInLayer = True
##            d_feature = ogr.Feature(dest_lyr_defn)
##
##            # Add field values from input Layer
##            for i in range(0, dest_lyr_defn.GetFieldCount()):
##                field_defn = dest_lyr_defn.GetFieldDefn(i)
##                field_name = field_defn.GetName()
##                if field_name in target_attribs:
##                    d_feature.SetField(
##                        dest_lyr_defn.GetFieldDefn(i).GetNameRef(),
##                        s_feature.GetField(i)
##                    )
##
##            # Set geometry as centroid
##            geom = s_feature.GetGeometryRef()
##            d_feature.SetGeometry(geom.Clone())
##            # Add new feature to output Layer
##            dest_lyr.CreateFeature(d_feature)
##            n += 1
##
##            s_feature.Destroy()
##            s_feature = source_lyr.GetNextFeature()
##    return n

def get_geom_details(shpf_geom_type):
    """Map geom type in config file (e.g. "pt") to ogr layer name and geom type"""
    logging.debug('get geometery details')
    # TODO What about the "multilinestrings" layer?
    # FIXME: source_geom is assigned to but never used
    if shpf_geom_type == "pt":
        source_geom = "POINTS"  # noqa
        source_layer = "points"
        dest_geom = ogr.wkbPoint
    elif shpf_geom_type == "ln":
        source_geom = "LINES"  # noqa
        source_layer = "lines"
        dest_geom = ogr.wkbLineString
    elif shpf_geom_type == "py":
        source_geom = "POLYGON"  # noqa
        source_layer = "multipolygons"
        dest_geom = ogr.wkbMultiPolygon
    elif shpf_geom_type == "rel":
        source_geom = "UNKNOWN"  # noqa
        source_layer = "other_relations"
        dest_geom = ogr.wkbUnknown
    # TODO raise invalid parameter exception
    else:
        raise ValueError()

    return source_layer, dest_geom

def parseAndCheckWhereClause(jsonWhere, source_lyr):
    ''' Create a where clause that only contains fields that are actually present.

    The PBF driver doesn't expose fields that aren't actually present in the data
    even if they are specified in the osmconf.ini file. Furthermore it appears that
    if such a field is mentioned in the where clause then the entire where
    clause is ignored and all the data from that layer (points / lines / polygons)
    are returned.

    So we need to clean the where clause that was generated from the Excel file
    to only mention fields that are present in our current dataset. This required
    refactoring the where clause generation in configengine to return something
    that can be more easily converted to a structured object again here i.e. json.
    The actual where clause string is then generated here at "runtime" once we know
    what is in the current pbf dataset.
    '''
    # the where clause is returned from configengine's in memory DB as a string
    # which is a serialized view of the dict, so recreate the dictionary from it
    where_clause_dict = json.loads(jsonWhere)
    source_lyr_defn = source_lyr.GetLayerDefn()
    # get all the fieldnames we actually have in the data
    sourceFieldNames = [source_lyr_defn.GetFieldDefn(i).GetName()
        for i in range(source_lyr_defn.GetFieldCount())]
    # only keep the parts of the where clause that refer to a field that we
    # actually have in the data
    relevantClauses = [' or '.join(where_clause_dict[colName])
        for colName in where_clause_dict.keys()
        if colName in sourceFieldNames]
    # return it as an or-separated string again
    if len(relevantClauses) > 0:
        return ' or '.join(relevantClauses)
    else:
        # if we don't have anything for the where clause then we won't want a
        # shapefile to be created, returning false will cause this.
        return '1 = 0'

def parseAndCheckAttribs(jsonAttribs):
    ''' Create a comma-separated list of attributes for the output shapefile.

    The DB (configengine) code now returns a set object (json-encoded to a string).
    See copyAttributes for justification of why.
    Here we just recreate the set from the json.
    '''
    # json lib can't automatically serialize a set
    listAttrs = json.loads(jsonAttribs)
    setAttrs = set(listAttrs)
    return setAttrs

def do_ogr2ogr_process(shp_defn, pbf_data_source, output_dir):
    ''' Generate one output shapefile from the PBF using the provided specification
    '''
    shpf_name, data_cat, shpf_geom_type, attribs, where_clause = shp_defn

    logging.info("".rjust(70,"_"))
    logging.debug(
        'starting ogr2ogr process for shapefile: {}'.format(shpf_name))

    # create output subdirectory if not already there
    cat_dir_path = _create_datacat_dir(output_dir, data_cat)
    # get type points/lines/polys
    osm_source_layer, dest_geom = get_geom_details(shpf_geom_type)
    pbf_lyr = pbf_data_source.GetLayerByName(osm_source_layer)

    whereClauseStr = str(parseAndCheckWhereClause(where_clause, pbf_lyr))
    logging.info("Where clause is " + whereClauseStr)

    #where_clause = str(where_clause) #.encode('utf-8')
    pbf_srs = pbf_lyr.GetSpatialRef()

    # if pbf_lyr.GetFeatureCount() was working I'd test to only copy files with
    # > 0 features.
    logging.debug('do_ogr2ogr_process: about to create new shapefile')
    shp_data_source, shp_lyr = _create_new_shpfile(
        shpf_name, cat_dir_path, dest_geom, pbf_srs)
    logging.debug('do_ogr2ogr_process: created new shapefile')

    logging.debug('do_ogr2ogr_process: about to copy attributes')
    attribSet = parseAndCheckAttribs(attribs)
    # Add the name attribute to the output
    # TODO: maybe specify "always copy" attributes on the commandline and carry
    # through to here?
    attribSet.add("name")
    _copy_attributes(pbf_lyr, shp_lyr, attribSet)
    logging.debug('do_ogr2ogr_process: copied attributes')

    logging.debug('do_ogr2ogr_process: about to copy features')
    pbf_lyr.SetAttributeFilter(None)
    pbf_lyr.SetAttributeFilter(whereClauseStr)
    nCopied = _copy_features(pbf_lyr, shp_lyr, attribSet)
    # "Correct" approach seems to make no difference.
    # Looks like if we want / need to use the interleaved reading,
    # we would have to read the entire source layer (points, lines, polygons)
    # unfiltered into an intermediate format (sqlite?) then apply the query to that
    # before writing to shapefile.
    #nCopied = _copy_features_interleaved(pbf_lyr, shp_lyr, attribs)
    logging.debug('do_ogr2ogr_process: copied features')

    createdFilePath = shp_data_source.GetName()
    shp_data_source.Destroy()

    # As we were unable to pre-test the number of features, instead we delete
    # the output shapefile if the return value indicates it was empty
    if nCopied == 0:
        shpf_driver = ogr.GetDriverByName("ESRI Shapefile")
        shpf_driver.DeleteDataSource(createdFilePath)
        logging.info("Removed empty shapefile output!")
    else:
        logging.info("Copied {0} features!".format(nCopied))


def batch_convert(xwalk, pbf_file, osmconf_path, output_dir):
    '''Generate each output shapefile that is specified in xwalk in turn, from pbf_file.
    '''
    gdal.UseExceptions()

    # This option probably "should" be set for safety in reading large files but
    # as it is, it causes NO data to be copied except for points. Turning it off
    # actually seems to work with the test oxfordshire file at least.
    # Turning it on causes only point data to be copied, even with the "correct"
    # reading function that destroys features before moving on.
    #gdal.SetConfigOption("OGR_INTERLEAVED_READING", "YES")

    # Tell OGR where to find the custom osmconf ini file
    gdal.SetConfigOption("OSM_CONFIG_FILE", osmconf_path)

    # Open input PBF driver
    pbf_driver = ogr.GetDriverByName("OSM")

    # Do conversion for each shpFile
    for shpDefinition in xwalk:
        # reopen the file for each reading to be sure we are resetting the
        # read position. Otherwise we are relying on the changing definition
        # query to reset the read position which "feels" a bit risky
        pbf_data_source = pbf_driver.Open(pbf_file, 0)
        logging.debug(shpDefinition[0])
        do_ogr2ogr_process(shpDefinition, pbf_data_source, output_dir)
        pbf_data_source.Destroy()
