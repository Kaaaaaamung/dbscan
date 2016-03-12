# -*- coding: utf-8 -*-

# A Density-Based Algorithm for Discovering Clusters in Large Spatial Databases with Noise
# Martin Ester, Hans-Peter Kriegel, Jörg Sander, Xiaowei Xu
# dbscan: density based spatial clustering of applications with noise
import arcpy
from dbscan import *
import numpy as np
import time
import numpy as np
import math


minx = float("inf")
maxx = 0
miny = float("inf")
maxy = 0
UNCLASSIFIED = False
NOISE = None
global m
print time.clock()
curs  = arcpy.SearchCursor(r"E:\study\NTL\DMSPDATA\2005urban\cities_unique_shp\morph\urban7_pts.shp")
# curs  = arcpy.SearchCursor("../Export_Output.shp")

pointx = []
pointy = []
c = 0
# for row in curs:
#     if row.Shape.firstPoint.X < minx:
#         minx = row.Shape.firstPoint.X
#     if row.Shape.firstPoint.Y < miny:
#         miny = row.Shape.firstPoint.Y
#     if row.Shape.firstPoint.X > maxx:
#         maxx = row.Shape.firstPoint.X
#     if row.Shape.firstPoint.Y > maxy:
#         maxy = row.Shape.firstPoint.Y
#     pointx.append(row.Shape.firstPoint.X)
#     pointy.append(row.Shape.firstPoint.Y)
#     c += 1
#     if c % 1000 == 0:
#         print "processing line %d"%c


 # cellw =(maxx-minx)/100
 # cellh =(maxy-miny)/100

# cellh = 48960.7966637
# cellw = 65773.0973122
maxx = 2137841.65955  # mercator 14950960.8649
maxy = 5807428.31244  # 6949025.64809
minx = -2536743.59237 # 8373651.13367
miny =1886097.41083   #2052945.98172
cellw =(maxx-minx)/10
cellh =(maxy-miny)/10

def count(curs):
    c = 0
    for feature in curs:
        c += 1
    return c


def build_id(curs):
    id = []
    for i in range(0,count(curs)):
        id.append(i)
    return id

# class grid:
#     def __init__(self,_extent,_i,_j):
#         self.extent=_extent
#         self.i=_i
#         self.j=_j

grid = [[[]for i in range(101)] for j in range(101)]

