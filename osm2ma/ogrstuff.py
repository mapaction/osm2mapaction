#-------------------------------------------------------------------------------
# Name:        ogrstuff
# Purpose:
#
# Author:      asmith
#
# Created:     02/09/2014
# Copyright:   (c) asmith 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from osgeo import ogr
import os, sys

class OGRStuff:

    def main( field_name_target ):
        # Get the input Layer
        inShapefile = "~/DATA/SHAPES/KC_ADMIN/parcel_address/parcel_address.shp"
        inDriver = ogr.GetDriverByName("ESRI Shapefile")
        inDataSource = inDriver.Open(inShapefile, 0)
        inLayer = inDataSource.GetLayer()
        inLayer.SetAttributeFilter("minor = 'HYDR'")



        # Create the output LayerS
        outShapefile = os.path.join( os.path.split( inShapefile )[0], "ogr_api_filter.shp" )
        outDriver = ogr.GetDriverByName("ESRI Shapefile")

        # Remove output shapefile if it already exists
        if os.path.exists(outShapefile):
            outDriver.DeleteDataSource(outShapefile)

        # Create the output shapefile
        outDataSource = outDriver.CreateDataSource(outShapefile)
        out_lyr_name = os.path.splitext( os.path.split( outShapefile )[1] )[0]
        outLayer = outDataSource.CreateLayer( out_lyr_name, geom_type=ogr.wkbMultiPolygon )

        # Add input Layer Fields to the output Layer if it is the one we want
        inLayerDefn = inLayer.GetLayerDefn()
        for i in range(0, inLayerDefn.GetFieldCount()):
            fieldDefn = inLayerDefn.GetFieldDefn(i)
            fieldName = fieldDefn.GetName()
            if fieldName not in field_name_target:
                continue
            outLayer.CreateField(fieldDefn)

        # Get the output Layer's Feature Definition
        outLayerDefn = outLayer.GetLayerDefn()

        # Add features to the ouput Layer
        for inFeature in inLayer:
            # Create output Feature
            outFeature = ogr.Feature(outLayerDefn)

            # Add field values from input Layer
            for i in range(0, outLayerDefn.GetFieldCount()):
                fieldDefn = outLayerDefn.GetFieldDefn(i)
                fieldName = fieldDefn.GetName()
                if fieldName not in field_name_target:
                    continue

                outFeature.SetField(outLayerDefn.GetFieldDefn(i).GetNameRef(),
                    inFeature.GetField(i))

            # Set geometry as centroid
            geom = inFeature.GetGeometryRef()
            outFeature.SetGeometry(geom.Clone())
            # Add new feature to output Layer
            outLayer.CreateFeature(outFeature)

        # Close DataSources
        inDataSource.Destroy()
        outDataSource.Destroy()

if __name__ == '__main__':

    if len( sys.argv ) < 2:
        print "[ ERROR ]: you need to pass at least one arg -- the field_names to include in output"
        sys.exit(1)

    main( sys.argv[1:] )