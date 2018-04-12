#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      ChardonnensB01
#
# Created:     16.11.2017
# Copyright:   (c) ChardonnensB01 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------


# Import librairie

import arcpy
import datetime
import numpy as np
import matplotlib.pyplot as plt


# On définit les variables

database = "C:\Users\ChardonnensB01\Documents\ArcGIS\Default.gdb"
cleardb = False
fc = "VUGIS2GDB"
field = "HEURE"

# On définit l'environnement

arcpy.env.workspace = database

# On autorise l'overwrite

arcpy.env.overwriteOutput = True

# On vide la BDD

if cleardb:
    fcs = arcpy.ListFeatureClasses("*")
    for x in fcs:
        arcpy.Delete_management(x)

# On sauve les données du champs

d = [row[0] for row in arcpy.da.SearchCursor(fc, field)]

h = np.array([x.hour for x in d])
m = np.array([x.minute for x in d])
# On plot l'histogramme

plt.hist(h,np.arange(0,24))
plt.show()
