#-------------------------------------------------------------------------------
# Name:        DissolveOverlay
# Purpose:     Ce script permet de fusionner des polygones superpos?es en tenant
#              compte d'un champs en particulier. Ex: Le polygon ayant le champs
#              FID le plus grand prend le dessus lors de la fusion.
#
# Author:      ChardonnensB01
#
# Created:     15.11.2017
# Copyright:   (c) ChardonnensB01 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy


# Parameter

database = arcpy.GetParameterAsText(0)
in_feature = arcpy.GetParameterAsText(1)
field = arcpy.GetParameterAsText(2)
out_feature = arcpy.GetParameterAsText(3)
minmax = arcpy.GetParameterAsText(4)
SplitMultiPart = arcpy.GetParameterAsText(5)


# Workspace definition

arcpy.env.workspace = database

# OverWrite settings

arcpy.env.overwriteOutput = True

# We dissolve the feature over the selected field

arcpy.Dissolve_management (in_feature, in_feature+"_diss",field)
in_feature = in_feature+"_diss"

# Select distinct value

with arcpy.da.SearchCursor(in_feature, [field]) as cursor:
        n = sorted({int(row[0]) for row in cursor})


# Make a layer from the feature class
arcpy.MakeFeatureLayer_management(in_feature, "lyr")


# We split the feature according to the field value.

for x in n:
    arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", field+'='+str(x))
    arcpy.CopyFeatures_management("lyr", 'lyr_'+str(x))

# We erase the unwanted polygon

for x in n:
    if minmax.lower() == 'min':
        for y in [xx for xx in n if xx < x]:
            arcpy.CopyFeatures_management('lyr_'+ str(x), "in_memory\lyr_" + str(x))
            arcpy.Erase_analysis("in_memory\lyr_" + str(x), 'lyr_'+ str(y), 'lyr_'+ str(x))
    else:
        for y in [xx for xx in n if xx > x]:
            arcpy.CopyFeatures_management('lyr_'+ str(x), "in_memory\lyr_" + str(x))
            arcpy.Erase_analysis("in_memory\lyr_" + str(x), 'lyr_'+ str(y), 'lyr_'+ str(x))

# Layer list creation.

layerlist = ['lyr_'+ str(x) for x in n];

# Layer union.
if SplitMultiPart == 'true':
    arcpy.Merge_management(layerlist, "in_memory\MergeTemp")
    arcpy.MultipartToSinglepart_management("in_memory\MergeTemp",out_feature)
else:
    arcpy.Merge_management(layerlist, out_feature)

# Delete intermediate result

deletelist = layerlist+[in_feature]
for s in deletelist:
    arcpy.Delete_management(s)