#last edited by Chris Ewing, MapAction, 4th May 2014
#0_get_OSM_files.py - gets the OSM pbf files from a geofabrik URL

import arcpy
from arcpy import env

import subprocess, os

import urllib2, re

#set the paths for the software
gnupth = r"D:\GnuWin32\bin\wget.exe"
osmopt = r"d:\osmosis\bin"
osmopth = r"d:\osmosis\bin\osmosis"
svnzpth = r"C:\program files\7-zip\7z.exe"


osmURL = arcpy.GetParameterAsText(0)
inWorkspace   = arcpy.GetParameterAsText(1)
getAll = arcpy.GetParameterAsText(2)


#function to get the PBF files
def getPBFs(url, fn):   
    sock = urllib2.urlopen(url + fn)
    local_filename = inWorkspace + '\\' + fn
    data = sock.read()    
    with open(local_filename, "wb") as local_file:
        local_file.write(data)
    local_file.close()


str = "reading and downloading the PBF files..."
print str
arcpy.AddMessage(str)

try:
    sock = urllib2.urlopen(osmURL)
    htmlSource = sock.read()
    links = re.findall('\d\d\d\d.\d\d.\d\d.\d\d.\d\d.osm.pbf"', htmlSource)
    sock.close()

    if getAll == 1:
        for l in links:
            url = osmURL + l[:-1]

            if os.path.exists(inWorkspace + "\\" + l[:-1]) == True:
                str = inWorkspace + "\\" + l[:-1] + " already exists"
                print str
                arcpy.AddMessage(str)
                continue
            
            str = "getting " + url
            print str
            arcpy.AddMessage(str)
            getPBFs(osmURL, l[:-1])

    #get latest file too
        getPBFs(osmURL, "latest.osm.pbf")
        
    else: # only get the latest file
        getPBFs(osmURL, "latest.osm.pbf")
        

    str = "...finished downloading PBF files"
    print str
    arcpy.AddMessage(str)

except:
    str = "there is a problem!"
    print str
    arcpy.AddMessage(str)



    

