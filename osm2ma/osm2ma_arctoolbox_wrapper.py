import argparse
import os
import logging

log = logging.getLogger(__name__)
ARC_ENABLED = False


def debug(message):
    log_message(message, level=log.debug)


def log_message(message, level=None):
    """Log using stdlib, and to ArcPy's message stack, if available."""
    level = level or log.info
    level(message)
    if ARC_ENABLED:
        arcpy.AddMessage(message)
        arcpy.GetMessages()

try:
    import arcpy
    ARC_ENABLED = True
except ImportError:
    ARC_ENABLED = False
    debug(
        "ArcPy doesn't seem to be available. Continuing with standard library."
    )

python_path = r"C:\OSGeo4W64\OSGeo4W.bat python"
python_script = r"C:\Github\osm2mapaction\osm2ma\osm2mapaction.py"


def main(python_path, python_script, path_to_excel, path_to_pbf, path_to_output, geoextent, scale):
    if not python_script.startswith(python_path):
        python_script = os.path.join(python_path, python_script)
    if not path_to_excel.startswith(python_path):
        path_to_excel = os.path.join(python_path, path_to_excel)
    if not path_to_pbf.startswith(python_path):
        path_to_pbf = os.path.join(python_path, path_to_pbf)
    if not path_to_output.startswith(python_path):
        path_to_output = os.path.join(python_path, path_to_output)
    if not geoextent.startswith(python_path):
        geoextent = os.path.join(python_path, geoextent)
    if not scale.startswith(python_path):
        scale = os.path.join(python_path, scale)

    try:
        args = [
            python_path,
            'osm2mapaction.py',
            path_to_excel,
            path_to_pbf,
            path_to_output,
            geoextent,
            scale,
        ]

        log_message("running osm2mapaction.py {} ...".format(" ".join(args)))
        os.system(" ".join(args))
        log_message("...finished!")
        log_message(
            "Output file to {}".format(os.path.abspath(path_to_output)))
    except Exception as e:
        import traceback
        traceback.print_exc()
        log_message("there is a problem: {}".format(e.message))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Runs osm2mapaction.py'
    )
    parser.add_argument(
        '-p', '--python path',
        help='path to where OSGeo4W Python instance sits',
        default=r'C:\OSGeo4W64\OSGeo4W.bat python'
    )
    parser.add_argument('--verbosity', '-v', action='count')
    parser.add_argument(
        '-pe', '--path to excel',
        help="Path to Excel config file",
        default=r'C:\Github\osm2mapaction\osm2ma\testfiles\OSM_to_MAv2.xls'
    )
    parser.add_argument(
        '-pp', '--path to pbf',
        help="Path to the PBF file which you want to convert",
        default=r'c:\github\osm2mapaction\osm2ma\testfiles\oxfordshire-latest.osm.pbf'
    )
    parser.add_argument(
        '-po', '--output path',
        help="path to output directory",
        default=os.getcwd()
    )
    parser.add_argument('-ge', '--geoextent', choices=('wrl',), default='wrl')
    parser.add_argument('-s', '--scale', choices=('su',), default='su')
    args = parser.parse_args()
    main(args)


if ARC_ENABLED:
    path_to_excel = arcpy.GetParameterAsText(0)
    path_to_pbf = arcpy.GetParameterAsText(1)
    path_to_output = arcpy.GetParameterAsText(2)
    geoextent = arcpy.GetParameterAsText(3)
    scale = arcpy.GetParameterAsText(4)


    main(python_path, python_script, path_to_excel, path_to_pbf, path_to_output, geoextent, scale)

