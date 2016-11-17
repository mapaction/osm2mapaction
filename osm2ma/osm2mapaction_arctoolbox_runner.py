import argparse
import os
import logging

# This script simply provides some plumbing to run the osm2mapaction script on a mapaction laptop 
# environment, providing fixed / known paths to config files and a simpler order-based set of 
# parameters that can be easily called by ArcToolbox
log = logging.getLogger(__name__)

ARC_ENABLED = False

# Some constants for running in a mapaction laptop environment to save the user 
# needing to specify these each time
# Using the shortened filename versions or else the whole thing disappears down a plughole of 
# quoting doom owing to the spaces and the multiple stacks of calling the final python script
OSGEO4W_ENV_PATH = r'C:\OSGeo4W64\OSGeo4W.bat'
OSM2MA_PATH = r'C:\Progra~2\MapAction\osm2mapaction\osm2ma\osm2mapaction.py'
EXCEL_CONF_PATH = r'C:\Progra~2\MapAction\osm2mapaction\config_files\OSM_to_MA_ascii_v6.xls'
OSMCONF_PATH = r'C:\Progra~2\MapAction\osm2mapaction\config_files\osmconf_mapaction.ini'
                 
SCHEMA_SCAN_MODE = 'full' # or fast or none


def debug(message):
    log_message(message, level=log.debug)


def log_message(message, level=None):
    """Log using stdlib, and to ArcPy's message stack, if available."""
    level = level or log.info
    level(message)
    if ARC_ENABLED:
        if level != log.error:
            arcpy.AddMessage(message)
            arcpy.GetMessages()
        else:
            arcpy.AddError(message)
            raise arcpy.ExecuteError

try:
    import arcpy
    ARC_ENABLED = True
except ImportError:
    ARC_ENABLED = False
    debug(
        "ArcPy doesn't seem to be available. Continuing with standard library."
    )

def callOSM2MA(pbfFile, outDir, xlsConfigPath, osmConfPath, geoExtClause, scaleClause):
    try:
        args = [
            '-c {}'.format(xlsConfigPath),
            '-f {}'.format(osmConfPath),
            '-g {}'.format(geoExtClause),
            '-s {}'.format(scaleClause),
            '-o {}'.format(outDir),
            '--schema_scan {}'.format(SCHEMA_SCAN_MODE),
            pbfFile
        ]
        log_message('*'*40)
        log_message("OSGEO4W Environment Path is {}".format(OSGEO4W_ENV_PATH))
        log_message("OSM2MA Python Code Path is {}".format(OSM2MA_PATH))
        log_message("Calling OSM2Mapaction using {} ...".format(" ".join(args)))
        log_message('*'*40)
        log_message("Ctrl-C in the process window that opens if you need to cancel!")
        log_message('*'*40)
        fullCommand = "{0} python {1} {2}".format(OSGEO4W_ENV_PATH, OSM2MA_PATH, " ".join(args))
        retval = os.system(fullCommand)
        if retval == 0:
            log_message("... finished!")
        else:
            log_message("Failed with command "+fullCommand)
            log_message("Return code was "+str(retval))
            raise Exception('An error occurred, please check the OSM2Mapaction files are in the '+
                'standard locations or else run this tool from the command line specifying the locations.')
    except Exception as e:
        log_message("ERROR: {}".format(e.message), log.error)

if __name__ == '__main__':
    if ARC_ENABLED:
        pbfFile = arcpy.GetParameterAsText(0)
        outDir = arcpy.GetParameterAsText(1)
        geoExtClause = arcpy.GetParameterAsText(2)
        scaleClause = arcpy.GetParameterAsText(3)
        callOSM2MA(pbfFile, outDir, EXCEL_CONF_PATH, OSMCONF_PATH, geoExtClause, scaleClause)