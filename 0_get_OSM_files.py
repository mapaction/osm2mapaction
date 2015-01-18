import argparse
import urlparse
import os
import urllib2
import re
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


def main(osm_url, workspace, get_all):
    """Get files form the given URL and put to the workspace if needed.

    :param str osm_url: url to PBF files (geofabrik)
    :param str workspace: local directory path for output
    :param str/bool get_all: a bool or bool-like string (1, from Arc)

    """
    def get_pbfs(url, fname):
        """Get PBF files from geofabrik."""
        sock = urllib2.urlopen(urlparse.urljoin(url, fname))
        local_filename = os.path.join(workspace, fname)
        with open(local_filename, "wb") as local_file:
            local_file.write(sock.read())

    if not os.path.exists(workspace):
        log_message("The working directory doesn't exist, attempting create.")
        os.mkdir(workspace)

    log_message("Reading and downloading the PBF files...")
    try:
        sock = urllib2.urlopen(osm_url)
        html_source = sock.read()
        links = re.findall(
            '\d{4}.\d{2}.\d{2}.\d{2}.\d{2}.osm.pbf"', html_source)
        log_message("Found {} files.".format(len(links)))
        sock.close()

        if get_all and get_all in ["1", 1, True]:
            for ix, link in enumerate(links[:1]):
                _link = link[:-1]
                debug("File number {} - {}".format(ix, link))
                url = urlparse.urljoin(osm_url, _link)

                if os.path.exists(os.path.join(workspace, _link)):
                    log_message("{} already exists".format(
                        os.path.join(workspace, _link)))
                    continue

                log_message("Getting {}".format(url))
                get_pbfs(osm_url, _link)

        # get latest file too
        log_message("Getting latest.osm.pbf")
        get_pbfs(osm_url, "latest.osm.pbf")

        log_message("...finished downloading PBF files")
    except Exception as e:
        log_message("There is a problem: {}".format(e.message))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Gets OSM PBF files from Geofabrik.'
    )
    parser.add_argument(
        '-o', '--output-dir',
        help='Directory containing existing PBFs/place new files.'
        ' (Defaults to current directory)',
        default=os.getcwd()
    )
    parser.add_argument('--verbosity', '-v', action='count')
    parser.add_argument(
        '-a', '--get-all',
        help="Get all files found at Geofabrik url. (Default false)",
        action='store_true',
        default=False
    )
    parser.add_argument('osm_url')  # positional, rather than option (required)

    if ARC_ENABLED:
        osm_url = arcpy.GetParameterAsText(0)
        workspace = arcpy.GetParameterAsText(1)
        get_all = arcpy.GetParameterAsText(2)
        main(osm_url, workspace, get_all)
    else:
        args = parser.parse_args()
        if args.verbosity >= 2:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)

        main(args.osm_url, args.output_dir, args.get_all)
