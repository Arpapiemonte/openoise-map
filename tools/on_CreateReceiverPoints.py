# -*- coding: utf-8 -*-
"""
/***************************************************************************
 opeNoise

 Qgis Plugin to compute noise levels

                             -------------------
        begin                : February 2022
        copyright            : (C) 2022 by Arpa Piemonte
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

from builtins import str
from builtins import range
from qgis.PyQt.QtCore import QObject
from qgis.PyQt.QtCore import QVariant, Qt
from qgis.core import QgsProject, QgsVectorFileWriter, QgsWkbTypes, QgsFields, QgsPointXY
from qgis.core import QgsPoint,QgsFeature,QgsGeometry,edit
from qgis.core import QgsVectorLayer,QgsSpatialIndex,QgsField,QgsRectangle,QgsFeatureRequest
from math import sqrt

import os
#from math import *

import processing




def middle(bar,buildings_layer_path,receiver_points_layer_path):
    
    buildings_layer_name = os.path.splitext(os.path.basename(buildings_layer_path))[0]
    buildings_layer = QgsVectorLayer(buildings_layer_path,buildings_layer_name,"ogr")
  
    # defines emission_points layer
    receiver_points_fields = QgsFields()
    receiver_points_fields.append(QgsField("id_pt", QVariant.Int))
    receiver_points_fields.append(QgsField("id_bui", QVariant.Int))
    receiver_points_fields.append(QgsField("facadeP", QVariant.Double,len=5,prec=2))


    receiver_points_writer = QgsVectorFileWriter(receiver_points_layer_path, "System",
                                                 receiver_points_fields, QgsWkbTypes.Point, buildings_layer.crs(),"ESRI Shapefile")


    # gets features from layer
    buildings_feat_all = buildings_layer.dataProvider().getFeatures()    
    
    # creates SpatialIndex
    buildings_spIndex = QgsSpatialIndex()
    buildings_feat_all_dict = {}
    for buildings_feat in buildings_feat_all:
        buildings_spIndex.insertFeature(buildings_feat)
        buildings_feat_all_dict[buildings_feat.id()] = buildings_feat
    
    # defines distanze_point
    distance_point = 0.1
    
    # re-gets features from layer
    buildings_feat_all = buildings_layer.dataProvider().getFeatures()    
    buildings_feat_total = buildings_layer.dataProvider().featureCount()
    
    pt_id = 0
    buildings_feat_number = 0
    for buildings_feat in buildings_feat_all:
        
        buildings_feat_number = buildings_feat_number + 1
        barValue = buildings_feat_number/float(buildings_feat_total)*100
        bar.setValue(barValue)

        building_geom = buildings_feat.geometry()
        if building_geom.isMultipart():
            buildings_pt = building_geom.asMultiPolygon()[0]
            gLine = QgsGeometry.fromPolylineXY(building_geom.asMultiPolygon()[0][0])
            totLen = gLine.length()
            #building_geom.convertToSingleType()
        else:
            buildings_pt = buildings_feat.geometry().asPolygon()
            totLen = building_geom.lenght()


        # creates the search rectangle to match the receiver point in the building and del them

        rect = QgsRectangle()
        rect.setXMinimum( buildings_feat.geometry().boundingBox().xMinimum() - distance_point )
        rect.setXMaximum( buildings_feat.geometry().boundingBox().xMaximum() + distance_point )
        rect.setYMinimum( buildings_feat.geometry().boundingBox().yMinimum() - distance_point )
        rect.setYMaximum( buildings_feat.geometry().boundingBox().yMaximum() + distance_point )
    
        buildings_selection = buildings_spIndex.intersects(rect)
        
        if len(buildings_pt) > 0:
            for i in range(0,len(buildings_pt)):
                
                buildings_pts = buildings_pt[i]
        
                ####
                # start part to delete pseudo vertex
                # this part it's different from the diffraction delete pseudo vertex part
                pts_index_to_delete_list = []
                m_delta = 0.01
  
                for ii in range(0,len(buildings_pts)-1):
                        
                    x1 = buildings_pts[ii-1][0]
                    x2 = buildings_pts[ii][0]
                    x3 = buildings_pts[ii+1][0]                    
                    y1 = buildings_pts[ii-1][1]
                    y2 = buildings_pts[ii][1]
                    y3 = buildings_pts[ii+1][1]

                    # particular cases: first point to delete! (remember that the first and the last have the same coordinates)
                    if ii == 0 and (x2 == x1 and y2 == y1):
                        x1 = buildings_pts[ii-2][0]
                        y1 = buildings_pts[ii-2][1]
                        
                    # angular coefficient to find pseudo vertex
                    if x2 - x1 != 0 and x3 - x1 != 0:
                        m1 = ( y2 - y1 ) / ( x2 - x1 )
                        m2 = ( y3 - y1 ) / ( x3 - x1 )

                        #if round(m1,2) <= round(m2,2) + m_delta and round(m1,2) >= round(m2,2) - m_delta:
                        if m1 <= m2 + m_delta and m1 >= m2 - m_delta:
                            pts_index_to_delete_list.append(ii)

                            # particular cases: first point to delete! (remember that the first and the last have the same coordinates)
                            # here we delete the last and add x3,y3 (buildings_pts[ii+1] - the new last point)
                            if ii == 0:
                                pts_index_to_delete_list.append(len(buildings_pts)-1)
                                buildings_pts.append(buildings_pts[ii+1])
                            
                # del pseudo vertex
                pts_index_to_delete_list = sorted(pts_index_to_delete_list, reverse=True)
                
                for pt_index_to_del in pts_index_to_delete_list:
                    del buildings_pts[pt_index_to_del]
                
                # end part to delete pseudo vertex

                        
                # for to generate receiver points
                for ii in range(0,len(buildings_pts)-1):
                    
                    x1 = buildings_pts[ii][0]
                    x2 = buildings_pts[ii+1][0]
                    y1 = buildings_pts[ii][1]
                    y2 = buildings_pts[ii+1][1]
                    facade_dist = sqrt( (x1-x2)**2 + (y1-y2)**2 )/building_geom.length()*100

                    xm = ( x1 + x2 )/2
                    ym = ( y1 + y2 )/2
                
                    if y2 == y1:
                        dx = 0
                        dy = distance_point
                    elif x2 == x1:
                        dx = distance_point
                        dy = 0
                    else:
                        m = ( y2 - y1 )/ ( x2 - x1 )
                        m_p = -1/m
                        dx = sqrt((distance_point**2)/(1 + m_p**2))
                        dy = sqrt(((distance_point**2)*(m_p**2))/(1 + m_p**2))
        
                    if (x2 >= x1 and y2 >= y1) or (x2 < x1 and y2 < y1):
                        pt1 = QgsPointXY(xm + dx, ym - dy)
                        pt2 = QgsPointXY(xm - dx, ym + dy)
                    if (x2 >= x1 and y2 < y1) or (x2 < x1 and y2 >= y1):
                        pt1 = QgsPointXY(xm + dx, ym + dy)
                        pt2 = QgsPointXY(xm - dx, ym - dy)
                    
                    pt = QgsFeature()
                    
                    # pt1, check if is in a building and eventually add it
                    pt.setGeometry(QgsGeometry.fromPointXY(pt1))
                    intersect = 0
                    for buildings_id in buildings_selection:
                        if buildings_feat_all_dict[buildings_id].geometry().intersects(pt.geometry()) == 1:
                            intersect = 1
                            break 
                    
                    if intersect == 0:
                        pt.setAttributes([pt_id, buildings_feat.id(),facade_dist])
                        receiver_points_writer.addFeature(pt)
                        pt_id = pt_id + 1
                    
                    # pt2, check if is in a building and eventually add it
                    pt.setGeometry(QgsGeometry.fromPointXY(pt2))
                    intersect = 0
                    for buildings_id in buildings_selection:
                        if buildings_feat_all_dict[buildings_id].geometry().intersects(pt.geometry()) == 1:
                            intersect = 1
                            break 
                    
                    if intersect == 0:
                        pt.setAttributes([pt_id, buildings_feat.id(),facade_dist/totLen*100])
                        receiver_points_writer.addFeature(pt)
                        pt_id = pt_id + 1                
    
    del receiver_points_writer
    #print receiver_points_layer_path
    receiver_points_layer_name = os.path.splitext(os.path.basename(receiver_points_layer_path))[0]
    #print receiver_points_layer_name
    receiver_points_layer = QgsVectorLayer(receiver_points_layer_path, str(receiver_points_layer_name), "ogr")

    QgsProject.instance().addMapLayers([receiver_points_layer])
    
    
def spaced(bar,buildings_layer_path,receiver_points_layer_path,spaced_pts_distance):
    
    distance_from_facades = 0.1

    buildings_layer_name = os.path.splitext(os.path.basename(buildings_layer_path))[0]
    buildings_layer = QgsVectorLayer(buildings_layer_path,buildings_layer_name,"ogr")
    
    
    # cp building layer to delete all fields
    buildings_memory_layer = QgsVectorLayer("Polygon?crs=" + str(buildings_layer.crs().authid()), "polygon_memory_layer", "memory")
    buildings_memory_layer.dataProvider().addAttributes([])
    
    buildings_feat_all = buildings_layer.dataProvider().getFeatures()    
    buildings_feat_list = []
    for buildings_feat in buildings_feat_all:
        buildings_feat_list.append(buildings_feat)

    buildings_memory_layer.dataProvider().addFeatures(buildings_feat_list)   
    buildings_memory_layer.updateExtents()

    # this is crazy: I had to add this line otherwise the first processing doesn't work...
    QgsProject.instance().addMapLayers([buildings_memory_layer])
    
    bar.setValue(1)

    # this processing alg has as output['OUTPUT'] the layer
    output = processing.run("native:buffer", {'INPUT': buildings_memory_layer,
                                             'DISTANCE': distance_from_facades,
                                             'DISSOLVE': False,
                                             'OUTPUT': 'memory:'})

    # I can now remove the layer from map...
    QgsProject.instance().removeMapLayers( [buildings_memory_layer.id()] )

    bar.setValue(25)

    # this processing alg has as output['OUTPUT'] the layer
    output = processing.run("qgis:polygonstolines", {'INPUT': output['OUTPUT'],
                                                     'OUTPUT': 'memory:'})
    bar.setValue(50)    

    # this processing alg has as output['output'] the layer path...
    poly_to_lines = output['OUTPUT']
    output = processing.run("qgis:pointsalonglines", {'INPUT': poly_to_lines,
                                                      'DISTANCE': spaced_pts_distance,
                                                      'START_OFFSET': 0,
                                                      'END_OFFSET': 0,
                                                      'OUTPUT': 'memory:'})


    bar.setValue(75)

    receiver_points_memory_layer = output['OUTPUT']


    del output



    ## Delete pts in buildings
    # creates SpatialIndex
    buildings_feat_all = buildings_layer.dataProvider().getFeatures()    
    buildings_spIndex = QgsSpatialIndex()
    buildings_feat_all_dict = {}
    for buildings_feat in buildings_feat_all:
        buildings_spIndex.insertFeature(buildings_feat)
        buildings_feat_all_dict[buildings_feat.id()] = buildings_feat

    receiver_points_memory_layer_all = receiver_points_memory_layer.dataProvider().getFeatures()

    receiver_points_layer_fields = QgsFields()
    receiver_points_layer_fields.append(QgsField("id_pt", QVariant.Int))
    receiver_points_layer_fields.append(QgsField("id_bui", QVariant.Int))
    receiver_points_layer_fields.append(QgsField("facadeP", QVariant.Double, len=5, prec=2))

    receiver_points_layer_writer = QgsVectorFileWriter(receiver_points_layer_path, "System",
                                                       receiver_points_layer_fields, QgsWkbTypes.Point,
                                                       buildings_layer.crs(), "ESRI Shapefile")

    receiver_points_feat_id = 0

    receiver_memory_feat_total = receiver_points_memory_layer.dataProvider().featureCount()
    receiver_memory_feat_number = 0

    for receiver_memory_feat in receiver_points_memory_layer_all:

        receiver_memory_feat_number = receiver_memory_feat_number + 1
        barValue = receiver_memory_feat_number/float(receiver_memory_feat_total)*25 + 75
        bar.setValue(barValue)

        rect = QgsRectangle()
        rect.setXMinimum(receiver_memory_feat.geometry().asPoint().x() - distance_from_facades)
        rect.setXMaximum(receiver_memory_feat.geometry().asPoint().x() + distance_from_facades)
        rect.setYMinimum(receiver_memory_feat.geometry().asPoint().y() - distance_from_facades)
        rect.setYMaximum(receiver_memory_feat.geometry().asPoint().y() + distance_from_facades)
        buildings_selection = buildings_spIndex.intersects(rect)

        to_add = True

        receiver_geom = receiver_memory_feat.geometry()
        building_id_correct = None

        for buildings_id in buildings_selection:
            building_geom = buildings_feat_all_dict[buildings_id].geometry()
            intersectBuilding = QgsGeometry.intersects(receiver_geom, building_geom)
            building_id_correct = buildings_id
            if intersectBuilding:
                to_add = False
                building_id_correct = None
                break

        # picking the nearest building to the receiver point analysed
        nearestIds = buildings_spIndex.nearestNeighbor(receiver_geom.asPoint(), 1)
        building_fid = []
        for featureId in nearestIds:
            request = QgsFeatureRequest().setFilterFid(featureId)
            for feature in buildings_layer.getFeatures(request):
                dist = receiver_geom.distance(feature.geometry())
                building_fid.append((dist, feature.id()))
        building_fid_correct = min(building_fid, key=lambda x: x[0])[-1]



        if to_add:
            attributes = [receiver_points_feat_id, building_fid_correct,spaced_pts_distance]
            fet = QgsFeature()
            fet.setGeometry(receiver_memory_feat.geometry())
            fet.setAttributes(attributes)
            receiver_points_layer_writer.addFeature(fet)
            receiver_points_feat_id = receiver_points_feat_id + 1


    del receiver_points_layer_writer
    
    receiver_points_layer_name = os.path.splitext(os.path.basename(receiver_points_layer_path))[0]
    receiver_points_layer = QgsVectorLayer(receiver_points_layer_path, str(receiver_points_layer_name), "ogr")

    QgsProject.instance().addMapLayers([receiver_points_layer])

    QgsProject.instance().reloadAllLayers()

def case2b(bar,buildings_layer_path,receiver_points_layer_path):
    buildings_layer_name = os.path.splitext(os.path.basename(buildings_layer_path))[0]
    buildings_layer = QgsVectorLayer(buildings_layer_path, buildings_layer_name, "ogr")

    # defines emission_points layer
    receiver_points_fields = QgsFields()
    receiver_points_fields.append(QgsField("id_pt", QVariant.Int))
    receiver_points_fields.append(QgsField("id_bui", QVariant.Int))
    receiver_points_fields.append(QgsField("facadeP", QVariant.Double, len=5, prec=2))

    receiver_points_writer = QgsVectorFileWriter(receiver_points_layer_path, "System",
                                                 receiver_points_fields, QgsWkbTypes.Point, buildings_layer.crs(),
                                                 "ESRI Shapefile")


    # gets features from layer
    buildings_feat_all = buildings_layer.dataProvider().getFeatures()

    # creates SpatialIndex
    buildings_spIndex = QgsSpatialIndex()
    buildings_feat_all_dict = {}
    for buildings_feat in buildings_feat_all:
        buildings_spIndex.insertFeature(buildings_feat)
        buildings_feat_all_dict[buildings_feat.id()] = buildings_feat

    # defines distanze_point
    distance_point = 0.1

    # re-gets features from layer
    buildings_feat_all = buildings_layer.dataProvider().getFeatures()
    buildings_feat_total = buildings_layer.dataProvider().featureCount()

    pt_id = 0
    reachLen = 5 # variable storing distance steps
    buildings_feat_number = 0



    for buildings_feat in buildings_feat_all:

        buildings_feat_number = buildings_feat_number + 1
        barValue = buildings_feat_number / float(buildings_feat_total) * 100
        bar.setValue(barValue)

        # creates the search rectangle to match the receiver point in the building and del them

        rect = QgsRectangle()
        rect.setXMinimum(buildings_feat.geometry().boundingBox().xMinimum() - distance_point)
        rect.setXMaximum(buildings_feat.geometry().boundingBox().xMaximum() + distance_point)
        rect.setYMinimum(buildings_feat.geometry().boundingBox().yMinimum() - distance_point)
        rect.setYMaximum(buildings_feat.geometry().boundingBox().yMaximum() + distance_point)

        buildings_selection = buildings_spIndex.intersects(rect)

        building_geom = buildings_feat.geometry()

        if building_geom.isMultipart():
            for ii in range(len(building_geom.asMultiPolygon())):
                gLine = QgsGeometry.fromPolylineXY(building_geom.asMultiPolygon()[ii][0])
                # distance 0.1 m from facades
                gLineBuf = gLine.buffer(0.1,5)
                gLine = QgsGeometry.fromPolylineXY(gLineBuf.asPolygon()[0])
                totLen = gLine.length()
                # prog = reachLen / 2.
                startReach = 0
                # endReach = 5

                steps = list()
                while startReach < totLen:
                    f = QgsFeature()
                    endReach = min(startReach + reachLen, totLen)
                    prog = (startReach + endReach) / 2
                    pt = gLine.interpolate(prog)
                    steps.append(prog)
                    f.setGeometry(pt)
                    intersect = 0
                    for buildings_id in buildings_selection:
                        if buildings_feat_all_dict[buildings_id].geometry().intersects(f.geometry()) == 1:
                            intersect = 1
                            break

                    if intersect == 0:
                        f.setAttributes([pt_id,buildings_feat.id() ,(min(endReach, totLen) - startReach)/totLen*100])
                        receiver_points_writer.addFeature(f)
                        pt_id = pt_id + 1
                    prog = prog + reachLen
                    endReach = endReach + reachLen
                    startReach += reachLen

            # building_geom.convertToSingleType()
        else:
            gLine = QgsGeometry.fromPolylineXY(building_geom.asPolygon()[0])
            # distance 0.1 m from facades
            gLine = gLine.buffer(0.1, 5)
            gLineBuf = gLine.buffer(0.1, 5)
            gLine = QgsGeometry.fromPolylineXY(gLineBuf.asPolygon()[0])
            totLen = gLine.length()
            # prog = reachLen / 2.
            startReach = 0
            # endReach = 5

            steps = list()
            while startReach < totLen and endReach < totLen:
                f = QgsFeature()
                endReach = min(startReach + reachLen, totLen)
                prog = (startReach + endReach) / 2
                pt = gLine.interpolate(prog)
                steps.append(prog)
                f.setGeometry(pt)
                intersect = 0
                for buildings_id in buildings_selection:
                    if buildings_feat_all_dict[buildings_id].geometry().intersects(f.geometry()) == 1:
                        intersect = 1
                        break

                if intersect == 0:
                    f.setAttributes([str(pt_id),buildings_feat.id(), (min(endReach, totLen) - startReach)/totLen*100])
                    receiver_points_writer.addFeature(f)
                    pt_id += 1
                prog = prog + reachLen
                endReach = endReach + reachLen
                startReach += reachLen



    del receiver_points_writer
    # print receiver_points_layer_path
    receiver_points_layer_name = os.path.splitext(os.path.basename(receiver_points_layer_path))[0]
    # print receiver_points_layer_name
    receiver_points_layer = QgsVectorLayer(receiver_points_layer_path, str(receiver_points_layer_name), "ogr")


    # cleaning -- remove feature inside buildings
    # with edit(receiver_points_layer):
    #     for receiverFeature in receiver_points_layer.getFeatures():
    #         for builFeature in buildings_layer.getFeatures():
    #             if builFeature.geometry().intersects(receiverFeature.geometry()):
    #                 receiver_points_layer.deleteFeature(receiverFeature.id())

    QgsProject.instance().addMapLayers([receiver_points_layer])

        # building_geom.lineLocatePoint(QgsGeometry().fromPointXY(1394677.00,4989762.05))