# for i in range(0,100):
#     for j in range(0,100):
#         x1=minx+j*cellw #每个格网minx
#         x2=minx+(j+1)*cellw
#         y2=maxy-i*cellh #每个格网maxy
#         y1=maxy-(i+1)*cellh #每个格网miny
#         _extent=extent(x1,y1,x2,y2)
#         grid[i][j]=_extent
c = 0
curs = arcpy.SearchCursor(r"E:\study\NTL\DMSPDATA\2005urban\cities_unique_shp\morph\urban7_pts.shp")
for row in curs:
    pointx.append(row.Shape.firstPoint.X)
    pointy.append(row.Shape.firstPoint.Y)
    a = int((row.Shape.firstPoint.X - minx) // cellw)
    b = int((row.Shape.firstPoint.Y - miny) // cellh)
    grid[a][b].append(c)
    c += 1
    if c % 1000 == 0:
        print "processing line %d" % c
m = np.matrix([pointx,pointy])
# def build_index(curs):
#     grid = [[[]for i in range(100)] for j in range(100)]
#     #grid=[[0 for x in range(100)] for y in range(100)]
#     # for i in range(0,100):
#     #     for j in range(0,100):
#     #         x1=minx+j*cellw #每个格网minx
#     #         x2=minx+(j+1)*cellw
#     #         y2=maxy-i*cellh #每个格网maxy
#     #         y1=maxy-(i+1)*cellh #每个格网miny
#     #         _extent=extent(x1,y1,x2,y2)
#     #         grid[i][j]=_extent
#     c=0
#     for row in curs:
#         a = int(row.Shape.firstPoint.X // cellw)
#         b = int(row.Shape.firstPoint.Y // cellh)
#         grid[a][b].append(c)
#         c += 1
#     return grid


def neighbor_cell(id,pointx,pointy,grid):
    a = int((pointx - minx) // cellw)
    b = int((pointy - miny) // cellh)
    list = []
    if a == 0:
        if b == 0:
            list.extend(grid[a][b])
            list.extend(grid[a+1][b])
            list.extend(grid[a][b+1])
            list.extend(grid[a+1][b+1])
        else:
            list.extend(grid[a][b-1])
            list.extend(grid[a][b+1])
            list.extend(grid[a][b])
            list.extend(grid[a+1][b-1])
            list.extend(grid[a+1][b])
            list.extend(grid[a+1][b+1])
        return list
    if a == 10:
        if b == 10:
            list.extend(grid[a][b])
            list.extend(grid[a-1][b])
            list.extend(grid[a][b-1])
            list.extend(grid[a-1][b-1])
        else:
            list.extend(grid[a][b-1])
            list.extend(grid[a][b+1])
            list.extend(grid[a][b])
            list.extend(grid[a-1][b-1])
            list.extend(grid[a-1][b])
            list.extend(grid[a-1][b+1])
        return list
    if b == 10:
        if a == 0:
            list.extend(grid[a][b])
            list.extend(grid[a+1][b])
            list.extend(grid[a][b-1])
            list.extend(grid[a+1][b-1])
        else:
            list.extend(grid[a-1][b])
            list.extend(grid[a][b])
            list.extend(grid[a+1][b])
            list.extend(grid[a-1][b])
            list.extend(grid[a][b])
            list.extend(grid[a+1][b])
        return list
    if b == 0:
        if a == 10:
            list.extend(grid[a][b])
            list.extend(grid[a-1][b])
            list.extend(grid[a][b+1])
            list.extend(grid[a-1][b+1])
        else:
            list.extend(grid[a-1][b])
            list.extend(grid[a][b])
            list.extend(grid[a+1][b])
            list.extend(grid[a-1][b])
            list.extend(grid[a][b])
            list.extend(grid[a+1][b])
        return list
    else:
        list.extend(grid[a-1][b-1])
        list.extend(grid[a-1][b])
        list.extend(grid[a+1][b+1])
        list.extend(grid[a][b-1])
        list.extend(grid[a][b])
        list.extend(grid[a][b+1])
        list.extend(grid[a+1][b-1])
        list.extend(grid[a+1][b])
        list.extend(grid[a+1][b+1])
    return list


EPS = [40000]
min_points = [4]
# 0.005 degree in wgs84, proximately 500m
# eps = 4000000
# min_points = 4


def _dist(p,q):
	return math.sqrt(np.power(p-q,2).sum())

def _eps_neighborhood(p,q,eps):
	return _dist(p,q) < eps

def _region_query(point_id, eps):
    n_points = m.shape[1]
    seeds = []
    #search_list = neighbor_cell(point_id, m[0, point_id], m[1, point_id], grid)
    for i in range(0,n_points):
        if _eps_neighborhood(m[:, point_id], m[:, i], eps):
            seeds.append(i)
    return seeds

def _expand_cluster(classifications, point_id, cluster_id, eps, min_points):
    seeds = _region_query(point_id, eps)
    if len(seeds) < min_points:
        classifications[point_id] = NOISE
        return False
    else:
        classifications[point_id] = cluster_id
        for seed_id in seeds:
            classifications[seed_id] = cluster_id

        while len(seeds) > 0:
            current_point = seeds[0]
            results = _region_query(current_point, eps)
            if len(results) >= min_points:
                for i in xrange(0, len(results)):
                    result_point = results[i]
                    if classifications[result_point] == UNCLASSIFIED or \
                       classifications[result_point] == NOISE:
                        if classifications[result_point] == UNCLASSIFIED:
                            seeds.append(result_point)
                        classifications[result_point] = cluster_id
            seeds = seeds[1:]
        return True

def dbscan(eps, min_points):
    """Implementation of Density Based Spatial Clustering of Applications with Noise
    See https://en.wikipedia.org/wiki/DBSCAN

    scikit-learn probably has a better implementation

    Uses Euclidean Distance as the measure

    Inputs:
    m - A matrix whose columns are feature vectors
    eps - Maximum distance two points can be to be regionally related
    min_points - The minimum number of points to make a cluster

    Outputs:
    An array with either a cluster id number or dbscan.NOISE (None) for each
    column vector in m.
    """
    c = 0
    cluster_id = 1
    n_points = m.shape[1]
    print "total points_num is: %d"%n_points
    classifications = [UNCLASSIFIED] * n_points
    for point_id in xrange(0, n_points):
        point = m[:,point_id]

        c += 1
        if c % (n_points/50) == 0:
            print "processing line %d" % c

        if classifications[point_id] == UNCLASSIFIED:
            if _expand_cluster(classifications, point_id, cluster_id, eps, min_points):
                cluster_id = cluster_id + 1
    return classifications

# input matrix with 2 column (x, y)

for eps in EPS:
    for min_pts in min_points:
        eps = int(eps)
        clusterlis = dbscan(eps, min_pts)
        f ='E:\\study\\NTL\\DMSPDATA\\2005urban\\cities_unique_shp\\morph\\'+ str(eps) + 'm_' + str(min_pts) + '.csv'
        with open(f,"w+") as res:
            res.write("x,y,clusterid\n")
            for i in xrange(0,len(pointy)):
                res.write("%f,%f,%s\n"%(pointx[i],pointy[i],clusterlis[i]))
        print str(eps) + "_" + str(min_pts) +"written down"
print "result written done!"
print time.clock()