
#first created by Chris Ewing, MapAction, 4th May 2014
#1_create_difference_SB.py - creates a bat file and runs against osmosis to generate
#an OSC file (containing the changes only)

import arcpy
from arcpy import env
import subprocess
import os
import urllib2
import re
import logging

log = logging.getLogger(__name__)

def print_str_to_console_and_arcpy(message):
    """Prints a string to the console, and also adds it to ArcPy's message stack"""
    log.debug(message)
    arcpy.AddMessage(message)

#set the paths for the software
gnupth = r"C:\GnuWin32\bin\wget.exe"
osmopt = r"c:\osmosis\bin"
osmopth = r"c:\osmosis\bin\osmosis"
svnzpth = r"C:\program files\7-zip\7z.exe"
javapth = r"C:\Windows\System32\java.exe"


##osmURL = r"http://labs.geofabrik.de/haiyan/" #arcpy.GetParameterAsText(0)
##in_workspace   = r"d:\Tools\toolbox\labs.geofabrik.de\haiyan"  #arcpy.GetParameterAsText(1)
##master_PBF = "2014-03-26-20-17.osm.pbf" #arcpy.GetParameterAsText(2)
##master_PBFF = in_workspace + "\\" + master_PBF
##latest_PBF = "latest.osm.pbf"
##latest_PBFF = in_workspace + "\\" + latest_PBF
##change_OSC = "planetdiff-latest.osc"
##change_OSCC = in_workspace + "\\" + change_OSC

in_workspace = arcpy.GetParameterAsText(0)
master_PBF = arcpy.GetParameterAsText(1)
master_PBFF = os.path.join(in_workspace,master_PBF)
latest_PBF = arcpy.GetParameterAsText(2)
latest_PBFF = os.path.join(in_workspace,latest_PBF)
change_OSC =  arcpy.GetParameterAsText(3)
change_OSCC = os.path.join(in_workspace,change_OSC)

env.workspace = in_workspace

#reversed order to be correct! 4th May 2014
#strtopass = osmopth + " --read-pbf file=" + '"' + latest_PBFF + '"' + " --read-pbf file=" + '"' + master_PBFF + '"' + "
#--derive-change --write-xml-change file=" + '"' + change_OSCC + '"'

to_pass = '{0} --read-pbf file="{1}" --read-pbf file="{2}" --derive-change --write-xml-change file"{3}"'.format(osmopth,latest_PBFF,master_PBFF,change_OSCC)


try:
    bat_filename = r"c:\temp\1_create_diff_SB.bat"
    #resorting to creating a bat file
    bat_file = open(bat_filename, "w")
    bat_file.write(to_pass)
    bat_file.close()
    print_str_to_console_and_arcpy("running Osmosis using " + bat_filename + " ...")
    subprocess.call([r"c:\temp\1_create_diff_SB.bat"])
    os.remove(r"c:\temp\1_create_diff_SB.bat")
    print_str_to_console_and_arcpy("...finished!")
except:
    print_str_to_console_and_arcpy("there is a problem!")




