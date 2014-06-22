
from dtImport import *
from calculation import  *
import json
def calc_return(filename):
    try:
        dt = readXlsData(filename)
        dur = dt["GazeEventDuration"]
        x = dt["FixationPointX (MCSpx)"]
        y = dt["FixationPointY (MCSpx)"]
        a1 = dt["AOI[Rectangle]Hit"]
        a2 = dt["AOI[Rectangle 2]Hit"]
        a3 = dt["AOI[Rectangle 3]Hit"]
        a4 = dt["AOI[Rectangle 4]Hit"]
        a5 = dt["AOI[Rectangle 5]Hit"]
        AOIs = [a1, a2, a3, a4, a5]

        dataDict = {}
        dataDict['AOI_Hit'] = AOIHit(AOIs)
        dataDict['AOI_Duration'] = AOIDuration(dur, AOIs)
        dataDict['AOI_Trans_Probablity'] = AOITrans_P_2(AOIs)
        dataDict['Spacial_Density'] = spacialDensity(10, 10, 1592, 1316, x, y)
        dataDict['Point_Number'] = len(y)
        xc, yc, area = convexArea(x, y)
        dataDict['Scan_Path'] = scanPath(x, y)
        dataDict['Scan_Duration Total'] = scanDuration(dur)
        dataDict['Scan_Duration Average'] = scanDurationAvg(dur)
        dataDict['Scan_Area'] = area

        return dataDict
    except:
        return {"Error": "Cannot read file!"}