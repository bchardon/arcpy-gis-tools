# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import arcpy

# Set the workspace for ListFeatureClasses
database = arcpy.GetParameterAsText(0)
arcpy.env.workspace = database

# Use the ListFeatureClasses function to return a list of
#  shapefiles.
fc = arcpy.ListFeatureClasses()
fr = arcpy.ListRasters()
ft = arcpy.ListTables()

fall = fc+fr+ft

for feature in fall:
    print("deleting {}".format(feature))
    arcpy.Delete_management(feature)

