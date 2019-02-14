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

#from PyQt4.QtGui import *
#from PyQt4.QtCore import *
from builtins import range
from qgis.core import QgsVectorLayer, QgsFeature, QgsGeometry, QgsPoint, QgsVectorFileWriter, QgsWkbTypes, QgsFields, \
    QgsPointXY
import os
#from math import *
from datetime import datetime
import collections


    
    
def run(bar,buildings_layer_path,diffraction_points_layer_path):
    
    buildings_layer_name = os.path.splitext(os.path.basename(buildings_layer_path))[0]
    buildings_layer = QgsVectorLayer(buildings_layer_path,buildings_layer_name,"ogr")
  

    diffraction_points_fields = QgsFields()

    diffraction_points_writer = QgsVectorFileWriter(diffraction_points_layer_path, "System",
                                                    diffraction_points_fields, QgsWkbTypes.Point,
                                                    buildings_layer.crs(),"ESRI Shapefile")

    # gets features from layer
    buildings_feat_all = buildings_layer.dataProvider().getFeatures()   
    buildings_feat_total = buildings_layer.dataProvider().featureCount()
    buildings_feat_number = 0
    
    all_coord_points = []
    
    for buildings_feat in buildings_feat_all:
        
        buildings_feat_number = buildings_feat_number + 1
        barValue = buildings_feat_number/float(buildings_feat_total)*100
        bar.setValue(barValue)

        building_geom = buildings_feat.geometry()
        if building_geom.isMultipart():
            building_geom.convertToSingleType()

        buildings_pt = building_geom.asPolygon()



        
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
                
                # remove duplicates from the single buildings
                buildings_pts = list(set(buildings_pts))           

                for pt in buildings_pts:
                    all_coord_points.append(pt)
    
    # remove duplicates from vertex of different buildings
    all_coord_points = collections.Counter(all_coord_points)

    for coord in list(all_coord_points.keys()):
        if all_coord_points[coord] == 1:
            pt = QgsFeature()
            pt.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(coord[0], coord[1])))
            diffraction_points_writer.addFeature(pt)
    #

                

    del diffraction_points_writer
