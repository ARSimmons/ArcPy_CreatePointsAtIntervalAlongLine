###############################################
## Arielle Simmons                           ##
## GIS Data Engineer                         ##
## Tableau Software                          ##
## Date created: December 25, 2013           ##
## Date modified: December 30, 2013          ##
###############################################

## This script is to create points at specific intervals
## along a measured line segment
## returns nothing if the line is too short according to
## user definition
## to call the function 'createPointsAtInterval'
## use : createPointsAtInterval('<name of line fc>', interval, shortestLineLength)  


import arcpy
from arcpy import env
import math

## declare your env.workspace as the geodatabase you are working in
env.workspace = r'<database>'

def createPointsAtInterval(inLine, interval, shortestLineLength):
    sr = arcpy.Describe(inLine).spatialReference
    inLineName = arcpy.Describe(inLine).name
    segPts = arcpy.CreateFeatureclass_management(env.workspace, inLineName + '_pts', 'POINT','','','',sr)
    icursor = arcpy.da.InsertCursor(segPts, ('SHAPE@'))
    with arcpy.da.SearchCursor(inLine, ("SHAPE@LENGTH", "SHAPE@")) as cursor:
        for row in cursor:
            # row is a tuple - containing  "SHAPE@LENGTH" and "SHAPE"
            length = row[0]
            # measures length of the line, determines number of point intervals
            numIntervals = int(math.floor(length / interval))
            for x in range(1, numIntervals + 1):
                # newPt = row[1].positionAlongLine(.50,True).firstPoint
                newPt = row[1].positionAlongLine(interval * x)
                icursor.insertRow((newPt,))
            # if line length is greater then 'shortestLineLength'
            # (but smaller then the 'interval' - because if
            # length < interval then 'numIntervals' = 0) then shortest
            # line will only create one midpoint
            # if shorter - leave blank
            if length > shortestLineLength and numIntervals < 2:
                midpoint = row[1].positionAlongLine(.50,True).firstPoint
                icursor.insertRow((midpoint,))
    return segPts

        





    
