

from osgeo import ogr
from osgeo import gdal
import os
import logging

logging.basicConfig(level=logging.INFO)


# do stuff
def _create_datacat_dir(output_dir, data_cat):
    """Create a per-datacategory subdirectory if required"""
    if os.path.isdir(output_dir):
        cat_dir_path = os.path.join(output_dir, data_cat)
        if not os.path.isdir(cat_dir_path):
            os.mkdir(cat_dir_path)
        return cat_dir_path
    # TODO raise error if invalid input


# do stuff
def _create_new_shpfile(shpf_name, shpf_dir, dest_geom_type, dest_srs):
    logging.info('Creating shapefile: {}'.format(shpf_name))
    # Create the output Layer
    shpf_path = os.path.join(shpf_dir, shpf_name)
    shpf_name = shpf_name.encode('utf-8')
    shpf_path = shpf_path.encode('utf-8')

    shpf_driver = ogr.GetDriverByName("ESRI Shapefile")

    # Remove output shapefile if it already exists
    if os.path.exists(shpf_path):
        shpf_driver.DeleteDataSource(shpf_path)

    # Create the output shapefile
    shp_data_source = shpf_driver.CreateDataSource(shpf_path)
    out_layer = None

    shpf_name = shpf_name.encode('utf-8')
    out_layer = shp_data_source.CreateLayer(
        os.path.splitext(shpf_name)[1], srs=dest_srs, geom_type=dest_geom_type
    )
    #_create_attributes(source_lyr, out_layer, attribs)

    return shp_data_source, out_layer


# do stuff
def _create_attributes(source_lyr, dest_lyr, target_attribs):
    logging.debug('copying attributes')
    # Add input Layer Fields to the output Layer if it is the one we want
    # By copying the field definition from the source it saves us having to worry
    # about data type or string widths etc.
    source_lyr_defn = source_lyr.GetLayerDefn()
    lst_attribs = map(unicode.strip, target_attribs.split(","))
    # print(lst_attribs)
    for i in range(0, source_lyr_defn.GetFieldCount()):
        field_defn = source_lyr_defn.GetFieldDefn(i)
        field_name = field_defn.GetName()
        dest_lyr.CreateField(field_defn)
    #    if field_name in lst_attribs:
    #        dest_lyr.CreateField(field_defn)
    #    else:
    #        print "PBF attrib not required; {}".format(field_name)
    #for attrib in target_attribs.split('r'):
    #    lyr.CreateField(field_defn)


# do stuff
def _copy_features(source_lyr, dest_lyr, target_attribs):
    logging.debug('copying features')
    logging.debug('copying features, value sourceLyr {}'.format(source_lyr))
    logging.debug('copying features, value destLyr {}'.format(dest_lyr))
    logging.debug('copying features, value target_attribs {}'.format(
        target_attribs))

    dest_lyr_defn = dest_lyr.GetLayerDefn()
    logging.debug('copying features, got dest_lyr_defn {}'.format(
        dest_lyr_defn))

    # sourceLyr.ResetReading()
    logging.info(
        'count of features {} in sourceLyr {}'.format(
            source_lyr.GetFeatureCount(force=True), source_lyr.GetName()))
    # Add features to the ouput Layer
    for s_feature in source_lyr:
        # logging.debug('copying features, in loop through sourceLyr')
        # Create output Feature
        d_feature = ogr.Feature(dest_lyr_defn)
        # logging.debug('copying features, got d_feature {}'.format(d_feature))

        # Add field values from input Layer
        for i in range(0, dest_lyr_defn.GetFieldCount()):
            field_defn = dest_lyr_defn.GetFieldDefn(i)
            field_name = field_defn.GetName()
            if field_name in target_attribs:
                d_feature.SetField(
                    dest_lyr_defn.GetFieldDefn(i).GetNameRef(),
                    s_feature.GetField(i)
                )

        # Set geometry as centroid
        geom = s_feature.GetGeometryRef()
        d_feature.SetGeometry(geom.Clone())
        # Add new feature to output Layer
        dest_lyr.CreateFeature(d_feature)


# functional
def get_geom_details(shpf_geom_type):
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


# do stuff
def do_ogr2ogr_process(shp_defn, pbf_data_source, output_dir):
    shpf_name, data_cat, shpf_geom_type, attribs, where_clause = shp_defn
    cat_dir_path = _create_datacat_dir(output_dir, data_cat)
    logging.info(
        'starting ogr2ogr process for shapefile: {}'.format(shpf_name))
    #logging.info(
    #    'using attributes : {}'.format(', '.join(attribs)))
    print "using attributes: {}".format(attribs)

    osm_source_layer, dest_geom = get_geom_details(shpf_geom_type)

    pbf_lyr = pbf_data_source.GetLayerByName(osm_source_layer)
    where_clause = where_clause.encode('utf-8')
    pbf_lyr.SetAttributeFilter(None)
    pbf_lyr.SetAttributeFilter(where_clause)

    pbf_srs = pbf_lyr.GetSpatialRef()

    # if pbf_lyr.GetFeatureCount() was working I'd test to only copy files with
    # > 0 features.
    logging.debug('do_ogr2ogr_process: about to create new shapefile')
    shp_data_source, shp_lyr = _create_new_shpfile(shpf_name, cat_dir_path, dest_geom, pbf_srs, )

    logging.debug('do_ogr2ogr_process: created new shapefile')
    logging.debug('do_ogr2ogr_process: about to copy attributes')
    _create_attributes(pbf_lyr, shp_lyr, attribs)

    logging.debug('do_ogr2ogr_process: copied attributes')
    logging.debug('do_ogr2ogr_process: about to copy features')
    _copy_features(pbf_lyr, shp_lyr, attribs)

    logging.debug('do_ogr2ogr_process: copied features')
    # cmd_str = compose_ogr2ogr_cmd(
    #     data_cat, geom_type, attribs, where_clause, pbf_file, shpf_name,
    #     cat_dir_path)
    shp_data_source.Destroy()


# do stuff
def batch_convert(xwalk, pbf_file, output_dir):
    gdal.UseExceptions()
    gdal.SetConfigOption("OGR_INTERLEAVED_READING", "YES")

    osmconf_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), r'osmconf.ini')
    gdal.SetConfigOption('OSM_CONFIG_FILE', osmconf_path)    # Open input PBF driver
    pbf_driver = ogr.GetDriverByName("OSM")
    pbf_data_source = pbf_driver.Open(pbf_file, 0)

    # Do conversation for each shpFile
    for shpDefinition in xwalk:
        logging.debug(shpDefinition[0])
        do_ogr2ogr_process(shpDefinition, pbf_data_source, output_dir)

    # Close input PBF file
    pbf_data_source.Destroy()
