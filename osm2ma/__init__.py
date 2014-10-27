#-------------------------------------------------------------------------------
# Name:        osm2ma
# Purpose:
#
# Author:      asmith
#
# Created:     20/08/2014
# Copyright:   (c) MapAction 2014
# Licence:     GPL
#-------------------------------------------------------------------------------

"""
Convert OSM/PBF native file to shapefiles using MapAction's data naming convention.

Key files
=========
osm2mapaction.py		This is the shell. It is what should be called either from the commandline or from other code.

raw_config_loader.py	This reads the contents of the excel config file. The excel config file described the mapping between the tags in OSM data and the attributes that the output shapefiles will have. No manipulation of this table occurs here.

configengine.py			This takes the table from from the excel config file and loads it into an in-memory SQLite DB. There it is 


Notes
Shell = osm2ma

- load excel file and normalise

configengine
-> Class ConfigXWalk
Provides a functional mapping between excel config file and xwalk table
provide excel as parameter to class constructor
One-to-one between class instance and actuall config file on disk/memory
Provide public methods to access xwalk somehow?
Possible abstract class and subclassed for excel? Or more generic way pof passing excell file?

XWalk
This is the fully populated shapefile table shpf_list

Wrap these two steps up in a function to apply to XWalk:
-> generate OGR SQL-like querry
-> Test feature count > 0
This should return a subset of shpf_list to which we apply:
-> Do export


OGR plumbing
============
-> Is OGR installed?
-> Is OGR high enough version?
-> Are the shapefile and OSM drivers installed?
-> Are the ErrorHandlers and Exceptions installed/enabled?

"""