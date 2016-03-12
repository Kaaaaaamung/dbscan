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

UNCLASSIFIED = False
NOISE = None
global m
print time.clock()
curs  = arcpy.SearchCursor(r"E:\study\NTL\DMSPDATA\2005urban\cities_unique_shp\cities2005Pts_prj.shp")
# curs  = arcpy.SearchCursor("../Export_Output.shp")
pointx = []
pointy = []
c = 0
for row in curs:
    pointx.append(row.Shape.firstPoint.X)
    pointy.append(row.Shape.firstPoint.Y)
    c += 1
    if c%1000 ==0:
        print "processing line %d"%c
m = np.matrix([pointx,pointy])
# 0.005 degree in wgs84, proximately 500m
eps = 10000
min_points = 4

def _dist(p,q):
	return math.sqrt(np.power(p-q,2).sum())

def _eps_neighborhood(p,q,eps):
	return _dist(p,q) < eps

def _region_query(point_id, eps):
    n_points = m.shape[1]
    seeds = []
    for i in xrange(0, n_points):
        if _eps_neighborhood(m[:,point_id], m[:,i], eps):
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

        c +=1
        if c%(n_points/50) == 0:
            print "processing line %d"%c

        if classifications[point_id] == UNCLASSIFIED:
            if _expand_cluster(classifications, point_id, cluster_id, eps, min_points):
                cluster_id = cluster_id + 1
    return classifications

# input matrix with 2 column (x, y)

clusterlis = dbscan(eps, min_points)
with open(r"E:\study\NTL\DMSPDATA\2005urban\cities_unique_shp\10km.csv","w+") as res:
    res.write("x,y,clusterid\n")
    for i in xrange(0,len(pointy)):
        res.write("%f,%f,%s\n"%(pointx[i],pointy[i],clusterlis[i]))
print "result written done!"
print time.clock()