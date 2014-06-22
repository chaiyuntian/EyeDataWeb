import xlrd
from calculation import *


def readXlsData(filename, picked=["FixationPointX (MCSpx)",
                                  "FixationPointY (MCSpx)",
                                  "GazeEventDuration",
                                  "AOI[Rectangle]Hit",
                                  "AOI[Rectangle 2]Hit",
                                  "AOI[Rectangle 3]Hit",
                                  "AOI[Rectangle 4]Hit",
                                  "AOI[Rectangle 5]Hit"]):
    data = xlrd.open_workbook(filename)
    table = data.sheets()[0]
    headers = table.row_values(0)
    rsltDict = {}

    for i in range(table.ncols):
        col = table.col_values(i)
        h = headers[i]
        if h in picked:
            col.pop(0)
            rsltDict[h] = col

    return rsltDict


if __name__ == "__main__":
    import time

    start_time = time.clock()
    fn = 'Demo.xls'
    dt = readXlsData(fn)
    dur = dt["GazeEventDuration"]
    x = dt["FixationPointX (MCSpx)"]
    y = dt["FixationPointY (MCSpx)"]
    a1 = dt["AOI[Rectangle]Hit"]
    a2 = dt["AOI[Rectangle 2]Hit"]
    a3 = dt["AOI[Rectangle 3]Hit"]
    a4 = dt["AOI[Rectangle 4]Hit"]
    a5 = dt["AOI[Rectangle 5]Hit"]
    AOIs = [a1, a2, a3, a4, a5]
    print "AOI Hit:", AOIHit(AOIs)
    print "AOI Duration:", AOIDuration(dur, AOIs)
    print "AOI Trans probablity:", AOITrans_P(AOIs)
    print "Spacial Density:", spacialDensity(10, 10, 1592, 1316, x, y)

    print "Point Number:", len(y)
    xc, yc, area = convexArea(x, y)
    print "Scan Path:", scanPath(x, y)
    print "Scan Duration Total:", scanDuration(dur)
    print "Scan Duration Average:", scanDurationAvg(dur)
    print "Scan Area:", area

    calc_time = time.clock() - start_time
    print "calculation time:", calc_time

    import matplotlib.pyplot as plt
    import numpy as np
    #To draw y =x^2 (-3<=x<=3)
    fig = plt.figure(1)
    ax = fig.add_subplot(211)
    line1 = ax.plot(x, y, 'ro')

    conves = ax.plot(xc, yc, 'bo-')
    plt.show()
    

