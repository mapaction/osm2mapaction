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


def main(workspace, master_pbf_name, latest_pbf_name, change_osc_name,
         osmosis_path):
    if not master_pbf_name.startswith(workspace):
        master_pbf_name = os.path.join(workspace, master_pbf_name)
    if not latest_pbf_name.startswith(workspace):
        latest_pbf_name = os.path.join(workspace, latest_pbf_name)
    if not change_osc_name.startswith(workspace):
        change_osc_name = os.path.join(workspace, change_osc_name)
    try:
        args = [
            osmosis_path,
            '--read-pbf', 'file="{}"'.format(latest_pbf_name),
            '--read-pbf', 'file="{}"'.format(master_pbf_name),
            '--derive-change',
            '--write-xml-change', 'file="{}"'.format(change_osc_name),
        ]

        log_message("running Osmosis using {} ...".format(" ".join(args)))
        os.system(" ".join(args))
        log_message("...finished!")
        log_message(
            "Output file to {}".format(os.path.abspath(change_osc_name)))
    except Exception as e:
        import traceback
        traceback.print_exc()
        log_message("there is a problem: {}".format(e.message))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Creates a bat file and runs against osmosis to generate'
        'an OSC file (containing the changes only)'
    )
    parser.add_argument(
        '-w', '--workspace',
        help='Directory containing existing PBFs/place new files.'
        ' (Defaults to current directory)',
        default=os.getcwd()
    )
    parser.add_argument('--verbosity', '-v', action='count')
    parser.add_argument(
        '-l', '--latest-pbf',
        help="Name of latest PBF file (if not latest.osm.pbf)",
        default='latest.osm.pbf'
    )
    parser.add_argument(
        '-c', '--change-osc',
        help="Name of change OSC file (if not planetdiff-latest.osc)",
        default='planetdiff-latest.osc'
    )
    parser.add_argument(
        '-o', '--osmosis-command',
        help="osmosis command (path?) If this is on your PATH then leave "
        "as default (osmosis)",
        default='osmosis'
    )
    # positional, rather than option (required)
    parser.add_argument('master_pbf')
    if ARC_ENABLED:
        workspace = arcpy.GetParameterAsText(0)
        master_pbf_name = arcpy.GetParameterAsText(1)
        latest_pbf_name = arcpy.GetParameterAsText(2)
        change_osc_name = arcpy.GetParameterAsText(3)
        main(
            workspace, master_pbf_name, latest_pbf_name, change_osc_name,
            r"'C:\Progra~2\osmosis\bin\osmosis'"
        )
    else:
        args = parser.parse_args()
        if args.verbosity >= 2:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)

        main(
            args.workspace, args.master_pbf, args.latest_pbf, args.change_osc,
            args.osmosis_command
        )
