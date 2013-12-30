###############################################
## Arielle Simmons                           ##
## GIS Data Engineer                         ##
## Tableau Software                          ##
## Date created: December 25, 2013           ##
## Date modified: December 28, 2013          ##
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
env.workspace = r'<geodatabase>'

def createPointsAtInterval(inLine, interval, shortestLineLength):
    sr = arcpy.Describe(inLine).spatialReference
    inLineName = arcpy.Describe(inLine).name
    segPts = arcpy.CreateFeatureclass_management(env.workspace, inLineName + '_pts', 'POINT','','','',sr)
    icursor = arcpy.da.InsertCursor(segPts, ('SHAPE@'))
    with arcpy.da.SearchCursor(inLine, ("SHAPE@LENGTH", "SHAPE@")) as cursor:
        for row in cursor:
            length = row[0]
            # measures length of the line, determines number of point intervals
            numIntervals = int(math.floor(length / interval))
            for x in range(1, numIntervals):
                # newPt = row[1].positionAlongLine(.50,True).firstPoint
                newPt = row[1].positionAlongLine(interval * x)
                icursor.insertRow((newPt,))
            # if line length is greater then shortest
            # line only create one endpoint
            # otherwise leave blank
            if length > shortestLineLength:
                lastPt = row[1].positionAlongLine(interval * numIntervals)
                icursor.insertRow((lastPt,))
    return segPts

        





    
