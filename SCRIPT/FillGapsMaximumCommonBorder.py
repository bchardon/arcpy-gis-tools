# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 12:45:31 2018

Ce script permet de remplir les trous totalement contenu à l'intérieur d'un 
ou de plusieurs polygones. Les nouveaux polygones acquièrent les caractéristiques
du polygone adjacent avec lequel il partage la plus grande frontières.

Il est possible de fixer une limite de surface au dessus de laquelle un trou
ne sera pas comblé.

@author: ChardonnensB01
"""
import arcpy
import numpy as np
import os
# Select the database
database = r'C:\Users\ChardonnensB01\Documents\ArcGIS\Default.gdb'

# Select the feature
fc = r'C:\Users\ChardonnensB01\Documents\ArcGIS\Output.gdb\SMO6101S_SURFACE_DESSERTE_TP_REEL'
fc_name = os.path.basename(os.path.normpath(fc));

# Workspace definition

arcpy.env.workspace = database

# OverWrite settings

arcpy.env.overwriteOutput = True

# Beginning of the process
arcpy.Union_analysis(fc, r'union_fc', 'ALL', '', 'NO_GAPS')
arcpy.Intersect_analysis([r'union_fc',fc], r'line_fc', '', '', 'LINE')


with arcpy.da.UpdateCursor(r'union_fc', ['FID_'+fc_name,'Shape_Area']) as cursor:
    for row in cursor:
        print(row[1])
        if row[1] > 9000 and row[0] == -1.0:
            print('delete')
            cursor.deleteRow()
            
with arcpy.da.UpdateCursor(r'line_fc', ['FID_'+fc_name]) as cursor:
    for row in cursor:
        if row[0] != -1.0:
            cursor.deleteRow()

UserField = []     
fields = arcpy.ListFields(fc)
for field in fields:
    if field.name not in ['Shape','OBJECTID','Shape_Length','Shape_Area']:
        UserField.append(field.name)


VAL = np.zeros(shape=(2,3+len(UserField)));          
cursor = arcpy.SearchCursor(r'line_fc')
for row in cursor:
    if VAL.any():
        if row.getValue('FID_union_fc') in VAL[:,0]:
            ind = np.where(VAL[:,0]==row.getValue('FID_union_fc'))[0][0]
            if VAL[ind,2] <= row.getValue('Shape_Length'):
                VAL[ind,0] = row.getValue('FID_union_fc')
                VAL[ind,1] = row.getValue('FID_'+fc_name+'_1')
                VAL[ind,2] = row.getValue('Shape_Length')
                for counter,field in enumerate(UserField):
                    VAL[ind,2+counter+1] = row.getValue(field+'_1')
        else:
            CAT = [row.getValue('FID_union_fc'),row.getValue('FID_'+fc_name+'_1'),row.getValue('Shape_Length')]
            CAT = CAT+[row.getValue(field+'_1') for field in UserField]
            VAL = np.vstack((VAL,CAT))
    else:
        CAT = [row.getValue('FID_union_fc'),row.getValue('FID_'+fc_name+'_1'),row.getValue('Shape_Length')]
        CAT = CAT+[row.getValue(field+'_1') for field in UserField]
        VAL = np.vstack((VAL,CAT))
    
VAL = VAL[2:,:]



with arcpy.da.UpdateCursor(r'union_fc', ['OBJECTID']+UserField) as cursor:
    for row in cursor:
        for value in VAL:
            if value[0].astype(int) == row[0]:
                for counter,field in enumerate(UserField):
                    row[counter+1] = value[2+counter+1]
                    print('replaced with {}'.format(value[2+counter+1]))
                    cursor.updateRow(row)

fields = arcpy.ListFields('union_fc')
for field in fields:
    if field.name not in ['Shape','OBJECTID','Shape_Length','Shape_Area']+UserField:
        arcpy.DeleteField_management("union_fc",field.name)
        print('Delete {}'.format(field.name))
            
arcpy.Delete_management('line_fc')