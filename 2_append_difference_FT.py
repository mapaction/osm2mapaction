
#last edited by Chris Ewing, MapAction, 4th May 2014
#2_append_difference_FT.py - creates a bat file and runs Osmosis to append the
#OSC file to the master OSM.PBF file

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
changeOSC =  arcpy.GetParameterAsText(2)
changeOSCC = inWorkspace + "\\" + changeOSC
cumulPBF = arcpy.GetParameterAsText(3)
cumulPBFF = inWorkspace + "\\" + cumulPBF

env.workspace = inWorkspace

strtopass2 = osmopth + " --read-xml-change file=" + '"' + changeOSCC + '"' + " --read-pbf " + '"' + masterPBFF + '"' + " --apply-change --write-pbf file=" + '"' + cumulPBFF + '"'

try:
    bat_filename2 = r"c:\4_apply_diff_FT.bat"
    #resorting to creating a bat file    
    bat_file2 = open(bat_filename2, "w")
    bat_file2.write(strtopass2)
    bat_file2.close()

    str = "running Osmosis using " + bat_filename2 + " ..."
    print str
    arcpy.AddMessage(str)
    subprocess.call([r"c:\4_apply_diff_FT.bat"])
    os.remove(r"c:\4_apply_diff_FT.bat")
    str = "...finished!"
    print str
    arcpy.AddMessage(str)    
    
except:
    str = "there is a problem!"
    print str
    arcpy.AddMessage(str)
    

