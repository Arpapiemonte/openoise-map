# -*- coding: utf-8 -*-
"""
/***************************************************************************
 opeNoise

 Qgis Plugin to compute noise levels

                             -------------------
        begin                : March 2014
        copyright            : (C) 2014 by Arpa Piemonte
        email                : s.masera@arpa.piemonte.it
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""


#from PyQt4.QtGui import *
from builtins import range
from qgis.PyQt.QtCore import QVariant
from qgis.core import (QgsVectorLayer,
                       QgsFeature, QgsSpatialIndex,
                       QgsField, QgsRectangle, QgsPoint,
                       QgsGeometry, QgsVectorFileWriter, QgsWkbTypes)
import os
from math import sqrt


    
    
# computes distance (input two QgsPoints, return a float)    
def compute_distance(QgsPoint1,QgsPoint2):
    return sqrt((QgsPoint1.x()-QgsPoint2.x())**2+(QgsPoint1.y()-QgsPoint2.y())**2)

def add_point_to_layer(writer,point,attributes):
    geometry = QgsGeometry.fromPoint(point)
    feature = QgsFeature()
    feature.setAttributes(attributes)
    feature.setGeometry(geometry)
    writer.addFeature(feature) 
        
def run(sources_layer_path,receivers_layer_path,emission_pts_layer_path,research_ray):

    sources_layer = QgsVectorLayer(sources_layer_path,"input layer","ogr")
    receivers_layer = QgsVectorLayer(receivers_layer_path,"output layer","ogr")
        
    sources_feat_all = sources_layer.dataProvider().getFeatures()
    
    receivers_feat_all_dict = {}
    receivers_feat_all = receivers_layer.dataProvider().getFeatures()
    receivers_spIndex = QgsSpatialIndex()            
    for receivers_feat in receivers_feat_all:
        receivers_spIndex.insertFeature(receivers_feat)
        receivers_feat_all_dict[receivers_feat.id()] = receivers_feat    
    
    

    emission_pts_fields = [QgsField("id_emi", QVariant.Int),
                           QgsField("id_emi_source", QVariant.Int),
                           QgsField("id_source", QVariant.Int),
                           QgsField("d_rTOe", QVariant.Double,len=10,prec=2)]
    # update for QGIS 3 converting VectorWriter to QgsVectorFileWriter
    #emission_pts_writer = VectorWriter(emission_pts_layer_path, None, emission_pts_fields, 0, sources_layer.crs())


    emission_pts_writer = QgsVectorFileWriter(emission_pts_layer_path,"System",
                                              emission_pts_fields,QgsWkbTypes.PointGeometry,sources_layer.crs(),"ESRI Shapefile")

    
    # initializes ray and emission point id
    emission_pt_id = 0

    for sources_feat in sources_feat_all:
   
        # researches the receiver points in a rectangle created by the research_ray
        # creates the search rectangle
        rect = QgsRectangle()
        rect.setXMinimum( sources_feat.geometry().boundingBox().xMinimum() - research_ray )
        rect.setXMaximum( sources_feat.geometry().boundingBox().xMaximum() + research_ray )
        rect.setYMinimum( sources_feat.geometry().boundingBox().yMinimum() - research_ray )
        rect.setYMaximum( sources_feat.geometry().boundingBox().yMaximum() + research_ray )
    
        receiver_pts_request = receivers_spIndex.intersects(rect)
        
        distance_min = []
        for receiver_pts_id in receiver_pts_request:
            receiver_pts_feat = receivers_feat_all_dict[receiver_pts_id]
            result = sources_feat.geometry().closestSegmentWithContext(receiver_pts_feat.geometry().asPoint())
            distance_min_tmp = sqrt(result[0])
            
            if distance_min_tmp <= research_ray:
                distance_min.append(distance_min_tmp)
    
        # defines segment max length
        if len(distance_min) >= 1:
            segment_max = min(distance_min)/2
            if segment_max < 2:
                segment_max = 2
        else:
            continue
        
        # splits the sources line in emission points at a fix distance (minimum distance/2) and create the emission point layer
        # gets vertex
        sources_feat_vertex_pt_all = sources_feat.geometry().asPolyline()
        
        emission_pt_id_road = 0
        
        for i in range(0,len(sources_feat_vertex_pt_all)):
            
            pt1 = QgsPoint(sources_feat_vertex_pt_all[i])

            add_point_to_layer(emission_pts_writer,pt1,[emission_pt_id,  emission_pt_id_road, sources_feat.id(),segment_max])
           
            emission_pt_id = emission_pt_id + 1
            emission_pt_id_road = emission_pt_id_road + 1
            
            if i < len(sources_feat_vertex_pt_all)-1:
                
                pt2 = QgsPoint(sources_feat_vertex_pt_all[i+1])
    
                x1 = pt1.x()
                y1 = pt1.y()
                x2 = pt2.x()
                y2 = pt2.y()
                
                if y2 == y1:
                    dx = segment_max
                    dy = 0
                    m = 0
                elif x2 == x1:
                    dx = 0
                    dy = segment_max
                else:
                    m = ( y2 - y1 )/ ( x2 - x1 )
                    dx = sqrt((segment_max**2)/(1 + m**2))
                    dy = sqrt(((segment_max**2)*(m**2))/(1 + m**2))
                
                pt = pt1
                
                while compute_distance(pt,pt2) > segment_max:
                    x_temp = pt.x()
                    y_temp = pt.y()
                    if x_temp < x2:
                        if m > 0:
                            pt = QgsPoint(x_temp + dx, y_temp + dy) 
                        elif m < 0:
                            pt = QgsPoint(x_temp + dx, y_temp - dy)
                        elif m == 0:
                            pt = QgsPoint(x_temp + dx, y_temp)
                    elif x_temp > x2:
                        if m > 0:
                            pt = QgsPoint(x_temp - dx, y_temp - dy) 
                        elif m < 0:
                            pt = QgsPoint(x_temp - dx, y_temp + dy)                   
                        elif m == 0:
                            pt = QgsPoint(x_temp - dx, y_temp)   
                    elif x_temp == x2:
                        if y2 > y_temp:
                            pt = QgsPoint(x_temp, y_temp + dy) 
                        else:
                            pt = QgsPoint(x_temp, y_temp - dy) 
        
                    add_point_to_layer(emission_pts_writer,pt,[emission_pt_id,emission_pt_id_road, sources_feat.id(),segment_max])
                    
                    emission_pt_id = emission_pt_id + 1
                    emission_pt_id_road = emission_pt_id_road + 1        
    
    del emission_pts_writer
