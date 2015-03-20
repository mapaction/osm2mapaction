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
        "ArcPy doesn't seem to be available"
    )


def main(master_pbf_name, bounding_box, clipped_pbf_name,
         osmosis_path):
    bb = bounding_box.split(" ")
    if not bounding_box.startswith(master_pbf_name):
        bounding_box = os.path.join(master_pbf_name, bounding_box)
    if not clipped_pbf_name.startswith(master_pbf_name):
        clipped_pbf_name = os.path.join(master_pbf_name, clipped_pbf_name)
    try:



        args = [
            osmosis_path,
            '--read-pbf', 'file="{}"'.format(master_pbf_name),
            '--bounding-box top=' + bb[3] + ' left=' + bb[0] + ' bottom=' + bb[1] + ' right=' + bb[2],
            '--write-pbf', 'file="{}"'.format(clipped_pbf_name),
        ]
        log_message("running Osmosis using {} ...".format(" ".join(args)))
        os.system(" ".join(args))
        log_message("...finished!")
        log_message(
            "Output file to {}".format(os.path.abspath(clipped_pbf_name)))
    except Exception as e:
        import traceback
        traceback.print_exc()
        log_message("there is a problem: {}".format(e.message))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Runs Osmosis to clip a PBF file by a bounding box"
        " file"
    )
    #master_pbf_name, bounding_box, clipped_pbf_name,osmosis_path
    parser.add_argument(
        '-m', '--masterpbf',
        help='Input OSM PBF file'
        ' (Defaults to current directory)',
        default=os.getcwd()
    )
    parser.add_argument('--verbosity', '-v', action='count')
    parser.add_argument(
        '-b', '--bounding-box',
        help="Bounding Box to clip the OSM pbf file by",
        default='.osc'
    )
    parser.add_argument(
        '-p', '--outputpbf',
        help="Name of resulting clipped PBF file",
        default='clipped.osm.pbf'
    )
    parser.add_argument(
        '-o', '--osmosis-command',
        help="osmosis command (path?) If this is on your PATH then leave "
        "as default (osmosis)",
        default='osmosis'
    )
    # positional, rather than option (required)
    #parser.add_argument('master_pbf')

    if ARC_ENABLED:

        #master_pbf_name, bounding_box, clipped_pbf_name,osmosis_path
        master_pbf_name = arcpy.GetParameterAsText(0)
        bounding_box = arcpy.GetParameterAsText(1)
        clipped_pbf_name = arcpy.GetParameterAsText(2)

        main(
            master_pbf_name, bounding_box, clipped_pbf_name,
            r"c:\osmosis\bin\osmosis"
        )
    else:
        #args = parser.parse_args()
        #-if args.verbosity >= 2:
        #    logging.basicConfig(level=logging.DEBUG)
        #else:
        #    logging.basicConfig(level=logging.INFO)

        #main(
        #    args.workspace, args.master_pbf, args.change_osc,
        #    args.cumulative_file, args.osmosis_command
        debug("Arcpy not enabled")
        #)
