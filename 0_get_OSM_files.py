#first created by Chris Ewing, MapAction, 4th May 2014
#0_get_OSM_files.py - gets the OSM pbf files from a geofabrik URL

import arcpy
from arcpy import env

import subprocess
import os
import urllib2
import re

#set the paths for the software
gnupth = r"c:\GnuWin32\bin\wget.exe"
osmopt = r"c:\osmosis\bin"
osmopth = r"c:\osmosis\bin\osmosis"
svnzpth = r"c:\program files\7-zip\7z.exe"


osm_url = arcpy.GetParameterAsText(0)
in_workspace   = arcpy.GetParameterAsText(1)
get_all = arcpy.GetParameterAsText(2)


#function to get the PBF files from geofabrik
class

def get_pbfs(url, fn):   
    sock = urllib2.urlopen(url + fn)
    local_filename = in_workspace + '\\' + fn
    data = sock.read()    
    with open(local_filename, "wb") as local_file:
        local_file.write(data)
    local_file.close()


str = "reading and downloading the PBF files..."
print str
arcpy.AddMessage(str)

try:
    sock = urllib2.urlopen(osm_url)
    html_source = sock.read()
    links = re.findall('\d\d\d\d.\d\d.\d\d.\d\d.\d\d.osm.pbf"', html_source)
    sock.close()

    if get_all == "1":
        for l in links:
            url = osm_url + l[:-1]

            if os.path.exists(in_workspace + "\\" + l[:-1]) == True:
                str = in_workspace + "\\" + l[:-1] + " already exists"
                print str
                arcpy.AddMessage(str)
                continue
            
            str = "getting " + url
            print str
            arcpy.AddMessage(str)
            get_pbfs(osm_url, l[:-1])

    #get latest file too
        get_pbfs(osm_url, "latest.osm.pbf")
        
    else: # only get the latest file
        get_pbfs(osm_url, "latest.osm.pbf")
        

    str = "...finished downloading PBF files"
    print str
    arcpy.AddMessage(str)

except:
    str = "there is a problem!"
    print str
    arcpy.AddMessage(str)



    

