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


def main(osm_url, workspace, get_all, country):
    """Get files form the given URL and put to the workspace if needed.

    :param str osm_url: url to PBF files (geofabrik)
    :param str workspace: local directory path for output
    :param str/bool get_all: a bool or bool-like string (1, from Arc)
    :param str country: name of the country to be downloaded

    """
    if osm_url[:-1] != r'/':
        osm_url = osm_url + r'/'
    
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
        country = country.replace(" ","-")
        country = country.lower()
        links = re.findall(
            country + '-\d{6}.osm.pbf"', html_source)
        log_message("Found {} files.".format(len(links)))
        sock.close()

        if get_all and get_all in ["1", 1, True]:
            for ix, link in enumerate(links):
                _link = link[:-1]
                debug("File number {} - {}".format(ix, _link))
                url = urlparse.urljoin(osm_url, _link)
                #debug(url)
                
                if os.path.exists(os.path.join(workspace, _link)):
                    log_message("{} already exists".format(
                        os.path.join(workspace, _link)))
                    continue

                log_message("Getting {}".format(url))
                get_pbfs(osm_url, _link)
                log_message("...downloaded")

        # get latest file too
        log_message("Getting latest.osm.pbf")
        get_pbfs(osm_url, country + "-latest.osm.pbf")

        log_message("...finished downloading PBF files")
    except Exception as e:
        log_message("There is a problem: {}".format(e.message))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Gets OSM PBF files from Geofabrik.'
    )
    parser.add_argument(
        '-w', '--workspace',
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
    # positional, rather than option (required)
    parser.add_argument('osm_url')  
    parser.add_argument('country')

    if ARC_ENABLED:
        osm_url = arcpy.GetParameterAsText(0)
        country = arcpy.GetParameterAsText(1)
        workspace = arcpy.GetParameterAsText(2)
        get_all = arcpy.GetParameterAsText(3)
        log_message(", ".join([osm_url,country,workspace,get_all]))

        main(osm_url, workspace, get_all, country)
    else:
        args = parser.parse_args()
        if args.verbosity >= 2:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)

        main(args.osm_url, args.workspace, args.get_all, args.country)
