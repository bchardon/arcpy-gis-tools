# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 08:54:33 2018

@author: ChardonnensB01
"""

import arcpy

# For each field in the Hospitals feature class, print
#  the field name, type, and length.

fc = [r'C:\Users\ChardonnensB01\AppData\Roaming\ESRI\Desktop10.5\ArcCatalog\SDPCONS.sde\SDPCONS.SDEUSER.SMO1010P_POSTE_COMPTAGE']
fields = arcpy.ListFields(fc[0])

for field in fields:
    print("{0};{1};{2}"
          .format(field.name, field.type, field.length))