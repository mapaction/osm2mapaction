
#last edited by Chris Ewing, MapAction, 4th May 2014
#1_create_difference_SB.py - creates a bat file and runs against osmosis to generate
#an OSC file (containing the changes only)

import arcpy
from arcpy import env
import subprocess, os
import urllib2, re, os

#set the paths for the software
gnupth = r"D:\GnuWin32\bin\wget.exe"
osmopt = r"c:\osmosis\bin"
osmopth = r"c:\osmosis\bin\osmosis"
svnzpth = r"C:\program files\7-zip\7z.exe"
javapth = r"C:\Windows\System32\java.exe"

##osmURL = r"http://labs.geofabrik.de/haiyan/" #arcpy.GetParameterAsText(0)
##inWorkspace   = r"d:\Tools\toolbox\labs.geofabrik.de\haiyan"  #arcpy.GetParameterAsText(1)
##masterPBF = "2014-03-26-20-17.osm.pbf" #arcpy.GetParameterAsText(2)
##masterPBFF = inWorkspace + "\\" + masterPBF
##latestPBF = "latest.osm.pbf"
##latestPBFF = inWorkspace + "\\" + latestPBF
##changeOSC = "planetdiff-latest.osc"
##changeOSCC = inWorkspace + "\\" + changeOSC

inWorkspace   = arcpy.GetParameterAsText(0)
masterPBF = arcpy.GetParameterAsText(1)
masterPBFF = inWorkspace + "\\" + masterPBF
latestPBF = arcpy.GetParameterAsText(2)
latestPBFF = inWorkspace + "\\" + latestPBF
changeOSC =  arcpy.GetParameterAsText(3)
changeOSCC = inWorkspace + "\\" + changeOSC

env.workspace = inWorkspace

#reversed order to be correct! 4th May 2014
strtopass = osmopth + " --read-pbf file=" + '"' + latestPBFF + '"' + " --read-pbf file=" + '"' + masterPBFF + '"' + " --derive-change --write-xml-change file=" + '"' + changeOSCC + '"'

try:
    bat_filename = r"c:\1_create_diff_SB.bat"
    #resorting to creating a bat file
    bat_file = open(bat_filename, "w")
    bat_file.write(strtopass)
    bat_file.close()
    str = "running Osmosis using " + bat_filename + " ..."
    print str
    arcpy.AddMessage(str)
    subprocess.call([r"c:\1_create_diff_SB.bat"])
    os.remove(r"c:\1_create_diff_SB.bat")
    str = "...finished!"
    print str
    arcpy.AddMessage(str)
except:
    str = "there is a problem!"
    print str
    arcpy.AddMessage(str)



