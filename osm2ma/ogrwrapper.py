

from osgeo import ogr
from osgeo import gdal
import os
import logging

logging.basicConfig(level=logging.INFO)

# do stuff
def _create_datacat_dir(output_dir, data_cat):
    """Create a per-datacategory subdirectory if required"""
    if os.path.isdir(output_dir):
        cat_dir_path = os.path.join(output_dir,data_cat)
        if not os.path.isdir(cat_dir_path):
            os.mkdir(cat_dir_path)
        return cat_dir_path
    # TODO raise error if invalid input

# do stuff
def _create_new_shpfile(shpf_name, shpf_dir, dest_geom_type, dest_srs):
    logging.info('Creating shapefile: {}'.format(shpf_name))
    # Create the output Layer
    shpf_path = os.path.join( shpf_dir, shpf_name )
    shpDriver = ogr.GetDriverByName("ESRI Shapefile")

    # Remove output shapefile if it already exists
    if os.path.exists(shpf_path):
        shpDriver.DeleteDataSource(shpf_path)

    # Create the output shapefile
    shpDataSource = shpDriver.CreateDataSource(shpf_path)
    # out_lyr_name = os.path.splitext( os.path.split( outShapefile )[1] )[0]
    # This should be just the shpfile name without extension - need to check
    outLayer = None

    shpf_name = shpf_name.encode('utf-8')
    outLayer = shpDataSource.CreateLayer(os.path.splitext(shpf_name)[1], srs=dest_srs, geom_type=dest_geom_type )
    # outLayer = shpDataSource.CreateLayer(name=u'wrl_util_bdg_py_su_osm_pp')
    return shpDataSource, outLayer

# do stuff
def _copy_attributes(sourceLyr, destLyr, target_attribs):
    logging.debug('copying attributes')
    # Add input Layer Fields to the output Layer if it is the one we want
    sLayerDefn = sourceLyr.GetLayerDefn()
    for i in range(0, sLayerDefn.GetFieldCount()):
        fieldDefn = sLayerDefn.GetFieldDefn(i)
        fieldName = fieldDefn.GetName()
        if fieldName in target_attribs:
            destLyr.CreateField(fieldDefn)

# do stuff
def _copy_features(sourceLyr, destLyr, target_attribs):
    logging.debug('copying features')
    logging.debug('copying features, value sourceLyr {}'.format(sourceLyr))
    logging.debug('copying features, value destLyr {}'.format(destLyr))
    logging.debug('copying features, value target_attribs {}'.format(target_attribs))

    destLyrDefn = destLyr.GetLayerDefn()
    logging.debug('copying features, got destLyrDefn {}'.format(destLyrDefn))

    # sourceLyr.ResetReading()
    logging.info('count of features {} in sourceLyr {}'.format(sourceLyr.GetFeatureCount(force=True),  sourceLyr.GetName()))
    # Add features to the ouput Layer
    for sFeature in sourceLyr:
        # logging.debug('copying features, in loop through sourceLyr')
        # Create output Feature
        dFeature = ogr.Feature(destLyrDefn)
        # logging.debug('copying features, got dFeature {}'.format(dFeature))

        # Add field values from input Layer
        for i in range(0, destLyrDefn.GetFieldCount()):
            fieldDefn = destLyrDefn.GetFieldDefn(i)
            fieldName = fieldDefn.GetName()
            if fieldName in target_attribs:
                dFeature.SetField(destLyrDefn.GetFieldDefn(i).GetNameRef(), sFeature.GetField(i))

        # Set geometry as centroid
        geom = sFeature.GetGeometryRef()
        dFeature.SetGeometry(geom.Clone())
        # Add new feature to output Layer
        destLyr.CreateFeature(dFeature)


# functional
def get_geom_details(shpf_geom_type):
    logging.debug('get geometery details')
    # TODO What about the "multilinestrings" layer?
    if shpf_geom_type == "pt":
        source_geom = "POINTS"
        source_layer = "points"
        dest_geom = ogr.wkbPoint
    elif shpf_geom_type == "ln":
        source_geom = "LINES"
        source_layer = "lines"
        dest_geom = ogr.wkbLineString
    elif shpf_geom_type == "py":
        source_geom = "POLYGON"
        source_layer = "multipolygons"
        dest_geom = ogr.wkbMultiPolygon
    elif shpf_geom_type == "rel":
        source_geom = "UNKNOWN"
        source_layer = "other_relations"
        dest_geom = ogr.wkbUnknown
    # TODO raise invalid parameter exception
    else:
        raise ValueError()

    return source_layer, dest_geom

# do stuff
def do_ogr2ogr_process(shpDefinition, pbfDataSource, output_dir):
    shpf_name, data_cat, shpf_geom_type, attribs, where_clause = shpDefinition
    cat_dir_path = _create_datacat_dir(output_dir, data_cat)
    logging.debug('starting ogr2ogr process for shapefile: {}'.format(shpf_name))

    osm_source_layer, dest_geom = get_geom_details(shpf_geom_type)

    pbfLayer = pbfDataSource.GetLayerByName(osm_source_layer)
    where_clause = where_clause.encode('utf-8')
    pbfLayer.SetAttributeFilter(None)
    pbfLayer.SetAttributeFilter(where_clause)

    pbfSRS = pbfLayer.GetSpatialRef()

    # if pbfLayer.GetFeatureCount() was working I'd test to only copy files with > 0 features.
    logging.debug('do_ogr2ogr_process: about to create new shapefile')
    shpDataSource, shpLayer = _create_new_shpfile(shpf_name, cat_dir_path, dest_geom, pbfSRS)
    logging.debug('do_ogr2ogr_process: created new shapefile')
    logging.debug('do_ogr2ogr_process: about to copy attributes')
    _copy_attributes(pbfLayer, shpLayer, attribs)
    logging.debug('do_ogr2ogr_process: copied attributes')
    logging.debug('do_ogr2ogr_process: about to copy features')
    _copy_features(pbfLayer, shpLayer, attribs)
    logging.debug('do_ogr2ogr_process: copied features')
    # cmd_str = compose_ogr2ogr_cmd(data_cat, geom_type, attribs, where_clause, pbf_file, shpf_name, cat_dir_path)
    shpDataSource.Destroy()


# do stuff
def batch_convert(xwalk, pbf_file, output_dir):
    gdal.UseExceptions()
    gdal.SetConfigOption("OGR_INTERLEAVED_READING", "YES")
    # Open input PBF driver
    pbfDriver = ogr.GetDriverByName("OSM")
    pbfDataSource = pbfDriver.Open(pbf_file, 0)

    # Do conversation for each shpFile
    for shpDefinition in xwalk:
        logging.debug(shpDefinition[0])
        do_ogr2ogr_process(shpDefinition, pbfDataSource, output_dir)

    # Close input PBF file
    pbfDataSource.Destroy()
