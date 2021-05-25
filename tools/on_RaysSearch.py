# -*- coding: utf-8 -*-
"""
/***************************************************************************
 opeNoise

 Qgis Plugin to compute noise levels

                             -------------------
        begin                : February 2019
        copyright            : (C) 2019 by Arpa Piemonte
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


from math import sqrt

from qgis.core import QgsVectorLayer, QgsSpatialIndex, QgsRectangle, QgsGeometry






    
    
# computes distance (input two QgsPoints, return a float)    
def compute_distance(QgsPoint1,QgsPoint2):
    return sqrt((QgsPoint1.x()-QgsPoint2.x())**2+(QgsPoint1.y()-QgsPoint2.y())**2)

def run(bar,layer1_path,layer2_path,obstacles_path,research_ray):

    output = {}
    #layer1 receiver
    layer1 = QgsVectorLayer(layer1_path,"layer1","ogr")
    #layer 2 source
    layer2 = QgsVectorLayer(layer2_path,"layer2","ogr")
    layer2_feat_all_dict = {}
    layer2_feat_all = layer2.dataProvider().getFeatures()
    layer2_spIndex = QgsSpatialIndex()
    for layer2_feat in layer2_feat_all:
        layer2_spIndex.insertFeature(layer2_feat)
        layer2_feat_all_dict[layer2_feat.id()] = layer2_feat


    if obstacles_path is not None:
        obstacles_layer = QgsVectorLayer(obstacles_path,"obstacles","ogr")
        obstacles_feat_all = obstacles_layer.dataProvider().getFeatures()
        obstacles_spIndex = QgsSpatialIndex()
        obstacles_feat_all_dict = {}
        for obstacles_feat in obstacles_feat_all:
            obstacles_spIndex.insertFeature(obstacles_feat)
            obstacles_feat_all_dict[obstacles_feat.id()] = obstacles_feat


    layer1_feat_all = layer1.dataProvider().getFeatures()
    layer1_feat_total = layer1.dataProvider().featureCount()
    layer1_feat_number = 0

    for layer1_feat in layer1_feat_all:

        layer1_feat_number = layer1_feat_number + 1
        barValue = layer1_feat_number/float(layer1_feat_total)*100
        bar.setValue(barValue)

        # researches the layer2 points in a rectangle created by the research_ray
        # creates the search rectangle from receiver geometry
        rect = QgsRectangle()
        rect.setXMinimum( layer1_feat.geometry().asPoint().x() - research_ray )
        rect.setXMaximum( layer1_feat.geometry().asPoint().x() + research_ray )
        rect.setYMinimum( layer1_feat.geometry().asPoint().y() - research_ray )
        rect.setYMaximum( layer1_feat.geometry().asPoint().y() + research_ray )

        layer2_request = layer2_spIndex.intersects(rect)

        layer2_points = []

        # layer2_request contain all source feature in rect of receiver
        for layer2_id in layer2_request:

            layer2_feat = layer2_feat_all_dict[layer2_id]

            ray_to_test_length = compute_distance(layer1_feat.geometry().asPoint(),layer2_feat.geometry().asPoint())

            if ray_to_test_length <= research_ray:

                ray_to_test = QgsGeometry.fromPolylineXY( [ layer1_feat.geometry().asPoint() , layer2_feat.geometry().asPoint() ] )

                intersect = 0

                if obstacles_path is not None:
                    obstacles_request = obstacles_spIndex.intersects(ray_to_test.boundingBox())
                    for obstacles_id in obstacles_request:
                        if obstacles_feat_all_dict[obstacles_id].geometry().crosses(ray_to_test) == 1:
                            intersect = 1
                            break

                if intersect == 0:

                    layer2_points.append(layer2_feat.id())

                    output[layer1_feat.id()] = layer2_points

    return output


def run_selection(bar,layer1_path,layer2_path,obstacles_path,research_ray,dict_selection):
    
    output = {}
    
    layer1 = QgsVectorLayer(layer1_path,"layer1","ogr")

    layer2 = QgsVectorLayer(layer2_path,"layer2","ogr")
    layer2_feat_all_dict = {}
    layer2_feat_all = layer2.dataProvider().getFeatures()
    layer2_spIndex = QgsSpatialIndex()            
    for layer2_feat in layer2_feat_all:
        layer2_spIndex.insertFeature(layer2_feat)
        layer2_feat_all_dict[layer2_feat.id()] = layer2_feat

    if obstacles_path is not None:
        obstacles_layer = QgsVectorLayer(obstacles_path,"obstacles","ogr")
        obstacles_feat_all = obstacles_layer.dataProvider().getFeatures()
        obstacles_spIndex = QgsSpatialIndex()
        obstacles_feat_all_dict = {}
        for obstacles_feat in obstacles_feat_all:
            obstacles_spIndex.insertFeature(obstacles_feat)
            obstacles_feat_all_dict[obstacles_feat.id()] = obstacles_feat
        
    layer1_feat_all = layer1.dataProvider().getFeatures()
    layer1_feat_total = layer1.dataProvider().featureCount()
    layer1_feat_number = 0
    
    for layer1_feat in layer1_feat_all:

        layer1_feat_number = layer1_feat_number + 1
        barValue = layer1_feat_number/float(layer1_feat_total)*100
        bar.setValue(barValue)        
        
        # researches the layer2 points in a rectangle created by the research_ray
        # creates the search rectangle
        rect = QgsRectangle()
        rect.setXMinimum( layer1_feat.geometry().asPoint().x() - research_ray )
        rect.setXMaximum( layer1_feat.geometry().asPoint().x() + research_ray )
        rect.setYMinimum( layer1_feat.geometry().asPoint().y() - research_ray )
        rect.setYMaximum( layer1_feat.geometry().asPoint().y() + research_ray )
        
        layer2_request = layer2_spIndex.intersects(rect)
        
        layer2_points = []
        
        for layer2_id in layer2_request:
            
            if layer2_id in dict_selection: 
            
                layer2_feat = layer2_feat_all_dict[layer2_id] 
                            
                ray_to_test_length = compute_distance(layer1_feat.geometry().asPoint(),layer2_feat.geometry().asPoint())
    
                if ray_to_test_length <= research_ray:
    
                    ray_to_test = QgsGeometry.fromPolylineXY( [ layer1_feat.geometry().asPoint() , layer2_feat.geometry().asPoint() ] )
    
                    intersect = 0
                
                    if obstacles_path is not None:
                        obstacles_request = obstacles_spIndex.intersects(ray_to_test.boundingBox())
                        for obstacles_id in obstacles_request:
                            if obstacles_feat_all_dict[obstacles_id].geometry().crosses(ray_to_test) == 1:
                                intersect = 1
                                break
                    
                    if intersect == 0:
    
                        layer2_points.append(layer2_feat.id())
                         
                        output[layer1_feat.id()] = layer2_points
 
    return output                    


def run_selection_distance(bar,layer1_path,layer2_path,obstacles_path,research_ray,dict_selection_layer2TOlayer3,layer3_path):
    '''runs only in the selection dict and check the distance also with the selection dict rays'''
    
    output = {}
    
    layer1 = QgsVectorLayer(layer1_path,"layer1","ogr")

    layer2 = QgsVectorLayer(layer2_path,"layer2","ogr")
    layer2_feat_all_dict = {}
    layer2_feat_all = layer2.dataProvider().getFeatures()
    layer2_spIndex = QgsSpatialIndex()            
    for layer2_feat in layer2_feat_all:
        layer2_spIndex.insertFeature(layer2_feat)
        layer2_feat_all_dict[layer2_feat.id()] = layer2_feat

    if obstacles_path is not None:
        obstacles_layer = QgsVectorLayer(obstacles_path,"obstacles","ogr")
        obstacles_feat_all = obstacles_layer.dataProvider().getFeatures()
        obstacles_spIndex = QgsSpatialIndex()
        obstacles_feat_all_dict = {}
        for obstacles_feat in obstacles_feat_all:
            obstacles_spIndex.insertFeature(obstacles_feat)
            obstacles_feat_all_dict[obstacles_feat.id()] = obstacles_feat
            
    layer3 = QgsVectorLayer(layer3_path,"layer3","ogr")       
    layer3_feat_all = layer3.dataProvider().getFeatures()
    layer3_feat_all_dict = {}
    for layer3_feat in layer3_feat_all:
        layer3_feat_all_dict[layer3_feat.id()] = layer3_feat
    
    layer1_feat_all = layer1.dataProvider().getFeatures()
    layer1_feat_total = layer1.dataProvider().featureCount()
    layer1_feat_number = 0
    
    for layer1_feat in layer1_feat_all:

        layer1_feat_number = layer1_feat_number + 1
        barValue = layer1_feat_number/float(layer1_feat_total)*100
        bar.setValue(barValue)        
        
        # researches the layer2 points in a rectangle created by the research_ray
        # creates the search rectangle
        rect = QgsRectangle()
        rect.setXMinimum( layer1_feat.geometry().asPoint().x() - research_ray )
        rect.setXMaximum( layer1_feat.geometry().asPoint().x() + research_ray )
        rect.setYMinimum( layer1_feat.geometry().asPoint().y() - research_ray )
        rect.setYMaximum( layer1_feat.geometry().asPoint().y() + research_ray )
        
        layer2_request = layer2_spIndex.intersects(rect)
        
        layer2_points = []
        
        for layer2_id in layer2_request:
            
            if layer2_id in dict_selection_layer2TOlayer3: 
            
                layer2_feat = layer2_feat_all_dict[layer2_id] 
                            
                ray_to_test_length = compute_distance(layer1_feat.geometry().asPoint(),layer2_feat.geometry().asPoint())
                
                distance_layer2_layer3 = []
                
                min_distance_layer2_layer3 = research_ray
                
                for layer3_id in dict_selection_layer2TOlayer3[layer2_id]:
                    
                    layer3_feat = layer3_feat_all_dict[layer3_id]
                    
                    ray_layer2_layer3 = compute_distance(layer2_feat.geometry().asPoint(),layer3_feat.geometry().asPoint())
                    
                    if ray_layer2_layer3 < min_distance_layer2_layer3:
                        min_distance_layer2_layer3 = ray_layer2_layer3
                
    
                if min_distance_layer2_layer3 + ray_to_test_length <= research_ray:
    
                    ray_to_test = QgsGeometry.fromPolyline( [ layer1_feat.geometry().asPoint() , layer2_feat.geometry().asPoint() ] ) 
    
                    intersect = 0
                
                    if obstacles_path is not None:
                        obstacles_request = obstacles_spIndex.intersects(ray_to_test.boundingBox())
                        for obstacles_id in obstacles_request:
                            if obstacles_feat_all_dict[obstacles_id].geometry().crosses(ray_to_test) == 1:
                                intersect = 1
                                break
                    
                    if intersect == 0:
    
                        layer2_points.append(layer2_feat.id())
                         
                        output[layer1_feat.id()] = layer2_points
 
    return output           
    
    
    
    
        
    
