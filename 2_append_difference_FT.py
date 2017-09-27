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


def main(workspace, master_pbf_name, change_osc_name, cumulative_pbf_name,
         osmosis_path):
    if not master_pbf_name.startswith(workspace):
        master_pbf_name = os.path.join(workspace, master_pbf_name)
    if not change_osc_name.startswith(workspace):
        change_osc_name = os.path.join(workspace, change_osc_name)
    if not cumulative_pbf_name.startswith(workspace):
        cumulative_pbf_name = os.path.join(workspace, cumulative_pbf_name)
    try:
        args = [
            osmosis_path,
            '--read-xml-change', 'file="{}"'.format(change_osc_name),
            '--read-pbf', 'file="{}"'.format(master_pbf_name),
            '--apply-change',
            '--write-pbf', 'file="{}"'.format(cumulative_pbf_name),
        ]
        log_message("running Osmosis using {} ...".format(" ".join(args)))
        os.system(" ".join(args))
        log_message("...finished!")
        log_message(
            "Output file to {}".format(os.path.abspath(cumulative_pbf_name)))
    except Exception as e:
        import traceback
        traceback.print_exc()
        log_message("there is a problem: {}".format(e.message))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Runs Osmosis to append the OSC file to the master OSM.pbf"
        " file"
    )
    parser.add_argument(
        '-w', '--workspace',
        help='Directory containing existing PBFs/place new files.'
        ' (Defaults to current directory)',
        default=os.getcwd()
    )
    parser.add_argument('--verbosity', '-v', action='count')
    parser.add_argument(
        '-c', '--change-osc',
        help="Name of change OSC file (if not planetdiff-latest.osc)",
        default='planetdiff-latest.osc'
    )
    parser.add_argument(
        '-r', '--cumulative-file',
        help="Name of resulting cumulative file (if not cumulative.osm.pbf)",
        default='cumulative.osm.pbf'
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
        change_osc_name = arcpy.GetParameterAsText(2)
        cumulative_pbf_name = arcpy.GetParameterAsText(3)
        main(
            workspace, master_pbf_name, change_osc_name, cumulative_pbf_name,
            r"c:\Progra~2\osmosis\bin\osmosis"
        )
    else:
        args = parser.parse_args()
        if args.verbosity >= 2:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)

        main(
            args.workspace, args.master_pbf, args.change_osc,
            args.cumulative_file, args.osmosis_command
        )
