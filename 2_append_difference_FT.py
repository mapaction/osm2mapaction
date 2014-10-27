
#first created by Chris Ewing, MapAction, 4th May 2014
#2_append_difference_FT.py - creates a bat file and runs Osmosis to append the
#OSC file to the master OSM.PBF file

import arcpy
from arcpy import env

import subprocess
import os

import urllib2
import re
import os

#set the paths for the software
gnupth = r"D:\GnuWin32\bin\wget.exe"
osmopt = r"c:\osmosis\bin"
osmopth = r"c:\osmosis\bin\osmosis"
svnzpth = r"C:\program files\7-zip\7z.exe"
javapth = r"C:\Windows\System32\java.exe"

##osmURL = r"http://labs.geofabrik.de/haiyan/" #arcpy.GetParameterAsText(0)
##in_workspace   = r"d:\Tools\toolbox\labs.geofabrik.de\haiyan"  #arcpy.GetParameterAsText(1)
##master_PBF = "2014-03-26-20-17.osm.pbf" #arcpy.GetParameterAsText(2)
##master_PBFF = in_workspace + "\\" + master_PBF
##latestPBF = "latest.osm.pbf"
##latestPBFF = in_workspace + "\\" + latestPBF
##change_OSC = "planetdiff-latest.osc"
##change_OSCC = in_workspace + "\\" + change_OSC


in_workspace   = arcpy.GetParameterAsText(0)
master_PBF = arcpy.GetParameterAsText(1)
master_PBFF = in_workspace + "\\" + master_PBF
change_OSC =  arcpy.GetParameterAsText(2)
change_OSCC = in_workspace + "\\" + change_OSC
cumul_PBF = arcpy.GetParameterAsText(3)
cumul_PBFF = in_workspace + "\\" + cumul_PBF

env.workspace = in_workspace

strtopass2 = osmopth + " --read-xml-change file=" + '"' + change_OSCC + '"' + " --read-pbf " + '"' + master_PBFF + '"' + " --apply-change --write-pbf file=" + '"' + cumul_PBFF + '"'

try:
    bat_filename2 = r"c:\temp\4_apply_diff_FT.bat"
    #resorting to creating a bat file    
    bat_file2 = open(bat_filename2, "w")
    bat_file2.write(strtopass2)
    bat_file2.close()

    str = "running Osmosis using " + bat_filename2 + " ..."
    print str
    arcpy.AddMessage(str)
    subprocess.call([r"c:\temp\4_apply_diff_FT.bat"])
    os.remove(r"c:\temp\4_apply_diff_FT.bat")
    str = "...finished!"
    print str
    arcpy.AddMessage(str)    
    
except:
    str = "there is a problem!"
    print str
    arcpy.AddMessage(str)
    

