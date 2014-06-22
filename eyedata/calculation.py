__all__ = ['scanPath', 'scanDuration', 'spacialDensity', 'scanDurationAvg', 'convexArea',
           'AOIHit', 'AOITrans_P', 'AOITrans_P_2',
           'AOIDuration']

import math

'''calculate the searching path of the eye'''


def scanPath(x, y):
    if type(x) != list and type(y) != list:
        return
    N = min([len(x), len(y)]) # get all the point numbers
    if (N <= 1):
        return
    path = 0
    for i in range(N - 1):
        path += math.sqrt((x[i] - x[i + 1]) ** 2 + (y[i] - y[i + 1]) ** 2)

    return path

'''total time of scanning'''


def scanDuration(t):
    return sum(t)


def scanDurationAvg(t):
    return sum(t) / len(t)


'''calculate the spacialDensity'''


def spacialDensity(N_w, N_h, width, height, x, y):
    kX = N_w * 1.0 / width
    kY = N_h * 1.0 / height
    dct = {}
    for i in range(len(x)):
        mx = int(x[i] * kX * 0.9999999999999)
        my = int(y[i] * kY * 0.9999999999999)
        dct[(mx, my)] = 1;
    return len(dct.keys()) * 1.0 / N_w / N_h


def AOIHit(AOIs):
    lens = map(len, AOIs)
    length = max(lens)
    if length != min(lens):
        print "Length not equal"
        return
    hitrate = [sum(AOI) * 1.0 / length for AOI in AOIs]

    return hitrate


def AOIDuration(time, AOIs):
    AOIDur = [0] * len(AOIs)
    for j in range(len(AOIs)):

        for i in range(len(AOIs[j])):
            if (AOIs[j][i] == 1):
                AOIDur[j] += time[i]
        N = sum(AOIs[j])
        if N == 0:
            AOIDur[j] = 0
        else:
            AOIDur[j] /= N

    return AOIDur


def AOITrans_P(AOIs):
    AOIseq = [0] * len(AOIs[0])
    trans = {}
    for i1 in range(len(AOIs[0])):
        for i2 in range(len(AOIs[0])):
            trans[(i1, i2)] = 0

    for j in range(len(AOIs)):
        for i in range(len(AOIs[j])):
            trans[(i, j)] = 0
            if AOIs[j][i] == 1:
                AOIseq[i] = j
    print "AOISeq:", AOIseq
    #transform matrix           
    trans = {}
    for i1 in range(len(AOIs)):
        for i2 in range(len(AOIs)):
            trans[(i1, i2)] = 0

    for i in range(len(AOIseq) - 1):
        trans[(AOIseq[i], AOIseq[i + 1])] += 1

    N = len(AOIseq) - 1
    for k in trans.keys():
        trans[k] = trans[k] * 1.0 / N

    return trans

def AOITrans_P_2(AOIs):
    AOIseq = [0] * len(AOIs[0])
    trans = {}
    for i1 in range(len(AOIs[0])):
        for i2 in range(len(AOIs[0])):
            trans[str(i1)+','+str(i2)] = 0

    for j in range(len(AOIs)):
        for i in range(len(AOIs[j])):
            trans[(i, j)] = 0
            if AOIs[j][i] == 1:
                AOIseq[i] = j
    print "AOISeq:", AOIseq
    #transform matrix
    trans = {}
    for i1 in range(len(AOIs)):
        for i2 in range(len(AOIs)):
            trans[str(i1)+','+str(i2)] = 0

    for i in range(len(AOIseq) - 1):
        trans[str(AOIseq[i])+','+str(AOIseq[i + 1])] += 1

    N = len(AOIseq) - 1
    for k in trans.keys():
        trans[k] = trans[k] * 1.0 / N

    return trans



def convex_hull(points):
    '''Computes the convex hull of a set of 2D points.
        
        Input: an iterable sequence of (x, y) pairs representing the points.
        Output: a list of vertices of the convex hull in counter-clockwise order,
        starting from the vertex with the lexicographically smallest coordinates.
        Implements Andrew's monotone chain algorithm. O(n log n) complexity.
    '''

    # Sort the points lexicographically (tuples are compared lexicographically).
    # Remove duplicates to detect the case we have just one unique point.
    points = sorted(set(points))

    # Boring case: no points or a single point, possibly repeated multiple times.
    if len(points) <= 1:
        return points

    # 2D cross product of OA and OB vectors, i.e. z-component of their 3D cross product.
    # Returns a positive value, if OAB makes a counter-clockwise turn,
    # negative for clockwise turn, and zero if the points are collinear.
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    # Build lower hull
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Build upper hull
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Concatenation of the lower and upper hulls gives the convex hull.
    # Last point of each list is omitted because it is repeated at the beginning of the other list.
    return lower[:-1] + upper[:-1]


def convexArea(x, y):
    points = []
    for i in range(len(x)):
        points.append((x[i], y[i]))
    outpoints = convex_hull(points)

    #calculate area
    x0, y0 = outpoints[0]
    area = 0
    for i in range(len(outpoints) - 2):
        x1, y1 = outpoints[i + 1]
        x2, y2 = outpoints[i + 2]
        #helen fomula
        a = math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)
        b = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        c = math.sqrt((x2 - x0) ** 2 + (y2 - y0) ** 2)
        p = (a + b + c) / 2
        s = math.sqrt(p * (p - a) * (p - b) * (p - c))
        area += s
    x_con = [x1 for x1, y1 in outpoints]
    y_con = [y1 for x1, y1 in outpoints]

    return x_con, y_con, area


if __name__ == "__main__":
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1]

    print scanPath(x, y)
    print spacialDensity(9, 2, 9, 2, x, y)
    print convexArea(x, y)
